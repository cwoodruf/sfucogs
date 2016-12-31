"""
defines behaviour of bfl master table field BuildOrder
"""

from bflmasterfield import MasterField
from bflfields.filter import building

class FieldBuildOrder(MasterField):
        def __init__(self, data):
                super(FieldBuildOrder, self).__init__("BuildOrder", "varbinary(128)", data)

        def calc(self):
                """
                'BuildOrder'; ...
                % BuildOrder is a string such as 'PylGatAssPylCybAssPylSta' of the
                nBuildings=12; % Specify here how many buildings need to be included in the buildorder variable.
                BuildOrder=horzcat(BuildingsAbbrev{1:nBuildings});

                """
                return ''.join(self.filter.action_results(self.events, building, limit=12))

def instance(data):
        """
        make an instance of FieldBuildOrder and return it
        """
        return FieldBuildOrder(data)

