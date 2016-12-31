"""
defines behaviour of bfl master table field NonPacFixDurationsMean
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldNonPacFixDurationsMean(MasterField):
        def __init__(self, data):
                super(FieldNonPacFixDurationsMean, self).__init__("NonPacFixDurationsMean", "float", data)

        def calc(self):
                return self.PAC.stats['nonpacfixdurationsmean']

def instance(data):
        """
        make an instance of FieldNonPacFixDurationsMean and return it
        """
        return FieldNonPacFixDurationsMean(data)

