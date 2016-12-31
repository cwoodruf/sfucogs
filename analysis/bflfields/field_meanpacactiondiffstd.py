"""
defines behaviour of bfl master table field MeanPACActionDiffStd
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldMeanPACActionDiffStd(MasterField):
        def __init__(self, data):
                super(FieldMeanPACActionDiffStd, self).__init__("MeanPACActionDiffStd", "float", data)

        def calc(self):
                return self.PAC.stats['meanpacactiondiffstd']

def instance(data):
        """
        make an instance of FieldMeanPACActionDiffStd and return it
        """
        return FieldMeanPACActionDiffStd(data)

