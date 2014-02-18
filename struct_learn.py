""" 
Learning tree structure using dynamic programming
"""
from collections import defaultdict
from itertools import product
from math import log

def pw_score (g, v1, v2 = None):
    """
    mutual information between v1 and v2
    if v2 is not given, just compute the score of v1
    """
    sum = 0;
    if v2 == None:
        for val1 in v1.values:
            n1,n = g.N (**{v1.var: val1}), g.N (**{})
            if n1 != 0:
                p1 = n1/n
                sum += p1 * log (p1, 2)
    else:
        for val1, val2 in product (v1.values, v2.values):
            n1,n2,n12,n = g.N (**{v1.var: val1}), g.N (**{v2.var: val2}), g.N (**{v1.var: val1, v2.var: val2}), g.N (**{})
            # print n1, n2, n12, n
            if n12 != 0:
                p1, p2, p12 = n1/n, n2/n, n12/n
                sum += p12 * log (p12 / (p1 * p2), 2)
    return sum

def learn (V, family_scores):
    """
    V: the list of variables
    family_weights: dict, the recomputed family weights table
    """
    
    #the best score for each node, default to -infinity, 
    #tuple -> numerical
    scores = defaultdict (lambda: float ('-inf')); scores [tuple ()] = 0 #empty set initialized to zero
    bp = {} #back pointer, (variable set -> what is added in the last step (previous_node, child, parent))
    
    def expand (U):
        """
        expand the current node U
        """
        best_score = float ('-inf')
        expanding_option = None #(parent of the child, thechild)
        
        #consider all variables in V which is not in U
        for v in (set(V) - set(U)):
            #which one in U is the best parent
            if len (U) != 0: #U is not empty
                best_u = max (U, key=lambda u: family_scores [(u, v)])
                score = scores [tuple(U)] + family_scores [(v, best_u)]
            else:
                best_u = None #no parent
                score = scores [tuple(U)] + family_scores [(v, )]
                
            newset = tuple(sorted(U + (v,))) #make it tuple to be hashable and sort it to be consistent

            #if better than the current score, replace it
            if score > scores [newset]: 
                scores [newset] = score
                bp [newset] = (tuple(U), v, best_u) #(previous_node, newly-added child, parent)
                
        
    #for each possible level/cardinality of the variable set, from 0 to |V|
    for l in xrange(len (V) + 1):

        #for each possibe variable set node of cardinality `l`
        nodes = filter(lambda n: len (n) == l, scores.keys())
        # print 'possible nodes are', nodes

        for u in nodes:
            #expand the node 
            expand (u)
            
    current = tuple (V)
    
    #backtracing
    while current != tuple ():
        print current
        current, child, parent = bp [current]
        print 'adding', child, 'parented by', parent
        print
        

    print '##please read bottom-up##'

    return scores [tuple (sorted(V))]
        

if __name__ == '__main__':
    from graph import BN, Variable
    from itertools import combinations
    
    HM = Variable('H3K27me3', ['Present', 'Absent']); HS = Variable('H2AK126su', ['Present', 'Absent']); H4A = Variable('H4AK5ac', ['Present', 'Absent']);
    HP = Variable('H2AS1ph', ['Present', 'Absent']); H3A = Variable('H3K27ac', ['Present', 'Absent']); TRANS = Variable('Transcription', ['Inactive', 'Active']);
    
    V = sorted([HM, HS, H4A, HP, H3A, TRANS])

    from data_reader import read_data
    data = read_data ('data.txt')

    g = BN (V, [], data)

    #computing family scores
    family_scores = {}

    for v1 in V:
        #single scores
        family_scores [(v1, )] = pw_score (g, v1)

    for v1, v2 in combinations (V, 2):
        #pair scores
        family_scores [(v1, v2)] = pw_score (g, v1, v2)
        family_scores [(v2, v1)] = family_scores [(v1, v2)]
    
    learn (V, family_scores)
    
