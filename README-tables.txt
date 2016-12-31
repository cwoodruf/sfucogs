INTRODUCTION

There are two main databases used for bfl analysis:

bfl - aggregate statistics, game data, survey data and player data

bfl_parsing - mostly player game events tables

These are mirrored in the cwoodruf@bugaboo.westgrid.ca account as cwoodruf_bfl
and cwoodruf_bfl_parsing. The bugaboo dbs are only available via ssh login to
that account.

Most of the tables in these databases are source data for the bfl_master and sc2survey
tables. These data sources should be kept as a record of what was processed to 
generate the final tables.

The databases have text backups on cwoodruf@bugaboo.westgrid.ca:~/data
and on Ling-CogSci-PC1 in /home/csladmin/ (from the cygwin prompt). 

===============================================================================
BFL 

The main copy of bfl is found on cslab.psyc.sfu.ca. The backup is 
cwoodruf_bfl on cwoodruf@bugaboo.westgrid.ca.

The main tables used are:

* bfl_master 
   statistical analysis of respondent behaviour for specific games
   (key: playerid, gameid) 

* bfl_gamelevel 
   source of game data used to generate bfl_master
   (keys: playerid, gameid; rowid) 

* bfl_playerlevel 
   source of player data used to generate bfl_master
   (key: playerid, gameid, gamerowid) 

* whoisfiles 
   documents game replays
   (keys: fid; player, game - same as playerid and gameid) 


* whois 
   table of players mapped to surveys 
   contains json survey data
   (key: player - equivalent to playerid) 

* sc2survey 
   split out survey responses
   (key: survey, respondent; player - equivalent to playerid) 

Note that in some cases player refers to the charactername (bfl_master 
and bfl_playerlevel) and sometimes refers to the player number generated earlier 
for each replay donor (whois and whoisfiles).

-------------------------------------------------------------------------------
Other tables in bfl: (*s indicate tables specifically relevant to bfl_master/sc2survey)

 _p_42 - player game action table with some data from player 42
 _whois_20160211 - obsolete back up of whois
 badlength - list of player games with invalid lengths in whoisfiles

 bfl_actioncounts - counts game actions per game
 bfl_actionpropcounts - flattened game action counts
 bfl_actionprops - proportions of game actions
 bfl_gamelevel - ** key table for generating bfl_master
 bfl_gamezips - older obsolete gzip data
 bfl_gamezips_aggregate - newer gzip data without confounds
 bfl_gzipgamewords - test of words generated from bfl_gamezip data split out by game
 bfl_gzipgamewords_aggregate - test of words generated from bfl_gamezip_aggregate data
 bfl_gzipwords - test of words generated from bfl_gamezip data
 bfl_gzipwords_aggregate - test of words generated from bfl_gamezip_aggregate
 bfl_master - *** master statistics table based on respondent game play
 bfl_playeractioncounts - counts of game actions per player per game
 bfl_playeractionpropcounts - flattened version of bfl_playeractioncounts
 bfl_playeractionprops - proportions of bfl_playeractionpropcounts
 bfl_playerlevel - ** key table used to generate bfl_master
 bfl_top99pctile - who played in the most games

 foldernaminglog - based on the text file in Parsing/FolderNamingLog mapping players to folders

 lime_answers - maps survey answer codes to actual strings
 lime_assessments
 lime_conditions
 lime_defaultvalues
 lime_expression_errors
 lime_failed_login_attempts
 lime_groups
 lime_labels
 lime_labelsets
 lime_old_survey_142181_20130304115623
 lime_old_survey_142181_20130304121903
 lime_old_survey_142181_20130304122723
 lime_old_survey_164172_20130304114109
 lime_participant_attribute
 lime_participant_attribute_names
 lime_participant_attribute_names_lang
 lime_participant_attribute_values
 lime_participant_shares
 lime_participants
 lime_question_attributes
 lime_questions - maps question numbers to actual questions
 lime_quota
 lime_quota_languagesettings
 lime_quota_members
 lime_saved_control
 lime_sessions
 lime_settings_global
 lime_survey_142181 - * actual survey responses (source for sc2surveys)
 lime_survey_164172
 lime_survey_286538
 lime_survey_333639 - * actual survey responses (source for sc2surveys)
 lime_survey_435536
 lime_survey_435536_timings
 lime_survey_446632 - * actual survey responses (source for sc2surveys)
 lime_survey_623295
 lime_survey_754839
 lime_survey_785323
 lime_survey_791296
 lime_survey_links
 lime_survey_permissions
 lime_survey_url_parameters
 lime_surveys
 lime_surveys_languagesettings
 lime_templates
 lime_templates_rights
 lime_tokens_286538
 lime_tokens_435536
 lime_tokens_791296
 lime_user_groups
 lime_user_in_groups
 lime_users

 player_109 - test game events data for player 109
 player_42 - test game events data for player 42

 sc2survey - ** amalgamated survey data
 sc2survey_schema - describes how to process the survey json data to make sc2survey

 template_chatlevel - empty template for chat data (copy of bfl_parsing table)
 template_replaylevel - empty template for player_% or _p_% tables in this db (copy of bfl_parsing table)

 whois - ** main map of players to surveys and donated files
 whois_20160415 - back up of whois missing survey_json
 whoischatfound - which chat files were processed
 whoisdates - ** comparison of dates in whoisfiles (actual file, sc2gears and sc2reader)
 whoiseventsfound - list of all game events files with statistics
 whoiseventsused - * list of events files that are actually used
 whoisfiles - ** contains a list of all donated files, game info, errors and test results for each
 whoisfiles_20160415 - backup of whoisfiles
 whoismissing - list of which players were missing replays
 whoisrawlogs - contains all zip and rar files including test uploads
 whoisrenamedfound - all game events files that were processed on bugaboo
 whoisrenamedused - * game events files used to make bfl_parsing.player_% tables
 whoisrenaminglogs - goes with foldernaming log: all renamed files on bugaboo
 whoisreparsed - raw replays that were rerun through sc2gears to check for errors
 whoisreparsedfailed - reparsed replays sc2gears gave errors on
 whoisuniquereplays - list of unique replays based on whoisfiles.raw_sha1 checksums

===============================================================================
BFL_PARSING 

The main copy of bfl_parsing is found on Ling-CogSci-PC2 and is
replicated on all Ling-CogSci-PC hosts and cwoodruf_bfl_parsing on bugaboo.

The main tables in this database are the player_% tables where % is the player
number (player or playerid in the bfl tables above). These tables contain only
games where bfl.whoisfiles.testpassed = 1. All data was generated by 
eventparse.py and checked using eventparsetest.py.

While there were players numbered 0 to 129 some player numbers are missing so 
code like:

  for player in xrange(130):

will not work like expected.

The all_players table is an enumeration of every player in every donated game.
Other tables are either test data generated by txtparse.m or copies of bfl tables.

Check copied tables to make sure they are up to date before using them for real analysis.

-------------------------------------------------------------------------------
Other tables in bfl_parsing:

 all_players - list of all 120,000+ players seen in the game data
 bfl_actioncounts - copy of bfl table
 bfl_gameleve - copy of bfl table
 bfl_gamezip - copy of bfl table
 bfl_gzipgameword - copy of bfl table
 bfl_gzipword - copy of bfl table  
 bfl_master - copy of bfl table 
 bfl_master_20160428_no_playerid - copy of bfl table 
 bfl_master_duplicate_sha1s - copy of bfl table 
 bfl_playerlevel - copy of bfl table 

 eventdata_player_101 - test game event table generated by txtparse.m
 eventdata_player_104 - test game event table generated by txtparse.m
 eventdata_player_118 - test game event table generated by txtparse.m
 eventdata_player_42 - test game event table generated by txtparse.m
 eventdata_player_72 - test game event table generated by txtparse.m
 eventdata_player_73 - test game event table generated by txtparse.m
 eventdata_player_74 - test game event table generated by txtparse.m
 eventparse_player_0 - test game event table generated by eventparse.py
 eventparse_player_118 - test game event table generated by eventparse.py
 eventparse_player_42 - test game event table generated by eventparse.py
 eventparse_player_57 - test game event table generated by eventparse.py
 eventparse_player_58 - test game event table generated by eventparse.py
 eventparse_player_73 - test game event table generated by eventparse.py
 games - list of games (empty)
 oddchars_eventdata_player_57 - test of using varchar for unicode fields (didn't work)

 player_0 - all game events for all games donated by player(id) 0 
            (and 108 tables similarly named for other players)

 sc2survey - copy of bfl table
 sc2survey_schema - copy of bfl table
 table2player - map of player number to player table

 template_chatlevel - template for chat tables
 template_replaylevel - template of all player_% tables

 test_74 - test table generated by txtparse.m
 test_replaylevel - test of template_replaylevel

 whois - copy of bfl table
 whois_20160429 - copy of bfl table
 whoisdates - copy of bfl table
 whoisfiles - copy of bfl table

