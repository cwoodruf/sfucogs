"""
defines behaviour of bfl master table field DistanceBetweenPACsMean
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldDistanceBetweenPACsMean(MasterField):
        def __init__(self, data):
                super(FieldDistanceBetweenPACsMean, self).__init__("DistanceBetweenPACsMean", "float", data)

        def calc(self):
                return self.PAC.stats['distancebetweenpacsmean']

def instance(data):
        """
        make an instance of FieldDistanceBetweenPACsMean and return it
        """
        return FieldDistanceBetweenPACsMean(data)

