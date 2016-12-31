"""
defines behaviour of bfl master table field is_competitive
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class Fieldis_competitive(MasterField):
        def __init__(self, data):
                super(Fieldis_competitive, self).__init__("is_competitive", "varbinary(128)", data)

        def calc(self):
                return self.game.gamemeta['Is_competitive']

def instance(data):
        """
        make an instance of Fieldis_competitive and return it
        """
        return Fieldis_competitive(data)

