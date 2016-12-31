"""
defines behaviour of bfl master table field NonPacFixDurationsStd
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldNonPacFixDurationsStd(MasterField):
        def __init__(self, data):
                super(FieldNonPacFixDurationsStd, self).__init__("NonPacFixDurationsStd", "float", data)

        def calc(self):
                return self.PAC.stats['nonpacfixdurationsstd']

def instance(data):
        """
        make an instance of FieldNonPacFixDurationsStd and return it
        """
        return FieldNonPacFixDurationsStd(data)

