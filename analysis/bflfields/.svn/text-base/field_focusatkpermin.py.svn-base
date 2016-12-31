"""
defines behaviour of bfl master table field FocusAtkPerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import focus_atk

class FieldFocusAtkPerMin(PerMinField):
        def __init__(self, data):
                super(FieldFocusAtkPerMin, self).__init__("FocusAtkPerMin", "float", data,
				focus_atk, "mean")

def instance(data):
        """
        make an instance of FieldFocusAtkPerMin and return it
        """
        return FieldFocusAtkPerMin(data)

