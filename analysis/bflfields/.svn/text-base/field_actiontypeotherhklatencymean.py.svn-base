"""
defines behaviour of bfl master table field ActionTypeOtherHKLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherHKLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherHKLatencyMean, self).__init__(
			"ActionTypeOtherHKLatencyMean", "float", data, "hk", False, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeOtherHKLatencyMean and return it
        """
        return FieldActionTypeOtherHKLatencyMean(data)

