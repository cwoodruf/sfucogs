"""
defines behaviour of bfl master table field ActionTypeOtherATKLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherATKLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherATKLatencyStd, self).__init__(
			"ActionTypeOtherATKLatencyStd", "float", data, "atk", False, "std")

def instance(data):
        """
        make an instance of FieldActionTypeOtherATKLatencyStd and return it
        """
        return FieldActionTypeOtherATKLatencyStd(data)

