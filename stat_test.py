"""
The module for statistical testing
"""
from scipy.stats import chi2_contingency

def marginal_independence (v1, v2, data, hypo_supporting_p = 0.05):
    """
    using chi independence testing to test the independence between v1 and v2
    """
    table = [[data.filter (**{v1.var: val1, v2.var: val2}).sum () for val2 in v2.values] for val1 in v1.values]

    chi2, p, dof, ex = chi2_contingency (table)
    
    print 'Independence Testing: '
    print 'Testing %s and %s' %(v1.var, v2.var)
    print 'p value is %f, thus we %s the independence hypothesis' %(p, p >= hypo_supporting_p and 'support' or 'reject')

    return p >= hypo_supporting_p



    
