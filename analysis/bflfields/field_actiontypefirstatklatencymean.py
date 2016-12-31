"""
defines behaviour of bfl master table field ActionTypeFirstATKLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstATKLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstATKLatencyMean, self).__init__(
			"ActionTypeFirstATKLatencyMean", "float", data, "atk", True, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeFirstATKLatencyMean and return it
        """
        return FieldActionTypeFirstATKLatencyMean(data)

