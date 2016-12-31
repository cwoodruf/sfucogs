"""
defines behaviour of bfl master table field ActionTypeFirstHKLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstHKLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstHKLatencyMean, self).__init__(
			"ActionTypeFirstHKLatencyMean", "float", data, "hk", True, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeFirstHKLatencyMean and return it
        """
        return FieldActionTypeFirstHKLatencyMean(data)

