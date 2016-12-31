"""
defines behaviour of bfl master table field ActionTypeOtherATKLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherATKLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherATKLatencyMean, self).__init__(
			"ActionTypeOtherATKLatencyMean", "float", data, "atk", False, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeOtherATKLatencyMean and return it
        """
        return FieldActionTypeOtherATKLatencyMean(data)

