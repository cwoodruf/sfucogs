"""
defines behaviour of bfl master table field PACDurationMinusFixDuration
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPACDurationMinusFixDuration(MasterField):
        def __init__(self, data):
                super(FieldPACDurationMinusFixDuration, self).__init__("PACDurationMinusFixDuration", "float", data)

        def calc(self):
                return self.PAC.stats['pacdurationminusfixduration']

def instance(data):
        """
        make an instance of FieldPACDurationMinusFixDuration and return it
        """
        return FieldPACDurationMinusFixDuration(data)

