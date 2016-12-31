"""
defines behaviour of bfl master table field ActionTypeOtherMAPABLLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeOtherMAPABLLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeOtherMAPABLLatencyMean, self).__init__(
			"ActionTypeOtherMAPABLLatencyMean", "float", data, "mapAbl", False, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeOtherMAPABLLatencyMean and return it
        """
        return FieldActionTypeOtherMAPABLLatencyMean(data)

