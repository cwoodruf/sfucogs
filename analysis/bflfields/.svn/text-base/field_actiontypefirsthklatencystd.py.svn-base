"""
defines behaviour of bfl master table field ActionTypeFirstHKLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstHKLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstHKLatencyStd, self).__init__(
			"ActionTypeFirstHKLatencyStd", "float", data, "hk", True, "std")

def instance(data):
        """
        make an instance of FieldActionTypeFirstHKLatencyStd and return it
        """
        return FieldActionTypeFirstHKLatencyStd(data)

