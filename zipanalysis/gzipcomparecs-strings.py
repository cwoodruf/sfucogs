#!/usr/bin/env python
"""
scan the comparecs23 table and look for 1,2,2 ... patterns 
in the zipseq column and 2,1,1 ... patterns in the CSCoding column
save the values of zipchar as a string in comparecs23_strings
identify which string is present in a group of rows using the
comparecs23_strings.sid in the zipstring and CSstring columns
Note that the zipstring ignores capitalized actions after the first
so that the actual compressed string can be compared over different
length instances of that string in the actual data
"""
import wgdb as db
sids = {}
maxsid = 0

def load_sids(conn):
	"""
	fills the sids dict with previous data from comparecs23_strings
	"""
	global sids
	global maxsid
	getsids = conn.cursor()
	getsids.execute(
		"select sid, word, source "
		"from comparecs23_strings "
		"order by sid "
	)
	sids['zip'] = {}
	sids['cs'] = {}
	for row in getsids:
		sid, word, source = row
		sids[source][word]
		maxsid = sid
	getsids.close()

def tag_string(conn, source, word, rows):
	"""
	insert or update string in comparecs23_strings
	tag all relevant comparecs23 rows with the sid 
	"""
	global maxsid
	global sids

	print source, word
	print rows
	# we have to ignore zip length differences as we are 
	# saving the compressed version of the string to see 
	# what the actual strings look like uncompressed
	if source == 'cs' and len(word) != len(rows):
		raise "ERROR: lengths don't match!"
	if len(rows) == 0:
		return	
	if word not in sids[source]:
		maxsid += 1
		sids[source][word] = maxsid
		sid = maxsid
		# for some reason this statement never resulted in the db updating the table?
		# instead printed these out and updated table manually via the mysql client
		# see comparecs23_strings-inserts.mysql in ~/data
		print "({},'{}','{}'),".format(sid,source,word)
		put = conn.cursor()
		put.execute(
			"insert into comparecs23_strings (sid,word,source) values (%s,%s,%s)",
			(sid, word, source)
		)
		put.close()
	else:
		sid = sids[source][word]
	rowids = []
	for rowid in rows:
		rowids.append((sid, rowid))
	upd = conn.cursor()
	upd.executemany(
		"update comparecs23 set {}=%s where rowid=%s".format(
			'csstring' if source == 'cs' else 'zipstring'
		), rowids
	)
	upd.close()


def scan_and_tag():
	"""
	read through comparecs23 and find/save strings
	run tag_string when a new string is found
	"""
	conn = db.conn()
	load_sids(conn)

	get = conn.cursor()
	get.execute(
		"select rowid, cscoding, zipseq, zipchar "
		"from comparecs23 "
		"order by rowid "
	)

	cscollect = False
	csstr = ''
	csrows = []
	zipcollect = False
	zipstr = ''
	zipprevchar = ''
	zipprevseq = None
	ziprows = []

	for row in get:
		rowid, cscoding, zipseq, zipchar = row

		if cscoding == 2:
			tag_string(conn,'cs',csstr,csrows)
			cscollect = True
			csstr = ''
			csrows = []
		elif cscoding != 1:
			cscollect = False

		if zipseq == 1 and zipprevseq != 1:
			tag_string(conn,'zip',zipstr,ziprows)
			zipcollect = True
			zipstr = ''
			zipprev = ''
			ziprows = []
		elif zipseq == 0:
			zipcollect = False
		
		if cscollect:
			csstr += zipchar
			csrows.append(rowid)

		if zipcollect:
			if zipchar.isupper():
				if zipprev != zipchar:
					zipstr += zipchar
			else:
				zipstr += zipchar
			ziprows.append(rowid)
			zipprev = zipchar

		zipprevseq = zipseq
		
	get.close()
	tag_string(conn,'zip',zipstr,ziprows)
	tag_string(conn,'cs',csstr, csrows)
	conn.close()

if __name__ == '__main__':
	scan_and_tag()

