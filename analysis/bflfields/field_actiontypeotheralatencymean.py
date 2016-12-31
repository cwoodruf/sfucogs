"""
defines behaviour of bfl master table field ActionTypeOtherALatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherALatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherALatencyMean, self).__init__(
			"ActionTypeOtherALatencyMean", "float", data, "a", False, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeOtherALatencyMean and return it
        """
        return FieldActionTypeOtherALatencyMean(data)

