"""
defines behaviour of bfl master table field FocusAtkPerMinStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import focus_atk

class FieldFocusAtkPerMinStd(PerMinField):
        def __init__(self, data):
                super(FieldFocusAtkPerMinStd, self).__init__("FocusAtkPerMinStd", "float", data,
				focus_atk, "std")

def instance(data):
        """
        make an instance of FieldFocusAtkPerMinStd and return it
        """
        return FieldFocusAtkPerMinStd(data)

