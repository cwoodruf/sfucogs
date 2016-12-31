"""
defines behaviour of bfl master table field GameVersion
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldGameVersion(MasterField):
        def __init__(self, data):
                super(FieldGameVersion, self).__init__("GameVersion", "varbinary(128)", data)

        def calc(self):
                return self.game.gamemeta['Version']

def instance(data):
        """
        make an instance of FieldGameVersion and return it
        """
        return FieldGameVersion(data)

