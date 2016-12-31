#!/usr/bin/env python
"""
runs pacshift on games assigned to a specific node
where this node is identified by a unique integer from 0 to 4 inclusive
the node number in os.environ['NODE'] maps to a node field in bfl.whoisfiles

process is that each instance of nodepacs.py grabs a list of files to 
process from whoisfiles and forks off processes to parse them

Date: 2016-09-25
Author: Cal Woodruff cwoodruf@sfu.ca
Reviewed: 
Verified:

"""
import testdb, bfldb
from pacshift import PACShift, PAC
import json
import os
import sys
import datetime
import time
import multiprocessing as mp
import traceback

schema = 'pacs_simple'
THREAD_COUNT = 11;
home = os.environ['HOME']
node = os.environ['NODE']
outtables = {}

def savepacs(pacout, outtable, conn):
        """
        save a bunch of pacs to a db table like template_pacs 
        """
        if len(pacout) == 0: return

        print "saving ",len(pacout),"pacs to",outtable
        put = conn.cursor()
        put.executemany(
                format(PAC.insert_statement(outtable, schema)),
                pacout
        )
        put.close()
        conn.commit()

def pacshifts_from_replay(row, conn, whoisfilesconn):
        """
        runs a game in a player table through pacshift
        """
        # need to do this to have coherent output see 
        # http://stackoverflow.com/questions/3029816/how-do-i-get-a-thread-safe-print-in-python-2-6
        player, gameid = row
        startstamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        sys.stdout.write("{} player {} game {}\n".format(startstamp,player,gameid))

        try:
                pacout = []
                outtable = "player_{}_pacs".format(player)
                try:
                        if outtable not in outtables:
                                mktb = conn.cursor()
                                mktb.execute("create table {} (like template_{})".format(outtable, schema))
                                mktb.close()
                                outtables[outtable] = True
                except:
                        pass

                table = "player_{}".format(player)
                print "processing player",player,"gameid",gameid,"saving to",outtable,"getting from",table
                getplayers = conn.cursor()
                getplayers.execute(
                        "select distinct player "
                        "from {} where GameID=%s".format(table),
                        (gameid,)
                )
                print getplayers._last_executed
                for playerrow in getplayers:
                        print playerrow
                        character = playerrow['player']
                        getactions = conn.cursor()
                        getactions.execute(
                                "select * "
                                "from {} "
                                "where GameID={} and Player='{}' "
                                "order by RowID, TimeStamp "
                                " ".format(table, gameid, character)
                        )
                        print getactions._last_executed
                        events = list(getactions)
                        try:
                                pac = PACShift(dispersion=6, duration=20)
                                pac.generate_stats(events)
                                print "found",len(pac.pacs),"pacs out of",len(events),"events"

                                for p in pac.pacs:
                                        print "key (pacord, player, gameid)",p.pacord,p.player,p.gameid
                                        print p.row(schema)
                                        pacout.append(p.row())
                                        if len(pacout) > 100:
                                                savepacs(pacout, outtable, conn)
                                                pacout = []
                                savepacs(pacout, outtable, conn)
                                pacout = []
                                 
                                finishcur = whoisfilesconn.cursor()
                                finishcur.execute(
                                        "update bfl.whoisfiles set processed=now() where player=%s and game=%s", 
                                        (player, gameid)
                                )
                                finishcur.close()
                        except Exception as e:
                                sys.stdout.write("generate_stats error: {}\n".format(e))
                                traceback.print_tb(sys.last_traceback)

                        try:
                                getactions.close()
                        except:
                                pass
                getplayers.close()
        except Exception as e:
                sys.stderr.write("player {} game {} error: {}\ntraceback:\n{}\n".format(
                        player,gameid,e,traceback.format_exc()))

def process_jobs(jobs):
        """
        should be run in its own thread
        players should only use one thread to avoid interleaving the rowids for games
        (more of a nuisance than a real problem probably)
        """
        conn = bfldb.dictconn()
        whoisfilesconn = testdb.conn()
        for row in jobs:
                pacshifts_from_replay(row, conn, whoisfilesconn)

def get_games(node):
        """
        gets the games for this node and start threads 
        to process them
        threads are allocated work based on the player
        this may result in a somewhat uneven workload
        """
        global THREAD_COUNT
        print "we are node", node
        conn = testdb.conn()
        get = conn.cursor()
        get.execute(
            "select distinct player, game "
            "from bfl.whoisfiles "
            "where node=%s "
            "and testpassed=1 "
            "and processed is null "
            "order by player, game "
            ,(node,)
        )
        # find all games for a given player
        gamelist = []
        games = 0
        for row in get:
                player, game = row
                # print player, game
                # assign games to threads based on the player
                gamelist.append((player, game))
                games += 1
        get.close()
        conn.close()
        
        # try and split jobs equally for each thread
        joblists = []
        maxjobs = int(games/THREAD_COUNT)
        startjob = 0
        for i in range(THREAD_COUNT):
                # print startjob,startjob+maxjobs
                joblists.append(gamelist[startjob:startjob+maxjobs])
                # print gamelist[startjob:startjob+maxjobs]
                startjob += maxjobs

        joblists.append(gamelist[startjob:])

        threads = []
        for i, jobs in enumerate(joblists):
                t = mp.Process(
                                 target=process_jobs,
                                 name='playergroup{}'.format(i),
                                 kwargs={'jobs':jobs})
                print "starting", t
                t.start()
                threads.append(t)

        for t in threads:
                t.join()


if __name__ == '__main__':
        # find all games for this node
        get_games(node)

