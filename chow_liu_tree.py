from __future__ import division

"""
Structure learning using the chow-liu algorithm.
Some resource: http://en.wikipedia.org/wiki/Chow%E2%80%93Liu_tree
"""
import math
from itertools import product, combinations

from graph import Variable
from data_reader import read_row_data
from suff_stats import Data
from util import viz_tree_str, has_loop

def chowliu_learn (data, variables):
    """
    Param
    data: the data rows
    variables: the variables of which we will study their relationship

    Return:
    the structure of the Chow&Liu Tree
    """
    m = data.sum (useMAP = False) #the total number of rows
    def calc_weight (v1, v2):
        """
        the weight/information gain between two variables, v1 and v2
        """
        vals = []
        for val1, val2 in product (v1.values, v2.values):
            p12 = data.filter(**{v1.var: val1, v2.var: val2}).sum(useMAP = False) / m
            p1 = data.filter(**{v1.var: val1}).sum(useMAP = False) / m
            p2 = data.filter(**{v2.var: val2}).sum(useMAP = False) / m

            if (p12 == 0):
                vals.append(0)
            else:
                vals.append(p12 * math.log (p12 / p1 / p2))

        return sum (vals)
        
    N = len (variables)
    
    #compute the weights of all edges
    
    edge_weight_map = dict(map(lambda (v1, v2): ((v1, v2), calc_weight (v1, v2)), 
                               combinations (variables, 2)))
    
    edge_weight_map_cp = dict(edge_weight_map.items ())#copy the edge weight map for return
    
    for v1, v2 in edge_weight_map:#for the sake of undirected graph, you get the idea
        edge_weight_map_cp [(v2, v1)] = edge_weight_map_cp [(v1, v2)]
    
    #start spanning greedily
    edges = []
    while len(edges) < N - 1:
        
        #find the edge with the highest weight that forms no loop within the current edge set
        succeed = False
        while not succeed:
            heaviest_edge, greatest_weight = max (tuple (edge_weight_map.items ()), key = lambda (edge, weight): weight)
            if not has_loop (edges + [heaviest_edge]):
                edges.append (heaviest_edge)
                succeed = True
            else:
                v1,v2 = heaviest_edge
                edge_weight_map_cp [heaviest_edge] = 0 #make the edge prob 0
                edge_weight_map_cp [(v2, v1)] = 0 
                
            del edge_weight_map [heaviest_edge]

        
    #learning the probabilities
    probs = {}
    for v1, v2 in edges:
        probs [(v1, v2)] = {}
        probs [(v2, v1)] = {}
        for val1, val2 in product(v1.values, v2.values):
            prob = data.filter(**{v1.var: val1, v2.var: val2}).sum(useMAP = False) / m
            probs [(v1, v2)] [(val1, val2)] = prob
            probs [(v2, v1)] [(val2, val1)] = prob

    return edges, probs, edge_weight_map_cp
    
def edge_weight_sorted_by_weight (edge_weights_map):
    """
    from edge->weight map to the sorted list of edge ordered by weight
    """
    return sorted (edge_weights_map.items (), key = lambda (edge, weight): weight, reverse = True)

def usage ():
    print """
    Usage:
    python chow_liu_tree.py [predict|sorted_edge|graphviz]
    """
    
if __name__ == "__main__":
    import string
    variables = map (lambda letter: Variable(letter, ['1', '2', '3']), string.uppercase)
    
    data = Data(read_row_data ('train_data.txt'))
    
    import os, pickle
    if os.path.exists ("chow_liu_tree.pickle"): 
        tree, probs, edge_weights = pickle.load (open ("chow_liu_tree.pickle", "r"))
    else:
        tree, probs, edge_weights = chowliu_learn (data, variables)
        pickle.dump (result, open ("chow_liu_tree.pickle", "w"))
        
    import sys
    try:
        arg = sys.argv [1]
    except IndexError:
        usage ()
    
    if arg == "predict":
        import networkx as nx
        g = nx.Graph ()
        g.add_edges_from (tree)
    
        from inference import Network, get_factors_MN
        mn = Network (get_factors_MN (g, variables, data))
        
        with open ('test_data.txt') as f:
            f.readline () #exclude the first row
            for l in f.readlines ():
                values = l.strip ().split ()
                assignment = dict(zip(variables, values))
                print mn.total_joint_prob (assignment)
        
    elif arg == "graphviz":
        viz_str = viz_tree_str (tree, variables, directed = False)
        print viz_str
    elif arg == "sorted_edges":
        for (v1, v2), w in edge_weight_sorted_by_weight (edge_weights):
            print "%s %s" %(v1, v2)
    else:
        usage ()
