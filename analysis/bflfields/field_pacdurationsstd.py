"""
defines behaviour of bfl master table field PACDurationsStd
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPACDurationsStd(MasterField):
        def __init__(self, data):
                super(FieldPACDurationsStd, self).__init__("PACDurationsStd", "float", data)

        def calc(self):
                return self.PAC.stats['pacdurationsstd']

def instance(data):
        """
        make an instance of FieldPACDurationsStd and return it
        """
        return FieldPACDurationsStd(data)

