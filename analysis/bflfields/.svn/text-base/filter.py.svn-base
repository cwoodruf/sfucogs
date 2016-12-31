"""
simplify filtering actions
"""
import re
import bflfields.time
from bflfields.ability import complex
from inspect import * # for isroutine, isfunction etc
import bflstats

# default level of verbosity for BFLFilter
VERBOSE = True

# some patterns to use for finding rows of interest
# the strings being matched are the 'composite' string which consists of
# ActionType Action...
# so exact matches on ActionType should follow ActionType with a space

ALLPAT = '^(a |atk |rc |b |tr |mapAtk |mapRCClick |mapAbl |sel |Cancel |hk )'

filters = {
     'a': '^a ',
     'atk': '^atk ',
     'Cancel': '^Cancel ',
     'b': '^b ',
     'f': '^f ',
     'hk': '^hk .*(Assign|Select)',
     'hk_assign': '^hk .*Assign',
     'hk_select': '^hk .*Select',
     'm': '^m ',
     'mapAbl': '^mapAbl ',
     'mapAtk': '^mapAtk ',
     'mapRCClick': '^mapRCClick ',
     'rc': '^rc ',
     'sel': '^sel ',
     'seld': '^seld ',
     'tr': '^tr ',
     'u': '^u ',
     'ALL': ALLPAT,
}

# utility functions
def concat(keys):
        """
        using keys combine more than one filter
        """
        f = []
        for k in keys:
            f.append(filters[k])
        return '|'.join(f)

# callbacks for action_matching
# these represent criteria for including something in a statistic
def queued(event):
        """
        identify queued events
        """
        if event['Queued'] == 1.0: return True
        return None

def building(event):
        """
        find what was being built in the action
        """
        if event['ActionType'] != 'b': return None
        b = re.match(r'Build (.*)')
        if b is not None:
                return (b.group(1))[:3]
        return None

def complex_ability_gt(event):
        """
        complex abilities associated with the 'a' actiontype
        these affect ground targets
        """
        if event['ActionType'] != 'a': return None
        if event['short_action'] not in complex: return None
        if complex[event['short_action']] == 'GT': return True
        return None

def complex_ability_ut(event):
        """
        complex abilities associated with the 'a' actiontype
        these affect unit targets
        """
        if event['ActionType'] != 'a': return None
        if event['short_action'] not in complex: return None
        if complex[event['short_action']] == 'UT': return True
        return None

def complex_ability_gt_norepeats(event):
        """
        complex abilities associated with the 'a' actiontype
        these affect ground targets
        this should only count if its the start of a group
        where the cleaned up actions are the same
        """
        if event['ActionType'] != 'a': return None
        if event['short_action'] not in complex: return None
        if complex[event['short_action']] == 'GT': 
                if event['prev'] is None or \
                        event['prev']['short_action'] != event['short_action']:
                                return True
        return None

def complex_units(event):
        """
        scan Action for units that are hard to train
        only relevant for the tr actiontype
        """
        if event['ActionType'] != 'tr': return None
        cu = re.match(r'.*(High Templar|Infestor|Ghost)', event['Action'])
        if cu is not None: 
                return True
        return None

def isfocused(event):
        """
        do we have anything real in the target?
        """
        f = re.match(r'.*(null|Coordinate)', event['Target'])
        if f is None:
                return True
        return None

def focus_atk(event):
        """
        find examples of atk where there is a real target
        """
        if event['ActionType'] != 'atk': return None
        return isfocused(event)

def focus_rc(event):
        """
        find examples of rc/right clicks with real targets
        """
        if event['ActionType'] != 'rc': return None
        return isfocused(event)

def worker_trained(event):
        """
        were workers (Probe|Drone|SCV) trained during this tr/training event?
        """
        if event['ActionType'] != 'tr': return None
        wt = re.match(r'.*(Probe|Drone|SCV).*', event['Action'], re.IGNORECASE)
        if wt is not None:
                return wt.group(1)
        return None

def _offscreen(event):
        """
        see if actiontype at was on the screen when it happened
        ie does the ActionX/Y fall within the bounds of ScreenX/Y
        see MiniMapUse.m for the matlab implementation
        """
        
        ax = event['ActionX']
        ay = event['ActionY']
        sx = event['ScreenX']
        sy = event['ScreenY']

        ViewWidth = 40 # The max view (based on Mark's 2560 by 1440 pixels monitor at home is 36 by 17.6).
        LowerBound= -6 # We added 2 units to each side as a buffer. 6 is the distance from centre to bottom.
        UpperBound= 15.5 # 15.5 = the distance from centre to top

        if abs(sx-ax) > ViewWidth/2 or (ay-sy) > UpperBound or (ay-sy) < LowerBound:
                return 1
        return 0


def rc_offscreen(event):
        """
        right click offscreen? also includes mapRCClick
        """
        at = event['ActionType']
        if at != 'mapRCClick' and at != 'rc': return None
        return _offscreen(event)

def atk_offscreen(event):
        """
        attack offscreen? also includes mapAtk
        """
        at = event['ActionType']
        if at != 'mapAtk' and at != 'atk': return None
        return _offscreen(event)

# filter class: used to calculate and save stats based on event values
class BFLFilter:
        """
        do basic stats on various things and remember the results
        """
        def __init__(self, verbose=VERBOSE):
                self.verbose = verbose
                self.allpat = ALLPAT
                # for anything else (eg apm)
                self.saved = {}
                # just for bucket_brigade to avoid name collisions
                self.buckets = {}
                # for the pac stats
                self.paclatencies = {}
                # for results of action_matching calls
                self.actionlists = {}
                self.actioncounts = {}

        def action_matching(self, events, patternstr, positive, returns, limit=None):
                """
                scan field.events ActionType concatenated with Action 
                use a callback or regex to match events

                event callbacks take the event as an input and are 
                expected to return None if they do not match the event

                setting positive to false will invert results

                set returns to 'list' to return a list of matching events
                instead of just a count
                """
                if isinstance(patternstr, basestring):
                        func = False
                        pattern = re.compile(patternstr)
                else:
                        # if patternstr is a callback we expect it to return None or not None
                        func = True
                        pattern = patternstr

                if returns == 'int': matching = 0
                elif returns == 'list' or returns == 'match': matching = []
                else: raise(Exception("bflfields.filter.action_count: don't know what to return!"))

                if limit == None: limit = len(events)

                for event in events:
                        limit -= 1;
                        if limit <= 0: break;
                        if func:
                                m = pattern(event)
                        else:
                                m = re.match(pattern, event['combined'])
                        if positive:
                                if m is not None: 
                                        if returns == "int": matching += 1
                                        elif returns == "list": matching.append(event)
                                        elif returns == "match": matching.append(m)
                        else:
                                if m is None: 
                                        if returns == "int": matching += 1
                                        elif returns == "list": matching.append(event)
                                        elif returns == "match": matching.append(m)
                return matching

        def action_count(self, events, patternstr, positive=True, limit=None):
                return self.action_matching(events, patternstr, positive=positive, limit=limit, returns='int')

        def action_list(self, events, patternstr, positive=True, limit=None):
                """
                returns a list of dicts of the matching events
                """
                return self.action_matching(events, patternstr, positive=positive, limit=limit, returns='list')

        def action_results(self, events, callback, positive=True, limit=None):
                """
                collects results of callback in a list
                """
                return self.action_matching(events, callback, positive=positive, limit=limit, returns='match')

        def apm(self, field, patternstr=None):
                """
                using a MasterField derived field do a count of relevant actions
                return proportion per minute based on game metadata
                in MasterBuilderBFL_Final.m this is redefined as the average 
                for single minute buckets
                """
                if 'apm' in self.saved: return self.saved['apm']
                if patternstr == None: patternstr = self.allpat
                actions = self.action_count(field.events, patternstr)
                minutes = field.minutes
                if self.verbose: print "minutes",minutes,"actions",actions
                apm = float(actions)/minutes
                self.saved['apm'] = apm
                return apm

        def field_failstime(self, field):
                """
                used for field_failstimewasteseconds and field_failssectionscount
                """
                if 'field_failstime' in self.saved: 
                        return self.saved['field_failstime']
                count = 0
                ticks = 0
                prev = None
                for event in field.events:
                        if event['ActionType'] == 'f':
                                if prev is None or prev['ActionType'] != 'f':
                                        count += 1
                                ticks += event['latency']

                seconds = bflfields.time.ts2seconds(ticks)
                self.saved['field_failstime'] = (count, seconds)
                return count,seconds

        def bucket_brigade(self, field, key, patternstr=None, ticks=bflfields.time.TSRTminute):
                """
                find mean and standard deviation of 
                number of events happening in time chunks
                of length ticks
                events selected using patternstr
                """
                if key in self.buckets: return self.buckets[key]
                if patternstr == None: patternstr = self.allpat
                start = field.events[0]['TimeStamp']
                chunk = []
                counts = []
                for evt in field.events:
                        if evt['TimeStamp'] - start >= ticks:
                                count = self.action_count(chunk, patternstr)
                                counts.append(count)
                                start = evt['TimeStamp']
                                chunk = []
                        chunk.append(evt)
                # left overs in chunk deliberately ignored as they won't be a full bucket
                avg, std = self._stats(counts)
                self.buckets[key] = (avg, std)
                return (avg, std)

        def pac_latency(self, field, actiontype, first):
                """
                find mean and standard deviation of 
                latencies in field.events records
                events selected using actiontype
                like bucket_brigade but uses pacs
                """
                key = "{}-{}".format(actiontype, "first" if first else "other")
                if key in self.paclatencies: return self.paclatencies[key]
                latencies = []
                for events in field.PAC.iterator(field.events):
                        seen = False
                        for evt in events:
                                if evt['ActionType'] == actiontype:
                                        lat = evt['latency']
                                        if not seen and first:
                                                latencies.append(lat)
                                        if seen and not first:        
                                                latencies.append(lat)
                                        seen = True

                avg, std = self._stats(latencies)

                self.paclatencies[key] = (avg, std)
                return avg, std

        def pacspermin(self, field, lookfor=None, ticks=bflfields.time.TSRTminute):
                """
                count the number of pacs showing up in each minute bucket
                replaces stats using:
                PACPerMinBin(MinBin)=sum(PACBounds(:,1)>=CurTimeStampMin & PACBounds(:,1)<CurTimeStampMax);
                note that the *end* of the pac is what is counted
                """
                if 'pacspermin' in self.saved: return self.saved['pacspermin']
                start = field.events[0]['TimeStamp']
                counts = []
                i = 0
                numpacs = 0
                pac = field.PAC
                # basic idea is to bite off a chunk of events 
                # then see how many pacs
                # ended before the end of the chunk
                # pacs are assumed to be in rowid order
                if self.verbose:
                        print "expecting about",len(pac.pacs)/field.minutes,\
                                "pacs",len(pac.pacs),"minutes",field.minutes
                lastat = {}
                for evt in field.events:
                        if evt['TimeStamp'] - start >= ticks:
                                # this counts the number of pacs that end in this time period
                                # we only visit each pac once as they are in time order
                                while i < len(pac.pacs) and pac.endrowid(i) < evt['RowID']:
                                        i += 1
                                        numpacs += 1
                                counts.append(numpacs)
                                start = evt['TimeStamp']
                                numpacs = 0

                avg, std = self._stats(counts)
                if self.verbose: print "actually got",avg,"std",std,"counts",counts
                self.saved['pacspermin'] = (avg, std)
                return avg, std

        def _stats(self, stat):
                # print stat
                return bflstats.mean(stat), bflstats.stdev(stat)

def instance():
        """
        create a new BFLFilter object
        """
        return BFLFilter()

