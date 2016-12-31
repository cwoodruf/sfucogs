"""
defines behaviour of bfl master table field ComplexAbilityPerMinNoRepeatsUT
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import complex_ability_gt_norepeats

class FieldComplexAbilityPerMinNoRepeatsUT(PerMinField):
        def __init__(self, data):
                super(FieldComplexAbilityPerMinNoRepeatsUT, self).__init__(
                                "ComplexAbilityPerMinNoRepeatsUT", "float", data,
				complex_ability_gt_norepeats, "std")

def instance(data):
        """
        make an instance of FieldComplexAbilityPerMinNoRepeatsUT and return it
        """
        return FieldComplexAbilityPerMinNoRepeatsUT(data)

