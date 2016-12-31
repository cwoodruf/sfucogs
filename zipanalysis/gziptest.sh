#!/bin/sh
# test contents of a large text file with gzipncd.py
# are nearby passages likely to be scored as correlated?
# all testing done on bugaboo.westgrid.ca
# test file was project gutenberg's version of alice in wonderland
f="$HOME/data/alice-in-wonderland.txt"
# check nearby regions
start1=$1
start2=`perl -e "print $1+$2"`
bytes=$2
echo start 1 $start1, start 2 $start2, $bytes bytes
tail -c+$start1 $f | head -c$bytes > gziptest1
tail -c+$start2 $f | head -c$bytes > gziptest2
# these first two should be close to zero
# however, if bytes > 32505 these diverge sharply
$HOME/bin/gzipncd.py gziptest1 gziptest1
$HOME/bin/gzipncd.py gziptest2 gziptest2
# these should be more than zero
# even passages from the same chapter are quite divergent
# the distance increases with length
# maybe we'd have better luck with Gertrude Stein or Samuel Beckett? 
# "a rose is a rose is a rose" should compress well
$HOME/bin/gzipncd.py gziptest1 gziptest2

# see ~/data/gzipncd-tests/ for some other test cases

