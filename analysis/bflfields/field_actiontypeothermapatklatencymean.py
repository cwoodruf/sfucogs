"""
defines behaviour of bfl master table field ActionTypeOtherMAPATKLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherMAPATKLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherMAPATKLatencyMean, self).__init__(
			"ActionTypeOtherMAPATKLatencyMean", "float", data, "mapAtk", False, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeOtherMAPATKLatencyMean and return it
        """
        return FieldActionTypeOtherMAPATKLatencyMean(data)

