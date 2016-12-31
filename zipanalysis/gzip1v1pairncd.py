#!/usr/bin/env python
"""
find the NCD for pairs of players who played together in games
idea is to see how coordinated their activity is
"""
# import testdb as db
import wgdb as db
import gzipncd as ncd
import sys

def update(ncds, statstable, conn):
	"""
	save a group of ncds to the table at once
	"""
	if len(ncds) == 0: return
	print "saving",len(ncds),"NCD values to",statstable
	upd = conn.cursor()
	upd.executemany(
		"update {} set ncd=%s "
		"where playerid=%s and gameid=%s ".format(statstable),
		ncds
	)
	upd.close()

def calculate(statstable):
	"""
	do the ncd distance calculation on pairs of 
	gamestr values for a given table
	"""
	conn = db.conn()
	get = conn.cursor()
	get.execute(
		"select playerid,gameid,gamestr1,gamestr2 "
		"from {} "
		"where gamestr1 is not null "
		"and gamestr2 is not null "
		"and ncd is null "
		"order by playerid, gameid ".format(statstable)
	)
	ncds = []
	for row in get:
		playerid, gameid, gamestr1, gamestr2 = row
		d = ncd.dist(gamestr1, gamestr2)
		ncdrow = (d, playerid, gameid)
		print ncdrow
		ncds.append(ncdrow)
	get.close()
	update(ncds, statstable, conn)
	conn.close()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		for statstable in sys.argv:
			calculate(statstable)
	else:
		calculate('bfl_1v1_gamestr_pairs')

