"""
unfortunately the python statistics module is not automatically 
included with the standard python distribution - at least not on windows
also, want the stats routines to not fail so easily
"""
from decimal import Decimal
import math

def mean(l):
        if len(l) == 0: return None
        return float(sum([float(v) for v in l])/float(len(l)))

def stdev(l):
        """
        sample standard deviation
        """
        if len(l) == 0: return None
        if len(l) == 1: return 0.0
        ss = sum([float(v) * float(v) for v in l])
        s = sum([float(v) for v in l])
        N = float(len(l))
        var = (ss - (s*s)/N)/(N - 1.0)
        return float(math.sqrt(var))

def median(l):
        if len(l) == 0: return None
        s = sorted(l)
        try:
                return float(s[(len(l)+1)/2])
        except Exception as e:
                print e
                return None

