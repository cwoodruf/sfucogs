"""
defines behaviour of bfl master table field ActionTypeFirstFLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstFLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstFLatencyMean, self).__init__(
			"ActionTypeFirstFLatencyMean", "float", data, "f", True, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeFirstFLatencyMean and return it
        """
        return FieldActionTypeFirstFLatencyMean(data)

