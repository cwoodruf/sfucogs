#!/usr/bin/env python
"""
Test NCD for games from one player - should these be correlated?
"""
# import testdb as db
import wgdb as db
import gzipncd as ncd
import sys
import re
import math
reload(sys)
sys.setdefaultencoding('utf8')
verbose = False

def measure(player, N, statstable):
	"""
	finds all the games for a specific player
	using sampling without replacement
	measures one NCD for half of the games 
	vs the other half for that player
	"""
	conn = db.conn()
	get = conn.cursor()
	get.execute(
		"select gameid, gamestr from {} "
		"where player=%s and gamestr is not null "
		"order by rand() limit {} ".format(statstable, N*2),
		(player,)
	)
	if get.rowcount < N*2:
		N = math.floor(get.rowcount/2)
	halves = []
	games = []
	count = 1
	for row in get:
		games.append(row[1])
		if count % N == 0:
			halves.append(''.join(games))
			games = []
		count += 1
	
	get.close()
	conn.close()
	NCD = ncd.dist(halves[0],halves[1])

	if verbose:
		print "player",player,"N",N,"count",count,"NCD: avg",avg,"var",var,"sd",sd
	return (NCD, len(halves[0]), len(halves[1]))

def scan_players(N,statstable):
	"""
	look for players with N*2 games
	measure the average NCD for each and print them out
	"""
	conn = db.conn()
	get = conn.cursor()
	get.execute(
		"select player from {} "
		"where gamestr is not null "
		"group by player "
		"having count(*) >= {} "
		"order by count(*) desc ".format(statstable, N*2)
	)
	ncds = []
	for row in get:
		player = row[0]
		NCD, len1, len2 = measure(player, N, statstable)
		ncds.append((player,NCD,len1,len2))
	print re.sub(r'[\[\]]','',str(ncds)),";"
	get.close()
	conn.close()
				
if __name__ == '__main__':
	player = sys.argv[1]
	N = 30
	statstable = 'bfl_gamezips_aggregate'

	if len(sys.argv) > 2:
		N = int(sys.argv[2])
		if len(sys.argv) > 3:
			statstable = sys.argv[3]

	if player == '':
		print "replace into bfl_self_ncds (player,ncd,len1,len2) values "
		scan_players(N, statstable)
	else:
		measure(player, N, statstable)

		

