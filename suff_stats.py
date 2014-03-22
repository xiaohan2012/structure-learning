from __future__ import division

class Data (list):
    def __init__ (self, data, prev={}):
        #prev is used to determined the alpha value in the MAP parameter estimation
        self.d = data;
        self.prev = prev
        
        super (Data, self).__init__ (data)        
        
    def filter (self, **kwargs):
        return Data(filter(lambda row: reduce (lambda acc, (field, value): acc and (row [field] == value), kwargs.items (), True),
                           self.d), prev=kwargs)

    def sum (self, useMAP = True, alpha = 1):
        if useMAP:
            return reduce (lambda acc, row: acc + row['count'], self.d, 0) +  alpha / (2 ** len(self.prev))
        else:
            return reduce (lambda acc, row: acc + row['count'], self.d, 0)
            
    
if __name__ == '__main__':
    
    rows=  [{'B': 'High',  'A': 'High',  'R': 'High',	'S': 'Low' ,    'T': 'High',	'P': 'Low' , 'count': 15 },
            {'B': 'High',  'A': 'Low' ,  'R': 'High', 	'S': 'High', 	'T': 'High', 	'P': 'Low' , 'count': 5  },
            {'B': 'High',  'A': 'Low' ,  'R': 'High', 	'S': 'Low' , 	'T': 'High', 	'P': 'Low' , 'count': 3  },
            {'B': 'High',  'A': 'High',  'R': 'Low' ,	'S': 'High', 	'T': 'Low' ,	'P': 'High', 'count':  2 },
            {'B': 'Low' ,  'A': 'Low' ,  'R': 'Low' ,	'S': 'High', 	'T': 'Low' ,	'P': 'High', 'count': 25 },
            {'B': 'Low' ,  'A': 'Low' ,  'R': 'Low' ,	'S': 'High', 	'T': 'High', 	'P': 'High', 'count': 7  },
            {'B': 'Low' ,  'A': 'High',  'R': 'Low' ,	'S': 'High', 	'T': 'High', 	'P': 'Low' , 'count': 3  },
            {'B': 'Low' ,  'A': 'Low' ,  'R': 'High',	'S': 'High', 	'T': 'High', 	'P': 'Low' , 'count': 5  }]
    d = Data (rows)

    print 'P (B)'
    print '%.4f' %(d.filter (B = 'High').sum () / d.sum ())
    print '%.4f' %(d.filter (B= 'Low').sum () / d.sum ())
    print 
    
    print 'P (A / B = High)'
    print '%.4f' %(d.filter (B = 'High', A= 'High').sum () / d.filter (B = 'High').sum ())
    print '%.4f' %(d.filter (B = 'High', A= 'Low').sum () / d.filter (B = 'High').sum ())
    print 'P (A / B = Low)'
    print '%.4f' %(d.filter (B= 'Low', A= 'High').sum () / d.filter (B= 'Low').sum ())
    print '%.4f' %(d.filter (B= 'Low', A= 'Low').sum () / d.filter (B= 'Low').sum ())
    print 

    print 'P (R / B = High'
    print '%.4f' %(d.filter (B = 'High', R= 'High').sum () / d.filter (B = 'High').sum ())
    print '%.4f' %(d.filter (B = 'High', R= 'Low').sum () / d.filter (B = 'High').sum ())
    print 'P (R / B = Low)'
    print '%.4f' %(d.filter (B= 'Low', R= 'High').sum () / d.filter (B= 'Low').sum ())
    print '%.4f' %(d.filter (B= 'Low', R= 'Low').sum () / d.filter (B= 'Low').sum ())
    print 

    print 'P (S / A = High)'
    print '%.4f' %(d.filter (A= 'High', S= 'High').sum () / d.filter (A= 'High').sum ())
    print '%.4f' %(d.filter (A= 'High', S= 'Low').sum () / d.filter (A= 'High').sum ())
    print 'P (S / A = Low)'
    print '%.4f' %(d.filter (A= 'Low', S= 'High').sum () / d.filter (A= 'Low').sum ())
    print '%.4f' %(d.filter (A= 'Low', S= 'Low').sum () / d.filter (A= 'Low').sum ())

    print 'P (T / R = High)'
    print '%.4f' %(d.filter (R= 'High', T= 'High').sum () / d.filter (R= 'High').sum ())
    print '%.4f' %(d.filter (R= 'High', T= 'Low').sum () / d.filter (R= 'High').sum ())
    print 'P (T / R = Low)'
    print '%.4f' %(d.filter (R= 'Low', T= 'High').sum () / d.filter (R= 'Low').sum ())
    print '%.4f' %(d.filter (R= 'Low', T= 'Low').sum () / d.filter (R= 'Low').sum ())
    print 

    print 'P (P / T = High, S = High)'
    print '%.4f' %(d.filter (S= 'High', T= 'High', P= 'High').sum () / d.filter (S= 'High', T= 'High').sum ())
    print '%.4f' %(d.filter (S= 'High', T= 'High', P= 'Low').sum () / d.filter (S= 'High', T= 'High').sum ())
    print 'P (P / T = Low, S = High)'
    print '%.4f' %(d.filter (S= 'High', T= 'Low', P= 'High').sum () / d.filter (S= 'High', T= 'Low').sum ())
    print '%.4f' %(d.filter (S= 'High', T= 'Low', P= 'Low').sum () / d.filter (S= 'High', T= 'Low').sum ())
    print 'P (P / T = High, S = Low)'
    print '%.4f' %(d.filter (S= 'Low', T= 'High', P= 'High').sum () / d.filter (S= 'Low', T= 'High').sum ())
    print '%.4f' %(d.filter (S= 'Low', T= 'High', P= 'Low').sum () / d.filter (S= 'Low', T= 'High').sum ())
    print 'P (P / T = Low, S = Low)'
    print '%.4f' %(d.filter (S= 'Low', T= 'Low', P= 'High').sum () / d.filter (S= 'Low', T= 'Low').sum ())
    print '%.4f' %(d.filter (S= 'Low', T= 'Low', P= 'Low').sum () / d.filter (S= 'Low', T= 'Low').sum ())
