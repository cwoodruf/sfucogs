"""
defines behaviour of bfl master table field PACContentsMean
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPACContentsMean(MasterField):
        def __init__(self, data):
                super(FieldPACContentsMean, self).__init__("PACContentsMean", "float", data)

        def calc(self):
                return self.PAC.stats['paccontentsmean']

def instance(data):
        """
        make an instance of FieldPACContentsMean and return it
        """
        return FieldPACContentsMean(data)

