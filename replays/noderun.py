#!/usr/bin/env python
"""
runs eventparse on games assigned to a specific node
where this node is identified by a unique integer from 0 to 4 inclusive
the node number in os.environ['NODE'] maps to a node field in bfl.whoisfiles

process is that each instance of noderun.py grabs a list of files to 
process from whoisfiles and forks off processes to parse them

the number of processes is configurable on the command line

Reviewed: Adam Bignell, September 1, 2016
"""
import testdb
import eventparse as ep 
import os
import sys
import subprocess
import datetime
import time
import threading

# lock = threading.Lock()

THREAD_COUNT = 12;
home = os.environ['HOME']
node = os.environ['NODE']

# for relative paths in whoisfiles
parsebase = os.path.join(home,'Parsing')
if not os.path.isdir(parsebase):
        raise(Exception("{} is not a directory".format(parsebase)))

def import_replay(row):
        """
        runs an sc2gears parsed game replay file through eventparse
        """
        player, game, events_file = row
        startstamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        start = time.time()
        # need to do this to have coherent output see 
        # http://stackoverflow.com/questions/3029816/how-do-i-get-a-thread-safe-print-in-python-2-6
        sys.stdout.write("{} player {} game {} events_file {}\n".format(startstamp,player,game,events_file))

        if events_file[0] == '/':
                events_path = events_file
        else:
                events_path = os.path.join(parsebase,events_file);

        ep.save_game(player, game, events_path)

        conn = testdb.conn()
        tag = conn.cursor()
        tag.execute(
             "update whoisfiles set processed=now() where player=%s and game=%s",
             (player, game)
        )
        tag.close()
        endstamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        end = time.time()
        elapsed = end - start
        sys.stdout.write("{} player {} game {} elapsed {} seconds\n".format(endstamp,player,game,elapsed))

def process_jobs(jobs):
        """
        should be run in its own thread
        players should only use one thread to avoid interleaving the rowids for games
        (more of a nuisance than a real problem probably)
        """
        for row in jobs:
                import_replay(row)

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
            "select distinct player, game, events_path "
            "from whoisfiles "
            "where node=%s and sc2gears_errors is null and processed is null "
            "order by player, game "
            ,(node,)
        )
        # find all games for a given player
        gamelist = []
        games = 0
        for row in get:
                player, game, events_file = row
                # assign games to threads based on the player
                gamelist.append((player, game, events_file))
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
                startjob += maxjobs

        joblists.append(gamelist[startjob:])

        threads = []
        for i, jobs in enumerate(joblists):
                t = threading.Thread(
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

