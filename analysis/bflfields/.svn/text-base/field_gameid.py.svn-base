"""
defines behaviour of bfl master table field gameid
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class Fieldgameid(MasterField):
        def __init__(self, data):
                super(Fieldgameid, self).__init__("gameid", "int(11)", data)

        def calc(self):
                return str(int(self.game.gamemeta['GameID']))

def instance(data):
        """
        make an instance of Fieldgameid and return it
        """
        return Fieldgameid(data)

