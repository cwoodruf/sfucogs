#!/usr/bin/env python
"""
find all the shuffled data and add it to the shuffle_gamestr field
for a given table 
"""
import testdb as db
import sys
import os
import gzip

def scan_shuffled(table):
        """
        given a table name try and grab the data from the shuffle_path
        file and put it in shuffle_gamestr
        not all of the *_gamezips tables have filled in shuffle_path
        """
        print "table",table
        conn = db.conn()
        get = conn.cursor()
        get.execute(
            "select shuffle_path, gameid, playerid, player "
            "from {} "
            "where shuffle_path <> '' "
            "and shuffle_gamestr is null "
            "order by playerid, gameid, player ".format(table)
        )
        for row in get:
                print row
                shuffle_path, gameid, playerid, player = row
                with gzip.open(shuffle_path, 'rb') as fh:
                        shuffle_gamestr = fh.read()
                        print "updating"
                        upd = conn.cursor()
                        upd.execute(
                            "update {} set shuffle_gamestr=%s where gameid=%s and playerid=%s and player=%s".format(table),
                            (shuffle_gamestr, gameid, playerid, player)
                        )
                        upd.close()
        get.close()
        conn.close()


if __name__ == '__main__':
        scan_shuffled(sys.argv[1]);
