"""
defines behaviour of bfl master table field PacCountOverFixCount
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPacCountOverFixCount(MasterField):
        def __init__(self, data):
                super(FieldPacCountOverFixCount, self).__init__("PacCountOverFixCount", "float", data)

        def calc(self):
                return self.PAC.stats['paccountoverfixcount']

def instance(data):
        """
        make an instance of FieldPacCountOverFixCount and return it
        """
        return FieldPacCountOverFixCount(data)

