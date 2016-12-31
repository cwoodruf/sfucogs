"""
defines behaviour of bfl master table field PACPerMin
"""

from bflmasterfield import MasterField

class FieldPACPerMin(MasterField):
        def __init__(self, data):
                super(FieldPACPerMin, self).__init__("PACPerMin", "float", data)

        def calc(self):
                mean, std = self.filter.pacspermin(self)
                return mean

def instance(data):
        """
        make an instance of FieldPACPerMin and return it
        """
        return FieldPACPerMin(data)

