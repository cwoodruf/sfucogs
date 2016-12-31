"""
defines behaviour of bfl master table field LatencyToFixationStd
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldLatencyToFixationStd(MasterField):
        def __init__(self, data):
                super(FieldLatencyToFixationStd, self).__init__("LatencyToFixationStd", "float", data)

        def calc(self):
                return self.PAC.stats['latencytofixationstd']

def instance(data):
        """
        make an instance of FieldLatencyToFixationStd and return it
        """
        return FieldLatencyToFixationStd(data)

