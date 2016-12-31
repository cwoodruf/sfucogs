"""
defines behaviour of bfl master table field ComplexAbilityPerMinGT
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import complex_ability_gt

class FieldComplexAbilityPerMinGT(PerMinField):
        def __init__(self, data):
                super(FieldComplexAbilityPerMinGT, self).__init__("ComplexAbilityPerMinGT", "float", data,
				complex_ability_gt, "mean")

def instance(data):
        """
        make an instance of FieldComplexAbilityPerMinGT and return it
        """
        return FieldComplexAbilityPerMinGT(data)

