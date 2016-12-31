"""
defines behaviour of bfl master table field ActionTypeOtherTRLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherTRLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherTRLatencyMean, self).__init__(
			"ActionTypeOtherTRLatencyMean", "float", data, "tr", False, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeOtherTRLatencyMean and return it
        """
        return FieldActionTypeOtherTRLatencyMean(data)

