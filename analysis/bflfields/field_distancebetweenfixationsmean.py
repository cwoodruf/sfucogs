"""
defines behaviour of bfl master table field DistanceBetweenFixationsMean
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldDistanceBetweenFixationsMean(MasterField):
        def __init__(self, data):
                super(FieldDistanceBetweenFixationsMean, self).__init__("DistanceBetweenFixationsMean", "float", data)

        def calc(self):
                return self.PAC.stats['distancebetweenfixationsmean']

def instance(data):
        """
        make an instance of FieldDistanceBetweenFixationsMean and return it
        """
        return FieldDistanceBetweenFixationsMean(data)

