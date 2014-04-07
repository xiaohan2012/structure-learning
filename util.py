import networkx as nx

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

def has_loop (edges):
    """
    Determines if the loops exist in the dge list
    
    Param: 
    edges: list of edges

    Return: 
    boolean: has loop or not
    """
    g = nx.DiGraph (edges + map(lambda (v1, v2): (v2, v1), edges))
    cycles = nx.simple_cycles (g)
    
    not_simple_cycles = filter (lambda path: len(path) > 3, cycles) #filter out selfloops

    return  len(not_simple_cycles) > 0
