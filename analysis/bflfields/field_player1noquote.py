"""
defines behaviour of bfl master table field player1noquote
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class Fieldplayer1noquote(MasterField):
        def __init__(self, data):
                super(Fieldplayer1noquote, self).__init__("player1noquote", "varbinary(128)", data)

        def calc(self):
                return self.game.playermeta['Player']

def instance(data):
        """
        make an instance of Fieldplayer1noquote and return it
        """
        return Fieldplayer1noquote(data)

