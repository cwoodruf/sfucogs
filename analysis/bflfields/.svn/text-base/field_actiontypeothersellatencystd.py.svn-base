"""
defines behaviour of bfl master table field ActionTypeOtherSELLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherSELLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherSELLatencyStd, self).__init__(
			"ActionTypeOtherSELLatencyStd", "float", data, "sel", False, "std")

def instance(data):
        """
        make an instance of FieldActionTypeOtherSELLatencyStd and return it
        """
        return FieldActionTypeOtherSELLatencyStd(data)

