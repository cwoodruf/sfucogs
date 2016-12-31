"""
defines behaviour of bfl master table field ActionsQueuedPerMinStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import queued

class FieldActionsQueuedPerMinStd(PerMinField):
        def __init__(self, data):
                super(FieldActionsQueuedPerMinStd, self).__init__("ActionsQueuedPerMinStd", "float", data,
				queued, "std")

def instance(data):
        """
        make an instance of FieldActionsQueuedPerMinStd and return it
        """
        return FieldActionsQueuedPerMinStd(data)

