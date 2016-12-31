"""
defines behaviour of bfl master table field WinLoss
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldWinLoss(MasterField):
        def __init__(self, data):
                super(FieldWinLoss, self).__init__("WinLoss", "float", data)

        def calc(self):
                """
            WinLoss=1;
            WinLoss=0;

                """
                return str(int(self.game.playermeta['Winner']))

def instance(data):
        """
        make an instance of FieldWinLoss and return it
        """
        return FieldWinLoss(data)

