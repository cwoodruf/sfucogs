"""
defines behaviour of bfl master table field ActionTypeFirstBLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstBLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstBLatencyMean, self).__init__(
			"ActionTypeFirstBLatencyMean", "float", data, "b", True, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeFirstBLatencyMean and return it
        """
        return FieldActionTypeFirstBLatencyMean(data)

