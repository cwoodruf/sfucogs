"""
defines behaviour of bfl master table field PACDurationsMean
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPACDurationsMean(MasterField):
        def __init__(self, data):
                super(FieldPACDurationsMean, self).__init__("PACDurationsMean", "float", data)

        def calc(self):
                return self.PAC.stats['pacdurationsmean']

def instance(data):
        """
        make an instance of FieldPACDurationsMean and return it
        """
        return FieldPACDurationsMean(data)

