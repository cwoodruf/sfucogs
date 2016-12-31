"""
defines behaviour of bfl master table field ComplexUnitsMadePerMinStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import complex_units

class FieldComplexUnitsMadePerMinStd(PerMinField):
        def __init__(self, data):
                super(FieldComplexUnitsMadePerMinStd, self).__init__("ComplexUnitsMadePerMinStd", "float", data,
				complex_units, "std")

def instance(data):
        """
        make an instance of FieldComplexUnitsMadePerMinStd and return it
        """
        return FieldComplexUnitsMadePerMinStd(data)

