"""
defines behaviour of bfl master table field AtkPerMinStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldAtkPerMinStd(PerMinField):
        def __init__(self, data):
                super(FieldAtkPerMinStd, self).__init__("AtkPerMinStd", "float", data,
				filters['atk'], "std")

def instance(data):
        """
        make an instance of FieldAtkPerMinStd and return it
        """
        return FieldAtkPerMinStd(data)

