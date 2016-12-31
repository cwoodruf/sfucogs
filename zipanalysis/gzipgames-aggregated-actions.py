#!/usr/bin/env python
"""
finds games that got missed by gzipgames.py
processes each game in turn
"""
import bfldb as db
import gzipgames 
import eventparse
import os
import sys

if len(sys.argv) > 1 and sys.argv[1] == 'reverse':
        orderby = "order by player desc, game desc "
        print "going backwards"
else:
        orderby = "order by player, game"

conn = db.conn()
games = conn.cursor()
games.execute(
    "select player,game from whoisfiles "
    "where gzip is null and testpassed=1 and game_linecount > 3000 "
    "{}".format(orderby)
)
for gamerow in games:
        player, game = gamerow
        table = eventparse.get_table(player)
        if not os.path.isdir(table):
                os.mkdir(table)
        ret = gzipgames.scan_one_game_aggregate(table,game,conn,statstable='bfl_gamezips_aggregate')
        save = conn.cursor()
        save.execute(
            "update whoisfiles set gzip=%s where player=%s and game=%s",
            (ret, player, game)
        )
        save.close()
games.close()
conn.close()

