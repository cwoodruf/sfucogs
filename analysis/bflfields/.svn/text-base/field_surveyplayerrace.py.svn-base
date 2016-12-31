"""
defines behaviour of bfl master table field SurveyPlayerRace
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldSurveyPlayerRace(MasterField):
        def __init__(self, data):
                super(FieldSurveyPlayerRace, self).__init__("SurveyPlayerRace", "varbinary(128)", data)

        def calc(self):
                return self.game.playermeta['Race']

def instance(data):
        """
        make an instance of FieldSurveyPlayerRace and return it
        """
        return FieldSurveyPlayerRace(data)

