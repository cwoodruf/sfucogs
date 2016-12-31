"""
defines behaviour of bfl master table field WorkersTrainedPerMinStd
"""

from bflfields.perminfield import PerMinField
from bflfields.filter import worker_trained

class FieldWorkersTrainedPerMinStd(PerMinField):
        def __init__(self, data):
                super(FieldWorkersTrainedPerMinStd, self).__init__("WorkersTrainedPerMinStd", "float", data,
				worker_trained, "std")

def instance(data):
        """
        make an instance of FieldWorkersTrainedPerMinStd and return it
        """
        return FieldWorkersTrainedPerMinStd(data)

