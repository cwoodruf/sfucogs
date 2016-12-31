"""
defines behaviour of bfl master table field APM
"""

from bflmasterfield import MasterField
from bflfields.filter import filters

class FieldAPM(MasterField):
        def __init__(self, data):
                super(FieldAPM, self).__init__("APM", "float", data)

        def calc(self):
                """
                This does not agree with matlab although the number of actions agrees 
                and the timestamp used to find things agrees

                discovered they are redefining certain measures using buckets
                so they can get standard devations
                """
                # original way to define this variable
                # apm = self.filter.apm(self)
                avg, std = self.filter.bucket_brigade(self, 'apm', self.filter.allpat)
                return avg

def instance(data):
        """
        make an instance of FieldAPM and return it
        """
        return FieldAPM(data)

