"""
defines behaviour of bfl master table field ActionTypeFirstFLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstFLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstFLatencyStd, self).__init__(
			"ActionTypeFirstFLatencyStd", "float", data, "f", True, "std")

def instance(data):
        """
        make an instance of FieldActionTypeFirstFLatencyStd and return it
        """
        return FieldActionTypeFirstFLatencyStd(data)

