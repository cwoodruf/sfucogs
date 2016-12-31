"""
defines behaviour of bfl master table field MapAblPerMinStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldMapAblPerMinStd(PerMinField):
        def __init__(self, data):
                super(FieldMapAblPerMinStd, self).__init__("MapAblPerMinStd", "float", data,
				filters['mapAbl'], "std")

def instance(data):
        """
        make an instance of FieldMapAblPerMinStd and return it
        """
        return FieldMapAblPerMinStd(data)

