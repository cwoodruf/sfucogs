"""
manage access to player ids
and lists of players to process
defines bfl_playermeta for use in locating bfl players
"""

# some bfl specific callbacks for accessing tables
# used by PlayerMeta object bfl_playermeta
def bfl_table(player, game):
	"""
	how to identify an events table in bfl
	"""
	return "player_{}".format(player.id)

def bfl_allplayersquery(level):
	playeridfield = level['idfields']['playerid']
	playerfield = level['idfields']['player']
        if 'playerids' in level and len(level['playerids']) > 0:
                return "select {},{} from {} where {} in ({}) order by {}".format(
                                playeridfield, 
                                playerfield, 
                                level['table'], 
                                playeridfield, 
                                ','.join([str(pid) for pid in level['playerids']]), 
                                playeridfield
                        )
	return "select {},{} from {} order by {}".format(
		playeridfield, playerfield, level['table'], playeridfield)
	
def bfl_allgamesquery(player, level):
	playeridfield = level['idfields']['playerid']
	playerfield = level['idfields']['player']
	return "select * from {} where {}='{}' and {}='{}' order by GameID ".format(
		level['table'], 
		playerfield, player.name,
		playeridfield, int(player.id)) 

def bfl_gamequery(player, level, gameid):
	playeridfield = level['idfields']['playerid']
	gameidfield = level['idfields']['gameid']
	return "select * from {} where {}='{}' and {}='{}'".format(
		level['table'], 
		playeridfield, int(player.id), 
		gameidfield, int(gameid))

def bfl_filequery(player, level, gameid):
	playeridfield = level['idfields']['playerid']
	gameidfield = level['idfields']['gameid']
	return "select game_lasttick from {} where {}='{}' and {}='{}'".format(
		level['table'], 
		playeridfield, int(player.id), 
		gameidfield, int(gameid))

def bfl_playerquery(player, level, gameid):
	playeridfield = level['idfields']['playerid']
	playerfield = level['idfields']['player']
	gameidfield = level['idfields']['gameid']
	return "select * from {} where {}='{}' and {}='{}'".format(
		level['table'],
		playeridfield, int(player.id), 
		gameidfield, int(gameid))

def bfl_evtquery(player, level, game):
	"""
	in the events table how to find the 
	game events
	"""
	playerfield = level['idfields']['player']
	gameidfield = level['idfields']['gameid']
	return "select * from {} where {}='{}' and {}='{}' order by RowID".format(
		player.table(),
		playerfield, player.name, 
		gameidfield, int(game.id))

# class definitions
class PlayerMeta:
	"""
	keeps track of how we identify groups of players of interest
	"""
	# add gamelevel and playerlevel tables here?
	def __init__(self, allplayers, allgames, 
                        playerlevel, gamelevel, filelevel, eventlevel):
		# where to get game metadata
		self.allplayers = allplayers
		self.allgames = allgames
		self.playerlevel = playerlevel
		self.gamelevel = gamelevel
		self.filelevel = filelevel
		self.eventlevel = eventlevel

	def __str__(self):
		return "allplayers {}\nallgames {}\n" \
		       "playerlevel {}\ngamelevel {}\nfilelevel {}\neventlevel{}\n".format(
				self.allplayers, self.allgames,
				self.playerlevel, self.gamelevel, 
				self.filelevel, self.eventlevel)

class Player:
	"""
	identifies a specific player
	"""
	def __init__(self, playerid, playername, playermeta):
		self.id = playerid
		self.name = playername
		self.playermeta = playermeta

	def __str__(self):
		return "Player id {} name {} playermeta {} ".format(
				self.id, self.name, self.playermeta)

	def allgamesquery(self):
		"""
		gets all games for this player
		"""
		level = self.playermeta.allgames
		cb = level['cb']
		return cb(self, level)

	def playerquery(self, gameid):
		"""
		find all the players for a game
		"""
		level = self.playermeta.playerlevel
		cb = level['cb']
		return cb(self, level, gameid)

	def gamequery(self, gameid):
		"""
		query to find game metadata
		from a gamelevel table
		"""
		level = self.playermeta.gamelevel
		cb = level['cb']
		return cb(self, level, gameid)

	def filequery(self, gameid):
		"""
		query to find game metadata
		in a table like whoisfiles
		"""
		level = self.playermeta.filelevel
		cb = level['cb']
		return cb(self, level, gameid)

	def evtquery(self, game):
		"""
		finds game actions in a game event table
		"""
		level = self.playermeta.eventlevel
		cb = level['evtcb']
		return cb(self, level, game)

	def table(self, game=None):
		"""
		get the table name for game events for this player
		"""
		level = self.playermeta.eventlevel
		cb = level['tablecb']
		return cb(self, game)

class Players:
	"""
	generate and manage a list of player character names
	using data from a playermeta instance
	"""
	def __init__(self, db, playerids, playermeta):
		"""
		get a map of player ids and names from table
		"""
                self.playerids = playerids
		self.playermeta = playermeta
		self.db = db
		self.set_players()

	def allplayersquery(self):
		"""
		use callback defined in playermeta to generate query
		to get all players
		"""
		level = self.playermeta.allplayers
		cb = level['cb']
                level['playerids'] = self.playerids
		return cb(level)

	def set_players(self):
		"""
		generate a list of playerid, player name pairs
		this could change depending on how players are identified
		"""
		conn = self.db.conn()
		get = conn.cursor()
		get.execute(self.allplayersquery())
		self.players = []
		for row in get:
			id, name = row
			self.players.append(Player(id, name, self.playermeta))
		
	
	def __iter__(self):
		for player in self.players:
			yield(player)


# define more of these as needed for other master tables
# provides specifics on how to access database tables to get player and game data
bfl_playermeta = PlayerMeta(
	allplayers={'table':'whois','cb':bfl_allplayersquery,
		'idfields':{'playerid':'player','player':'canonical'}}, 
	allgames={'table':'bfl_playerlevel','cb':bfl_allgamesquery,
		'idfields':{'playerid':'PlayerID','player':'Player'}},
        playerlevel={'table': 'bfl_playerlevel', 'cb': bfl_playerquery, 
		'idfields':{'playerid':'PlayerID','gameid':'GameID','player':'Player'}},
	gamelevel={'table': 'bfl_gamelevel', 'cb': bfl_gamequery, 
		'idfields':{'playerid':'PlayerID','gameid':'GameID'}},
	filelevel={'table': 'bfl_filelevel', 'cb': bfl_filequery, 
		'idfields':{'playerid':'player','gameid':'game'}},
	eventlevel={'tablecb': bfl_table, 'evtcb': bfl_evtquery, 
		'idfields':{'playerid':'PlayerID','gameid':'GameID','player':'Player'}}
)

