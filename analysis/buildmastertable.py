#!/usr/bin/env python
"""
This script initates the build of the master table 
as defined in template_master.mysql in this directory.
Based on public/projects/Starcraft/MasterTableBuilderBFL_Final.m

Idea is to make an extensible framework for these types of tables.
So each field is encapsulated in a class which determines its SQL
properties as well as how to build the field data.

Fields can be text, counts, means or standard deviations. Combining
related measures in a single class would make sense.

Because python is viewing source data row-wise it may be important that
the field data constructors be able to update themselves on the fly.
In other words the classes would hold data primitives that are then
transformed as needed into the data they represent.
"""
from pacshift import PACMeta

# this represents metadata from a game
import bflgames

# this manages class definitions for the fields used in the master table
# it also contains a map of how those fields are represented by objects
import bflmaster

# to get game event tables, gameids, playerids and player names
import bflplayers

import sys
import platform
import time

if platform.node() == 'bugaboo.westgrid.ca':
	import wgdb as db
else:
	import bfldb as db

class MasterBuilder:
	"""
	class that builds a master table from 
	game and player metadata and event tables
	"""
	def __init__(self, db, mastertb, playermeta, pacmeta):
		"""
		gamestb, playerstb both refer to metadata tables
		for games and players 
		"""
		self.tables = {}
		self.db = db
		self.tables['master'] = mastertb
		self.playermeta = playermeta
		self.pacmeta = pacmeta
		self.master = bflmaster.Master(self)
                self.start = time.time()

	def add_game(self,game):
		"""
		Given eventstb the game events table,
		the mastertb master table and
		a game metadata object gameinfo
		create db row for that game using the 
		master fields classes
		"""
		self.master.add(game, self.start)

	def create_master(self,players):
		"""
		Given the list of players from init
		grab a list of games for each player
		add each game in turn to the master table

		players is a list of player objects used to find
		it should include the game identifiers for games
		which could be compound identifiers 
		and the tables in which to find the games
		"""
		self.players = players
		for player in self.players:
			games = bflgames.Games(self,player)
			for game in games:
                                self.start = time.time()
				self.add_game(game)
                                print "game processing elapsed time", (time.time() - self.start)

	def master_from_playerids(self, playerids=None):
		"""
		use full list of players to make a master table
		playermeta is an object that contains information
		on how to create a player list 
		"""
		players = bflplayers.Players(self.db, playerids, self.playermeta)
		self.create_master(players)

if __name__ == '__main__':
	builder = MasterBuilder(
		db, 'bfl_master_test', 
		bflplayers.bfl_playermeta, 
		PACMeta(dispersion=6, duration=20)
	)
	builder.master_from_playerids(playerids=[29,50])

