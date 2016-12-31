INTRODUCTION

Most of the scripts in this directory were used to 
analyze the sc2 game replay files donated by starcraft II players
in 2013 and 2014 to the SFU Cognitive Sciences lab. These
replays were accompanied by questionnaire responses from 
approximately 130 players. For analysis only games played by
players with questionnaire responses were used.

There were a number of issues found during processing:
- No clear indication of which player donated which replay set
- Redundant replays (i.e. players donating the same game twice)
- Replays that could not be parsed with our parsing tools (sc2gears)
- The sheer size of the dataset (over 180,000 games originally)

These issues were addressed by:
- generating a db table (whois) to map players to replays
- generating sha1 checksums to identify redundant games (whoisfiles.raw_sha1)
- running sc2reader to identify the superset of potentially parseable games
  independently of sc2gears
- reextracting replays that either failed to parse with sc2gears 
  or were believed to be truncated
- testing replay data after it was imported into a database
- parallelizing data processing on our local network

OVERVIEW OF STEPS

surveys & replay data 
  L_> extraction of game events & game info to files
       L_>  import of file data to database tables
             L_> statistical analysis of game events & game info

NETWORK ENVIRONMENT

For processing, the small lab subnet of Dell computers was used.
These are identified locally as Ling-CogSci-PC1, Ling-CogSci-PC2, 
Ling-CogSci-PC3 and Ling-CogSci-PC4. The Ling-CogSci-PC1 server
is a 64 bit machine with 8 processors and 8GB ram. The others 
are 32 bit machines with 4 processors and 4GB ram. Some additional
processing and database mirroring were done in the cwoodruf
account on bugaboo.westgrid.ca

One part of the results of this effort are stored in the bfl database
on cslab.psyc.sfu.ca or cwoodruf_bfl on bugaboo.westgrid.ca
in a set of tables that all begin "whois", "bfl" or "sc2survey". 
The cslab server did not have enough space to store the game events data.
As a result, second database was created (bfl_parsing) on 
Ling-CogSci-PC2. This database contains all the parsed game data for 
each player (in tables bfl_parsing.player_% where % is the player number). 
This database is mirrored in cwoodruf_bfl_parsing on bugaboo.westgrid.ca.

All of the Dell computers have cygwin installed and cygwin
should be assumed to be the default execution environment
with the exception of the matlab script for master table generation.
Paths in this document refer to the paths when logged in to the
cygwin bash prompt as csladmin. The environment on each Ling-CogSci
server should be roughly the same. The ~ refers to /home/csladmin.
The actual location of ~ is c:\cygwin\home\csladmin.

The replays are stored locally in the ~/Parsing directory
on Ling-CogSci-PC1,2,3,4 (the Dell computers in the lab). 
The Parsing directory is a copy of the original Parsing directory
in katst@bugaboo.westgrid.ca. 

The Parsing directory files are either renamed Sc2 replay 
files or the results of parsing these renamed replays from previous 
import attempts. Newly processed files are stored outside of the 
Parsing tree to avoid confusion (see ~/unzipped and ~/reparsed 
on Ling-CogSci-PC1 for the original replays and reparsed game events).
At the moment there should be little need to refer back to files for
data analysis.

This bin directory contains smaller scripts that are meant to be reused.
In addition to these reusable tools, large mysql scripts stored 
in the ~/data directory on the Dell network Ling-CogSci-PC1 were 
used to initally load the tables. 

NOTES

See README-tables.txt in this directory for a description of the
contents of these databases.

Note that none of the chat data has been imported into a database yet.

Note that westgrid limits the number of files per user to 1,000,000 
we are currently over our quota and cannot continue to use 
westgrid for processing.

Work was mostly done by Cal unless otherwise noted.

Newer scripts are denoted ==> <==

SCRIPTS:

The following sections outline the scripts in the Starcraft/BFL/LocalParsing/bin 
directory.

-------------------------------------------------------------------------------
MASTER TABLE GENERATION

This is the last processing step after event parsing.

These scripts generate the bfl_master table of statistics.
The bfl_master table maps game statistics to bfl survey respondents.

In svn, the scripts below are not in the bin directory but can be found 
two levels up in clsabsvn/public/projects/Starcraft.

The output of these scripts is saved in a "nodes" directory where they
are run. They were run on the Dell Ling-CogSci-PCs in the lab in parallel.

../../MTBControllerBFL_Final.m
  (by Joe)
  runs the MasterTableBuilderBFL_Final.m script 

../../MasterTableBuilderBFL_Final.m
  (by Joe)
  this script combines event parsing data in the bfl_parsing.player_% 
  tables with data from the bfl_gamelevel and bfl_playerlevel 
  tables generated by buildleveltables.py
  
../../MTBControllerBFL_Find_Missing.m
  (by Joe but adapted by Cal)
  some players' games were missed by the other scripts - this script
  finds these games and adds them

-------------------------------------------------------------------------------
EVENT PARSING

Tools were developed to create per game-donor tables in bfl_parsing.
These tables all have the form player_N where N is the value of the player
field in whoisfiles. These player tables are later used to build the 
bfl_gamelevel and bfl_playerlevel tables which are in turn used to build
the bfl_master statistical analysis table.

These tools required data in the bfl and bfl_parsing databases created by
tools in the following sections.

Note that bfl and bfl_parsing are available on westgrid via the cwoodruf
account as cwoodruf_bfl and cwoodruf_bfl_parsing. Unfortunately, remote
access is not possible at this time but anyone with access to the cwoodruf
account on bugaboo.westgrid.ca can access these by running the mysql 
client from the command line:

bugaboo> mysql

The scripts:

eventparse.py
  python library that replicates the matlab script txtparse.m for 
  parsing event files. This is what actually fills the player_% tables.

==> eventparseutils.py <==
  utility functions used by eventparse.py and eventparsetest.py
  for processing individual event lines

==> eventparsetest.py <==
  used to test the ouput of eventparse.py
  Each test case is encapsulated in a method that returns: 
    True = pass False = fail
  Actual output is in the bfl.whoisfiles.testinfo field.
  A value of 1 in the bfl.whoisfiles.testpassed field indicates 
  that all test passed.
  The buildleveltables.py script takes the data from testpassed=1 whoisfiles
  records and creates the bfl_playerlevel and bfl_gamelevel tables.

==> eventtests.py <==
  Classes and functions for checking individual event records
  in a player_* table in the db

==> gametests.py <==
  Classes that define tests that check whole games in player_* tables
  these tests use other modules to define subtests (e.g. eventtests.py)

==> testanalyze.py <==
  for games that failed testing find out why they failed

==> buildleveltables.py <==
  this script combines bfl.whoisfiles.sc2gears_gameinfo and gameinfo fields
  to produce data for the bfl.bfl_gamelevel and bfl.bfl_playerlevel tables

==> insgameids.py <==
  utility to find players in whoisfiles where the game column is null
  assign numbers to those games in a reasonable way

==> insgameinfo.py <==
  find all gameinfo files and insert them into the 
  sc2gears_gameinfo field in whoisfiles
  run sc2gears on anything that doesn't have a gameinfo file
  only do this for games with null sc2gears_errors fields

==> noderun.py <==
  runs eventparse on games assigned to a specific node
  where this node is identified by a unique integer from 0 to 4 inclusive
  the node number in os.environ['NODE'] maps to a node field in bfl.whoisfiles

==> nodetest.py <==
  runs eventparsetest on games assigned to a specific node
  where this node is identified by a unique integer from 0 to 4 inclusive
  the node number in os.environ['NODE'] maps to a node field in bfl.whoisfiles

==> template_replaylevel.mysql <==
  makes template for the bfl_parsing.player_% tables.
  These tables hold the output from eventparse.py.

==> other_bfl_tables.mysql <==
  creates tables filled by buildleveltables.py.
  See template_replaylevel.mysql for player table definition.

-------------------------------------------------------------------------------
FILE ANALYSIS SCRIPTS

These scripts were the first attempt at gathering replay data.
The raw_sha1 field is the result of running sha1sum on the original replay
files. This field is used to identify identical files with different 
file names. 

The raw replay files were matched up with already parsed game events files.
These events files are the output of sc2gears (an older java based tool that
could be run from the command line). For files that were missing or believed
corrupt sc2gears was rerun on the Ling-CogSci pcs.

replaysha1.py
  python script that unpacks player donated zip files and runs sha1 on
  the contents of the SC2Replay files
  this data is saved to whoisrawlogs
  unzipped replay files saved in ~/unzipped

==> replaygameinfo-check.py <==
  after running replaysha1.py get game info for all replay files
  put this in the gameinfo field in whoisrawlogs as json
  grab relevant game data from sc2reader

replaysha1-missing.py
  like replaysha1 but designed to redo the sha1 checksum on files
  that were missed in the original replaysha1.py run on
  some donated files contained other zip files that needed to 
  be reprocessed

replaygameinfo.py
  python script run after a replaysha1*.py script that uses sc2reader 
  to produce json format data on game stats 
  data is saved to the test.whoisrawlogs table (basis for whoisfiles)

replaygameinfo-check.py
  version of replaygameinfo designed to be run after an initial attempt
  using replaygameinfo

replaytimezone.py
  inserts the time zone from the gameinfo field in whoisrawlogs into the 
  timezone field in the same table - turns out this is not that useful
  when comparing sc2gears and sc2reader game info - both have different 
  ideas of when the game was played (usually date and minutes are the same)

==> sc2_gameinfo.py <==
  given a player id and optionally a game id find one or more games 
  for that player and parse sc2gears_gameinfo. 

-------------------------------------------------------------------------------
MISSING REPLAYS

Because of the wide variation in file names (some unicode some not)
the game replays had to be imported into bfl.whoisrawlogs in steps.

The bfl.whoisrawlogs table is a superset of games included in bfl.whoisfiles.
This superset includes test uploads to the system (e.g. player 120).

==> replaysha1.py <==
  grab all zip/rar files in whoissums
  unzip each file in ReplaysInParts (which is a flattened version of the 
  original ReplayPrts.tar dir structure) in a processing directory, 
  use sha1 to calculate the checksum, save the results in bfl.whoisrawlogs.

==> replaysha1-missing.py <==
  redo replaysha1.py-like processing on files missed by replaysha1.py.

==> replaysha1-not_in_whoisfiles.py <==
  reprocessed some files missing from whoisrawlogs 2016-03-12 

==> unzip-missing-replays.sh <==
  some replay zip files contained other zip files.
  This finds zip and rar files in the unzipped output for specific 
  upload files in ~/unzipped and unpacks them.

==> replaysha1-missing-rows.sh <==
  runs replaysha1.py-like processing on missed replays.

==> unparseable2.py <==
  (by Adam)
  a tool used to find all the unparseable replays in AllCleanReplays.
  This compared the contents of the most recent replay directory and
  the contents of the extracted game actions directories to find missing files.
  Similar data can be found by comparsing bfl.whoisrawlogs with bfl.whoisfiles.

-------------------------------------------------------------------------------
GAME EVENT FILE REBUILDING

After reviewing game data in whoisfiles some games were rerun 
through sc2gears. 

Specialized scripts had to be developed to do this task as the 
sc2gears libraries did not recognize cygwin paths to the raw input
files.

The output of running the redo* scripts on the Dell servers was 
collated can be found on the Ling-CogSci-PC1 box in
cygwin under the ~/reparsed directory.

==> redo-cygwin.py <==
  redo the sc2gears parsing for the input data - original script

==> redo-cygwin-failed.py <==
  retry the redo of the sc2gears parsing for the input data
  focus on replay files that failed

==> redo-errno-22-cygwin.py <==
  retry the redo of the sc2gears parsing for the input data
  focus on replay files where errors were detected in 
  bfl.whoisreparsed where errors = '[Errno 22] Invalid argument'

-------------------------------------------------------------------------------
GAME STATS

For extracted game events files generate stats. Some of these include:
- Number of lines
- Last timestamp
- When players leave
- Who played in a given game

These are stored in the bfl.whoiseventsfound and bfl.whoiseventsused
tables and are incorporated in bfl.whoisfiles in the game_% columns.

==> whoisreparsed.py <==
  for all paths in whoisreparsed find get game stats.
  Used as the basis for the bfl.whoiseventsfound and bfl.whoiseventsused tables.

==> whoissums.mysql <==
  creates whoissums table that is the basis of whoisrawlogs.
  The bfl.whoisrawlogs table contains all replays even from test uploads.
  The bfl.whoisfiles table contains only those replays from real respondents.

==> updatecharacters.py <==
  for the listed games try and find the complete list of characters
  from whoiseventsused clients and use that to update whoisfiles game_clients

whoiseventsfound.py
  updates game data from .gameinfo files for the whoiseventsfound table 
  whoiseventsfound is based on the output of find -name '*.events' in
  the Parsing directory 

-------------------------------------------------------------------------------
PLAYER IDENTIFICATION 

As we do not have a listing of which survey respondent provided which games
or the character names they used in the provided replays, we had to figure
out, based on heuristics, what replay set belonged to which respondent.
This data is captured in the bfl.whois table. The bfl.whois.canonical field
was used for selecting player-game data used in bfl_master. For some players
using a single name severely limits the games we can analyze.

whois.pl
  perl script that finds most common player id from the Clients field 
  from a collection of .gameinfo files

whois.sh
  shell script that runs whois.pl on a group of player game files
  generates output for the whois table in the test db

whois-check.pl
  perl script that runs grep on the Parsing/RenamingLogs/FolderNamingLog.txt
  for a specific player id - used to add the filename field to the whois table
  takes as input the output of whois.sh

whois-csv.sh
  run whois-check.pl and save the csv output to a file

-------------------------------------------------------------------------------
SURVEYS

Survey data in the bfl database was gathered from the latest back up
of the lime database from the original survey server. 

Unfortunately, the survey data was spread among 3 tables:
lime_survey_446632
lime_survey_142181
lime_survey_333639

While the surveys generally had the same questions the question 
fields were different for each. Tools were developed to amalgamate
the survey data and save it in the bfl.sc2surveys table. Json data
for individual players can be found in bfl.whois.survey_json.

==> lime_format.pl <==
  this goes through the output of the lime_surveys_corrected file
  This file was generated with:
    select 'lime_survey_446632' tb, a.* 
    from lime_survey_446632 a join whois b 
    on (b.lime_survey=446632 and a.id=b.lime_respondent) 
    where lastpage is not null\G 
  (the \G is important as it formats the output in column: data format).
  This is repeated for lime_survey_142181 and lime_survey_333639.
  Match up questions and answers from the lime surveys
  prints unicode json to STDOUT.

==> Lime.pm <==
  perl module used by lime_format.pl.
  This maps lime_survey_% field names to actual questions.
  It also provides a way to interpret numbered answers.

==> sc2fields.py <==
  read a file of survey data and get a summary of questions.
  Uses the output of lime_format.pl as its input. 
  Used as a starting point to build the bfl.sc2survey_schema table.

==> sc2survey_insert.py <==
  uses sc2survey_schema and whoisfiles.survey_json to build the sc2survey table 

==> sc2surveys.py <==
  test sc2surveys.json output 

-------------------------------------------------------------------------------
PLAYER ENUMERATION

The bfl_parsing.all_players table contains a list of all character
names that show up in the donated games. Originally the numbers
were to be used to identify players but the raw character names are
now used in bfl_playerlevel and other tables where players are
individually identified.

==> players.py <==
  grabbed player data as needed from bfl_replays and remembered it in a dict.
  use replayplayers.py to load the all_players table in bfl_replays

==> replayplayers.py <==
  made a master list of replay players based on who shows up in
  actual games - keep the whois enumeration and add new names after.
  Not currenly used. Data in bfl_parsing.all_players.

-------------------------------------------------------------------------------
BASIC SCRIPTS FOR PARSING REPLAYS

sc2gears.sh
  run sc2gears in a linux environment - won't work on windows

sc2gwin.sh
  run sc2gears in a cygwin environment - won't work on linux

==> sc2wchat.sh <==
  get chat data using sc2gears.
  We have not yet (2016-05) analyzed chat data.

==> sc2wevents.sh <==
  get game events (actions) using sc2gears.
  This is the data that has eventually ended up in the 
  bfl_parsing.player_% tables (using the EVENT PARSING
  tools described below).

==> sc2wgameinfo.sh <==
  get general game stats using sc2gears.
  This is saved in bfl.whoisfiles.sc2gears_gameinfo.

sc2json.py
  dump json formatted data using sc2reader
  This is saved in bfl.whoisfiles.gameinfo.

scdump.py
  dump event logs using sc2reader
  note that these event logs are not compatible with sc2gears

scelight.sh
  run scelight in linux - not useful unless the display is set up

-------------------------------------------------------------------------------
LIBRARIES & UTILITIES FOR FILE ANALYSIS

db, tstdb, bfldb
  scripts to start mysql client (
  tst for test db, bfl for bfl_parsing on 192.168.0.100)

testdb.py
  python library for connecting to the test database in the lab
  used by the various replay*.py scripts

isfinished.py
  python library used to test whether an events log stopped prematurely

unzip-missing-replays.sh
  used with replaysha1-missing* scripts to get at the SC2Replay files
  missed in the initial pass with replaysha1.py

SCRIPTS THAT ARE REALLY DOCUMENTATION

replaysinparts.sh
  this is not a runnable script but describes part of the process of
  analyzing the donated zip files 

-------------------------------------------------------------------------------
OTHER UTILITIES

dumpanalysis.sh
  does analysis of unix "time" program output saved in a log file

parsing-size.sh
  sum the file sizes from find -ls

==> dbip.sh <==
  uses dig to find the ip address of cslab.psyc.sfu.ca

==> parsing-size.sh <==
  utility that generates stats from the Parsing.txt file on katst@bugaboo.westgrid.ca
  This file contains all a list of all files in the Parsing directory.
  The Parsing directory is the original directory used for saving sc2gears output.
  We had to move processing to local servers (the Ling-CogSci Dell computers in the lab).
  This directory can be found in /home/csladmin/Parsing under cygwin on all 4 computers.

==> oddfilenames.sh <==
  utility that runs grep on text output looking for the file ids (bfl.whoisfiles.fid column) 
  of replay files with characters that could not be stored in whoisrawlogs 
  prior to using blob and varbinary for unicode column data.

===============================================================================
OTHER RELATED SCRIPTS

These scripts process the bfl game data in various ways 
for different types of analyses other than the bfl_master stats.

-------------------------------------------------------------------------------
GZIP SEQUENCE ANALYSIS

Some utilities were developed to test the hypothesis that simply gzipping
lists of actiontypes from the bfl_parsing.player_% tables could be a
useful way to distinguish players.

Relevant tables in the bfl database are bfl_gamezips (older using an invalid 
form of game output), bfl_gamezips_aggregate (more accurate).

==> gzipgames-aggregated-actions.py <==
  runs the gzipgames.scan_one_game_aggregate function on games
  and saves them to the bfl_gamezips_aggregate table.
  The aggregate function translates all actiontypes to single
  letters and saves a gzip of game data without whitespace:
  amap = {'sel':'s','rc':'R','tr':'T','a':'A','hk':'H','b':'b','m':'M','atk':'k','mapAtk':'t','mapRCClick':'c'}
  This is preferred over the default behaviour of gzipgames.py
  and the scan_one_game function.

==> get_gzipstrings.py <==
  use a modified version of pyzip to capture compressed strings in games
  Placeholders for some actions in /home/csladmin/gzipgames in ling-cogsci-pc1 c:\cygwin.
  This script is meant to be run as part of a find command
  find -name '*.txt.gz' -a -! -name '*_shuffled.txt.gz' -exec ~/bin/get_gzipstrings.py {} \;

==> gzipgames.py <==
  library used by other gzipgames-*.py scripts
  to extract game data in various ways, run gzip on it
  and save the results to a bfl_gzipgames% table.
  Was the original tool used to generate the somewhat wrong 
  bfl.bfl_gamezips table.

==> gzipskillcraft.py <==
  ran the gzipping test on a group of games from 
  skillcraft prepared specially to only have the
  400 actions around the 10 minute mark.
  Used the obsolete scan_one_game function to process 
  the actiontypes.

==> gzipgames-leftovers.py <==
  found games that got missed by gzipgames.py
  processes each game in turn using the obsolete scan_one_game function

==> gzipstrings.py <==
  adapted version of pyflate (Copyright 2006--2007-01-21 Paul Sladen)
  that inflates data compressed using deflate
  that can ouput repeated strings found by deflate
  example output of this can be found in bfl.bfl_gzipwords and bfl.bfl_gzipgamewords
  (as of 2016-05-16 only player 0 has been processed).

==> pyflate.py <==
  original library used for gzipstrings
  Copyright 2006--2007-01-21 Paul Sladen
  http://www.paul.sladen.org/projects/compression/
  Do not change this library as it is a reference for modifications.
  Stand-alone pure-Python DEFLATE (gzip) and bzip2 decoder/decompressor.

==> bfl_gamezips_test.mysql <==
  does a paired t test on compression ratios in bfl_parsing

-------------------------------------------------------------------------------
ACTION STATS

Another hypothesis is that the distribution of actions per player over a
large number of games could be a useful way to distinguish players.

Relevant tables in bfl:
bfl_actioncounts - breaks out actions by actiontype per game 
                   in playerid,gameid,actiontype,count(*) form
bfl_actionpropcounts - flattened table where every column is an action type
bfl_actionprops - decimal proportions of every column for that game

The tables above are totals by game. These tables break out each game by players:

bfl_playeractioncounts
bfl_playeractionpropcounts
bfl_playeractionprops

==> create_actioncounts.sh <==
  make a table bfl_actioncounts with total action counts by game
  and bfl_gameactioncounts with counts broken out by player
  used by ins_actioncounts.mysql

==> create_actioncounts.mysql <==
  creates the bfl_%action% tables in bfl.

==> fix_actioncountnulls.mysql <==
  change NULL values in the resulting tables - this can be 
  fixed permanently by making the default value for action fields 0

==> ins_actioncounts.mysql <==
  creates the bfl_action%prop% tables above for whole games.
  Assumes we made the bfl_actioncounts table and filled it with 
  playerid, gameid, actiontype and the number of instances.

==> ins_playeractioncounts.mysql <==
  creates the bfl_playeraction%prop% tables above for whole games.
  Assumes we made the bfl_playeractioncounts table.

