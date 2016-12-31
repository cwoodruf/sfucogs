"""
defines behaviour of bfl master table field ActionTypeOtherSELLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherSELLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherSELLatencyMean, self).__init__(
			"ActionTypeOtherSELLatencyMean", "float", data, "sel", False, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeOtherSELLatencyMean and return it
        """
        return FieldActionTypeOtherSELLatencyMean(data)

