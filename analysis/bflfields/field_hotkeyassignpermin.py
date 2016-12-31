"""
defines behaviour of bfl master table field hotkeyassignpermin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import filters

class Fieldhotkeyassignpermin(PerMinField):
        def __init__(self, data):
                super(Fieldhotkeyassignpermin, self).__init__("hotkeyassignpermin", "float", data,
				filters['hk_assign'], "mean")

def instance(data):
        """
        make an instance of Fieldhotkeyassignpermin and return it
        """
        return Fieldhotkeyassignpermin(data)

