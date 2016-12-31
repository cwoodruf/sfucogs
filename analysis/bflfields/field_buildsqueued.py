"""
defines behaviour of bfl master table field BuildsQueued
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldBuildsQueued(MasterField):
        def __init__(self, data):
                super(FieldBuildsQueued, self).__init__("BuildsQueued", "float", data)

        def calc(self):
                buildsqueued = 0
                for event in self.events:
                        if event['ActionType'] == 'b' and event['Queued'] == '1.0':
                                buildsqueued += 1
                return buildsqueued

def instance(data):
        """
        make an instance of FieldBuildsQueued and return it
        """
        return FieldBuildsQueued(data)

