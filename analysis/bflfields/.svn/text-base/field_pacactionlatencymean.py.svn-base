"""
defines behaviour of bfl master table field PACActionLatencyMean
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPACActionLatencyMean(MasterField):
        def __init__(self, data):
                super(FieldPACActionLatencyMean, self).__init__("PACActionLatencyMean", "float", data)

        def calc(self):
                return self.PAC.stats['pacactionlatencymean']

def instance(data):
        """
        make an instance of FieldPACActionLatencyMean and return it
        """
        return FieldPACActionLatencyMean(data)

