"""
defines behaviour of bfl master table field FocusRcPerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import focus_rc

class FieldFocusRcPerMin(PerMinField):
        def __init__(self, data):
                super(FieldFocusRcPerMin, self).__init__("FocusRcPerMin", "float", data,
				focus_rc, "mean")

def instance(data):
        """
        make an instance of FieldFocusRcPerMin and return it
        """
        return FieldFocusRcPerMin(data)

