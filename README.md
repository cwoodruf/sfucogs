# sfucogs
A selection of my work for the cognitive science lab at sfu.

Most of the scripts are python with some Mysql, shell and perl mixed in.

The scope of the work was processing a dataset of over 180,000 starcraft II replays.
These were initially processed using the third party tool sc2gears. 
The output of sc2gears was saved into individual tables per player. 
Processing was done in parallel on a small network of windows 7 servers using cygwin.
The game replays in the database were then reprocessed and analyzed to find screen
fixations using the Identification through Dispersion Tracking algorithm (IDT).

While IDT is normally used to identify fixation points in eye tracking data screen
fixation in starcraft II relate to instances where a player is at a relatively stationary
point on the game map. Players cannot see the entire game map in detail and so must move
around to see the status of their armies and what the other player(s) may be doing.
This fixation data is important for understanding player cognition. Fixations coupled 
with game actions such as building bases, attacking etc. are called Perception Action
Cycles (PACs) and are the essential unit of cognitive analysis.

The raw replay actions and fixation data were then further analyzed to generate statistics
for each game and each player. This data was correlated with questionnaire data to identify
relevant person data that correlated with in game behaviour.

