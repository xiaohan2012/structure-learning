"""
Inference in Markov Random Field
"""
from itertools import product

class Factor (object):
    def __init__ (self, variable, dependences, data):
        self.var = variable
        self.deps = dependences
        self.all_vars = tuple(sorted([self.var] + self.deps))
        dep_var_names = tuple(sorted(map(lambda dep_var: dep_var.var, dependences)))
        
        self.table = {}
        
        for var_value in self.var.values:
            for dep_values in product(*map(lambda dep_var: dep_var.values, dependences)):
                dep_values = list (dep_values)
                assignment = tuple([var_value] + dep_values)

                condition_tuple = zip(dep_var_names, dep_values)

                prob = data.filter (**dict(condition_tuple + [(self.var.var, var_value)])).sum (useMAP = True) / data.filter (**dict (condition_tuple)).sum (useMAP = True)
                
                self.table [assignment] = prob
                
    def get (self, assignment):
        """
        assignment: dict of Variable -> str|int|...
        """
        assignment_vars = tuple(sorted(assignment.keys ()))
        assignment_values = tuple(map(lambda var: assignment [var], assignment_vars))

        if  assignment_vars != self.all_vars:
            raise ValueError ('Wrong number of arguments. Expecting %d, but is %d' %(len (self.all_vars), len (assignment_vars)))
        else:
            return self.table [assignment_values]
            
    def __repr__ (self):
        return 'Variables: %s | %s' %(self.var.var, ' '.join(map (lambda var: var.var, self.deps)))

class Network (object):
    """
    The network used for exact inference on assignments involving all variable
    Note: the inference here is not general.
    """
    
    def __init__ (self, factors):
        self.factor_dict = dict (map(lambda f: (f.var, f), factors)) #dict: leading variable -> factor
        
    def total_joint_prob (self, assignment):
        """
        The joint probability of given assignment of **all** variables
        """
        product = 1
        for var, value in assignment.items ():
            factor = self.factor_dict [var]
            local_assignment = dict([(var, value)] + map(lambda v: (v, assignment [v]),factor.deps))
            product *=  factor.get(local_assignment)
        return product
        
    def factors (self):
        return self.factor_dict.values ()
        
def get_factors_MN (graph, variables, data):
    """
    Get the factors given the graph structure of a Markov network  and the varibles

    Param:
    graph: bidirected graph
    """
    considered_vars = []
    factors = []
    for var in variables:
        dependence = filter (lambda nbr: nbr not in considered_vars, 
                             graph [var])
        considered_vars.append (var)
        factors.append (Factor(var, dependence, data))
    
    return factors
    
def get_factors_BN (graph, variables, data):
    """
    Get the factors given the graph structure of a Bayesian network  and the varibles

    Param:
    graph: directed graph
    """
    considered_vars = []
    factors = []
    for var in variables:
        dependence = filter (lambda pred: pred not in considered_vars, 
                             graph.predecessors(var))
        considered_vars.append (var)
        factors.append (Factor(var, dependence, data))
    
    return factors
    
if __name__ == '__main__':
    import pickle, string
    from graph import Variable
    variables = map (lambda letter: Variable(letter, ['1', '2', '3']), string.uppercase)

    tree, _, __ = pickle.load (open ("chow_liu_tree.pickle", "r"))
    
    
    from suff_stats import Data
    from data_reader import read_row_data
    print "reading data..."
    data = Data(read_row_data ('train_data.txt'))

    from gpt import GPT_learn
    tree = GPT_learn (tree, data, variables) #edges according to the GPT algorithm
        
    import networkx as nx
    g = nx.DiGraph ()
    g.add_edges_from (tree)
    
    #get the markov network
    n = Network (get_factors_BN (g, variables, data))

    for factor in n.factors ():
        print factor
    values = '2 1 3 3 1 3 2 2 1 3 3 2 1 1 2 3 2 3 1 2 3 1 2 1 2 3'.split ()
    
    assignment = dict(zip(variables, values))
    print assignment
    print n.total_joint_prob (assignment)
