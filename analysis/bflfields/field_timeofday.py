"""
defines behaviour of bfl master table field TimeOfDay
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldTimeOfDay(MasterField):
        def __init__(self, data):
                super(FieldTimeOfDay, self).__init__("TimeOfDay", "time", data)

        def calc(self):
                return str(self.game.gamemeta['Time'])

def instance(data):
        """
        make an instance of FieldTimeOfDay and return it
        """
        return FieldTimeOfDay(data)

