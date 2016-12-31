"""
defines behaviour of bfl master table field ActionTypeFirstBLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstBLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstBLatencyStd, self).__init__(
			"ActionTypeFirstBLatencyStd", "float", data, "b", True, "std")

def instance(data):
        """
        make an instance of FieldActionTypeFirstBLatencyStd and return it
        """
        return FieldActionTypeFirstBLatencyStd(data)

