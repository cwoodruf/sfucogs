"""
defines behaviour of bfl master table field ActionTypeFirstALatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstALatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstALatencyStd, self).__init__(
			"ActionTypeFirstALatencyStd", "float", data, "a", True, "std")

def instance(data):
        """
        make an instance of FieldActionTypeFirstALatencyStd and return it
        """
        return FieldActionTypeFirstALatencyStd(data)

