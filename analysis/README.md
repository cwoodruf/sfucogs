# BFL Analysis Tools

The main starting point is the *buildmastertable.py* script. 

This script intiates making the container for the player game statistics and filling it with values.
The values are created by field classes in the bflfields directory. Which fields are included
in a given table is determined in the <pre>__init__.py</pre> file. Changing the list will include or 
exclude fields in the resulting table.

The container table consists of one row per game for each surveyed player.

These tools are based on an older matlab script. 18 of the 134 calculated values were off by +/-10%
comparing the orginal matlab script and buildmastertable.py results. Reasons for these discrepancies
might include using different algorithms or the substantial difference in how python calculates
floating point values compared to matlab. Even the high precision Decimal python library does not 
give exactly the same results as matlab when doing the same calculation on the same data.

These tools use the *pacs/pacshift.py* module for many calculations.
