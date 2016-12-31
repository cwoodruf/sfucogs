#!/usr/bin/env python
"""
save time by putting the uncompressed gzip string 
in the bfl_gamezips_aggregate table.

this will scan a directory produced by gzipgames-aggregate.py and 
imput the uncompressed data to the corresponding bfl_gzipgames_aggregate
row for later processing.

the rationale is that we want to be able to do calculations of mutual
information for larger arrays of events and the db makes this doable
on westgrid.
"""
import testdb as db
conn = db.conn()

import gzip
import sys
import os
import re

reload(sys)
sys.setdefaultencoding('utf8')

ext = '.txt.gz'
shufext = '_shuffled.txt.gz'
maxlen = 0
gamestrings = []
UPD_COUNT = 100

def save():
        """
        save a group of gamestr fields together to save time
        """
        global gamestrings
        if len(gamestrings) == 0: return
        print "saving"
        upd = conn.cursor()
        upd.executemany(
            "update bfl_gamezips_aggregate "
            "set gamestr=%s "
            "where playerid=%s and gameid=%s and player=%s",
            gamestrings
        )
        upd.close()
        gamestrings = []

def step(ext, dirname, names):
        """
        for any non-shuffled txt.gz file record the 
        related record for bfl_gamezips_aggregate
        save using save() in groups
        """
        global maxlen
        pg = re.match(r'.*player_(\d+)/(\d+)', dirname)
        if pg == None: return
        playerid, gameid = (pg.group(1), pg.group(2))
        for name in names:
                if not name.endswith(ext): continue
                if name.endswith(shufext): continue
                n = re.match(r'player_(.*).txt.gz', name)
                if n == None: continue
                player = n.group(1)
                gzfile = os.path.join(dirname, name)
                with gzip.open(gzfile, 'rb') as gh:
                        gamestr = gh.read()
                        if len(gamestr) > maxlen: maxlen = len(gamestr)
                        print "playerid",playerid,"gameid",gameid, \
                                        "player",player,"maxlen",maxlen
                        gamestrings.append((gamestr, playerid, gameid, player))
                        if len(gamestrings) >= UPD_COUNT:
                                save()

os.path.walk(sys.argv[1], step, ext)
save()
conn.close()

