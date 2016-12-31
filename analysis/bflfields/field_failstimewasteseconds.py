"""
defines behaviour of bfl master table field FailsTimeWasteSeconds
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldFailsTimeWasteSeconds(MasterField):
        def __init__(self, data):
                super(FieldFailsTimeWasteSeconds, self).__init__("FailsTimeWasteSeconds", "float", data)

        def calc(self):
                count, seconds = self.filter.field_failstime(self)
                return seconds

def instance(data):
        """
        make an instance of FieldFailsTimeWasteSeconds and return it
        """
        return FieldFailsTimeWasteSeconds(data)

