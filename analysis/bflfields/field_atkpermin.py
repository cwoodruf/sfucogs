"""
defines behaviour of bfl master table field AtkPerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldAtkPerMin(PerMinField):
        def __init__(self, data):
                super(FieldAtkPerMin, self).__init__("AtkPerMin", "float", data,
				filters['atk'], "mean")

def instance(data):
        """
        make an instance of FieldAtkPerMin and return it
        """
        return FieldAtkPerMin(data)

