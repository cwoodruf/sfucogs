"""
defines behaviour of bfl master table field ladderseason
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class Fieldladderseason(MasterField):
        def __init__(self, data):
                super(Fieldladderseason, self).__init__("ladderseason", "varbinary(128)", data)

        def calc(self):
                return self.game.gamemeta['Ladder_season']

def instance(data):
        """
        make an instance of Fieldladderseason and return it
        """
        return Fieldladderseason(data)

