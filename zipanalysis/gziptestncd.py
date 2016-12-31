#!/usr/bin/env python
"""
do a group of ncds on various shuffles 
generate average ncd and standard deviation
"""
# import testdb as db
import wgdb as db
import gzipncd as ncd
import zlib
import random
import time
import sys

UPD_COUNT = 1000

def update(ncdstats):
	"""
	save avg, std dev and count of ncd compression ncds
	"""
	if len(ncdstats) == 0: return
	print "saving"
	conn = db.conn()
	upd = conn.cursor()
	upd.executemany(
		"update {} set ncd_avg=%s, ncd_sd=%s, ncd_N=%s "
		"where playerid=%s and gameid=%s and player=%s ".format(statstable),
		ncdstats
	)
	upd.close()
	conn.close()
	

def ncd_sample(statstable, N=30):
	"""
	for a given table in the form of bfl_gamezips_aggregate
	ncd the gamestr field a number of times
	and calculate the compression ncd - in this case the space saved
	"""
	conn = db.conn()
	get = conn.cursor()

	get.execute(
		"select playerid,gameid,player,gamestr "
		"from {} "
		"where gamestr is not null and gamestr <> '' "
		"and ncd_avg is null "
		"order by playerid,gameid ".format(statstable)
	)
	ncdstats = []
	for row in get:
		playerid, gameid, player, gamestr = row
		start = time.clock()
		gamelist = list(gamestr)
		gamelen = float(len(gamestr)) 
		ncds = []
		s = 0.0
		ss = 0.0
		for i in xrange(N):
			random.shuffle(gamelist)
			# this is an approximation of Kolmogorov complexity 
			# it is a distance measure from the random string to the game string
			# comparing two shuffled strings of 119 characters is NCD of .7
			NCD = ncd.dist(gamestr, ''.join(gamelist))
			# print "len",len(compressed),"game",gamelen,"NCS",NCD
			ncds.append(NCD)
			s += NCD
			ss += NCD*NCD
		avg = s/N
		var = (ss - s*s/N)/(N - 1)
		if var > 0: sd = var**0.5
		else: sd = 0.0
		print ncds
		ncdstats.append((avg, sd, N, playerid, gameid, player))
		if len(ncdstats) >= UPD_COUNT:
			update(ncdstats)
			ncdstats = []
		elapsed = time.clock() - start
		print "elapsed",elapsed,"avg",avg,"sd",sd,"N",N,"for",playerid,gameid,player
	get.close()
	update(ncdstats)
	conn.close()

if __name__ == '__main__':
	statstable = sys.argv[1]
	ncd_sample(statstable)
 
