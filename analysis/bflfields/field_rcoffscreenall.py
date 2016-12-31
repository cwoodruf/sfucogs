"""
defines behaviour of bfl master table field RcOffscreenAll
"""

from bflmasterfield import MasterField
from bflfields.filter import rc_offscreen

class FieldRcOffscreenAll(MasterField):
        def __init__(self, data):
                super(FieldRcOffscreenAll, self).__init__("RcOffscreenAll", "float", data)

        def calc(self):
                return sum(self.filter.action_results(self.events, rc_offscreen))

def instance(data):
        """
        make an instance of FieldRcOffscreenAll and return it
        """
        return FieldRcOffscreenAll(data)

