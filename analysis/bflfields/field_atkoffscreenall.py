"""
defines behaviour of bfl master table field AtkOffscreenAll
"""

from bflmasterfield import MasterField
from bflfields.filter import atk_offscreen

class FieldAtkOffscreenAll(MasterField):
        def __init__(self, data):
                super(FieldAtkOffscreenAll, self).__init__("AtkOffscreenAll", "float", data)

        def calc(self):
                return sum(self.filter.action_results(self.events, atk_offscreen))

def instance(data):
        """
        make an instance of FieldAtkOffscreenAll and return it
        """
        return FieldAtkOffscreenAll(data)

