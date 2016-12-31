"""
defines behaviour of bfl master table field AtkPropOffscreenAll
"""

from bflmasterfield import MasterField
from bflfields.filter import atk_offscreen

class FieldAtkPropOffscreenAll(MasterField):
        def __init__(self, data):
                super(FieldAtkPropOffscreenAll, self).__init__("AtkPropOffscreenAll", "float", data)

        def calc(self):
                offscreen = self.filter.action_results(self.events, atk_offscreen)
                if len(offscreen) == 0: return None
                return float(sum(offscreen))/float(len(offscreen))

def instance(data):
        """
        make an instance of FieldAtkPropOffscreenAll and return it
        """
        return FieldAtkPropOffscreenAll(data)

