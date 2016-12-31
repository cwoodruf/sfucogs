"""
utility functions used by eventparse.py and eventtest.py
for processing individual event lines
these are used by extract_action to form the
database record for specific actions

Date: Sat Apr  9 16:49:11 2016
Author: Cal Woodruff cwoodruf@sfu.ca
Reviewed: Adam Bignell, Aug 19, 2016
Verified:
"""
import re

###############################################################################
# utilities

def extract_coords(a):
    """
    utility function used by various callbacks:
    use a regexp to find coordinates
    return -1,-1 or coords as tuple
    typically coordinates look like this:
    x=131.00,y=125.50
    """
    g = re.search(r'x=(\d+\.?\d*)\s*,\s*y=(\d+\.?\d*)', a)
    if g == None: return (-1.0,-1.0)
    x = float(g.group(1))
    y = float(g.group(2))
    return (x,y)

###############################################################################
"""
callbacks used by extract_action to make sense of events

these callbacks all take an action array, which is returned modified at the end,
an action string and a list of words from the action string as input

the action array is modified based on the contents of the action string
and returned to be saved in the database

as far as possible the exact output from txtparse.m is returned in the
action array

a significant difference with txtparse.m is that, instead of failing when
an error occurs, the "errors" key in the action array is set
the resulting tables produced by eventparse.py should be checked
for these error messages

"""

def set_coords(action, a, awords):
    """
    used for Move, Select and Deselect actions
    scans for coordinates and update action
    """
    x, y = extract_coords(a)
    action['x'] = x
    action['y'] = y
    return action

def right_click(action, actionstr, awords):
    """
    right clicks can be of the form:
    Right click target: Something(abcdef) target: x=NN.NN,y=NN.NN
    Right click target: x=NN.NN,y=NN.NN
    """
    actions = " ".join(awords[2:])
    
    x, y = extract_coords(actionstr)
    if x > -1.0 and y > -1.0:
        action['x'] = x
        action['y'] = y
        action['target'] = 'Coordinate'
        t = re.search(r'target: (.*\(\w+\))', actionstr)
        if not t == None:
            action['action'] = t.group(1)
        else:
            action['action'] = 'null'
    else:
        t = re.search(r'target: (.*)', actionstr)
        if not t == None:
            action['target'] = t.group(1)
        else:
            action['target'] = actions;

    return action

def hotkey(action, actionstr, awords):
    """
    stores hotkey press
    these action strings can have two or three relevant fields
    the target is the key number
    """
    h = re.match(r'Hotkey (\w*) (\d*)\s*(.*)', actionstr)
    if h == None: return action
    if len(h.group(3)) > 0:
        action['action'] = "{} {}".format(h.group(1),h.group(3))
    else:
        action['action'] = h.group(1)
    action['target'] = h.group(2)
    return action

def train(action, actionstr, awords):
    """
    handles training action storing what was trained
    """
    t = re.match(r'.*? (.*)\n', actionstr)
    if t == None: return action
    action['action'] = t.group(1)
    return action

def build(action, actionstr, awords):
    """
    this is very similar to fail below 
    we should combine these if they do the same thing
    """
    a = re.search(r'Build ([^;]+); (.*)', actionstr)
    if a == None: return action
    action['action'] = a.group(1)

    x, y = extract_coords(actionstr)
    if x > -1.0 and y > -1.0:
        action['target'] = 'Coordinate'
        action['x'] = x
        action['y'] = y
    else:
        action['target'] = a.group(2)

    return action

def fail(action, actionstr, awords):
    """
    checks if an action failed
    extracts coordinates if they exist
    """
    f = re.match(r'\[Failed\] ([^;]*);?(.*)', actionstr)
    if f == None: return action
    action['action'] = f.group(1)
    x, y = extract_coords(actionstr)
    if x > -1.0 and y > -1.0:
        action['x'] = x
        action['y'] = y
        action['target'] = 'Coordinate'
    else:
        if len(f.group(2)) > 0:
            action['target'] = f.group(2)
        else:
            action['target'] = 'null'
    return action

def mini_map_click(action, actionstr, awords):
    """
    handle click on a mini map
    these can be for attacks, context menus (right click) 
    or, by default, ability
    extracts coordinates from replay line
    """
    #consult the second word to see if its an attack or rc
    if awords[1] == 'Attack;':
        action['type']='mapAtk';          
    elif awords[1] == 'Right':
        action['type']='mapRCClick';
    else:
        action['type']='mapAbl'; 
    m = re.match(r'\[MinimapClick\] ([^;]*);?\s*\S*\s+(.*)', actionstr)
    if m == None: return action
    action['action'] = m.group(1)
    if len(m.group(2)) > 0:
        x, y = extract_coords(actionstr)
        if x > -1.0 and y > -1.0:
            action['x'] = x
            action['y'] = y
            action['target'] = 'Coordinate'
        else:
            action['target'] = m.group(2)
    return action

def extract_targets(action, actionstr, awords):
    """
    ability and attack are sharing this callback
    this looks for coordinates and targets in the action string
    there should always be coordinates if "target:" exists in string
    """
    target = 'null'
    targets = re.match(r'^([^;]*);\s*(.*)', actionstr)
    if targets == None:
        # print "couldn't find target for",actionstr
        action['action'] = actionstr
        return action

    action['action'] = targets.group(1)
    if len(targets.group(2)) > 0:
        at = re.search(r'target:\s*(.*\(\w*\))', actionstr)
        if not at == None:
            target = at.group(1)

    x, y = extract_coords(actionstr)
    if x > -1.0 and y > -1.0:
        action['x'] = x
        action['y'] = y
        if target == 'null':
            action['target'] = 'Coordinate'
        else:
            action['target'] = target
    else:
        targetcount = targets.group(2).count('target:')
        if not target == 'null' and targetcount > 1:
            action['errors'] = "has target but coordinates missing"
        elif target == 'null' and targetcount <= 1:
            action['errors'] = "no target but coordinates missing"
        action['target'] = targets.group(2)

    return action
        
# end of callbacks for extract_action
###############################################################################
# code for parsing action strings
actiontypes = {
    'Move': {'type':'m','action':'null','callback': set_coords},
    'Select': {'type':'sel','callback': set_coords},
    'Deselect': {'type':'seld','callback': set_coords},
    'Selection': {'type':'u','action':'unknown'},
    'Right': {'type':'rc','callback': right_click},
    'Hotkey': {'type':'hk','callback': hotkey},
    'Train': {'type':'tr','callback': train},
    'Build': {'type':'b','callback': build},
    '[Failed]': {'type':'f','callback': fail},
    '[MinimapClick]': {'type':'null', 'callback': mini_map_click},
    'Attack;': {'type':'atk','callback': extract_targets}
}

def extract_action(l):
    # Reviewed by Yue Chen and Adam Bignell August 5, 2016

    """
    based on an input string parse out what a player is doing
    returns an action dict with relevant data that can be saved
    to the database

    this will only work with sc2gears output but could be adapted to
    work with other replay extraction output formats that use the form
    {int timestamp} {playerid} {action}

    uses a dictionary of actiontypes that maps action keywords to action 
    codes used in the player tables
    actions are parsed based on their first word with three exceptions:
        [Queued] - this is removed from the string and queued is set to True
                   rest of string is then parsed normally
        Cancel   - can show up anywhere in string, parse is aborted at this point
        ability  - any first word not matched in actiontypes 

    """

    # t = textscan(f, '%d %s %[^\n]', 'headerLines', 2);  
    # gets out the timestamp, player, and actioninfo (including coordinates), respectively
    # assuming if we don't have this then we ignore the line - ??

    # AY: What precisely does this line do. What is it searching using the parameters from 'l'?
    g = re.match(r'^\s*(\d+)\s+(\S+)\s+(.*)\n', l)
    if g == None: 
        raise(Exception('no data found'))

    # data = cell(length(t{1,3})+1, 11); % +1 for the header. %11 is the # of columns!
    # AY: Note that group(0) returns the FULL return, i.e. tick, curr_player and actionstr concatenated
    tick = int(g.group(1))
    cur_player = g.group(2)
    actionstr = g.group(3)

    # initialize the actions.
    # AY: Dictionary
    action = {
        'player':cur_player, 
        'tick': tick, 
        'type':None, 
        'action':'null', 
        'target':'null', 
        'x':-1.0, 
        'y':-1.0,
        'queued':0,
        'errors':None,
        'actionstr':actionstr,
    }

    #checks for empty actions. label them u for unknown
    if actionstr == '':
        action['type'] = 'u';
        action['action'] = 'blank'; #used to be 'tab' (See comments above)
        return action

    #AY: Split actionstr into discrete words representing actions
    awords = g.group(3).split(' ')

    ## Jan 2014 Code: check if action is queued and, if so, remove the '[queued]' from the action string
    # AY: Does this imply that we ignore queued actions or ignore the label "queued"?
    if awords[0] == '[Queued]':
        action['queued'] = 1; # AY: If action is queued set "queued" to 1
        del(awords[0])
        actionstr = re.sub(r'^\[Queued\] *','',actionstr)
        
    ## Jan 2014 Code: if condition: Check entire string for the word Cancel, else use original code
    hasCancel = re.search(r'Cancel', actionstr)
    if not hasCancel == None:
        action['type'] = 'Cancel'
        action['action'] = actionstr
        return action

    # For clarity:
    # AY: 
    # action [Variable] -> Dictionary of ALL attributes associated with an action corresponds to line "l" with only relevant data
    # awords -> Example: [Select Larva x3 (1020c,10210,10214), Deselect all]
    # actiontypes -> Predefined above: dictionary of legitimate actions
    # Example of actiontypes['Select'] = {'type':'sel','callback': set_coords},
    # atype -> type of a given action: I.e. Select, Hotkey Assign etc.
    # atype['type'] = 'sel'

    # use callbacks (mostly) to handle actions
    # AY: Note that actiontypes was declared above as a global dictionary
    # AY: awords[0] refers to the TYPE of action in a tick
    if awords[0] in actiontypes:
        # AY: atype will be the values associated with the now returned action type
        atype = actiontypes[awords[0]]

        action['type'] = atype['type']
        action['action'] = " ".join(awords[1:])

        if 'action' in atype:
            # AY: This line only applies to moves
            action['action'] = atype['action']
        if 'callback' in atype:
            # AY: How is callback useful? What do action/actionstr/awords
            action = atype['callback'](action, actionstr, awords)

    else:
        # by default we assume the action is an ability modification
        # AY: Does this always hold?
        action['type'] = 'a'
        action = extract_targets(action, actionstr, awords)

    return action

