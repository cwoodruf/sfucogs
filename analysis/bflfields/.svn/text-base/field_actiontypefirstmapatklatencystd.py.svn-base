"""
defines behaviour of bfl master table field ActionTypeFirstMAPATKLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstMAPATKLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstMAPATKLatencyStd, self).__init__(
			"ActionTypeFirstMAPATKLatencyStd", "float", data, "mapAtk", True, "std")

def instance(data):
        """
        make an instance of FieldActionTypeFirstMAPATKLatencyStd and return it
        """
        return FieldActionTypeFirstMAPATKLatencyStd(data)

