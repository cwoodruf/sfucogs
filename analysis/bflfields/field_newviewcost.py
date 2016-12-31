"""
defines behaviour of bfl master table field NewViewCost
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldNewViewCost(MasterField):
        def __init__(self, data):
                super(FieldNewViewCost, self).__init__("NewViewCost", "float", data)

        def calc(self):
                return self.PAC.stats['newviewcostmean']

def instance(data):
        """
        make an instance of FieldNewViewCost and return it
        """
        return FieldNewViewCost(data)

