"""
defines behaviour of bfl master table field FixCountPerMin
"""

from bflmasterfield import MasterField
from decimal import Decimal

class FieldFixCountPerMin(MasterField):
        def __init__(self, data):
                super(FieldFixCountPerMin, self).__init__("FixCountPerMin", "float", data)

        def calc(self):
                return float(Decimal(len(self.PAC.pacs))/Decimal(self.minutes))

def instance(data):
        """
        make an instance of FieldFixCountPerMin and return it
        """
        return FieldFixCountPerMin(data)

