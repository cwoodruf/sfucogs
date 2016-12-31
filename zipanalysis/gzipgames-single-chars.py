#!/usr/bin/env python
"""
processes each game in turn
saves un-aggregated string representing that game to statstable
as well as some basic gzip data
"""
# import bfldb as db
# tabledb = 'bfl_parsing'
import wgdb as db
tabledb = 'cwoodruf_bfl_parsing'
import gzipgames 
import eventparse
import os
import sys

conn = db.conn()
games = conn.cursor()
games.execute(
    "select player,game from whoisfiles "
    "where gzip is null and testpassed=1 and game_linecount > 3000 "
)
for gamerow in games:
        player, game = gamerow
        table = eventparse.get_table(player)
	# instead of aggregating this version saves every action - but as a single character
	# now, by default we don't save anything to the file system - hopefully faster
        ret = gzipgames.scan_one_game_aggregate(
		"{}.{}".format(tabledb,table),
		game,
		conn,
		statstable='bfl_gamezips',
		agg={}
	)
        save = conn.cursor()
        save.execute(
            "update whoisfiles set gzip=%s where player=%s and game=%s",
            (ret, player, game)
        )
        save.close()
games.close()
conn.close()

