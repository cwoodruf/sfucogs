"""
defines behaviour of bfl master table field ComplexUnitsMade
"""

from bflmasterfield import MasterField
from bflfields.filter import complex_units

class FieldComplexUnitsMade(MasterField):
        def __init__(self, data):
                super(FieldComplexUnitsMade, self).__init__("ComplexUnitsMade", "float", data)

        def calc(self):
                cus = self.filter.action_count(self.events, complex_units)
                return cus

def instance(data):
        """
        make an instance of FieldComplexUnitsMade and return it
        """
        return FieldComplexUnitsMade(data)

