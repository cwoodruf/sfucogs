#!/usr/bin/perl -n
# compare two files - one unshuffled and one shuffled
# report side by side character differences
# assumes each file is only a single line w/o newline
$c[$i++] = [split //, $_]; 
END { 
        $l = scalar(@{$c[1]}); 
        for ($i=0; $i < $l; $i++) { 
                print "$c[0][$i] $c[1][$i]"; 
                print " diff" and $d++ if $c[0][$i] ne $c[1][$i];  
                print "\n"; 
        } 
        printf "$d different out of $l %f%%\n", 100*$d/$l 
}
