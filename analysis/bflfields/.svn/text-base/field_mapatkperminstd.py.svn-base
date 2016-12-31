"""
defines behaviour of bfl master table field MapAtkPerMinStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldMapAtkPerMinStd(PerMinField):
        def __init__(self, data):
                super(FieldMapAtkPerMinStd, self).__init__("MapAtkPerMinStd", "float", data,
				filters['mapAtk'], "std")

def instance(data):
        """
        make an instance of FieldMapAtkPerMinStd and return it
        """
        return FieldMapAtkPerMinStd(data)

