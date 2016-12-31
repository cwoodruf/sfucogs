"""
defines behaviour of bfl master table field ActionTypeFirstTRLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstTRLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstTRLatencyStd, self).__init__(
			"ActionTypeFirstTRLatencyStd", "float", data, "tr", True, "std")

def instance(data):
        """
        make an instance of FieldActionTypeFirstTRLatencyStd and return it
        """
        return FieldActionTypeFirstTRLatencyStd(data)

