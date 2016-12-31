"""
defines behaviour of bfl master table field ActionTypeOtherBLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherBLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherBLatencyMean, self).__init__(
			"ActionTypeOtherBLatencyMean", "float", data, "b", False, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeOtherBLatencyMean and return it
        """
        return FieldActionTypeOtherBLatencyMean(data)

