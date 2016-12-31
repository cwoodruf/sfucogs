"""
defines behaviour of bfl master table field AllyMatchup
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldAllyMatchup(MasterField):
        def __init__(self, data):
                super(FieldAllyMatchup, self).__init__("AllyMatchup", "varbinary(128)", data)

        def calc(self):
                """
                find the races those on our team
                does it matter if this includes us?
                """
                myteam = self.game.playermeta['Team']
                races = self.game.playermeta['races']
                for team, racelist in races.iteritems():
                        if team == myteam and len(racelist) > 1:
                                return ''.join(racelist)
                return \
                                None

def instance(data):
        """
        make an instance of FieldAllyMatchup and return it
        """
        return FieldAllyMatchup(data)

