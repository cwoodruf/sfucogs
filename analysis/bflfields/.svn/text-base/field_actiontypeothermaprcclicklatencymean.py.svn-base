"""
defines behaviour of bfl master table field ActionTypeOtherMAPRCCLICKLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherMAPRCCLICKLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherMAPRCCLICKLatencyMean, self).__init__(
			"ActionTypeOtherMAPRCCLICKLatencyMean", "float", data, "mapRCClick", False, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeOtherMAPRCCLICKLatencyMean and return it
        """
        return FieldActionTypeOtherMAPRCCLICKLatencyMean(data)

