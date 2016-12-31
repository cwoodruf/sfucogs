"""
defines behaviour of bfl master table field ActionTypeOtherHKLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherHKLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherHKLatencyStd, self).__init__(
			"ActionTypeOtherHKLatencyStd", "float", data, "hk", False, "std")

def instance(data):
        """
        make an instance of FieldActionTypeOtherHKLatencyStd and return it
        """
        return FieldActionTypeOtherHKLatencyStd(data)

