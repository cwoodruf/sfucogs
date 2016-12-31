"""
defines behaviour of bfl master table field ComplexUnitsMadePerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import complex_units

class FieldComplexUnitsMadePerMin(PerMinField):
        def __init__(self, data):
                super(FieldComplexUnitsMadePerMin, self).__init__("ComplexUnitsMadePerMin", "float", data,
				complex_units, "mean")

def instance(data):
        """
        make an instance of FieldComplexUnitsMadePerMin and return it
        """
        return FieldComplexUnitsMadePerMin(data)

