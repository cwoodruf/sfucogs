"""
defines behaviour of bfl master table field Speed
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldSpeed(MasterField):
        def __init__(self, data):
                super(FieldSpeed, self).__init__("Speed", "varbinary(128)", data)

        def calc(self):
                return self.game.gamemeta['Game_speed']

def instance(data):
        """
        make an instance of FieldSpeed and return it
        """
        return FieldSpeed(data)

