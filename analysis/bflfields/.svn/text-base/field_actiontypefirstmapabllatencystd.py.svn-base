"""
defines behaviour of bfl master table field ActionTypeFirstMAPABLLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstMAPABLLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstMAPABLLatencyStd, self).__init__(
			"ActionTypeFirstMAPABLLatencyStd", "float", data, "mapAbl", True, "std")

def instance(data):
        """
        make an instance of FieldActionTypeFirstMAPABLLatencyStd and return it
        """
        return FieldActionTypeFirstMAPABLLatencyStd(data)

