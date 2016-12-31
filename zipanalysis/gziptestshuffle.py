#!/usr/bin/env python
"""
do a group of shuffles and zip each
generate average compression ratio and standard deviation
"""
# import testdb as db
import wgdb as db
import zlib
import random
import time
import sys

UPD_COUNT = 1000

def update(ratiostats):
	"""
	save avg, std dev and count of shuffle compression ratios
	"""
	if len(ratiostats) == 0: return
	print "saving"
	conn = db.conn()
	upd = conn.cursor()
	upd.executemany(
		"update {} set shuffle_ratio_avg=%s, shuffle_ratio_sd=%s, shuffle_ratio_N=%s "
		"where playerid=%s and gameid=%s and player=%s ".format(statstable),
		ratiostats
	)
	upd.close()
	conn.close()
	

def shuffle_sample(statstable, N=30):
	"""
	for a given table in the form of bfl_gamezips_aggregate
	shuffle the gamestr field a number of times
	and calculate the compression ratio - in this case the space saved
	"""
	conn = db.conn()
	get = conn.cursor()

	get.execute(
		"select playerid,gameid,player,gamestr "
		"from {} "
		"where gamestr is not null and gamestr <> '' "
		"and shuffle_ratio_avg is null "
		"order by playerid,gameid ".format(statstable)
	)
	ratiostats = []
	for row in get:
		playerid, gameid, player, gamestr = row
		start = time.clock()
		gamelist = list(gamestr)
		gamelen = float(len(gamestr)) 
		ratios = []
		s = 0.0
		ss = 0.0
		for i in xrange(N):
			random.shuffle(gamelist)
			compressed = zlib.compress(''.join(gamelist), 6)
			# this is actually the space savings according to wikipedia (Data compression ratio)
			ratio = 100.0 * (1.0 - float(len(compressed))/gamelen)
			# print "len",len(compressed),"game",gamelen,"ratio",ratio
			ratios.append(ratio)
			s += ratio
			ss += ratio*ratio
		avg = s/N
		var = (ss - s*s/N)/(N - 1)
		if var > 0: sd = var**0.5
		else: sd = 0.0
		print ratios
		ratiostats.append((avg, sd, N, playerid, gameid, player))
		if len(ratiostats) >= UPD_COUNT:
			update(ratiostats)
			ratiostats = []
		elapsed = time.clock() - start
		print "elapsed",elapsed,"avg",avg,"sd",sd,"N",N,"for",playerid,gameid,player
	get.close()
	update(ratiostats)
	conn.close()

if __name__ == '__main__':
	statstable = sys.argv[1]
	shuffle_sample(statstable)
 
