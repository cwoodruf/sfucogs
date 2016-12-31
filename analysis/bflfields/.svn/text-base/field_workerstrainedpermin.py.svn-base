"""
defines behaviour of bfl master table field WorkersTrainedPerMin
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import worker_trained

class FieldWorkersTrainedPerMin(PerMinField):
        def __init__(self, data):
                super(FieldWorkersTrainedPerMin, self).__init__("WorkersTrainedPerMin", "float", data,
				worker_trained, "mean")

def instance(data):
        """
        make an instance of FieldWorkersTrainedPerMin and return it
        """
        return FieldWorkersTrainedPerMin(data)

