"""
defines behaviour of bfl master table field MapAtkPerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldMapAtkPerMin(PerMinField):
        def __init__(self, data):
                super(FieldMapAtkPerMin, self).__init__("MapAtkPerMin", "float", data,
				filters['mapAtk'], "mean")

def instance(data):
        """
        make an instance of FieldMapAtkPerMin and return it
        """
        return FieldMapAtkPerMin(data)

