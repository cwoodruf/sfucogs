"""
defines behaviour of bfl master table field hotkeyselectperminStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldhotkeyselectperminStd(PerMinField):
        def __init__(self, data):
                super(FieldhotkeyselectperminStd, self).__init__("hotkeyselectperminStd", "float", data,
				filters['hk_select'], "std")

def instance(data):
        """
        make an instance of FieldhotkeyselectperminStd and return it
        """
        return FieldhotkeyselectperminStd(data)

