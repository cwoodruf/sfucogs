#!/usr/bin/env python
"""
creates stripped down game sequences for each player
each of these is saved as a file and a shuffled version is saved
the files are compressed with gzip 
the original size and compressed size of each is saved along 
with the compression ratio to bfl_playerlevelgzip

2016-06-18: Cal changed all calls to save_games to save_gamestrs

"""
import subprocess
import pexpect
import platform
if platform.node() == 'bugaboo.westgrid.ca':
        import wgdb as bfldb
        import wgdb as testdb
else:
        import bfldb
        import testdb
import os
import sys
import re
import random
import zlib

verbose = False

# translate actiontype into single letter code
def_map = { 'sel':'s','seld':'d','rc':'R','tr':'T','a':'A','hk':'H','b':'b','m':'M',
        'atk':'k','mapAtk':'t','mapRCClick':'c','mapAbl':'l','ps':'p','f':'f','u':'u','Cancel':'n' }
def_accept = { 'sel':True,'rc':True,'tr':True,'a':True,'hk':True,'b':True,'m':True,
        'atk':True,'mapAtk':True,'mapRCClick':True,'ps':True }
# if a sequence of just this action is found only keep one instance from the sequence
def_agg = { 'hk':True,'m':True,'rc':True,'a':True,'tr':True } 

gzip = '/usr/bin/gzip'
if not os.path.isfile(gzip):
        print "can't find gzip!"
        sys.exit(1)

home = os.environ['PWD']
if home == None or home == '':
        print "can't find current directory"
        sys.exit(1)
if not os.path.isdir(home):
        print home,"is not a directory"
        sys.exit(1)

reload(sys)
sys.setdefaultencoding('utf8')
uconn = testdb.conn()
conn = bfldb.conn()

def scan_gzip_l(gzinfo):
        """
        read gzip info from gzip -l output 
        and turn it into a nice array
        """
        gz = re.search(r'\s*(\d+)\s*(\d+)\s*(\d+\.\d+)%', gzinfo)
        if gz == None:
                return (None, None, None)
        return gz.groups()

def gzip_file(pfile):
        """
        run gzip on a file and
        return stats from gzip -l
        """
        subprocess.call([gzip,'-f',pfile])
        zipped = "{}.gz".format(pfile)
        # this isn't working on PC3 - unable to write to stdout
        try:
                gzinfo = subprocess.check_output([gzip,'-l',zipped])
        except:
                gzinfo = pexpect.run("{} -l {}".format(gzip, zipped), logfile=sys.stdout)

        return scan_gzip_l(gzinfo)

def gzip_string(st, level=6):
        """
        using python gzip to zip a string
        find the space savings and return a tuple like gzip -l
        """
        if st == None or len(st) == 0: 
                return (None,None,None)
        if verbose: print "using compression level",level
        zipped = zlib.compress(st,level)
        lz = len(zipped)
        lst = len(st)
        saved = 100.0 * (1.0 - float(lz)/float(lst))
        return (lz, lst, saved)

def save_stats(gzstats, myconn=None, statstable='bfl_gamezips'):
        """
        save all the gzip information
        for one or more games
        """
        if myconn != None:
                save = myconn.cursor()
        else:
                myconn = uconn
                save = uconn.cursor()
        if verbose: print gzstats
        save.executemany(
            "replace into {} "
            "(playerid, gameid, player, "
            " path, compressed, uncompressed, ratio, "
            " shuffle_path, shuffle_compressed, shuffle_uncompressed, shuffle_ratio, gamestr) "
            "values "
            "(%s, %s, %s, "
            " %s, %s, %s, %s, "
            " %s, %s, %s, %s, %s) ".format(statstable),
            gzstats
        )
        save.close()

def save_shuffle(shufstats, myconn, statstable):
        """
        add on to save the shuffled string with the gamestr data for reproducablility analysis
        IMPORTANT: must be run after save_stats
        """
        if verbose: print shufstats
        try:
                save = myconn.cursor()
                save.executemany(
                    "update {} set shuffle_gamestr=%s "
                    "where playerid=%s and gameid=%s and player=%s".format(statstable),
                    shufstats
                )
                save.close()
        except Exception as e:
                print str(e)

def save_gamestrs(table, game, gamedata, myconn=None, statstable='bfl_gamezips', delim="",level=6):
        """
        create the gamestr field for each player and save the game into statstable
        use python gzip to do the gzip stuff instead of the gzip program
        level is the compression level for zlib
        """
        playerid = re.sub(r'.*_','',table)
        for p in gamedata:
                gamestr = delim.join(gamedata[p])
                gzdata = gzip_string(gamestr,level)
                shuffled = gamedata[p]
                random.shuffle(shuffled)
                shuffledstr = delim.join(shuffled)
                gzdatac = gzip_string(shuffledstr,level)
                save_stats([(playerid, game, p, "", gzdata[0], gzdata[1], gzdata[2], 
                                "", gzdatac[0], gzdatac[1], gzdatac[2], gamestr)], 
                                myconn, statstable)
                save_shuffle([(shuffledstr, playerid, game, p)], myconn, statstable)

def save_existing_gamestrs(playerid, game, gamedata, myconn=None, statstable='bfl_gamezips', delim="",level=6):
        """
        create the gamestr field for each player and save the game into statstable
        use python gzip to do the gzip stuff instead of the gzip program
        level is the compression level for zlib
        in this case don't create the shuffled string, used what you are given
        """
        for p in gamedata:
                gamestr = delim.join(gamedata[p]['unshuffled'])
                shuffledstr = delim.join(gamedata[p]['shuffled'])
                gzdata = gzip_string(gamestr,level)
                gzdatac = gzip_string(shuffledstr,level)
                save_stats([(playerid, game, p, "", gzdata[0], gzdata[1], gzdata[2], 
                                "", gzdatac[0], gzdatac[1], gzdatac[2], gamestr)], 
                                myconn, statstable)
                save_shuffle([(shuffledstr, playerid, game, p)], myconn, statstable)

def save_games(table, game, gamedata, myconn=None, statstable='bfl_gamezips', delim="\n"):
        """
        extract individual games to files
        """
        t = re.match(r'player_(\d+)', table)
        if t == None:
                playerid = '999'
                print "no playerid in table",table,"using",playerid
        else:
                playerid = t.group(1)
        gamedir = os.path.join(home,table,str(game))

        try:
                os.mkdir(gamedir)
        except:
                pass

        if not os.path.isdir(gamedir):
                print "missing game directory",gamedir
                sys.exit(1)

        print "using gamedir",gamedir
        for p in gamedata:
                pfile = u"player_{}.txt".format(p.encode('utf-8'))
                outpath = os.path.join(gamedir,pfile)
                print "saving",outpath
                with open(outpath, 'wb') as fh:
                        for l in gamedata[p]:
                                fh.write("{}{}".format(l,delim))
                gzdata = gzip_file(outpath)
                print outpath,gzdata

                pfile = u"player_{}_shuffled.txt".format(p.encode('utf-8'))
                outpathc = os.path.join(gamedir,pfile)
                with open(outpathc, 'wb') as fh:
                        randomized = gamedata[p]
                        random.shuffle(randomized)
                        for l in randomized:
                                fh.write("{}{}".format(l,delim))
                gzdatac = gzip_file(outpathc)
                print outpathc,gzdatac

                # in the future may want to do a bunch of inserts at once
                # hence the list
                save_stats([(playerid, game, p, outpath.encode('utf8'), gzdata[0], gzdata[1], gzdata[2], 
                                outpathc.encode('utf8'), gzdatac[0], gzdatac[1], gzdatac[2], gamedata[p])], 
                                myconn, statstable)

def save_existing_games(playerid, game, player, gamedata, myconn, statstable, delim=""):
        """
        run gzip -l on existing files generated by earlier runs of save_games
        """
        table = "player_{}".format(playerid)
        gamedir = os.path.join(home,table,str(game))

        try:
                os.mkdir(gamedir)
        except:
                pass

        if not os.path.isdir(gamedir):
                print "missing game directory",gamedir
                sys.exit(1)

        print "using gamedir",gamedir
        for p in gamedata:
                pfile = u"player_{}.txt.gz".format(p.encode('utf-8'))
                outpath = os.path.join(gamedir,pfile)
                gzdata = scan_gzip_l(subprocess.check_output([gzip,'-l',outpath]))
                print "existing",outpath,gzdata

                pfile = u"player_{}_shuffled.txt.gz".format(p.encode('utf-8'))
                outpathc = os.path.join(gamedir,pfile)
                gzdatac = scan_gzip_l(subprocess.check_output([gzip,'-l',outpathc]))
                print "existing shuffled",outpathc,gzdatac

                # in the future may want to do a bunch of inserts at once
                # hence the list
                save_stats([(playerid, game, p, outpath.encode('utf8'), gzdata[0], gzdata[1], gzdata[2], 
                                outpathc.encode('utf8'), gzdatac[0], gzdatac[1], gzdatac[2], gamedata[p])], 
                                myconn, statstable)

def scan_one_game(table,gameid,myconn,statstable='bfl_gamezips',props=None):
        """
        given a player table and gameid
        get all the game events for that player
        save and process files when the game number changes
        """
        print "scanning",table,"gameid",gameid
        get = myconn.cursor()
        get.execute(
            "select gameid, player, actiontype "
            "from {} "
            # what was originally used - note that ps won't exist in the data so we have no moves
            # "where actiontype in ('sel','rc','tr','a','h','b','ps','atk','mapAtk','mapRCClick') "
            "where actiontype in ('sel','rc','tr','a','hk','b','m','atk','mapAtk','mapRCClick','ps') "
            "and gameid = %s "
            "order by rowid "
            .format(table),
            (gameid,)
        )
        amap = def_map
        gamedata = {}
        game = None
        for row in get:
                if verbose: print row
                game, player, action = row
                if player not in gamedata:
                        gamedata[player] = []
                gamedata[player].append(amap[action])
        get.close()
        if len(gamedata) > 0 and game != None:
                print "saving"
                #save_games(table, game, gamedata, uconn, statstable)
                save_gamestrs(table, game, gamedata, uconn, statstable)
                return 1
        return 0

def scan_one_game_aggregate(table,gameid,myconn,statstable='bfl_gamezips',
        props=None,
        # which actions to aggregate
        agg = def_agg
):
        """
        given a player table and gameid
        get all the game events for that player
        save and process files when the game number changes
        aggregates actions when actiontype is 'hk','m','rc','a','tr'
        """
        get = myconn.cursor()
        get.execute(
            "select player, actiontype "
            "from {} "
            "where actiontype in ('sel','rc','tr','a','hk','b','m','atk','mapAtk','mapRCClick','ps') "
            "and gameid = %s "
            "order by rowid "
            .format(table),
            (gameid,)
        )
        # make actions single characters so compression matches behaviour of other sequencing scripts
        amap = def_map
        gamedata = {}
        prevaction = {}
        for row in get:
                player, action = row

                if player not in gamedata:
                        prevaction[player] = None
                        gamedata[player] = []

                if action in agg:
                        if prevaction[player] != action:
                                gamedata[player].append(amap[action])
                else:
                        gamedata[player].append(amap[action])

                prevaction[player] = action

        get.close()
        if len(gamedata) > 0:
                # given that all actions are single characters we don't want to use delimiters
                # save_games(table, gameid, gamedata, uconn, statstable, delim='')
                save_gamestrs(table, gameid, gamedata, uconn, statstable, delim='')
                return 1
        return 0

def scan_one_gamestr(playerid,gameid,myconn,statstable='bfl_gamezips_aggregate',props=None):
        """
        given a playerid and gameid get all game strings 
        then zip, shuffle and save results to stats table
        assumes gamestr in stats table has a valid game string in it
        generated by scan_one_game_aggregate
        """
        get = myconn.cursor()
        gamedata = {}
        get.execute(
            "select player,gamestr from {} where playerid=%s and gameid=%s".format(statstable),
            (playerid, gameid)
        )
        for row in get:
                player, gamestr = row
                gamedata[player] = gamestr
        get.close()
        if len(gamedata) > 0:
                save_existing_games(playerid, gameid, gamedata, myconn, statstable, delim='')
                return 1
        return 0

def update_cs_zipchar(table,myconn,rowid,zipchar):
        """
        show which actiontype got saved as what character
        in the original table - used later for identifying where repeated sequences show up
        """
        upd = myconn.cursor()
        upd.execute(
            "update {} set zipchar=%s where rowid=%s".format(table),
            (zipchar, rowid)
        )
        upd.close()

def scan_one_game_cs(table,gameid,myconn,statstable='bfl_gamezips',
        props=None,
        # which actions to aggregate
        agg = def_agg
):
        """
        given a table and gameid
        using a table schema like the CSCodingLevel tables in skillcraft_survey
        get all the game events for that game
        save and process files when the game number changes
        aggregate actions when actiontype is 'hk','m','rc','a','tr'
        update a zipchar field with the char actually used in the compression test

        takes updatezipchar (default True) and
        compressionlevel (compression level for zlib) as additional arguments
        """
        updatezipchar = True,
        compressionlevel = 6 # for zlib
        if props != None:
                if 'updatezipchar' in props: updatezipchar = props['updatezipchar']
                if 'compressionlevel' in props: compressionlevel = props['compressionlevel']
        print 'updatezipchar',updatezipchar,'compressionlevel',compressionlevel
        get = myconn.cursor()
        get.execute(
            "select actiontype, rowid "
            "from {} "
            "where actiontype in ('sel','rc','tr','a','hk','b','m','atk','mapAtk','mapRCClick','ps') "
            "and gameid = %s "
            "order by rowid "
            .format(table),
            (gameid,)
        )
        # make actions single characters so compression matches behaviour of other sequencing scripts
        amap = def_map
        print amap
        gamedata = {}
        prevaction = {}
        game = 'gameid_{}'.format(gameid)
        for row in get:
                action, rowid = row

                if game not in gamedata:
                        prevaction[game] = None
                        gamedata[game] = []

                if action in agg:
                        if prevaction[game] != action:
                                if updatezipchar: update_cs_zipchar(table,myconn,rowid,amap[action])
                                gamedata[game].append(amap[action])
                else:
                        if updatezipchar: update_cs_zipchar(table,myconn,rowid,amap[action])
                        gamedata[game].append(amap[action])

                prevaction[game] = action

        get.close()
        if len(gamedata) > 0:
                # given that all actions are single characters we don't want to use delimiters
                #save_games(table, gameid, gamedata, uconn, statstable, delim='')
                # assumes that table has the playerid 
                #save_gamestrs(table, gameid, gamedata, uconn, statstable, delim='')
                # add compression level so we can manipulate that as a variable
                save_gamestrs(str(game), gameid, gamedata, uconn, statstable, 
                                delim='', level=compressionlevel)
                return 1
        return 0

def scan_statstable(table,gameid,myconn,statstable='bfl_gamezips',props=None):
        """
        in this case we ignore table and grab gamestr and shuffle_gamestr
        from the stats table and recompress them using a given compression level
        """
        updatezipchar = True,
        compressionlevel = 6 # for zlib
        if props != None:
                if 'compressionlevel' in props: compressionlevel = props['compressionlevel']
        print 'compressionlevel',compressionlevel
        get = myconn.cursor()
        get.execute(
            "select playerid, gameid, player, gamestr, shuffle_gamestr "
            "from {} "
            "where gameid = %s "
            .format(table),
            (gameid,)
        )
        for row in get:
                playerid, gameid, player, gamestr, shuffle_gamestr = row
                gamedata = {player: {'shuffled': shuffle_gamestr,'unshuffled': gamestr}}
                save_existing_gamestrs(playerid, gameid, gamedata, myconn, statstable, 
                                delim='', level=compressionlevel)
        get.close()

def scan_one_table(
        table,
        myconn=None,
        statstable='bfl_gamezips',
        scanner=scan_one_game,
        props = None
):
        """
        given a player table name (player_NN form)
        or any other table with a set of games with distinct gameids
        get all games for that player/table and 
        process them using the scanner callback
        use props to configure the scanner callback
        """
        print "in table",table
        try:
                os.mkdir(table)
        except:
                pass

        if not os.path.isdir(table):
                print "missing directory",table
                sys.exit(1)

        playerid = None
        pr = re.match(r'.*_(\d+)', table)
        if pr != None:
                playerid = pr.group(1)
                print "playerid",playerid

        if myconn == None:
                myconn = conn
        get = myconn.cursor()
        get.execute(
            "select distinct gameid "
            "from {} "
            "order by gameid".format(table) 
        )
        newgamesonly = False
        visited = {}
        if props != None: 
                print "props",props
                if 'newgamesonly' in props:
                        newgamesonly = props['newgamesonly']
                        getnew = myconn.cursor()
                        if playerid != None:
                                getnew.execute("select gameid from {} where playerid=%s".format(statstable), (playerid,))
                        else:
                                getnew.execute("select gameid from {}".format(statstable))
                        print getnew._last_executed
                        for row in getnew:
                                gameid = float(row[0])
                                visited[gameid] = True
                        getnew.close()
        for row in get:
                gameid = row[0]
                if newgamesonly and gameid in visited and visited[gameid]: 
                        if verbose: print "skipping", gameid
                        continue
                scanner(table, gameid, myconn, statstable, props)
        get.close()

def scan_tables(firsttable=None,inreverse=False,props=None):
        """
        get a list of tables
        do the gzip process on each table
        this really should use the NODE / node in whoisfiles
        so we can parallelize things by player
        """
        if inreverse:
                print "in reverse"
        gettables = conn.cursor()
        gettables.execute(
            "show tables like 'player_%'"
        )
        tables = []
        start = False
        for row in gettables:
                table = row[0]
                if not start and firsttable != None and firsttable != table:
                        continue
                start = True
                tables.append(table)
        for table in tables:
                scan_one_table(table,props=props)

if __name__ == '__main__':
        verbose = False
        if len(sys.argv) > 1:
                if len(sys.argv) > 2:
                        inreverse = True if sys.argv[2] == 'reverse' else False
                        scan_tables(sys.argv[1], inreverse)
                else:
                        scan_tables(sys.argv[1])
        else:
                scan_tables(props={'newgamesonly': False})

