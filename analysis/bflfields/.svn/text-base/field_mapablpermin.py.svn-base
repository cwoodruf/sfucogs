"""
defines behaviour of bfl master table field MapAblPerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldMapAblPerMin(PerMinField):
        def __init__(self, data):
                super(FieldMapAblPerMin, self).__init__("MapAblPerMin", "float", data,
				filters['mapAbl'], "mean")

def instance(data):
        """
        make an instance of FieldMapAblPerMin and return it
        """
        return FieldMapAblPerMin(data)

