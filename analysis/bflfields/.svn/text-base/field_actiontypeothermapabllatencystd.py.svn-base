"""
defines behaviour of bfl master table field ActionTypeOtherMAPABLLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherMAPABLLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherMAPABLLatencyStd, self).__init__(
			"ActionTypeOtherMAPABLLatencyStd", "float", data, "mapAbl", False, "std")

def instance(data):
        """
        make an instance of FieldActionTypeOtherMAPABLLatencyStd and return it
        """
        return FieldActionTypeOtherMAPABLLatencyStd(data)

