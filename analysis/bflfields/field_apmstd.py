"""
defines behaviour of bfl master table field APMStd
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldAPMStd(MasterField):
        def __init__(self, data):
                super(FieldAPMStd, self).__init__("APMStd", "float", data)

        def calc(self):
                avg, std = self.filter.bucket_brigade(self, 'apm', self.filter.allpat)                
                return std

def instance(data):
        """
        make an instance of FieldAPMStd and return it
        """
        return FieldAPMStd(data)

