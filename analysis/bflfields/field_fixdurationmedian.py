"""
defines behaviour of bfl master table field FixDurationMedian
"""

from bflmasterfield import MasterField
import bflstats

class FieldFixDurationMedian(MasterField):
        def __init__(self, data):
                super(FieldFixDurationMedian, self).__init__("FixDurationMedian", "float", data)

        def calc(self):
                return bflstats.median(self.PAC.durations)

def instance(data):
        """
        make an instance of FieldFixDurationMedian and return it
        """
        return FieldFixDurationMedian(data)

