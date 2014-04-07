def viz_tree_str (tree, variables, directed = True):
    """
    the graph viz tree string representation
    """
    if directed:
        edge_str = ""
    else:
        edge_str = "dir=none"
        
    viz_str = "digraph g{\n"
    for v1, v2 in tree:
        #add edges
        if (v2, v1) in tree:
            if tree.index((v2, v1)) > tree.index((v1, v2)): #to ensure we only plotted one
                viz_str += ("%s -> %s[%s]\n" %(v1.var, v2.var, "dir=none,penwidth=3,color=blue"))
        else:
            viz_str += ("%s -> %s[%s]\n" %(v1.var, v2.var, edge_str))
    viz_str += '}';
    return viz_str

def sort_edges (graph_edges, all_possible_edges, weight_table):
    """
    sort the edges according to its member ship in graph_edges and its weight in ascending order
    """
    
    key_func = lambda edge: weight_table [edge]
    remaining_edges = list(set (all_possible_edges) - set (graph_edges))
    return sorted (graph_edges, key = key_func, reverse= True) + sorted (remaining_edges, key = key_func, reverse= True)
    

def has_loop (edges):
    """
    Determines if the loops exist in the dge list
    
    Param: 
    edges: list of edges

    Return: 
    boolean: has loop or not
    """
    import networkx as nx
    g = nx.DiGraph (edges + map(lambda (v1, v2): (v2, v1), edges))
    cycles = nx.simple_cycles (g)
    not_simple_cycles = filter (lambda path: len(path) > 3, cycles) #filter out selfloops
    return  len(not_simple_cycles) > 0
