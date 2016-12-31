"""
defines behaviour of bfl master table field UniqueHotkeys
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldUniqueHotkeys(MasterField):
        def __init__(self, data):
                super(FieldUniqueHotkeys, self).__init__("UniqueHotkeys", "float", data)

        def calc(self):
                hkevents = self.filter.action_list(self.events, filters['hk'])
                hk = {}
                for event in hkevents:
                        hk[event['Target']] = True
                return len(hk.keys())

def instance(data):
        """
        make an instance of FieldUniqueHotkeys and return it
        """
        return FieldUniqueHotkeys(data)

