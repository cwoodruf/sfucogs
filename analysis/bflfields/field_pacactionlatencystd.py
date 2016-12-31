"""
defines behaviour of bfl master table field PACActionLatencyStd
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPACActionLatencyStd(MasterField):
        def __init__(self, data):
                super(FieldPACActionLatencyStd, self).__init__("PACActionLatencyStd", "float", data)

        def calc(self):
                return self.PAC.stats['pacactionlatencystd']

def instance(data):
        """
        make an instance of FieldPACActionLatencyStd and return it
        """
        return FieldPACActionLatencyStd(data)

