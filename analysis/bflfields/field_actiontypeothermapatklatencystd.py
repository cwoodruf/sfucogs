"""
defines behaviour of bfl master table field ActionTypeOtherMAPATKLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherMAPATKLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherMAPATKLatencyStd, self).__init__(
			"ActionTypeOtherMAPATKLatencyStd", "float", data, "mapAtk", False, "std")

def instance(data):
        """
        make an instance of FieldActionTypeOtherMAPATKLatencyStd and return it
        """
        return FieldActionTypeOtherMAPATKLatencyStd(data)

