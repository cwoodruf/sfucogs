#!/usr/bin/env python
"""
using gzipstrings (hack of pyflate), get a list of literals vs chunks
then line these up with the data in comparecs23 to identify where the
chunks show up in the game events
note that this will only work on Ling-CogSci-PC1 using the cygwin prompt
"""
import gzipstrings
import testdb
import os
import sys
from collections import deque

conn = testdb.conn()
get = conn.cursor()
get.execute(
    "select rowid, gameid, zipchar from comparecs23 "
    "order by rowid "
)
prevgameid = -1.0
prevchar = None
for row in get:
        rowid, gameid, zipchar = row
        if gameid != prevgameid:
                prevgameid = gameid
                prevchar = None
                filename = os.path.join(
                            os.environ['HOME'],
                            'comparecs23_gamezips',
                            'comparecs23',
                            str(gameid),
                            'player_gameid_{}.txt.gz'.format(gameid)
                        )
                print filename
                if not os.path.isfile(filename):
                        print "does not exist"
                        sys.exit(1)
                gzipstrings.verboselist = True
                chars = gzipstrings.gunzip_file(filename)
                cq = deque(chars)
        
        # check if we need to look at the next character in the chars list
        if zipchar == None:
                pass
        elif zipchar.isupper():
                # upper case means the action represents a group of repeated actions
                # if we are at the start of the sequence, get the next char dict
                if zipchar != prevchar:
                        # without deque can also do chars.pop(0) but this is less memory efficient
                        c = cq.popleft()
        else:
                c = cq.popleft()

        prevchar = zipchar

        print row, c, prevchar
        if zipchar != None and zipchar != c['zipchar']:
                print "got",zipchar,"from db but gzipstrings is",c
                sys.exit(2)
        
        put = conn.cursor()
        put.execute(
            "update comparecs23 "
            "set zipchar=%s, zipoffs=%s, zipseq=%s "
            "where rowid=%s ",
            (c['zipchar'], c['offset'], c['zipseq'], rowid)
        )
        put.close()
get.close()


