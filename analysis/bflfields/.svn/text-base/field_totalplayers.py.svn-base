"""
defines behaviour of bfl master table field totalplayers
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class Fieldtotalplayers(MasterField):
        def __init__(self, data):
                super(Fieldtotalplayers, self).__init__("totalplayers", "float", data)

        def calc(self):
                return str(len(self.game.teams))

def instance(data):
        """
        make an instance of Fieldtotalplayers and return it
        """
        return Fieldtotalplayers(data)

