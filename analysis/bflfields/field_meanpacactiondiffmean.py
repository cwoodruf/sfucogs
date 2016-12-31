"""
defines behaviour of bfl master table field MeanPACActionDiffMean
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldMeanPACActionDiffMean(MasterField):
        def __init__(self, data):
                super(FieldMeanPACActionDiffMean, self).__init__("MeanPACActionDiffMean", "float", data)

        def calc(self):
                return self.PAC.stats['meanpacactiondiffmean']

def instance(data):
        """
        make an instance of FieldMeanPACActionDiffMean and return it
        """
        return FieldMeanPACActionDiffMean(data)

