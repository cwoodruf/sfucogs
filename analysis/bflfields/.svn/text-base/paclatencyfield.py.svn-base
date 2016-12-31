"""
This module effectively replaces the following from MasterTableBuilderBFL_Final.m:
% For the each of action types in the list, calculate the following:
% First(ActionType)LatencyMean
% First(ActionType)LatencyStd
% Other(ActionType)LatencyMean
% Other(ActionType)LatencyStd

ActionTypes={'a','atk','b','f','hk','mapRCClick','mapAtk','mapAbl','tr','sel'};
for act=ActionTypes
  eval(['ActionTypeFirst' upper(act{1}) 'LatencyMean=nanmean(ActionLatency(strcmp(FirstActionTypes,act{1})));']);
  eval(['ActionTypeFirst' upper(act{1}) 'LatencyStd=nanstd(ActionLatency(strcmp(FirstActionTypes,act{1})));']);
  eval(['ActionTypeOther' upper(act{1}) 'LatencyMean=nanmean(OtherActionLatency(strcmp(OtherActionTypes,act{1})));']);
  eval(['ActionTypeOther' upper(act{1}) 'LatencyStd=nanstd(OtherActionLatency(strcmp(OtherActionTypes,act{1})));']);
end
"""
from bflmasterfield import MasterField

class PacLatencyField(MasterField):
	"""
	These fields examine PACs to find the first instance of a 
	specific ActionType and do a bucket_brigade style calculation
	on the resulting data
	"""
	def __init__(self, name, datatype, data, actiontype, first, statistic):
		"""
		This constructor remembers the actiontype it needs to look
		for as well as the position (first or not) in the
		PAC. The statistic can be either mean or std.
		"""
		super(PacLatencyField, self).__init__(name, datatype, data)
		self.actiontype = actiontype
		self.first = first
		self.statistic = statistic

	def calc(self):
		"""
		for each pac get the latency for this particular actiontype
		in some cases this is the first and in some cases any subsequent action
		"""
		mean, std = self.filter.pac_latency(self, self.actiontype, self.first)

		if self.statistic == 'mean':
			return mean
		if self.statistic == 'std':
			return std

		raise(Exception("invalid statistic in PacLatencyField! {}".format(self.statistic)))

