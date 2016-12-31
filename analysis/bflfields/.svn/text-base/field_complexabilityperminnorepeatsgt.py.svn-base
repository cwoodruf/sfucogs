"""
defines behaviour of bfl master table field ComplexAbilityPerMinNoRepeatsGT
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import complex_ability_gt_norepeats

class FieldComplexAbilityPerMinNoRepeatsGT(PerMinField):
        def __init__(self, data):
                super(FieldComplexAbilityPerMinNoRepeatsGT, self).__init__(
                                "ComplexAbilityPerMinNoRepeatsGT", "float", data,
				complex_ability_gt_norepeats, "mean")

def instance(data):
        """
        make an instance of FieldComplexAbilityPerMinNoRepeatsGT and return it
        """
        return FieldComplexAbilityPerMinNoRepeatsGT(data)

