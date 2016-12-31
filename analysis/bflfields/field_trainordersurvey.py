"""
defines behaviour of bfl master table field TrainOrderSurvey
"""

from bflmasterfield import MasterField
from bflfields.filter import complex_units
import re

class FieldTrainOrderSurvey(MasterField):
        def __init__(self, data):
                super(FieldTrainOrderSurvey, self).__init__("TrainOrderSurvey", "varbinary(128)", data)

        def calc(self):
                unitevts = self.filter.action_list(self.events, complex_units)
                units = []
                c = 12
                for event in unitevts:
                        u = re.match(r'.*(High|Infe|Ghos)', event['Action'])
                        if u is not None:
                                units.append(u.group(1))
                                c -= 1
                        if c == 0: break

                return ''.join(units)

def instance(data):
        """
        make an instance of FieldTrainOrderSurvey and return it
        """
        return FieldTrainOrderSurvey(data)

