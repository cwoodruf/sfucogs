"""
defines behaviour of bfl master table field GameDate
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldGameDate(MasterField):
        def __init__(self, data):
                super(FieldGameDate, self).__init__("GameDate", "date", data)

        def calc(self):
                return str(self.game.gamemeta['Date'])

def instance(data):
        """
        make an instance of FieldGameDate and return it
        """
        return FieldGameDate(data)

