"""
defines behaviour of bfl master table field FailsSectionsCount
"""

from bflmasterfield import MasterField

class FieldFailsSectionsCount(MasterField):
        def __init__(self, data):
                super(FieldFailsSectionsCount, self).__init__("FailsSectionsCount", "float", data)

        def calc(self):
                count, seconds = self.filter.field_failstime(self)
                return count

def instance(data):
        """
        make an instance of FieldFailsSectionsCount and return it
        """
        return FieldFailsSectionsCount(data)

