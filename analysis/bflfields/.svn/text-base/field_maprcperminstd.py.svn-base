"""
defines behaviour of bfl master table field MapRCPerMinStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldMapRCPerMinStd(PerMinField):
        def __init__(self, data):
                super(FieldMapRCPerMinStd, self).__init__("MapRCPerMinStd", "float", data,
				filters['mapRCClick'], "std")

def instance(data):
        """
        make an instance of FieldMapRCPerMinStd and return it
        """
        return FieldMapRCPerMinStd(data)

