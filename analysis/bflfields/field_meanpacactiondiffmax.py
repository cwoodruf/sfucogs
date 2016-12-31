"""
defines behaviour of bfl master table field MeanPACActionDiffMax
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldMeanPACActionDiffMax(MasterField):
        def __init__(self, data):
                super(FieldMeanPACActionDiffMax, self).__init__("MeanPACActionDiffMax", "float", data)

        def calc(self):
                return self.PAC.stats['meanpacactiondiffmax']

def instance(data):
        """
        make an instance of FieldMeanPACActionDiffMax and return it
        """
        return FieldMeanPACActionDiffMax(data)

