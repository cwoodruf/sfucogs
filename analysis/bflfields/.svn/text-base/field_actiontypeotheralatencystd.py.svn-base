"""
defines behaviour of bfl master table field ActionTypeOtherALatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherALatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherALatencyStd, self).__init__(
			"ActionTypeOtherALatencyStd", "float", data, "a", False, "std")

def instance(data):
        """
        make an instance of FieldActionTypeOtherALatencyStd and return it
        """
        return FieldActionTypeOtherALatencyStd(data)

