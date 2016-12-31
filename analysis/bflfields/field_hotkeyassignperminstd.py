"""
defines behaviour of bfl master table field hotkeyassignperminStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class FieldhotkeyassignperminStd(PerMinField):
        def __init__(self, data):
                super(FieldhotkeyassignperminStd, self).__init__("hotkeyassignperminStd", "float", data,
				filters['hk_assign'], "std")

def instance(data):
        """
        make an instance of FieldhotkeyassignperminStd and return it
        """
        return FieldhotkeyassignperminStd(data)

