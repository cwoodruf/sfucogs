"""
defines behaviour of bfl master table field ComplexAbilityPerMinGTStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import complex_ability_gt

class FieldComplexAbilityPerMinGTStd(PerMinField):
        def __init__(self, data):
                super(FieldComplexAbilityPerMinGTStd, self).__init__("ComplexAbilityPerMinGTStd", "float", data,
				complex_ability_gt, "std")

def instance(data):
        """
        make an instance of FieldComplexAbilityPerMinGTStd and return it
        """
        return FieldComplexAbilityPerMinGTStd(data)

