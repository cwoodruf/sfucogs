"""
defines behaviour of bfl master table field ActionTypeFirstMAPABLLatencyMean
"""

from bflfields.paclatencyfield import PacLatencyField

class FieldActionTypeFirstMAPABLLatencyMean(PacLatencyField):
        def __init__(self, data):
                super(FieldActionTypeFirstMAPABLLatencyMean, self).__init__(
			"ActionTypeFirstMAPABLLatencyMean", "float", data, "mapAbl", True, "mean")

def instance(data):
        """
        make an instance of FieldActionTypeFirstMAPABLLatencyMean and return it
        """
        return FieldActionTypeFirstMAPABLLatencyMean(data)

