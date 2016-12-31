"""
defines behaviour of bfl master table field RcPropOffscreenAll
"""

from bflmasterfield import MasterField
from bflfields.filter import rc_offscreen

class FieldRcPropOffscreenAll(MasterField):
        def __init__(self, data):
                super(FieldRcPropOffscreenAll, self).__init__("RcPropOffscreenAll", "float", data)

        def calc(self):
                offscreen = self.filter.action_results(self.events, rc_offscreen)
                return float(sum(offscreen))/float(len(offscreen))

def instance(data):
        """
        make an instance of FieldRcPropOffscreenAll and return it
        """
        return FieldRcPropOffscreenAll(data)

