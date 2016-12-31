"""
Manage binned per minute statistics for different things
These use timestamps to group fields together and the
statistic is something about the typical bin 
rather than the game as a whole
"""
from bflmasterfield import MasterField
from bflfields.time import TSRTminute

class PerMinField(MasterField):
        """
        like MasterField but defines a canned calc function
        that can identify specific actions based on a given regex
        should also support filter callbacks for more complex filtering
        """
        def __init__(self, name, datatype, data, patternstr, stat):
                """
                filter is a regex string or callback and stat can be mean or std
                """
                super(PerMinField, self).__init__(name, datatype, data)
                self.patternstr = patternstr
                self.stat = stat
                self.key = "{}-{}".format(stat, patternstr)

        def calc(self):
                """
                does a bucket brigade and returns mean, std
                returns one or the other depending on stat
                """
                mean, std = self.filter.bucket_brigade(self, self.key, self.patternstr, TSRTminute)
                if self.stat == 'mean':
                        return mean
                if self.stat == 'std':
                        return std
                Raise(Exception("PerMinField: don't know what stat {} is!".format(self.stat)))

