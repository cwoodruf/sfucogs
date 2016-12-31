"""
defines behaviour of bfl master table field ActionTypeFirstMAPRCCLICKLatencyStd
"""

from bflfields.paclatencyfield import PacLatencyField
from bflfields.filter import filters

class FieldActionTypeFirstMAPRCCLICKLatencyStd(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstMAPRCCLICKLatencyStd, self).__init__(
			"ActionTypeFirstMAPRCCLICKLatencyStd", "float", data, "mapRCClick", True, "std")

def instance(data):
        """
        make an instance of FieldActionTypeFirstMAPRCCLICKLatencyStd and return it
        """
        return FieldActionTypeFirstMAPRCCLICKLatencyStd(data)

