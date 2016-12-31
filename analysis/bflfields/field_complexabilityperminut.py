"""
defines behaviour of bfl master table field ComplexAbilityPerMinUT
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import complex_ability_ut

class FieldComplexAbilityPerMinUT(PerMinField):
        def __init__(self, data):
                super(FieldComplexAbilityPerMinUT, self).__init__("ComplexAbilityPerMinUT", "float", data,
				complex_ability_ut, "mean")

def instance(data):
        """
        make an instance of FieldComplexAbilityPerMinUT and return it
        """
        return FieldComplexAbilityPerMinUT(data)

