"""
defines behaviour of bfl master table field PACCount
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPACCount(MasterField):
        def __init__(self, data):
                super(FieldPACCount, self).__init__("PACCount", "float", data)

        def calc(self):
                return len(self.PAC.pacs)

def instance(data):
        """
        make an instance of FieldPACCount and return it
        """
        return FieldPACCount(data)

