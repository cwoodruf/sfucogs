"""
defines behaviour of bfl master table field ActionTypeFirstMAPATKLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstMAPATKLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstMAPATKLatencyMean, self).__init__(
			"ActionTypeFirstMAPATKLatencyMean", "float", data, "mapAtk", True, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeFirstMAPATKLatencyMean and return it
        """
        return FieldActionTypeFirstMAPATKLatencyMean(data)

