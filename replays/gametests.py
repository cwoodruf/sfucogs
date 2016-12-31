"""
classes that define tests that check whole games in player_* tables
these tests use other modules to define subtests (e.g. eventtests.py)

Date: Sat Apr  9 16:49:11 2016
Author: Cal Woodruff cwoodruf@sfu.ca
Reviewed: Adam Bignell
Verified:
"""
import eventtests as et
import eventparseutils as epu
import re
verbose = False
reallyverbose = False

###############################################################################
# tests for whole games
class GameTest(object):
        """
        This is a superclass for tests that check a whole game
        """
        def __init__(this):
                this.name = et.get_name(this.__class__)
                this.passed = None
                this.data = None

        def run(this, metadata, events):
                pass

        def results(this):
                return (this.passed, this.data)

class MonotonicTest(GameTest):
        """
        Do the TimeStamp fields always increase with the RowID
        """
        def __init__(this):
                super(MonotonicTest, this).__init__()

        def run(this, metadata, events):
                """
                we assume that events are ordered via rowid
                so we should also assume that TimeStamp only increases
                """
                prev_rowid = None
                prev_ts = None

                for event in events:
                        if prev_rowid == None: 
                                prev_rowid = event['RowID']
                                prev_ts = event['TimeStamp']
                                continue
                        if prev_ts == None: 
                                raise(Exception("MonotonicTest: missing timestamp!"))
                        if prev_rowid == None: 
                                raise(Exception("MonotonicTest: missing rowid!"))
                        if event['RowID'] <= prev_rowid: 
                                raise(Exception("MonotonicTest: out of order rowids: prev {} > {}".format(
                                        prev_rowid, event['RowID'])))
                        if prev_ts > event['TimeStamp']:
                                this.passed = False
                                this.data = { 
                                    "errors": "prev ts {} more than current ts {} at rowid {}".format(
                                                    prev_ts, event['TimeStamp'], event['RowID'])
                                }
                                return
                        prev_ts = event['TimeStamp']
                        prev_rowid = event['RowID']

                this.passed = True
                this.data = None

        
class CoordsTest(GameTest):
        """
        Does ScreenX and ScreenY match what we'd expect for this character?
        To get actual rows set t.verbose = True before running test
        """
        def __init__(this):
                super(CoordsTest, this).__init__()
                this.show_rows = False

        def run(this, metadata, events):
                """
                Prior to the first Move ScreenX and ScreenY should be 0 for any player
                ScreenX and ScreenY should only change when a Move occurs
                After a move (x, y) should not be (-1, -1) 
                i.e. coordinates are expected for move actions
                """
                curpos = {}
                if this.show_rows: 
                        rowids = []
                errors = 0
                for event in events:
                        player = event['Player']
                        here = (event['ScreenX'], event['ScreenY'])
                        rowid = event['RowID']
                        actionstr = event['actionstr']

                        if event['ActionType'] == 'm':
                                x, y = epu.extract_coords(actionstr)
                                if reallyverbose:
                                        print player,"at",x,y,"in",actionstr
                                        print event
                                        print

                                if x == -1 and y == -1:
                                        this.passed = False
                                        if verbose:
                                                print "FAILED: player",player,"didn't move!"
                                                print curpos
                                                print event
                                                print
                                        errors += 1
                                        if this.show_rows: rowids.append(rowid)

                                curpos[player] = ((x if x > -1 else 0), (y if y > -1 else 0))

                        if player not in curpos and here > (0,0):
                                this.passed = False
                                if verbose:
                                        print "FAILED: player",player,"should be 0,0 but was",here
                                        print curpos
                                        print event
                                        print
                                errors += 1
                                if this.show_rows: rowids.append(rowid)
                                continue

                        if player in curpos and here != curpos[player]:
                                this.passed = False
                                if verbose:
                                        print "FAILED: player",player,"should be at ",curpos[player],"but was",here
                                        print curpos
                                        print event
                                        print
                                errors += 1
                                if this.show_rows: rowids.append(rowid)
                                continue

                if this.passed == None and errors == 0:
                        this.passed = True

                this.data = {}
                this.data['errors'] = errors
                if this.show_rows: 
                        this.data['rowids'] = rowids

class LengthTest(GameTest):
        """
        Does the reported game_lasttick show up in the events?
        """
        def __init__(this):
                super(LengthTest, this).__init__()

        def run(this, metadata, events):
                """
                Check for TimeStamp of last event
                Passes if last TimeStamp is the same as game_lasttick
                """
                if len(events) <= 0:
                        raise(Exception("LengthTest: no events list!"))
                        return
                lasttick = events[-1]['TimeStamp']
                if metadata['game_lasttick'] == lasttick:
                        this.passed = True
                else:
                        this.passed = False
                        if verbose:
                                print "FAILED: bad last tick",lasttick,"expecting",metadata['game_lasttick']
                                print
                this.data = {'lasttick': events[-1]['TimeStamp']}

class CharacterTest(GameTest):
        """
        Do the characters listed show up in the game events 
        and vice versa
        """
        def __init__(this):
                super(CharacterTest, this).__init__()

        def run(this, metadata, events):
                """
                using game_clients in metadata find all the character names
                scan events looking for characters
                pass if the lists match
                fail if they don't
                data is the characters actually in the game
                """
                characters = {}
                for character in metadata['game_clients'].split(','):
                        characters[character] = True
                gamecharacters = {}
                missingcharacters = {}
                nonplaying = []
                for event in events:
                        player = event['Player']
                        if player not in gamecharacters:
                                gamecharacters[player] = 0
                        gamecharacters[player] += 1
                        if player not in characters:
                                missingcharacters[player] = True

                for character in characters:
                        if character not in gamecharacters:
                                nonplaying.append(character)

                missing = len(missingcharacters.keys())
                if missing > 0:
                        this.passed = False
                        if verbose:
                                print "FAILED: missing",missingcharacters
                                print "expecting",characters
                                print "got",gamecharacters
                                print
                else:
                        this.passed = True
                total = len(gamecharacters.keys())
                this.data = {'missing': missing, 'total': total, 
                        'characters': {'all':gamecharacters,'missing':missingcharacters,'nonplaying':nonplaying}}


class EventsTest(GameTest):
        """
        Run tests on individual events
        Tally which events had failures
        along with other statistics
        """
        def __init__(this):
                super(EventsTest, this).__init__()
                this.data = {}
                this.data['empty'] = 0
                this.data['queued'] = 0
                this.data['passed'] = 0
                this.data['failed'] = 0
                this.data['queuefailed'] = 0
                this.data['events'] = {}
                this.data['coordinate_errors'] = 0
                this.data['total_unknown_targets'] = 0
                this.data['unknown_targets'] = {}

        def tally_actiontype(this, at):
                """
                keep stats on action types
                """
                if at not in this.data['events']:
                        this.data['events'][at] = 0
                this.data['events'][at] += 1

        def tally_unknowns(this, at, unknowns):
                """
                collect stats on unknown targets to flag possible 
                custom games - based on counts per action type
                """
                if at not in this.data['unknown_targets']:
                        this.data['unknown_targets'][at] = 0
                this.data['unknown_targets'][at] += unknowns
                this.data['total_unknown_targets'] += unknowns

        def run(this, metadata, events):
                """
                Checks every event based on the first 
                word in actionstr using test classes from 
                eventtests.py 
                """
                for event in events:

                        if len(event['actionstr']) == 0:
                                this.data['empty'] += 1
                                continue

                        # how many unknown targets were found in sel/rc actions
                        unknowns = 0

                        if re.search(r'Cancel;?', event['actionstr']):
                                t = et.CancelTest()
                        else:
                                actionary = event['actionstr'].split(' ')
                                at = actionary[0]
                                if at == '[Queued]':
                                        queued = True
                                        this.data['queued'] += 1
                                        at = actionary[1]
                                else:
                                        queued = False
                                t = None
                                if at == 'Move':
                                        t = et.MoveTest()
                                elif at == 'Select':
                                        t = et.SelectTest('sel')
                                        unknowns = t.unknowns(event)
                                elif at == 'Deselect':
                                        t = et.SelectTest('seld')
                                elif at == 'Selection':
                                        t = None
                                        this.tally_actiontype('u')
                                        continue
                                elif at == 'Right':
                                        t = et.RightClickTest()
                                        unknowns = t.unknowns(event)
                                elif at == 'Hotkey':
                                        t = et.HotkeyTest()
                                elif at == 'Train':
                                        t = et.TrainTest()
                                elif at == 'Build':
                                        t = et.BuildTest()
                                elif at == '[Failed]':
                                        t = et.FailTest()
                                elif at == '[MinimapClick]':
                                        t = et.MinimapTest()
                                elif at == 'Attack;':
                                        t = et.AttackTest()
                                else:
                                        t = et.AbilityTest()

                        t.run(event)
                        passed, errors = t.results()

                        if passed == True: 
                                this.data['passed'] += 1
                        else: 
                                if verbose:
                                        print "FAILED:"
                                        print event
                                        print t.errors
                                        print
                                this.data['failed'] += 1

                        if queued == True:
                                tq = et.QueuedTest()
                                tq.run(event)
                                passed, errors = tq.results()
                                if passed == False:
                                        this.data['queuefailed'] += 1

                        if t.coordinate_error == True:
                                this.data['coordinate_errors'] += 1

                        if unknowns > 0:
                                this.tally_unknowns(t.actiontype, unknowns)

                        this.tally_actiontype(t.actiontype)

        def results(this):
                if this.data['failed'] > 0:
                        this.passed = False
                else:
                        this.passed = True

                return (this.passed, this.data)

