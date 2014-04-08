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

def GPT_learn_modified (chow_liu_tree, data, variables):
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
        possibilities = list(combinations(g.neighbors (node), 2))
        random.shuffle(possibilities)
        for v1, v2 in possibilities:
            #if v1 and v2 independent according to some statistical indepdencen test
            if marginal_independence (v1, v2, data):
                if (v1, node) not in edges and (node, v1) not in edges: #does not exist and does not form self-loop
                    edges.append ((v1, node))
                if (v2, node) not in edges and (node, v2) not in edges:
                    edges.append ((v2, node))
                
    # 2. For nodes with at least one incoming arrow, use type-3 test to determine the direction of its neighbours.
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
                
    #then we need to find out those whose directions have not been decided
    not_decided_edges = []
    for n1, n2 in chow_liu_tree:
        if (n1, n2) not in edges and (n2, n1) not in edges:
            not_decided_edges.append ((n1, n2))
            not_decided_edges.append ((n2, n1))
            
    return edges + not_decided_edges

def GPT_learn_original (chow_liu_tree, data, variables):
    """
    The original GPT structure learning algorithm.
    
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
    cur_edge_index = 0 #for the third step    
    
    while True:
        # 1. Finding the first multi-parent node base on the chow-liu tree topology
        # start with the internal nodes (non-leaves) and use the type-3 test: 
        # For example: there are two edges between AB and BC, A-B-C, calculate I (A,C|B).
        # If the gain the zero (or under some threshold, in case there are noise), then A and C are parents of A
        # Once such node is found, junp out of this step
        
        base_node, base_node_parents = None, None
        first_step_success_flag = False
        for node in g.nodes ():
            possibilities = list(combinations(g.neighbors (node), 2))
            random.shuffle(possibilities)
            
            if first_step_success_flag: #we found it, so jump out
                break
            for v1, v2 in possibilities:
                
                #if v1 and v2 independent according to some statistical indepdencen test
                if marginal_independence (v1, v2, data):
                    if (v1, node) not in edges: #add if not yet there
                        edges.append ((v1, node))
                        first_step_success_flag = True
                        
                    if (v2, node) not in edges:
                        edges.append ((v2, node))    
                        first_step_success_flag = True
                        
                    if first_step_success_flag:
                        base_node, base_node_parents = node, (v1, v2)

        
        if not first_step_success_flag: #we found nothing
            break

        #2. resolve the direction of the rest of base node's nbrs
        discussed_parents = base_node_parents
        for nbr in g [base_node]:
            if nbr in discussed_parents: continue #already discussed
            
            #independence test regarding to the discussed parents
            ind_test_results = map (lambda parent: marginal_independence (nbr, parent, data), discussed_parents)

            ind_consistent = reduce (lambda acc, result: acc and result, ind_test_results, True) == True#all supporting independence?
            dep_consistent = reduce (lambda acc, result: acc or result, ind_test_results, False) == False #all supporting dependence?
            
            if ind_consistent:
                edges.append ((nbr, base_node))
                discussed_parents.append (nbr)

            if dep_consistent:
                edges.append ((base_node, nbr))

            if not ind_consistent and not dep_consistent: 
                print 'Warning: inconsistency arises! So cannot determine the directionality.'

        # 3. For nodes with at least one incoming arrow, use type-3 test to determine the direction of its neighbours.
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
                    
    
    #then we need to find out those whose directions have not been decided
    not_decided_edges = []
    for n1, n2 in chow_liu_tree:
        if (n1, n2) not in edges and (n2, n1) not in edges:
            not_decided_edges.append ((n1, n2))
            not_decided_edges.append ((n2, n1))
            
    return edges + not_decided_edges
    
if __name__ == "__main__":
    import sys

    try:
        algo = sys.argv [1]
        arg = sys.argv [2]
    except IndexError:
        usage ()


    
    import string
    variables = map (lambda letter: Variable(letter, ['1', '2', '3']), string.uppercase)
    
    data = Data(read_row_data ('train_data.txt'))
    
    from chow_liu_tree import chowliu_learn
    
    import os, pickle
    if os.path.exists ("chow_liu_tree.pickle"): 
        tree, _, edge_weights = pickle.load (open ("chow_liu_tree.pickle", "r"))
    else:
        tree, _, edge_weights = chowliu_learn (data, variables)
        pickle.dump (result, open ("chow_liu_tree.pickle", "w"))

    if algo == 'orig':
        edges = GPT_learn_original (tree, data, variables)        
    elif algo == 'mod':
        edges = GPT_learn_modified (tree, data, variables)
    else:
        print 'wrong algo'
        sys.exit (-1)
    
    if arg == "predict":
        import networkx as nx
        g = nx.DiGraph ()
        g.add_edges_from (edges)
    
        from inference import Network, get_factors_BN
        n = Network (get_factors_BN (g, variables, data))
        
        with open ('test_data.txt') as f:
            f.readline () #exclude the first row
            for l in f.readlines ():
                values = l.strip ().split ()
                assignment = dict(zip(variables, values))
                print n.total_joint_prob (assignment)

    elif arg == "graphviz":
        viz_str = viz_tree_str (edges, variables, directed = True)
        print viz_str
    elif arg == "sorted_edges":
        for v1, v2 in sort_edges (edges, list (permutations (variables, 2)), edge_weights):
            print "%s %s" %(v1, v2)
    else:
        usage ()
