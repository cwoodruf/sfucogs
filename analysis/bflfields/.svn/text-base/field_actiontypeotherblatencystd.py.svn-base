"""
defines behaviour of bfl master table field ActionTypeOtherBLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField
from bflfields.filter import filters

class FieldActionTypeOtherBLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherBLatencyStd, self).__init__(
			"ActionTypeOtherBLatencyStd", "float", data, "b", False, "std")

def instance(data):
        """
        make an instance of FieldActionTypeOtherBLatencyStd and return it
        """
        return FieldActionTypeOtherBLatencyStd(data)

