"""
defines behaviour of bfl master table field GameType
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldGameType(MasterField):
        def __init__(self, data):
                super(FieldGameType, self).__init__("GameType", "varbinary(128)", data)

        def calc(self):
                return self.game.gamemeta['Game_type']

def instance(data):
        """
        make an instance of FieldGameType and return it
        """
        return FieldGameType(data)

