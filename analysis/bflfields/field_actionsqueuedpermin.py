"""
defines behaviour of bfl master table field ActionsQueuedPerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import queued

class FieldActionsQueuedPerMin(PerMinField):
        def __init__(self, data):
                super(FieldActionsQueuedPerMin, self).__init__("ActionsQueuedPerMin", "float", data,
				queued, "mean")

def instance(data):
        """
        make an instance of FieldActionsQueuedPerMin and return it
        """
        return FieldActionsQueuedPerMin(data)

