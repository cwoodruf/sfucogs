"""
defines behaviour of bfl master table field ActionTypeFirstSELLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstSELLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstSELLatencyStd, self).__init__(
			"ActionTypeFirstSELLatencyStd", "float", data, "sel", True, "std")

def instance(data):
        """
        make an instance of FieldActionTypeFirstSELLatencyStd and return it
        """
        return FieldActionTypeFirstSELLatencyStd(data)

