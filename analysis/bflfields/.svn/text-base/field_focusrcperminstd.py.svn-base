"""
defines behaviour of bfl master table field FocusRcPerMinStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import focus_rc

class FieldFocusRcPerMinStd(PerMinField):
        def __init__(self, data):
                super(FieldFocusRcPerMinStd, self).__init__("FocusRcPerMinStd", "float", data,
				focus_rc, "mean")

def instance(data):
        """
        make an instance of FieldFocusRcPerMinStd and return it
        """
        return FieldFocusRcPerMinStd(data)

