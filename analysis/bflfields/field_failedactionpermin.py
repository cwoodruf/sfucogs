"""
defines behaviour of bfl master table field FailedActionPerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldFailedActionPerMin(PerMinField):
        def __init__(self, data):
                super(FieldFailedActionPerMin, self).__init__("FailedActionPerMin", "float", data,
				filters['f'], "mean")

def instance(data):
        """
        make an instance of FieldFailedActionPerMin and return it
        """
        return FieldFailedActionPerMin(data)

