"""
defines behaviour of bfl master table field numonplayerteam
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class Fieldnumonplayerteam(MasterField):
        def __init__(self, data):
                super(Fieldnumonplayerteam, self).__init__("numonplayerteam", "float", data)

        def calc(self):
                return self.game.playermeta['team_size']

def instance(data):
        """
        make an instance of Fieldnumonplayerteam and return it
        """
        return Fieldnumonplayerteam(data)

