"""
defines behaviour of bfl master table field ActionTypeOtherMAPRCCLICKLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherMAPRCCLICKLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherMAPRCCLICKLatencyStd, self).__init__(
			"ActionTypeOtherMAPRCCLICKLatencyStd", "float", data, "mapRCClick", False, "std")

def instance(data):
        """
        make an instance of FieldActionTypeOtherMAPRCCLICKLatencyStd and return it
        """
        return FieldActionTypeOtherMAPRCCLICKLatencyStd(data)

