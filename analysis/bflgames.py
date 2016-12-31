"""
manages game metadata
knows how to get a list of games for a specific player
for each game manages how to access the data
"""
import re

verbose = False

class Game:
        """
        holds metadata for a specific game and player
        """
        def __init__(self, id, player, gamemeta, playermeta, filemeta):
                self.id = id
                self.player = player
                self.table = player.table(gamemeta)
                self.gamemeta = gamemeta
                self.filemeta = filemeta
                self.set_playermeta(playermeta)

        def set_playermeta(self, rows):
                """
                read through all player rows for this game and
                make sense of who is doing what
                """
                teams = {}
                for row in rows:
                        if row['Team'] not in teams:
                                teams[row['Team']] = []
                        teams[row['Team']].append(row)

                        if row['Player'] == self.player.name:
                                self.playermeta = row
                myteam = self.playermeta['Team']
                self.playermeta['team_size'] = len(teams[myteam])
                races = {}
                for team, players in teams.iteritems():
                        if team not in races:
                                races[team] = []
                        for player in players:
                                races[team].append(player['Race'][0])
                self.playermeta['races'] = races
                self.teams = teams
                
        def events(self, conn):
                """
                gets actual game data for this game
                sets self.events, assumes tables always ordered by RowID
                """
                getevents = conn.cursor()
                getevents.execute(
                        self.evtquery()
                )
                if verbose: print getevents._last_executed
                self.events = list(getevents)
                getevents.close()

                # for filtering actions we sometimes need more than the actiontype
                # also want to calculate latency
                prev = None
                for i in xrange(len(self.events)):
                        evt = self.events[i]
                        self.events[i]['prev'] = prev
                        self.events[i]['combined'] = "{} {}".format(evt['ActionType'], evt['Action'])
                        self.events[i]['short_action'] = re.sub(
                                r'\[(Queued|Toggle|Autocast|Wireframe(Click|Cancel|Unload))\]\s*',
                                '',
                                self.events[i]['Action'])
                        if prev is not None: 
                                self.events[i]['prevts'] = prev['TimeStamp']
                                self.events[i]['latency'] = evt['TimeStamp'] - prev['TimeStamp']
                        else: 
                                self.events[i]['prevts'] = 0
                                self.events[i]['latency'] = evt['TimeStamp']
                        # for identifing when pacs start
                        prev = evt

                return self.events

        def evtquery(self):
                """
                run an id query for this particular player
                and game
                """
                return self.player.evtquery(self)

        def __str__(self):
                return "Game id {} table {}\ngamemeta {}\nplayermeta {}\nfilemeta {}\nplayer {}\nteams {}\n".format(
                        self.id, self.table, self.gamemeta, self.playermeta, self.filemeta, self.player, self.teams)
        
class Games:
        """
        manage a list of game objects for a specific player
        """
        def __init__(self, controller, player):
                """
                uses controller to generate a series of games
                relating to a specific player identified by player
                builds the self.games member from this data
                """
                self.player = player
                self.playermeta = player.playermeta
                self.gameidfield = self.playermeta.gamelevel['idfields']['gameid']
                conn = controller.db.dictconn()
                playerget = conn.cursor()
                playerget.execute(
                        player.allgamesquery()
                )
                self.games = []
                for playerrow in playerget:
                        gameid = playerrow[self.gameidfield]
                        gameget = conn.cursor()
                        gameget.execute(
                                player.gamequery(gameid)
                        )
                        gamerow = gameget.fetchone()
                        # we don't assume there will always be a second table with game data
                        filequery = player.filequery(gameid)
                        if filequery is not None:
                                gameget.execute(filequery)
                                filerow = gameget.fetchone()
                        else:
                                filerow = None
                        playerrows = []
                        gameget.execute(
                                player.playerquery(gameid)
                        )
                        for playerrow in gameget:
                                playerrows.append(playerrow)
                        self.games.append(Game(gameid, player, gamerow, playerrows, filerow))
                        gameget.close()
                playerget.close()
                conn.close()

        def __iter__(self):
                """
                for situations where we are trying to reel off games in a for loop
                """
                for game in self.games:
                        yield(game)

