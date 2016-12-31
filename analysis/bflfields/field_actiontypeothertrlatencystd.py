"""
defines behaviour of bfl master table field ActionTypeOtherTRLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherTRLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherTRLatencyStd, self).__init__(
			"ActionTypeOtherTRLatencyStd", "float", data, "tr", False, "std")

def instance(data):
        """
        make an instance of FieldActionTypeOtherTRLatencyStd and return it
        """
        return FieldActionTypeOtherTRLatencyStd(data)

