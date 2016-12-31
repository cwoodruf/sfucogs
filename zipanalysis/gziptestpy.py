#!/usr/bin/env python
"""
run python's version of compress on the gamestr field
for a table and save the resulting space savings in 
the ratio_python field for comparison with mysql and 
the gzip program
"""
# import testdb as db
import wgdb as db
import zlib
import sys

UPD_COUNT = 1000

def save(ratios, statstable):
	"""
	save a group of ratios to ratio_python in the given
	statstable
	"""
	if len(ratios) == 0: return
	print "saving"
	conn = db.conn()
	upd = conn.cursor()
	upd.executemany(
		"update {} set ratio_python=%s "
		"where playerid=%s and gameid=%s and player=%s ".format(statstable),
		ratios
	)
	upd.close()
	conn.close()

def process(statstable):
	"""
	scan the statstable for non-null gamestr fields
	calculate the space savings of compressing them using
	zlib.compress(gamestr, 6) then save the result in
	ratio_python
	"""
	conn = db.conn()
	get = conn.cursor()
	get.execute(
		"select playerid,gameid,player,gamestr,uncompressed "
		"from {} "
		"where gamestr is not null "
		"order by playerid, gameid ".format(statstable)
	)
	ratios = []
	for row in get:
		playerid, gameid, player, gamestr, uncompressed = row
		compressed = float(len(zlib.compress(gamestr, 6)))
		gamelen = float(len(gamestr))
		if gamelen != uncompressed:
			raise Exception("gamelen {} uncompressed {}".format(gamelen, uncompressed))
		saved = 100.0 * (1.0 - compressed/gamelen)
		r = (saved, playerid, gameid, player)
		print r
		ratios.append(r)
		if len(ratios) > UPD_COUNT:
			save(ratios, statstable)
			ratios = []
	get.close()
	save(ratios, statstable)
	conn.close()

if __name__ == '__main__':
	statstable = sys.argv[1]
	process(statstable)
