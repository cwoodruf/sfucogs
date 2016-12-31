#!/usr/bin/env python
"""
use a modified version of pyzip to capture 
compressed strings in games
placeholders for some actions in /home/csladmin/gzipgames
in ling-cogsci-pc1 c:\cygwin
this script is meant to be run like this:
find -name '*.gz' -exec ~/bin/get_gzipstrings.py {} \;
"""
import gzipstrings as gs
import json
import bfldb
import testdb
import sys
import re


filename = sys.argv[1]
input = open(filename)
field = gs.RBitfield(input)

magic = field.readbits(16)
chunks = None
if magic == 0x1f8b: # GZip
        chunks = gs.gzip_main(field)
else:
        raise "Unknown file magic "+hex(magic)+", not a gzip file"
input.close()

if chunks == None or len(chunks) == 0:
        print "no chunks for", filename
        sys.exit(0)

words = json.dumps(chunks, indent=4)
words = re.sub(r'\\n',' ',words)
print "filename",filename
print "chunks",words

conn = bfldb.conn()
saveconn = testdb.conn()
cur = saveconn.cursor()
cur.execute(
        "replace into bfl_gzipgamewords (filename, words) "
        "values (%s, %s) ",
        (filename, words)
)
cur.close()

for word, count in chunks.iteritems():
        word = re.sub(r"\n",' ',word)
        cur = conn.cursor()
        cur.execute(
                "select instances from bfl_gzipwords "
                "where word=%s ",
                (word,)
        )
        if cur.rowcount > 0:
                irow = cur.fetchone()
                instances = irow[0]
        else:
                instances = 0
        cur.close()
        instances += count
        print "instances", instances, "word", word 
        cur = saveconn.cursor()
        cur.execute(
                "replace into bfl_gzipwords (word, instances) "
                "values (%s, %s) ",
                (word, instances)
        )
        cur.close()

conn.close()
saveconn.close()
