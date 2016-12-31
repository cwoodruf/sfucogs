#!/usr/bin/env python
"""
runs the gzipping test on a group of games from 
skillcraft_survey.CSCodingLevel23 not specially prepared 
in this case we are saving the encoded character with the game
event data to, we hope, match up with what was grabbed by gzip as a redundant seqence
in this case we use data generated for comparecs23_gamezips_compressionlevel9
that was copied to two other tables and rerun the zip on the given gamestr and
shuffle_gamestr fields with different compression levels to see the effects
this has to be done for the default compression level (which was what was checked initially) 
as I foolishly did not record the shuffled string

note that scan_statstable expects an existing stats table with gamestr data in it already
the library reinserts the data so its not super efficient but that probably doesn't matter
"""
import gzipgames as gg
import wgdb as testdb
skconn = testdb.conn(d='cwoodruf_bfl')
gg.verbose = True
gg.scan_one_table(
    'comparecs23_gamezips_compressionlevel9',
    skconn,
    'comparecs23_gamezips_compressionlevel9',
    gg.scan_statstable,
    { 'compressionlevel': 9 }
)
gg.scan_one_table(
    'comparecs23_gamezips_compressionlevel6',
    skconn,
    'comparecs23_gamezips_compressionlevel6',
    gg.scan_statstable,
    { 'compressionlevel': 6 }
)
gg.scan_one_table(
    'comparecs23_gamezips_compressionlevel1',
    skconn,
    'comparecs23_gamezips_compressionlevel1',
    gg.scan_statstable,
    { 'compressionlevel': 1 }
)
skconn.close()
