from __future__ import division
import math

def product (vals):
    return reduce (lambda acc, val: acc * val, vals, 1)
    
def mdl (g):
    """
    the Minimum Descrition Length calculator for Bayesian network g
    """
    n = len (g.V) # the variable count
    N = len (g.data)# the sample number
    
    logn = math.log (n, 2) # value of log (n)
    logN = math.log (N, 2) # value of log (N)
    
    complexity = sum([logn * len(g.getParentOf(v)) + logN / 2 * product (g.getParentOf(v).cards()) * (v.card - 1) 
                      for v in g.V]) 
    
    logll = 0 #log likelihood 
    for v in g.V:
        for parentVals in g.getParentOf (v).allAssignments ():
            for val in v.values:
                # assignment of the parent
                parentAssignments = dict(zip(map(lambda p: p.var, g.getParentOf (v)), parentVals))
                
                assignments = parentAssignments.copy () #including the child value in the assignment
                assignments[v.var] = val
                
                #the empirical count of the given assignments of parent
                parentN = g.N (**parentAssignments)
                
                #the empirical count of the given assignments of parent and child
                childN = g.N (**assignments)

                if childN != 0:
                    logll += (childN * math.log (childN / parentN, 2))                
                else:
                    pass #nothing happens

    return -logll + complexity
                
def BDeu (g, alpha):
    """
    the BDeu score for graph g
    """
    lll = 0 # log likelihood

    for v in g.V:
        for parentVals in g.getParentOf (v).allAssignments ():
            alpha_denom = alpha / product (g.getParentOf (v).cards())
            for val in v.values:
                alpha_numer = alpha / (product (g.getParentOf (v).cards()) * len (v.values))
                
                # assignment of the parent
                parentAssignments = dict(zip(map(lambda p: p.var, g.getParentOf (v)), parentVals))
                
                assignments = parentAssignments.copy () #including the child value in the assignment
                assignments[v.var] = val
                
                #the empirical count of the given assignments of parent
                parentN = g.N (**parentAssignments)
                
                #the empirical count of the given assignments of parent and child
                childN = g.N (**assignments)
                
                lll +=  childN * math.log ((childN + alpha_numer) / (parentN + alpha_denom), 2)
                
    return lll
