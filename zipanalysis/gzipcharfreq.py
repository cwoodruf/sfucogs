#public/projects/Starcraft/BFL/LocalParsing/bin gzipCharFreq.py
"""
July 28th 2016
Script to compare character frequencies between gamestr and shuffle_gamestr
in comparecs23_gamezips, bfl_gamezips and bfl_gamezips_aggregate tables.

Used for verification purposes to confirm that shuffling retains action counts (which are 
represented by characters)

Adam Bignell - (Let it be known that I'm learning MySQL as I write this Script
so if there are obvious changes that could be made, they are more than welcome)
"""

# based on 'bfldb' I assume that this imports the BFL SQL database?
#import platform
#if platform.node() == 'bugaboo.westgrid.ca':
#         import wgdb as bfldb
#         import wgdb as testdb
#else:
#         import bfldb
#         import testdb

# Does this connect us to the database we previous imported?
#
# Cal - yes; note you want to make sure you are connecting to the db with the table you are interested in
#            that probably won't be bfldb which has all the player tables on the windows network
#

db = bfldb.conn()
get = db.cursor()
get.execute(
	# MySQL code in double quotes is executed as a MySQL query?
    #
    # Cal - yes; consider making the table a user supplied parameter
    #
	# "select gamestr, shuffle_gamestr from comparecs23_gamezips"
	)

# I'm not sure exactly how this works, but from your scripts it appears that
# the return from the above query is stored in a list that I can iterate through
#
# Cal - yes, have a look at the "yield" keyword
#

# The following code assumes I have an n X 2 array where n refers to number of games
# and 2 refers to gamestr, shuffle_gamestr that I attempted to pull above
for row in get:
	flag = 0
	chardict = {}
	shuffchardict = {}
	for str in row:
		#Variable used to check if the two dictionaries match
		identity = False
		actionList = []
		discrepencyList = []
		# if we are on the first column, add to first dictionary
		if (flag == 0):
			for char in str:
				chardict[char] += 1
				actionList.append(char)
		# if we are on the second column, add to the second dictionary
		if (flag == 1):
			for char in str:
				shuffchardict[char] += 1
			# we can check the identity only after completing the entries
			# in the second dictionary
			for action in actionList:
				if (chardict[action] ==  shuffchardict[action]):
					identity = True
				else:
					identity = False
					discrepencyList.append[action]

		# this allows our flag to switch from 0 to 1 only
		flag = (flag + 1) % 2

		if (!identity):
			# It would make sense to also return the game number in the above SQL query
			# so that we can print precisely which games have discrepencies
			# but I don't fully understand the SQL stuff yet so I have ommitted that for now
            #
            # Cal - perhaps it might be a good idea to add a flag field in each table you check so we can more quickly find wonky records
            #       there is at least one wonky record in one of the tables
            #
			print("\n gamestr and shuffled gamestr do not have the same frequencies of these characters \n")
			print discrepencyList



