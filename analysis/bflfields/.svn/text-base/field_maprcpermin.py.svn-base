"""
defines behaviour of bfl master table field MapRCPerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldMapRCPerMin(PerMinField):
        def __init__(self, data):
                super(FieldMapRCPerMin, self).__init__("MapRCPerMin", "float", data,
				filters['mapRCClick'], "mean")

def instance(data):
        """
        make an instance of FieldMapRCPerMin and return it
        """
        return FieldMapRCPerMin(data)

