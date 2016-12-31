"""
defines behaviour of bfl master table field FixDurationStd
"""

from bflmasterfield import MasterField
import bflstats

class FieldFixDurationStd(MasterField):
        def __init__(self, data):
                super(FieldFixDurationStd, self).__init__("FixDurationStd", "float", data)

        def calc(self):
                return bflstats.stdev(self.PAC.durations)

def instance(data):
        """
        make an instance of FieldFixDurationStd and return it
        """
        return FieldFixDurationStd(data)

