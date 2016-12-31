"""
defines behaviour of bfl master table field MeanPACActionDiffMin
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldMeanPACActionDiffMin(MasterField):
        def __init__(self, data):
                super(FieldMeanPACActionDiffMin, self).__init__("MeanPACActionDiffMin", "float", data)

        def calc(self):
                return self.PAC.stats['meanpacactiondiffmin']

def instance(data):
        """
        make an instance of FieldMeanPACActionDiffMin and return it
        """
        return FieldMeanPACActionDiffMin(data)

