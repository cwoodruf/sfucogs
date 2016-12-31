"""
defines behaviour of bfl master table field LatencyToFixationMean
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldLatencyToFixationMean(MasterField):
        def __init__(self, data):
                super(FieldLatencyToFixationMean, self).__init__("LatencyToFixationMean", "float", data)

        def calc(self):
                return self.PAC.stats['latencytofixationmean']

def instance(data):
        """
        make an instance of FieldLatencyToFixationMean and return it
        """
        return FieldLatencyToFixationMean(data)

