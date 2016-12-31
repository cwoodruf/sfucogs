#!/usr/bin/env python
"""
runs the gzipping test on a group of games from 
skillcraft prepared specially to only have the
400 actions around the 10 minute mark
"""
import gzipgames as gg
import testdb
skconn = testdb.conn(d='skillcraft_survey')
gg.scan_one_table('CalsStarSequences',skconn,'CalsStarSequencesZipStats_aggregate',gg.scan_one_game_aggregate)
skconn.close()
