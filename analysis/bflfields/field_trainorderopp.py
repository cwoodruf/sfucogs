"""
defines behaviour of bfl master table field TrainOrderOpp
"""

from bflmasterfield import MasterField
from bflfields.filter import worker_trained

class FieldTrainOrderOpp(MasterField):
        def __init__(self, data):
                super(FieldTrainOrderOpp, self).__init__("TrainOrderOpp", "varbinary(128)", data)

        def calc(self):
                return ''.join(self.filter.action_results( self.events, worker_trained, limit=12))

def instance(data):
        """
        make an instance of FieldTrainOrderOpp and return it
        """
        return FieldTrainOrderOpp(data)

