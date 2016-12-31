"""
defines behaviour of bfl master table field ActionTypeFirstALatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstALatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstALatencyMean, self).__init__(
			"ActionTypeFirstALatencyMean", "float", data, "a", True, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeFirstALatencyMean and return it
        """
        return FieldActionTypeFirstALatencyMean(data)

