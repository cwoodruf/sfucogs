# sfucogs
A selection of my work for the cognitive science lab at sfu.

Most of the scripts are python with some Mysql, shell and perl mixed in.

The scope of the work was processing a dataset of over 180,000 
starcraft II replays. While the tools as a whole may not be in a functional 
state in this repository they should suffice as an example of a system design
that can be extended to process an arbitrary number of starcraft II games on an arbitrary
number of hosts. The design is such that it is possible to create a "shared nothing" 
deployment where processing nodes are truly independent.

The history of the BFL project was that most of the games had already been processed 
using the third party tool *sc2gears* as plain text files. The game data saved in replays
is logically divided into game metadata, game events and chat.
The output of sc2gears processed game events was saved into individual tables per player. 
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

Many of these scripts are based on earlier matlab scripts created by students in the 
SFU Cognitive Science Lab. It was hoped that rewriting them in python and expanding 
their functionality would simplify processing large amounts of data on multiple hosts.

See the README.txt for an overview of the tools. The PDF contains an overview of the 
database schema used.
