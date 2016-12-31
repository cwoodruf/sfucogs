#!/usr/bin/env python
"""
finds games that got missed by gzipgames.py
processes each game in turn
"""
import bfldb
import gzipgames 
import eventparse
import os

conn = bfldb.conn()
games = conn.cursor()
games.execute(
    "select player,game from whoisfiles "
    "where gzip is null"
)
for gamerow in games:
        player, game = gamerow
        table = eventparse.get_table(player)
        if not os.path.isdir(table):
                os.mkdir(table)
        ret = gzipgames.scan_one_game(table,game,conn,statstable='bfl_gamezips')
        save = conn.cursor()
        save.execute(
            "update whoisfiles set gzip=%s where player=%s and game=%s",
            (ret, player, game)
        )
        save.close()
games.close()
conn.close()

