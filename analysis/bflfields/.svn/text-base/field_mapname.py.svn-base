"""
defines behaviour of bfl master table field MapName
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldMapName(MasterField):
        def __init__(self, data):
                super(FieldMapName, self).__init__("MapName", "varbinary(128)", data)

        def calc(self):
                return self.game.gamemeta['Map_name']

def instance(data):
        """
        make an instance of FieldMapName and return it
        """
        return FieldMapName(data)

