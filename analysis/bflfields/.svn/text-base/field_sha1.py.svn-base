"""
defines behaviour of bfl master table field sha1
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class Fieldsha1(MasterField):
        def __init__(self, data):
                super(Fieldsha1, self).__init__("sha1", "varchar(64)", data)

        def calc(self):
                return self.game.gamemeta['Sha1']

def instance(data):
        """
        make an instance of Fieldsha1 and return it
        """
        return Fieldsha1(data)

