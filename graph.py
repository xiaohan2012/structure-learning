from suff_stats import Data

class BN (object):
    """Bayesian Network with data"""
    def __init__ (self, V, E, data):
        self.E = E
        self.V = V
        self.data = Data(data)
        
        # constructing the parents
        #be functional!
        # for from_v, to_v in self.E:
        #     to_v.parents.append (from_v)
        self.parentTable = {}
        
    def N (self, useMap = False, alpha = 1, **kwargs):
        """get sufficient statistics from the data"""
        return self.data.filter (**kwargs).sum (useMap, alpha)

    def getParentOf (self, v):
        if not self.parentTable.has_key (v):
            self.parentTable [v] = Parents(map(lambda (from_v, _): from_v, filter (lambda (_, to_v): to_v == v, self.E)))
        return self.parentTable [v]
        
    def __str__ (self):
        return '\n'.join (map (lambda v: str(v) + ('' if len(self.getParentOf (v)) == 0 else ' '.join (map(lambda p: str (p), self.getParentOf (v)))) , self.V))

class Parents (list):
    def cards (self):
        """the cardinalities of the parents"""
        return map (lambda p: p.card, self)
        
    def allAssignments (self):
        """return all possible assignments of the parents"""
        from itertools import product
        return product (*map (lambda p: p.values, self))
            
class Variable (object):
    def __init__ (self, var, values):
        self.var = var
        self.values = values

        self.card = len(self.values) # the cardinality
    
    def __str__ (self):
        return "%s" %(self.var)
        
    def __repr__ (self):
        return str (self)

    def __eq__ (self, obj):
        return hasattr (obj, 'var') and hasattr (obj, 'values') and self.var == obj.var and self.values == obj.values
        
    def __hash__(self):
        return hash (self.var + ','.join(self.values))

from data_reader import read_data
data = read_data ('data.txt')

HM = Variable('H3K27me3', ['Present', 'Absent']); HS = Variable('H2AK126su', ['Present', 'Absent']); H4A = Variable('H4AK5ac', ['Present', 'Absent']);
HP = Variable('H2AS1ph', ['Present', 'Absent']); H3A = Variable('H3K27ac', ['Present', 'Absent']); TRANS = Variable('Transcription', ['Inactive', 'Active']);
    
V = [HM, HS, H4A, HP, H3A, TRANS]

def get_g1 ():

    E = [(HM, HS), (HM, H3A), (H3A, H4A), (H4A, TRANS), (H3A, HP)]

    G = BN (V, E, data)

    return G

def get_g2 ():
    
    E = [(HM, HS), (HM, H3A), (HS, H3A), (HS, H4A), (H3A, H4A), (H4A, TRANS), (H3A, TRANS), (H3A, HP)]

    G = BN (V, E, data)

    return G
    
def g1_score ():
    G = get_g1 ()
    
    print 'mdl', mdl (G)
    print 'BDeu 1', BDeu (G, 1)
    print 'BDeu 1000', BDeu (G, 1000)
    
def g2_score ():
    G = get_g2 ()
    
    print 'mdl',  mdl (G)
    print 'BDeu 1',  BDeu (G, 1)
    print 'BDeu 1000', BDeu (G, 1000)


def search_for_improvement ():
    g = get_g1 ()
    
    #add edge
    from itertools import permutations

    possible_edges = set(permutations (g.V, 2)) - set (g.E)

    gMDL, gBD1, gBD1000  = mdl (g), BDeu (g, 1), BDeu (g, 1000)
    
    for edge in possible_edges:
        
        E = g.E + [edge]

        newg = BN (g.V, E, g.data)
        
        if mdl (newg) < gMDL and BDeu (newg, 1) > gBD1 and BDeu (newg, 1000) > gBD1000:
            print 'bingo! adding edge',edge
            print 'MDL from', mdl (newg), 'to',  gMDL
            print 'BDeu (alpha=1) from', BDeu (newg, 1), 'to' , gBD1
            print 'BDeu (alpha=1000) from', BDeu (newg, 1000), 'to' , gBD1000
            print 
            
if __name__ == '__main__':
    from scores import mdl, BDeu
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv [1] == 'improve':
        search_for_improvement ()
    else:
        print 'G1'
        g1_score ()
        print '\nG2'
        g2_score ()

        
        
