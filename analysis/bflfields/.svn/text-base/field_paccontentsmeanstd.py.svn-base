"""
defines behaviour of bfl master table field PACContentsMeanStd
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPACContentsMeanStd(MasterField):
        def __init__(self, data):
                super(FieldPACContentsMeanStd, self).__init__("PACContentsMeanStd", "float", data)

        def calc(self):
                return self.PAC.stats['paccontentsmeanstd']

def instance(data):
        """
        make an instance of FieldPACContentsMeanStd and return it
        """
        return FieldPACContentsMeanStd(data)

