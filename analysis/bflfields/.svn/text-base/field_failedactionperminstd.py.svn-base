"""
defines behaviour of bfl master table field FailedActionPerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldFailedActionPerMinStd(PerMinField):
        def __init__(self, data):
                super(FieldFailedActionPerMinStd, self).__init__("FailedActionPerMinStd", "float", data,
				filters['f'], "std")

def instance(data):
        """
        make an instance of FieldFailedActionPerMin and return it
        """
        return FieldFailedActionPerMinStd(data)

