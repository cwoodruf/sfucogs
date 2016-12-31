"""
defines behaviour of bfl master table field Format
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldFormat(MasterField):
        def __init__(self, data):
                super(FieldFormat, self).__init__("Format", "varchar(128)", data)

        def calc(self):
                return self.game.gamemeta['Format']

def instance(data):
        """
        make an instance of FieldFormat and return it
        """
        return FieldFormat(data)

