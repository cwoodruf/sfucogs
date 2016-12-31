"""
defines behaviour of bfl master table field OpponentMatchup
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldOpponentMatchup(MasterField):
        def __init__(self, data):
                super(FieldOpponentMatchup, self).__init__("OpponentMatchup", "varbinary(128)", data)

        def calc(self):
                """
                first letters of races for the opposing team
                """
                myteam = self.game.playermeta['Team']
                races = self.game.playermeta['races']
                for team, racelist in races.iteritems():
                        if team != myteam:
                                return ''.join(racelist)
                return \
                None

def instance(data):
        """
        make an instance of FieldOpponentMatchup and return it
        """
        return FieldOpponentMatchup(data)

