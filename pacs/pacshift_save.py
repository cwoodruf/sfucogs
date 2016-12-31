#!/usr/bin/env python
"""

purpose of this script is to create a series of pac shifts 
from the 3200 games in CSCodingLevel in skillcraft_survey
it saves the data as a table of pac shift objects along with strings 
of the pac actions in the pac shift

run with --help to get command line options

"""
import argparse
from pacshift import PACShift, PAC
import gzipgames
import testdb as db
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')

def getsave(database, table, outtable, dispersion, duration, display=True, schema='pacs_simple'):
        """
        scan table for all games
        make a table of pacs for each, or display them, or both
        """
        conn = db.conn(d=database)
        dictconn = db.dictconn(d=database) # get rows with field names
        try:
                createtb = conn.cursor()
                createtb.execute('create table {} (like template_{})'.format(outtable, schema))
                createtb.close()
        except Exception as e:
                print "{}: {}".format(outtable, e)

        def savepacs(pacout):
                """
                save a bunch of pacs to a db table like template_pacs 
                """
                if len(pacout) == 0: return

                print "saving ",len(pacout),"pacs to",outtable
                put = conn.cursor()
                put.executemany(
                        format(PAC.insert_statement(outtable, schema)),
                        pacout
                )
                put.close()
                conn.commit()

        getgames = conn.cursor()
        getgames.execute("select distinct player,gameid from {} order by gameid, player".format(table))
        """
        # some test examples
        getgames = [('Itchy','457'),('dave','6'),('Zone','5'),('Veritas','5')]
        """

        pacout = []
        for gamerow in getgames:
                player, gameid = gamerow
                print "processing player",player,"gameid",gameid
                getactions = dictconn.cursor()
                getactions.execute(
                        "select * "
                        "from {} "
                        "where Player=%s and GameID=%s "
                        "order by RowID, TimeStamp "
                        " ".format(table),
                        (player, gameid)
                )
                events = list(getactions)

                pac = PACShift(dispersion, duration)
                pac.generate_stats(events)

                print "found",len(pac.pacs),"pacs out of",len(events),"events"

                for p in pac.pacs:
                        print "key (pacord, player, gameid)",p.pacord,p.player,p.gameid
                        print p.row(schema=schema)
                        pacout.append(p.row())
                        if len(pacout) > 100:
                                savepacs(pacout)
                                pacout = []
                savepacs(pacout)
                pacout = []
                 
                try:
                        getactions.close()
                except:
                        pass

        try:
                getgames.close()
                conn.close()
                dictconn.close()
        except:
                pass

if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Build pac data from a table of replay data')
        parser.add_argument('--db', nargs=1, default=['skillcraft_survey'], help='database')
        parser.add_argument('--table', nargs=1, help='replay table', required=True)
        parser.add_argument('--schema', nargs=1, help='output table schema - '
                                        '"template_{schema}" table used to make output table', 
                                        default=['pacs_simple'])
        parser.add_argument('--dispersion',type=int, default=[6], help='dispersion for IDT - typically 6 or 7')
        parser.add_argument('--duration',type=int, default=[20], help='duration for IDT - typically 20 or 40')
        args = vars(parser.parse_args())

        database = args['db'][0]
        table = args['table'][0]
        schema = args['schema'][0]
        outtable = "{}_{}".format(table, schema)
        dispersion = args['dispersion'][0]
        duration = args['duration'][0]
        print "using","db",database, "table",table, "out table", outtable, \
                "IDT dispersion and duration settings:", dispersion, duration

        getsave(database, table, outtable, dispersion, duration, display=True)

