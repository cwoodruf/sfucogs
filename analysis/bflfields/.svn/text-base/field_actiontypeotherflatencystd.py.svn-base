"""
defines behaviour of bfl master table field ActionTypeOtherFLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherFLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherFLatencyStd, self).__init__(
			"ActionTypeOtherFLatencyStd", "float", data, "f", False, "std")

def instance(data):
        """
        make an instance of FieldActionTypeOtherFLatencyStd and return it
        """
        return FieldActionTypeOtherFLatencyStd(data)

