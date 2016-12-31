"""
defines behaviour of bfl master table field MapAtkProportion
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldMapAtkProportion(MasterField):
        def __init__(self, data):
                super(FieldMapAtkProportion, self).__init__("MapAtkProportion", "float", data)

        def calc(self):
                mapatks = self.filter.action_count(self.events, filters['mapAtk'])
                atks = self.filter.action_count(self.events, filters['atk'])
                allatks = mapatks + atks
                if allatks > 0:
                        return float(mapatks)/float(allatks)
                return 0.0

def instance(data):
        """
        make an instance of FieldMapAtkProportion and return it
        """
        return FieldMapAtkProportion(data)

