"""
defines behaviour of bfl master table field PacableActionsOutsidePacProp
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldPacableActionsOutsidePacProp(MasterField):
        def __init__(self, data):
                super(FieldPacableActionsOutsidePacProp, self).__init__("PacableActionsOutsidePacProp", "float", data)

        def calc(self):
                return self.PAC.stats['pacableactionsoutsidepacprop']

def instance(data):
        """
        make an instance of FieldPacableActionsOutsidePacProp and return it
        """
        return FieldPacableActionsOutsidePacProp(data)

