#!/usr/bin/env python
"""
library to replicate behaviour of matlab script txtparse.m
see txtparse function below for starting point
instead of saving data to a file save it directly into mysql

see also eventparseutils.py for event processing callback
functions used by this module

Date: Sat Apr  9 16:49:11 2016
Author: Cal Woodruff cwoodruf@sfu.ca

Reviewed: Yue Chen & Adam Bignell, August 5 2016

Verified:
"""
import sys
import re
import os
# import bfldb
import wgdb as bfldb
import eventparseutils as epu

###############################################################################
# data is saved as it is parsed to a table for each player as identified by
# their player number

tables = {} # declare tables as a dictionary

def get_table(player):
    """
    player event data is stored in individual tables
    for each player (note: these tables can be huge)

    this function finds out if we have a table for a given player
    if so return that table name
    if not make a new table and return the name
    """
    global tables

    # AY: Why is this part of this function. Doesn't this populate tables?
    if len(tables) == 0: # AY: If no tables
        conn = bfldb.conn() # AY: connect python to MySQL
        cur = conn.cursor() # AY: create cursor for "conn" connection
        cur.execute("show tables like 'player_%'") # AY: return all the player_% tables
        for row in cur:
            t = row[0] # AY: What is the 0th element of a given row?? It appears to be player #
            m = re.match(r'player_(\d+)', t)
            if m == None:
                # print "odd table name",t
                continue
            p = m.group(1) # AY: P is now a string of the form "player_%"
            tables[p] = t # AY: If above holds, set the value in table[player_%] to t
        cur.close()
        conn.close()
        # print tables

    if player in tables:
        return tables[player] # AY: If the desired player table is in tables, return it
    conn = bfldb.conn()
    cur = conn.cursor()
    table = "player_{}".format(player) # AY: String formatting to create string "player_%"
    try:
        cur.execute("create table {} (like template_replaylevel)".format(table)) # AY: See above
    except Exception as e:
        sys.stderr.write("table create error: {}\n".format(e))
    cur.close()
    conn.close()
    tables[player] = table # Return the table now inserted into "tables"
    return table

def delete_events(table, game, conn):
    """
    removes a game from a table in
    preparation for the game being 
    reloaded into the table from a file
    """

    # AY: What is the motivation for deleting a game from a table: To empty the table if txt.parse failed?
    try:
        cur = conn.cursor()
        cur.execute("delete from {} where gameid=%s".format(table), (game,))
    except Exception as e:
        sys.stderr.write("error in delete_events: {}\n".format(e))

def insert_events(table, events, conn):
    """
    inserts a group of events all at once
    using the mysqldb built in function executemany
    the cost of setting up the insert can often
    outstrip the actual cost of inserting the data
    """
    try:
        cur = conn.cursor()
        # AY: Insert into a supplied table using a list "events" which contains events for "timeStamp" time (?)
        # AY: This all looks good
        cur.executemany(
            "insert into {} " 
            "(GameID, ScreenX, ScreenY, TimeStamp, Player, "
            "ActionType, Action, Target, ActionX, ActionY, Queued, "
            "errors, actionstr) "
            " values "
            "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ".format(table),
            events
        )
        cur.close()
        return True
    except Exception as e:
        sys.stderr.write("error in insert_events: {}\n".format(e))
        return False

def txtparse(f, gameid, table):

    """
    this is the main driver function for parsing events files
    it reads text output from an already open file handle f
    then saves the data to a given table
    the idea is that players have at least one table each

    this function is not specific to sc2gears and could be 
    adapted to work with other replay extracting tools that
    extract replay data as strings

    the exact table definition can be found in template_replaylevel
    in the bfl_parsing database or the template_replaylevel.mysql 
    script (which should be in the same directory as eventparse.py)

    """ 
    try:
        conn = bfldb.conn()
    except Exception as e:
        sys.stderr.write("DB connect failed: {} parsing to STDOUT\n".format(e))
        table = None
        # a hack to get with to work below
        # AY: What does the above mean?
        conn = open(".eventparse.tmp","w")

    with conn:
        delete_events(table, gameid, conn)
        with f:
            # initialize
            previous_player = "";
            # where each player is
            players = {}
            # list of events
            events = []
            # number of events to accumulate before doing an insert
            EVENT_THRESHOLD = 1000
    
            lcount = 0
            # AY: For line in file
            for l in f:
                lcount += 1
                if lcount <= 2: continue
                # test without tables
                if table == None:
                   print l
                try:
                    action = epu.extract_action(l)

                    # AY: If we don't know who did the action, set coordinates to 0
                    if action['player'] not in players:
                        players[action['player']] = {'x': 0, 'y': 0}

                    # AY: If action is move, if move is valid, set to where the move was to
                    if action['type'] == 'm':
                        # some of the move actions have no coordinates ...
                        # txtparse.m changes these to 0 s
                        if action['x'] == -1 or action['y'] == -1:
                            players[action['player']] = {'x': 0, 'y': 0}
                        else:
                            players[action['player']] = {'x': action['x'], 'y': action['y']}

                        # AY: Does this indicate that the move has been prcessed? Why do we set them to -1?
                        action['x'] = -1.0 
                        action['y'] = -1.0

                    # AY: Is this equivalent to error handling?
                    if table == None:
                        print "gameid", gameid,"previous_player",previous_player
                        print "players", players
                        print "action", action
                    else:
                        events.append(
                            (gameid, players[action['player']]['x'], players[action['player']]['y'],
                                    action['tick'], action['player'], action['type'], 
                                    action['action'][:100], action['target'], 
                                    action['x'], action['y'], action['queued'], 
                                    action['errors'], action['actionstr'])
                        )
                        if len(events) >= EVENT_THRESHOLD:
                            ret = insert_events(table, events, conn)
                            # AY: Unload all our events
                            events = []
                            if ret == False:
                                sys.exit(1)

                    # AY: What is the relevance of this? Don't we immediately undo it on the next iteration?
                    previous_player = action['player'];

                except Exception as e:
                        sys.stderr.write("error processing {} : {}\n".format(l,e))

            # make sure to insert stragglers
            insert_events(table, events, conn)

def save_game(player, game, events_path):
        """
        given a player number, game number and 
        path to the sc2gears parsed events
        save everything to the player's table 
        """
        if not os.path.isfile(events_path):
            sys.stderr.write("save_game events_path missing {} \n".format(events_path))
            return

        with open(events_path,'rb') as fh:
            table = get_table(player)
            txtparse(fh, game, table)
    
###############################################################################
# test code

if __name__ == '__main__':
    # test code:

    # always assume we have an events text file for test processing
    with open(sys.argv[1], 'rb') as f:

        # check for specially formatted player game files
        g = re.match(r'.*?Player_(\d+)_Game_(\d+)', sys.argv[1])

        if not g == None:
            # test using file name as guide to player, game 
            player = g.group(1)
            game = g.group(2)
            table = get_table(player)
            print "saving game",game,"for player",player,"to table",table
            txtparse(f, game, table)
        else:
            # test with any file
            if len(sys.argv) > 2 and len(sys.argv[2]) > 0:
                print "saving data to table", sys.argv[2]
                try:
                    g = int(sys.argv[3])
                    print "game",g
                    txtparse(f, g, sys.argv[2], )
                except:
                    txtparse(f, 999999999, sys.argv[2])
            else:
                    txtparse(f, 999999999, None)

