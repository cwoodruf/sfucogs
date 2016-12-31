"""
defines behaviour of bfl master table field FixDurationMean
"""

from bflmasterfield import MasterField
import bflstats

class FieldFixDurationMean(MasterField):
        def __init__(self, data):
                super(FieldFixDurationMean, self).__init__("FixDurationMean", "float", data)

        def calc(self):
                return bflstats.mean(self.PAC.durations)

def instance(data):
        """
        make an instance of FieldFixDurationMean and return it
        """
        return FieldFixDurationMean(data)

