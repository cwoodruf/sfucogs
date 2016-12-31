"""
defines behaviour of bfl master table field playerid
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class Fieldplayerid(MasterField):
        def __init__(self, data):
                super(Fieldplayerid, self).__init__("playerid", "int(11)", data)

        def calc(self):
                return str(int(self.game.gamemeta['PlayerID']))

def instance(data):
        """
        make an instance of Fieldplayerid and return it
        """
        return Fieldplayerid(data)

