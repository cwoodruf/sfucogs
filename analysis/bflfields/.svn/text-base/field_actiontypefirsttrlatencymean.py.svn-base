"""
defines behaviour of bfl master table field ActionTypeFirstTRLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstTRLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstTRLatencyMean, self).__init__(
			"ActionTypeFirstTRLatencyMean", "float", data, "tr", True, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeFirstTRLatencyMean and return it
        """
        return FieldActionTypeFirstTRLatencyMean(data)

