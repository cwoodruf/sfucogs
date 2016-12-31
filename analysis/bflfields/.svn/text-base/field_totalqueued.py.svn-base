"""
defines behaviour of bfl master table field TotalQueued
"""

from bflmasterfield import MasterField
from bflfields.filter import queued

class FieldTotalQueued(MasterField):
        def __init__(self, data):
                super(FieldTotalQueued, self).__init__("TotalQueued", "float", data)

        def calc(self):
                return self.filter.action_count(self.events, queued)

def instance(data):
        """
        make an instance of FieldTotalQueued and return it
        """
        return FieldTotalQueued(data)

