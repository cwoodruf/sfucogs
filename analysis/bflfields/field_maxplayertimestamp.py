"""
defines behaviour of bfl master table field MaxPlayerTimeStamp
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldMaxPlayerTimeStamp(MasterField):
        def __init__(self, data):
                super(FieldMaxPlayerTimeStamp, self).__init__("MaxPlayerTimeStamp", "float", data)

        def calc(self):
                """
                    'MaxGameTimeStamp'; 'MaxPlayerTimeStamp';...
        MaxPlayerTimeStamp=max(RawTimeStamp);

                """
                return str(self.events[-1]['TimeStamp'])

def instance(data):
        """
        make an instance of FieldMaxPlayerTimeStamp and return it
        """
        return FieldMaxPlayerTimeStamp(data)

