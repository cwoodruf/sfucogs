"""
defines behaviour of bfl master table field PACActionLatencyMax
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPACActionLatencyMax(MasterField):
        def __init__(self, data):
                super(FieldPACActionLatencyMax, self).__init__("PACActionLatencyMax", "float", data)

        def calc(self):
                return self.PAC.stats['pacactionlatencymax']

def instance(data):
        """
        make an instance of FieldPACActionLatencyMax and return it
        """
        return FieldPACActionLatencyMax(data)

