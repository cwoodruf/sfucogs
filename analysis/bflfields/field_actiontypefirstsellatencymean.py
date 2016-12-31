"""
defines behaviour of bfl master table field ActionTypeFirstSELLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstSELLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstSELLatencyMean, self).__init__(
			"ActionTypeFirstSELLatencyMean", "float", data, "sel", True, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeFirstSELLatencyMean and return it
        """
        return FieldActionTypeFirstSELLatencyMean(data)

