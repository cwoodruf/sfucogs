"""
defines behaviour of bfl master table field MaxGameTimeStamp
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldMaxGameTimeStamp(MasterField):
        def __init__(self, data):
                super(FieldMaxGameTimeStamp, self).__init__("MaxGameTimeStamp", "float", data)

        def calc(self):
                """
        MaxGameTimeStamp=max(WholeGameTimeStamp);
        GamelengthSeconds=TimeStampToRealTime(MaxGameTimeStamp);

                """
                return str(self.game.filemeta['game_lasttick'])

def instance(data):
        """
        make an instance of FieldMaxGameTimeStamp and return it
        """
        return FieldMaxGameTimeStamp(data)

