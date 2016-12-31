"""
defines behaviour of bfl master table field FixCount
"""

from bflmasterfield import MasterField

class FieldFixCount(MasterField):
        def __init__(self, data):
                super(FieldFixCount, self).__init__("FixCount", "float", data)

        def calc(self):
                return len(self.PAC.pacs)

def instance(data):
        """
        make an instance of FieldFixCount and return it
        """
        return FieldFixCount(data)

