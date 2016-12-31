"""
defines behaviour of bfl master table field hotkeyselectpermin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class Fieldhotkeyselectpermin(PerMinField):
        def __init__(self, data):
                super(Fieldhotkeyselectpermin, self).__init__("hotkeyselectpermin", "float", data,
				filters['hk_select'], "mean")

def instance(data):
        """
        make an instance of Fieldhotkeyselectpermin and return it
        """
        return Fieldhotkeyselectpermin(data)

