from __future__ import division

"""
The GPT algorithm

Reference:
George Rebane & Judea Pearl, THE RECOVERY OF CAUSAL POLY-TREES FROM STATISTICAL DATA
"""

import math, random
from itertools import product, combinations, groupby, permutations
from graph import Variable
from data_reader import read_row_data
from suff_stats import Data
from stat_test import marginal_independence
from util import viz_tree_str, sort_edges

import networkx as nx

def GPT_learn (chow_liu_tree, data, variables):
    """
    Param:
    chow_liu_tree: edges of the chow liu tree
    data: the data object consisting of rows
    variables: the vars we are interested in their structure

    Output: 
    the directed edges of GPT
    """
    
    edges = []
    
    #using Graph to represent to the tree topology, for later easier retrieval of node neighbours
    g = nx.Graph ()
    g.add_nodes_from (variables)
    g.add_edges_from (chow_liu_tree)
    
    m = data.sum (useMAP = False) #the total number of rows
    
    ###STEPS:####
    
    # 1. Finding the multi-parent node base on the chow-liu tree topology: 
    # start with the internal nodes (non-leaves) and use the type-3 test: 
    # For example: there are two edges between AB and BC, A-B-C, calculate I (A,C|B).
    # If the gain the zero (or under some threshold, in case there are noise), then A and C are parents of A

    for node in g.nodes ():
        I_12 = 0#mutual information between var 1 and var 2
        possibilities = list(combinations(g.neighbors (node), 2))
        random.shuffle(possibilities)
        for v1, v2 in possibilities:
            #if v1 and v2 independent according to some statistical indepdencen test
            if marginal_independence (v1, v2, data):
                if (v1, node) not in edges and (node, v1) not in edges: #does not exist and does not form self-loop
                    edges.append ((v1, node))
                if (v2, node) not in edges and (node, v2) not in edges:
                    edges.append ((v2, node))
    
    print edges

    print 'Determining direction for neighors of nodes with at least one incoming arrow '
    # 3. For nodes with at least one incoming arrow, use type-3 test to determine the direction of its neighbours.
    cur_edge_index = 0
    while cur_edge_index < len (edges): #when all edges have been checked, quit the  loop
        from_node, to_node = edges [cur_edge_index]
        for neighbor in g.neighbors (to_node):
            if neighbor == from_node: #no self-loop
                continue
            if marginal_independence (neighbor, from_node, data):
                if (neighbor, to_node) not in edges and (to_node, neighbor) not in edges: # it has not been added before and does not form self-loop
                    edges.append ((neighbor, to_node))
            else: #marginal independence does not hold, they should be dependent
                if (to_node, neighbor) not in edges and (neighbor, to_node) not in edges: # it has not been added before
                    edges.append ((to_node, neighbor))
        cur_edge_index += 1
                
    print 'Final edge set:', edges
    print len (edges)
    
    #then we need to find out those whose directions have not been decided
    not_decided_edges = []
    for n1, n2 in chow_liu_tree:
        if (n1, n2) not in edges and (n2, n1) not in edges:
            not_decided_edges.append ((n1, n2))
            not_decided_edges.append ((n2, n1))
            
    return edges + not_decided_edges
    
if __name__ == "__main__":
    import string
    variables = map (lambda letter: Variable(letter, ['1', '2', '3']), string.uppercase)
    
    print "reading data..."
    data = Data(read_row_data ('train_data.txt'))
    
    from chow_liu_tree import chowliu_learn
    
    import os, pickle
    if os.path.exists ("chow_liu_tree.pickle"): 
        print "pickle exists, load it directly"
        tree, _, edge_weights = pickle.load (open ("chow_liu_tree.pickle", "r"))
    else:
        print "pickle does not exist, calculate it and dump it"
        tree, _, edge_weights = chowliu_learn (data, variables)
        pickle.dump (result, open ("chow_liu_tree.pickle", "w"))
        
    print "learning structure..."
    edges = GPT_learn (tree, data, variables)

    import sys

    try:
        arg = sys.argv [1]
    except IndexError:
        usage ()
    
    if arg == "predict":
        new_rows = read_row_data ('test_data.txt')
        for row in new_rows:
            print predict (tree, probs, row);
    elif arg == "graphviz":
        viz_str = viz_tree_str (edges, variables, directed = True)
        print viz_str
    elif arg == "sorted_edges":
        for v1, v2 in sort_edges (edges, list (permutations (variables, 2)), edge_weights):
            print "%s %s" %(v1, v2)
    else:
        usage ()
