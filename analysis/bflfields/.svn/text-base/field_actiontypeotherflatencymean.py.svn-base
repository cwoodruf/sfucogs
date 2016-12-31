"""
defines behaviour of bfl master table field ActionTypeOtherFLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherFLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherFLatencyMean, self).__init__(
			"ActionTypeOtherFLatencyMean", "float", data, "f", False, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeOtherFLatencyMean and return it
        """
        return FieldActionTypeOtherFLatencyMean(data)

