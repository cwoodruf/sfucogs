#!/usr/bin/env python
"""
Find Perception Action Cycle shifts (PAC shifts)
PAC shifts effectively represent screen fixations.

This class can conver a series of tuples of the form 
(TimeStamp, ScreenX, ScreenY, RowID)
to a series of PAC shift fixations in the form
of PAC objects using the Identification by Dispersion 
Threshold (IDT) algorithm.

Author: Cal cwoodruf@sfu.ca [2016-07-17]
Reviewed: Chen Yue [2016-09-19]
Validated:

Based on Starcraft/ScreenFixationIDT.m

"""
# needed to get matlab like arithmetic precision
from decimal import Decimal
import re
import time
import math
import gzipgames
import array

# values used in VerifyScreenFixationIDTscript.m
DEF_DISPERSION = 7
DEF_DURATION = 40

verbose = False

def is_pacable(at, action):
        """
        return true if action is a real action
        relative to a the requirements for PAC actions
        in general we want to avoid automatically generated
        actions as these do not reflect the planning and
        execution of moves by a player

        Y: at stands for type of actiontypes which are in form of the abbreviation of actiontypes
        Y: f == failed; u == selection; m == move; seld == Deselect (cancel select); hk == hotkey
        Y: fixations contain these actions should be ignored
        Y: Fixations are pacable if this function return True
        """
        if at == 'f' or at == 'u' or at == 'm' or at == 'seld':
                return False
        if at == 'hk':
                issel = re.search(r'Select',action)
                if issel != None: 
                        return False
        return True

def rowid(event):
        """
        expecting a dictionary or tuple
        tuple ordering follows original matlab script

        Y: events = self.positions
        Y: postions are in form of (TimeStamp, ScreenX, ScreenY, RowID)
        Y: then event[3] = RowID
        """
        try:
                rowid = event['RowID']
        except:
                try:
                        rowid = event[3]
                except:
                        return -1
        return rowid

# some callbacks used in stats generation below

def minimum(ary):
        """
        use min or some other method to find lowest value in list
        """
        return min(ary)

def maximum(ary):
        """
        use max or some other method to find highest value in list
        """
        return max(ary)

def avg(ary):
        """
        check for length of list and 
        either return None if 0 or the average
        can also return None if the array has 
        non-numeric contents
        """
        try:
                if len(ary) == 0: return None
                # attempt to be more like matlab in accuracy
                return float(Decimal(sum(ary))/Decimal(len(ary)))
        except:
                return None

def sd(ary):
        """
        check for length of input list
        either return None if length <= 1 or sample std deviation
        """
        try:
                if len(ary) <= 1: return None
                s = sum([Decimal(x) for x in ary])
                ss = sum([Decimal(x)*Decimal(x) for x in ary])
                N = Decimal(len(ary))
                return float(math.sqrt((ss - (s*s)/N)/(N - Decimal(1.0))))
        except:
                return None

class PACMeta:
        """
        Store metadata for an instance of PACShift
        """
        def __init__(self, dispersion, duration):
                self.dispersion = dispersion
                self.duration = duration
class PAC:
        """
        provide named access to pac contents
        """
        def __init__(self, dur, x, y, fixbounds, rowbounds):
                """
                dur - duration
                x - average x coordinate
                y - average y coordinate
                fixbounds - timestamp boundaries of this fixation
                rowbounds - rowids for this fixation
                """
                self.dur = dur
                self.x = x
                self.y = y
                self.fixbounds = fixbounds
                self.fixstart = fixbounds[1]
                self.fixend = fixbounds[0]
                self.rowbounds = rowbounds
                self.rowstart = rowbounds[1]
                self.rowend = rowbounds[0]
                self.init_stats()

        def __str__(self):
        	"""
        	Y: the difference between _str_ and _repr_
        	   eg: t1=datetime.datetime.now()
        	       print repr(t1)
        	       -----> datetime.datetime(2014, 9, 9, 6, 34, 29, 756000)
        	       print str(t1)
        	       -----> 2014-09-09 06:34:29.756000
        	"""
                return str(self.tuple())

        def __repr__(self):
                return str(self.tuple())

        def tuple(self):
                """
                tuple similar to matlab vector
                """
                return (self.dur, 
                        self.x,
                        self.y,
                        self.fixbounds,
                        self.rowbounds)

        @staticmethod
        def insert_statement(outtable, schema='pacs_simple'):
                """
                see row for more on this
                the default insert statement for a 
                pac table as we can have different collections of fields
                depending on what we are interested in we have different schemas

                schema depends on how pac table was defined
                possibilities are:
                        pacs
                        pacs_simple
                look for template_*.mysql files with these names for actual schema
                """

                # full schema originally used for developing this
                if schema == 'pacs':
                        placeholders = ", ".join(['%s' for i in xrange(28)])
                        return "replace into {} " \
                                "( " \
                                "pacord, " \
                                "player, " \
                                "gameid, " \
                                "duration, " \
                                "x, " \
                                "y, " \
                                "fixend, " \
                                "fixstart, " \
                                "rowend, " \
                                "rowstart, " \
                                "firstactiontype, " \
                                "firstaction, " \
                                "firstactionx, " \
                                "firstactiony, " \
                                "pacactioncount, " \
                                "firstactionlatency, " \
                                "betweenactionlatency, " \
                                "newviewcost, " \
                                "latencytoend, " \
                                "latencyfrompriorfix, " \
                                "pac_actiontypes, " \
                                "pac_actiontimes, " \
                                "pac_actionchars, " \
                                "pac_actionagg, " \
                                "fix_actiontypes, " \
                                "fix_actiontimes, " \
                                "fix_actionchars, " \
                                "fix_actionagg " \
                                ") values ({}) ".format(outtable, placeholders)

                # smaller schema for the large BFL data set
                if schema == 'pacs_simple':
                        placeholders = ", ".join(['%s' for i in xrange(22)])
                        return "replace into {} " \
                                "( " \
                                "pacord, " \
                                "player, " \
                                "gameid, " \
                                "duration, " \
                                "x, " \
                                "y, " \
                                "fixend, " \
                                "fixstart, " \
                                "rowend, " \
                                "rowstart, " \
                                "firstactiontype, " \
                                "firstaction, " \
                                "firstactionx, " \
                                "firstactiony, " \
                                "pacactioncount, " \
                                "firstactionlatency, " \
                                "betweenactionlatency, " \
                                "newviewcost, " \
                                "latencytoend, " \
                                "latencyfrompriorfix, " \
                                "pac_actiontimes, " \
                                "pac_actionchars " \
                                ") values ({}) ".format(outtable, placeholders)

                raise(Exception("Don't know what schema to use for insert!"))

        def row(self, schema='pacs_simple'):
                """
                tuple that can be used to save stats
                in a PAC table in the db
                see insert method for meaning of schema
                Y: return a simple version of the schema 
                """
                if schema == 'pacs':
                        return (
                                self.pacord,
                                self.player,
                                self.gameid,
                                self.dur,
                                self.x,
                                self.y,
                                self.fixend,
                                self.fixstart,
                                self.rowend,
                                self.rowstart,
                                self.firstactiontype,
                                self.firstaction,
                                self.firstactionx,
                                self.firstactiony,
                                self.pacactioncount,
                                self.firstactionlatency,
                                self.betweenactionlatency,
                                self.newviewcost,
                                self.latencytoend,
                                self.latencyfrompriorfix,
                                self.pac_actiontypes,
                                self.pac_actiontimes,
                                self.pac_actionchars,
                                self.pac_actionagg,
                                self.fix_actiontypes,
                                self.fix_actiontimes,
                                self.fix_actionchars,
                                self.fix_actionagg,
                        )
                if schema == 'pacs_simple':
                        return (
                                self.pacord,
                                self.player,
                                self.gameid,
                                self.dur,
                                self.x,
                                self.y,
                                self.fixend,
                                self.fixstart,
                                self.rowend,
                                self.rowstart,
                                self.firstactiontype,
                                self.firstaction,
                                self.firstactionx,
                                self.firstactiony,
                                self.pacactioncount,
                                self.firstactionlatency,
                                self.betweenactionlatency,
                                self.newviewcost,
                                self.latencytoend,
                                self.latencyfrompriorfix,
                                self.pac_actiontimes,
                                self.pac_actionchars,
                        )
                raise(Exception("Don't know what schema to use for row!"))
                        
        def init_stats(self):
                """
                generates the stats vars and sets them to None
                we set pacord, player, gameid to None here
                this may change in the future
                """
                self.pacord = None
                self.player = None
                self.gameid = None
                self.firstactiontype = None
                self.firstaction = None
                self.firstactionx = None
                self.firstactiony = None
                self.pacactioncount = None
                self.firstactionlatency = None
                self.betweenactionlatency = None
                self.latencytoend = None
                self.latencyfrompriorfix = None
                self.newviewcost = None
                self.pac_actiontypes = None
                self.pac_actiontimes = None
                self.pac_actionchars = None
                self.pac_actionagg = None
                self.fix_actiontypes = None
                self.fix_actiontimes = None
                self.fix_actionchars = None
                self.fix_actionagg = None
                self.betweenpacs = None
                self.betweenfixations = None

        def update( self,
                    pacord=None,
                    player=None,
                    gameid=None,
                    dur=None,
                    x=None,
                    y=None,
                    fixend=None,
                    fixstart=None,
                    rowend=None,
                    rowstart=None,
                    firstactiontype=None,
                    firstaction=None,
                    firstactionx=None,
                    firstactiony=None,
                    pacactioncount=None,
                    firstactionlatency=None,
                    betweenactionlatency=None,
                    latencytoend=None,
                    latencyfrompriorfix=None,
                    newviewcost=None,
                    pac_actiontypes=None,
                    pac_actiontimes=None,
                    pac_actionchars=None,
                    pac_actionagg=None,
                    fix_actiontypes=None,
                    fix_actiontimes=None,
                    fix_actionchars=None,
                    fix_actionagg=None,
                    betweenpacs=None,
                    betweenfixations=None):
                """
                given the massive number of things associated with a PAC,
                decided to provide them outside of __init__
                best practice is to always call function with args by name
                to avoid issues with getting fields out of order
                """
                self.pacord = pacord
                if player != None: self.player = player
                if gameid != None: self.gameid = gameid
                if dur != None: self.dur = dur
                if x != None: self.x = x
                if y != None: self.y = y
                if fixend != None: self.fixend = fixend
                if fixstart != None: self.fixstart = fixstart
                if rowend != None: self.rowend = rowend
                if rowstart != None: self.rowstart = rowstart
                self.firstactiontype = firstactiontype
                self.firstaction = firstaction
                self.firstactionx = firstactionx
                self.firstactiony = firstactiony
                self.pacactioncount = pacactioncount
                self.firstactionlatency = firstactionlatency
                self.betweenactionlatency = betweenactionlatency
                self.latencytoend = latencytoend
                self.latencyfrompriorfix = latencyfrompriorfix
                self.newviewcost = newviewcost
                self.pac_actiontypes = pac_actiontypes
                self.pac_actiontimes = pac_actiontimes
                self.pac_actionchars = pac_actionchars
                self.pac_actionagg = pac_actionagg
                self.fix_actiontypes = fix_actiontypes
                self.fix_actiontimes = fix_actiontimes
                self.fix_actionchars = fix_actionchars
                self.fix_actionagg = fix_actionagg
                self.betweenpacs = betweenpacs
                self.betweenfixations = betweenfixations

class PACShift:
        """
        This class can take as input dispersion, duration limits 
        and a series of positions.

        If given a series of positions in 
        (TimeStamp, ScreenX, ScreenY, RowID)
        form a set of fixations will be returned in
        the form of PAC objects

        With no input this class uses default dispersion and duration
        thresholds. Use idt_convert to change an arbitrary list of
        points into a list of PAC shift fixations.
        """

        def __init__(self, dispersion=None, duration=None):
                """
                create PACShift object
                optionally set max dispersion and duration
                """
                self.positions = []
                self.nrows = 0
                self.pacs = []
                self.durations = []

                if dispersion == None: self.max_disp = DEF_DISPERSION
                else: self.max_disp = dispersion

                if duration == None: self.max_duration = DEF_DURATION
                else: self.max_duration = duration

        # exploring PACs
        def iterator(self, events=None, invert=False):
                """
                iterator that finds the next group of events 
                based on the PAC row boundaries and returns them
                assumes a PAC creation method such as idt_convert was run 
                and self.pacs exists
                this method will return nonsensical results if the
                events do not contain rowids matching pac rowbounds

                usage:
                ps = PACShift()
                ps.idt_convert(positions)
                for i, pac_events in Enumerate(ps.iterator(events)):
                    # we now have chunk of events we can look at
                    print "the pac",ps.pacs[i]
                    for event in pac_events:
                        print "a pac event",event

                if no argument is given uses its own internally saved 
                list of tuples in (TimeStamp, ScreenX, ScreenY, RowID) form
                
                Y: this function set a start point and iterator through rows until hits the bounds
                """
                if len(self.pacs) == 0:
                        yield([])
                else:
                        if events == None:
                                events = self.positions
                        i = 0
                        chunk = []
                        for pac in self.pacs:
                                dur, x, y, fixbounds, rowbounds = pac.tuple()
                                end, start = rowbounds
                                # include start?
                                while i < len(events) and rowid(events[i]) < start:
                                        if invert:
                                                chunk.append(events[i])
                                        i += 1
                                # include end?
                                while i < len(events) and rowid(events[i]) <= end:
                                        if not invert:
                                                chunk.append(events[i])
                                        i += 1
                                yield(chunk)
                                chunk = []
                                if i >= len(events): break


        # main IDT algorithm
        def idt_convert(self, positions):
                """
                IDT algorithm:

                given a set of positions and timestamps
                return a set of pac shifts

                the set of positions is presumed to be ordered in time
                and of the form (TimeStamp, ScreenX, ScreenY, RowID)

                time is based on the arbitrary units 
                used by sc2gears and sc2reader (both are different)
                max_duration may need to be adjusted accordingly

                sets the self.positions and self.pacs members

                position format:
                (TimeStamp, ScreenX, ScreenY, RowID)
                use self.dict2tuple or self.dicts2tuples to convert 
                dictionary cursor db rows into the right tuple.
                
                Y: check whether the pac is overtime, then check whether it is fixed at certain area
                Y: if it is, then it is a pac and return it
                """
                pacs = []
                self.pacs = pacs
                fixstart = 0
                fixend = 0
                nrows = len(positions)
                self.nrows = nrows
                end = nrows + 1
                self.positions = positions
                while fixend < nrows:
                        # initially set our fixend based on timestamps
                        # xrange always goes to one less than the upper bound
                        for i in xrange(fixstart, end):
                                if self.overtime(fixstart, i): 
                                        fixend = i - 1
                                        break

                        # if time threshold too high all move actions ignored?
                        if i >= nrows: break

                        # remove first point from points if out of bounds
                        # this was near the end in ScreenFixationsIDT.m
                        if not self.inbounds(fixstart, fixend): 
                                fixstart += 1
                                if verbose: print "out of bounds: fixstart now",fixstart
                                continue

                        while fixend < nrows:
                                # adds additional points to window until its over 
                                # the dispersion threshold - windows are never
                                # less than this threshold
                                if self.inbounds(fixstart, fixend):
                                        fixend += 1
                                else:
                                        break

                        if verbose: print fixstart, fixend, nrows

                        # add PAC shift if we were at this spot long enough
                        if self.overtime(fixstart, fixend):
                                self.add_pac(fixstart, fixend)

                        # remove window points from points
                        # whether or not we actually kept them
                        fixstart = fixend

                # return list to mimic ScreenFixationsIDT.m behaviour
                # self.add_pac appends new PACs to this list
                return self.pacs

        # IDT - add PAC to list
        def add_pac(self, fixstart, fixend):
                """
                adds a range of points as a PAC to self.pacs
                if fixstart or fixend have exceeded the
                bounds of self.positions this will fail

                Y: the function above identify a pac and this function is to add to the list
                """
                fixend = self._end(fixend)
                avx, avy = self._means(fixstart, fixend)
                actual_duration = self._duration(fixstart, fixend)
                pac = PAC( 
                          actual_duration,              # aka dur 
                          avx, avy,                     # spatial position
                          (self.positions[fixend][0],   # TimeStamps aka FixBounds
                           self.positions[fixstart][0]), 
                          (self.positions[fixend][3],   # RowIDs aka RowBounds
                           self.positions[fixstart][3]) 
                        ); # RowIDs ordered as in ScreenFixationsIDT.m
                if verbose: 
                        print "fixstart",fixstart,"fixend",fixend
                        print "start pos",self.positions[fixstart]
                        print "end pos",self.positions[fixend]
                        print "pac",pac
                self.durations.append(actual_duration)
                self.pacs.append(pac)

        # bounds checking methods
        def inbounds(self, fixstart, fixend):
                """
                get the box for fixstart to fixend
                see if we are within bounds for that box
                based on our dispersion threshold
                """
                if fixend >= len(self.positions): return False
                max_x, min_x, max_y, min_y = self._minmax(fixstart, fixend)
                return self._checkbounds(max_x, min_x, max_y, min_y)

        def overtime(self, fixstart, fixend):
                """
                for a range of points bounded by fixstart and fixend
                are we over our time threshold?
                """
                if fixend < fixstart:
                        raise Exception("bad start and end in overtime {} {}".format(fixstart,fixend))
                try:
                        if (self.positions[self._end(fixend)][0] - self.positions[fixstart][0]) > self.max_duration:
                                return True
                except Exception as e:
                        print e
                        print "fixend",fixend,"fixstart",fixstart
                        try:
                                print "start",self.positions[fixstart]
                                print "end",self.positions[fixend]
                        except:
                                print " - error printing"
                                pass
                return False

        # some utility methods
        # Y: game tables contain many information which is not in the form of ['TimeStamp','ScreenX','ScreenY','RowID']
        # Y: there following functions are to exact standard form of data we need from the db

        # external
        def fields(self):
                """
                what fields to look for in the game events table
                like those in template_replaylevel.mysql
                """
                return ['TimeStamp','ScreenX','ScreenY','RowID']

        def dict2tuple(self, dictrow, fields=None):
                """
                grab the relevant field data from a single dictionary row
                """
                if fields == None: fields = self.fields()
                return tuple(dictrow[fname] for fname in fields)

        def dicts2tuples(self, dictrows, fields=None):
                """
                convert dictionary rows to tuples
                use the method like this:

                        import testdb as db
                        conn = db.dictconn()
                        cursor = conn.cursor()
                        cursor.execute("select * from some_table where ...")
                        rows = list(cursor)
                        # rows are a list of dictionaries
                        cursor.close()
                        conn.close()
                        ps = pacshift.PACShift(duration=20,dispersion=6)
                        # turn row dictionaries into tuples and do IDT
                        ps.idt_convert(ps.dicts2tuples(rows))

                at the last line the correct fields are extracted from rows
                to build the ps.pacs list
                
                optionally supply a list of 4 fields
                by default these fields are:

                ['TimeStamp','ScreenX','ScreenY','RowID']

                """
                if fields == None: fields = self.fields()
                positions = []
                for dictrow in dictrows:
                        positions.append(self.dict2tuple(dictrow, fields))
                return positions

        # internal
        def _duration(self, fixstart, fixend):
                """
                time from start to end of fixation
                assumes that positions exists
                """
                return self.positions[fixend][0] - self.positions[fixstart][0]

        def _means(self, fixstart, fixend):
                """
                given a range calculate the mean of x and y
                """
                if fixend < fixstart:
                        raise Exception("bad start and end in _means {} {}".format(fixstart,fixend))
                positions = self.positions
                if fixend == fixstart:
                        return positions[fixstart][1], positions[fixstart][2]
                # Decimal needed here to coerce python to behave like matlab
                sx = sum([Decimal(positions[j][1]) for j in xrange(fixstart, fixend)])
                sy = sum([Decimal(positions[j][2]) for j in xrange(fixstart, fixend)])
                n = Decimal(fixend - fixstart)
                return float(sx/n), float(sy/n)

        def _minmax(self, fixstart, fixend):
                """
                within a given range of positions
                find the bounds of x and y
                """
                if fixend < fixstart:
                        raise Exception("bad start and end in _minmax {} {}".format(fixstart,fixend))
                positions = self.positions
                if fixstart == fixend:
                        return (positions[fixstart][1],
                                positions[fixstart][1],
                                positions[fixstart][2],
                                positions[fixstart][2],)
                rx = [positions[j][1] for j in xrange(fixstart, fixend+1)]
                ry = [positions[j][2] for j in xrange(fixstart, fixend+1)]
                max_x = max(rx)
                min_x = min(rx)
                max_y = max(ry)
                min_y = min(ry)
                return max_x, min_x, max_y, min_y

        def _checkbounds(self, max_x, min_x, max_y, min_y):
                """
                are we within our dispersion threshold?
                """
                if max_x < min_x: raise Exception("max_x smaller than min_x {} {}".format(max_x,min_x))
                if max_y < min_y: raise Exception("max_y smaller than min_y {} {}".format(max_y,min_y))
                if (max_x-min_x) + (max_y-min_y) <= self.max_disp:
                        return True
                return False

        def _end(self, fixend):
                """
                check if we are out of bounds
                if not return given fixend
                """
                end = fixend if fixend < self.nrows else self.nrows-1
                return end

        # get/display object data - assumes there is something to get/display
        def endrowid(self, i):
                """
                returns rowid of end of pac
                for a specific pac entry
                """
                return self.pacs[i].rowend

        def __str__(self):
                """
                how to represent this PACShift object for print statements
                """
                nrows = 0
                pacs = 0
                try:
                        nrows = len(self.positions)
                        pacs = len(self.pacs)
                except:
                        pass
                return "dispersion {} duration {} rows {} (self.nrows: {}) pacs {}".format(
                        self.max_disp, self.max_duration, nrows, self.nrows, pacs)

        def print_positions(self):
                """
                print current list of raw input used to make PACs
                """
                try:
                        for p in self.positions:
                                print p
                except:
                        print "unable to print"

        def print_pacs(self):
                """
                print current list of PACs
                """
                try:
                        for p in self.pacs:
                                print p
                except:
                        print "unable to print"

        # stats generation methods
        def stats_init(self):
                """
                resets the self.statlists dictionary
                """
                self.stats = {}
                self.statlists = {}
                self.statlists['newviewcost'] = []
                self.statlists['latencytoend'] = []
                self.statlists['betweenactionlatency'] = []
                self.statlists['firstactionlatency'] = []
                self.statlists['pacactioncount'] = []
                self.statlists['betweenfixations'] = []
                self.statlists['betweenpacs'] = []

        def stats_append(self, p):
                """
                append pac statistics to various lists
                """
                if p.newviewcost is not None:
                        self.statlists['newviewcost'].append(p.newviewcost)
                if p.latencytoend is not None:
                        self.statlists['latencytoend'].append(p.latencytoend)
                if p.betweenactionlatency is not None:
                        self.statlists['betweenactionlatency'].append(p.betweenactionlatency)
                if p.firstactionlatency is not None:
                        self.statlists['firstactionlatency'].append(p.firstactionlatency)
                if p.pacactioncount is not None:
                        self.statlists['pacactioncount'].append(p.pacactioncount)
                if p.betweenfixations is not None:
                        self.statlists['betweenfixations'].append(p.betweenfixations)
                if p.betweenpacs is not None:
                        self.statlists['betweenpacs'].append(p.betweenpacs)

        def stat(self, key, callback):
                """
                generate a statistic using a callback
                based on a key into the self.statlists dictionary
                callback is assumed to return None if 
                the self.statlists[key] list is empty 

                sometimes the callbacks fail because there is nothing in the list
                making executive decision to return None in this case and in case of error
                we may want to review this decision
                """
                if key in self.statlists:
                        try:
                                if len(self.statlists[key]) == 0: return None
                                return callback(self.statlists[key])
                        except Exception as e:
                                print "callback",str(callback),"key",key,"failed",str(e),"returning None"
                                return None
                return None

        def generate_stats(self, events, schema='pacs_simple'): 
                """
                convenience method to run IDT and generate stats on the PACs
                their original row data and update each PAC object 
                with some statistics
                note that these stats depend on field names matching
                those in template_replaylevel.mysql

                the schema parameter determines what string fields get included in the table
                these fields are controlled by variables starting do_

                the do_.* variables determine what text fields get included
                they do not affect the other statistics
                        do_fix: (False) include strings representing fixation data (i.e. non-pacable actions)
                        do_elist: (False) include full actiontype strings 
                        do_tlist: (True) include when actions occurred
                        do_clist: (True) include single character action strings
                        do_alist: (False) include aggregated single character strings
                """
                if schema == 'pacs_simple':
                        do_fix = False
                        do_elist = False
                        do_tlist = True
                        do_clist = True
                        do_alist = False
                elif schema == 'pacs':
                        do_fix = True
                        do_elist = True
                        do_tlist = True
                        do_clist = True
                        do_alist = True
                else:
                        raise(Exception("generate_stats: need a valid schema!"))

                self.idt_convert(self.dicts2tuples(events))

                if len(self.pacs) == 0:
                        return

                gameid = events[0]['GameID']
                player = events[0]['Player']
                pacdurs = []
                fixdurs = []
                self.stats_init()
                pacableactions = 0
                #Y: enumerate(thing that is a iteratior) 
                #Y: this returns a iterator that will return (0, thing[0]), (1, thing[1]), (2, thing[2]), and so forth.
                for pacord, pevents in enumerate(self.iterator(events, invert=False)):
                        if pevents is None: continue

                        p = self.pacs[pacord]
                        if do_fix:
                                # a fixation can be all moves (m)
                                if do_elist: fix_elist = [] # actions as ActionTypes
                                if do_tlist: fix_tlist = [] # action timestamps
                                if do_clist: fix_clist = [] # actions as single characters
                                if do_alist: fix_alist = [] # aggregated actions as single chars
                                prevat = None
                                for evt in pevents:
                                        at = evt['ActionType']
                                        if do_elist: fix_elist.append(at)
                                        if do_tlist: fix_tlist.append(float(evt['TimeStamp']))
                                        if do_clist: fix_clist.append(gzipgames.def_map[at])
                                        # for aggregated strings we are only interested in some actions
                                        if do_alist:
                                                if at in gzipgames.def_accept:
                                                        # find actions that are aggregatable
                                                        if at in gzipgames.def_agg:
                                                                if at != prevat:
                                                                        fix_alist.append(gzipgames.def_map[at])
                                                        else:
                                                                fix_alist.append(gzipgames.def_map[at])

                                                prevat = at

                        # a pac should involve actually doing something
                        if do_elist: pac_elist = [] # actions as ActionTypes
                        pac_tlist = [] # action timestamps
                        if do_clist: pac_clist = [] # actions as single characters
                        if do_alist: pac_alist = [] # aggregated actions as single chars
                        prevat = None
                        firstactionidx = None
                        firstactionts = None
                        firstactiontype = None
                        firstaction = None
                        firstactionx = None
                        firstactiony = None
                        firstactionlatency = None
                        pacactioncount = 0
                        lastactionts = None
                        lastactionidx = None
                        firstpacts = None
                        for i, evt in enumerate(pevents): #Y: pevents in events, evt in pevents??
                                ts = evt['TimeStamp']
                                if firstpacts == None: firstpacts = ts
                                lastpacts = ts
                                at = evt['ActionType']
                                action = evt['Action']
                                # this is from Starcraft/PACBuilding/PACTableBuilderbyRowid.m
                                if not is_pacable(at, action):
                                        continue
                                pacactioncount += 1
                                lastactionidx = i
                                lastactionts = ts
                                if firstactiontype == None:
                                        firstactionidx = i
                                        firstactionts = ts
                                        firstactiontype = at
                                        firstaction = action
                                        firstactionx = evt['ActionX']
                                        firstactiony = evt['ActionY']
                                        firstactionlatency = ts - p.fixstart
                                if do_elist: pac_elist.append(at)
                                pac_tlist.append(float(ts))
                                if do_clist: pac_clist.append(gzipgames.def_map[at])
                                # for aggregated strings we are only interested in some actions
                                if do_alist:
                                        if at in gzipgames.def_accept:
                                                # find actions that are aggregatable
                                                if at in gzipgames.def_agg:
                                                        if at != prevat:
                                                                pac_alist.append(gzipgames.def_map[at])
                                                else:
                                                        pac_alist.append(gzipgames.def_map[at])

                                        prevat = at

                        if len(pac_tlist) > 1:
                                sumal = sum([ pac_tlist[i] - pac_tlist[i-1] \
                                                for i in xrange(1, len(pac_tlist))])
                                betweenactionlatency = float(Decimal(sumal) / Decimal(len(pac_tlist)-1.0))
                        else:
                                betweenactionlatency = firstactionlatency

                        if firstactionlatency is None or betweenactionlatency is None:
                                newviewcost = None
                        else:
                                newviewcost = firstactionlatency - betweenactionlatency

                        if lastpacts is None or lastactionts is None:
                                latencytoend = None
                        else:
                                latencytoend = lastpacts - lastactionts

                        if pacord == 0:
                                latencyfrompriorfix = None
                        else:
                                try:
                                        latencyfrompriorfix = p.fixstart - self.pacs[pacord-1].fixend
                                except:
                                        if verbose: print self.pacs
                                        raise Exception("bad latencyfrompriorfix at pacord {} ".format(pacord))

                        if pacord > 0:
                                between = self.pacs[pacord].fixstart - self.pacs[pacord-1].fixend
                        else:
                                between = None

                        if len(pac_tlist) > 0: 
                                pacdurs.append(p.dur)
                                betweenpacs = between
                        else:
                                betweenpacs = None

                        fixdurs.append(p.dur)
                        betweenfixations = between
                        pacableactions += pacactioncount

                        if do_elist: pac_actiontypes = ' '.join(pac_elist)
                        # possible to store times as 4 byte floats but no way to get them out
                        # e.g. pac_actiontimes = array.array('f', pactlist)
                        if do_tlist: pac_actiontimes = ' '.join([str(int(t - p.fixstart)) for t in pac_tlist])
                        if do_clist: pac_actionchars = ''.join(pac_clist)
                        if do_alist: pac_actionagg = ''.join(pac_alist)
                        if do_fix:
                                if do_elist: fix_actiontypes = ' '.join(fix_elist)
                                if do_tlist: fix_actiontimes = ' '.join([str(int(t - p.fixstart)) for t in fix_tlist])
                                if do_clist: fix_actionchars = ''.join(fix_clist)
                                if do_alist: fix_actionagg = ''.join(fix_alist)
                        p.update(
                                gameid=gameid,
                                player=player,
                                pacord=pacord,
                                firstactiontype=firstactiontype,
                                firstaction=firstaction,
                                firstactionx=firstactionx,
                                firstactiony=firstactiony,
                                pacactioncount=pacactioncount,
                                firstactionlatency=firstactionlatency,
                                betweenactionlatency=betweenactionlatency,
                                latencytoend=latencytoend,
                                latencyfrompriorfix=latencyfrompriorfix,
                                newviewcost=newviewcost,
                                pac_actiontypes=(pac_actiontypes if do_elist else None),
                                pac_actiontimes=(pac_actiontimes if do_tlist else None),
                                pac_actionchars=(pac_actionchars if do_clist else None),
                                pac_actionagg=(pac_actionagg if do_alist else None),
                                fix_actiontypes=(fix_actiontypes if do_elist and do_fix else None),
                                fix_actiontimes=(fix_actiontimes if do_tlist and do_fix else None),
                                fix_actionchars=(fix_actionchars if do_clist and do_fix else None),
                                fix_actionagg=(fix_actionagg if do_alist and do_fix else None),
                                betweenpacs=betweenpacs,
                                betweenfixations=betweenfixations
                        )
                        self.stats_append(p)

                # fields for master table
                self.stats['newviewcostmean'] = self.stat('newviewcost',avg)
                self.stats['distancebetweenfixationsmean'] = self.stat('betweenfixations',avg)

                self.stats['distancebetweenpacsmean'] = self.stat('betweenpacs', avg)
                self.stats['distancebetweenpacsmeanstd'] = self.stat('betweenpacs', sd)

                self.stats['latencytofixationmean'] = self.stat('latencytoend', avg)
                self.stats['latencytofixationstd'] = self.stat('latencytoend', sd)

                self.stats['meanpacactiondiffmax'] = self.stat('betweenactionlatency', maximum)
                self.stats['meanpacactiondiffmean'] = self.stat('betweenactionlatency', avg)
                self.stats['meanpacactiondiffmin'] = self.stat('betweenactionlatency', minimum)
                self.stats['meanpacactiondiffstd'] = self.stat('betweenactionlatency', sd)

                self.stats['pacactionlatencymax'] = self.stat('firstactionlatency', max)
                self.stats['pacactionlatencymean'] = self.stat('firstactionlatency', avg)
                self.stats['pacactionlatencystd'] = self.stat('firstactionlatency', sd)

                self.stats['paccontentsmean'] = self.stat('pacactioncount', avg)
                self.stats['paccontentsmeanstd'] = self.stat('pacactioncount', sd)

                self.stats['pacs'] = len(pacdurs)
                self.stats['fixations'] = len(fixdurs)
                self.stats['fixduration'] = avg(fixdurs)

                self.stats['pacdurationsmean'] = avg(pacdurs)
                self.stats['pacdurationsstd'] = sd(pacdurs)

                if self.stats['fixations'] > 0.0:
                        self.stats['paccountoverfixcount'] =  \
                                float(Decimal(self.stats['pacs'])/Decimal(self.stats['fixations']))
                else:
                        self.stats['paccountoverfixcount'] = None

                if self.stats['fixduration'] is None or self.stats['pacdurationsmean'] is None:
                        self.stats['pacdurationminuxfixduration'] = None
                else:
                        self.stats['pacdurationminusfixduration'] = \
                                float(Decimal(self.stats['pacdurationsmean']) - Decimal(self.stats['fixduration']))

                self.stats['pacableactionsinsidepac'] = pacableactions

                pacableactions = 0
                durations = []
                # in this loop we find events that are *between* PACs and do action counts
                for i, nonevents in enumerate(self.iterator(events, invert=True)):
                        durations.append(self.pacs[i].dur)
                        for evt in nonevents:
                                at = evt['ActionType']
                                action = evt['Action']
                                if is_pacable(at, action):
                                        continue
                                pacableactions += 1
                                
                self.stats['nonpacfixdurationsmean'] = avg(durations)
                self.stats['nonpacfixdurationsstd'] = sd(durations)
                self.stats['pacableactionsoutsidepacprop'] = pacableactions


if __name__ == '__main__':
        verbose = False

        # do a basic test
        import sys
        table = sys.argv[1]
        gameid = sys.argv[2]

        import platform
        if platform.node() == 'bugaboo.westgrid.ca':
                # the player tables are the only ones we know about in wgdb
                if re.match(r'player_', table):
                        import wgdb as bfldb
                else:
                        import testdb as bfldb
        else:
                # ditto
                if re.match(r'player_', table):
                        import bfldb
                else:
                        import testdb as bfldb

        conn = bfldb.dictconn()
        get = conn.cursor()

        
        try:
                player = sys.argv[3]
        except:
                # pick a random player if we don't already have one
                get.execute(
                    "select player from {} where gameid=%s limit 1".format(table),
                    (gameid,)
                )
                row = get.fetchone()
                player = row['player']

        print "looking for player",player,"in game",gameid,"table",table
        starttime = time.time()
        get.execute(
            # "select TimeStamp,ScreenX,ScreenY,RowID "
            "select * "
            # "from {} where GameID=%s and Player=%s and ActionType = 'm' "
            "from {} where GameID=%s and Player=%s "
            "order by RowID;".format(table), 
            (gameid,player)
        )
        print get._last_executed

        print "query elapsed",(time.time()-starttime)
        positions = list(get)
        get.close()
        conn.close()

        ps = PACShift()
        print "get positions from query elapsed",(time.time()-starttime),len(positions),"positions"
        ps.generate_stats(positions)
        print "generate_stats elapsed",(time.time()-starttime)

        # print "\nPAC shift fixations:"
        ps.print_pacs()
        print "elapsed",(time.time()-starttime)
        """
        print "test iterator with no input"
        for i, evts in enumerate(ps.iterator()):
                print ps.pacs[i]
                print "found",len(evts),"events"
                print evts
        print "test iterator with input"
        for i, evts in enumerate(ps.iterator(positions)):
                print ps.pacs[i]
                print "found",len(evts),"events"
                print evts
        """
        print "elapsed",(time.time()-starttime)
        print ps.stats
        # print ps.statlists
        print "elapsed",(time.time()-starttime)
        # print ps


