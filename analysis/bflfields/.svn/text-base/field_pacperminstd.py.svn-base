"""
defines behaviour of bfl master table field PACPerMinStd
"""

from bflmasterfield import MasterField

class FieldPACPerMinStd(MasterField):
        def __init__(self, data):
                super(FieldPACPerMinStd, self).__init__("PACPerMinStd", "float", data)

        def calc(self):
                mean, std = self.filter.pacspermin(self)
                return std

def instance(data):
        """
        make an instance of FieldPACPerMinStd and return it
        """
        return FieldPACPerMinStd(data)

