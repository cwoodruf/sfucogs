"""
defines behaviour of bfl master table field ActionTypeFirstATKLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstATKLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstATKLatencyStd, self).__init__(
			"ActionTypeFirstATKLatencyStd", "float", data, "atk", True, "std")

def instance(data):
        """
        make an instance of FieldActionTypeFirstATKLatencyStd and return it
        """
        return FieldActionTypeFirstATKLatencyStd(data)

