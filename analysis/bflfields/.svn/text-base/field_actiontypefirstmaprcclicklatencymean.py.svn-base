"""
defines behaviour of bfl master table field ActionTypeFirstMAPRCCLICKLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstMAPRCCLICKLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstMAPRCCLICKLatencyMean, self).__init__(
			"ActionTypeFirstMAPRCCLICKLatencyMean", "float", data, "mapRCClick", True, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeFirstMAPRCCLICKLatencyMean and return it
        """
        return FieldActionTypeFirstMAPRCCLICKLatencyMean(data)

