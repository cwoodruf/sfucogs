#!/usr/bin/env python
"""
runs the gzipping test on a group of games from 
skillcraft_survey.CSCodingLevel23 not specially prepared 
in this case we are saving the encoded character with the game
event data to, we hope, match up with what was grabbed by gzip as a redundant seqence
"""
import gzipgames as gg
import testdb
skconn = testdb.conn(d='bfl')
gg.scan_one_table('comparecs23',skconn,'comparecs23_gamezips',gg.scan_one_game_cs)
skconn.close()
