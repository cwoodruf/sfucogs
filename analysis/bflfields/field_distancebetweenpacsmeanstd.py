"""
defines behaviour of bfl master table field DistanceBetweenPACsMeanStd
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldDistanceBetweenPACsMeanStd(MasterField):
        def __init__(self, data):
                super(FieldDistanceBetweenPACsMeanStd, self).__init__("DistanceBetweenPACsMeanStd", "float", data)

        def calc(self):
                return self.PAC.stats['distancebetweenpacsmeanstd']

def instance(data):
        """
        make an instance of FieldDistanceBetweenPACsMeanStd and return it
        """
        return FieldDistanceBetweenPACsMeanStd(data)

