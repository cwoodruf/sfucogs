#!/usr/bin/perl
## compare bfl_master_test made by buildmaster.py with bfl_master from matlab
while (<DATA>) {
        next if /^\s*#/;
        $p = $g = undef and next if /^\*{3,}/;
        $p = $1 if /playerid: (\d+)/;
        $g = $1 if /gameid: (\d+)/;
        $f = $1 and push @{$diff{$p}{$g}{$f}}, $2 if /(\w+): (.*)/;
        next if /(playerid|gameid):/;
        push @fields, $f unless $seen{$f};
        $seen{$f} = 1;
}
print "fields @fields\n";

$isnum = qr/^\d+\.\d+$|^\d*$/;

foreach $p (sort keys %diff) {
        foreach $g (sort keys %{$diff{$p}}) {
                foreach $f (@fields) {
                        next unless $f =~ /\w+/;
                        @vals = @{$diff{$p}{$g}{$f}};
# print "field $f had @vals\n";
                        ($verbose ? warn "$p $g $f had wrong number of items @vals": undef) and next
                                unless scalar(@vals) == 2;
                        next unless $vals[0] =~ $isnum and $vals[1] =~ $isnum;
                        $vals[0] = 0 unless $vals[0] =~ /\d/;
                        $vals[1] = 0 unless $vals[1] =~ /\d/;
                        $d = abs($vals[0] - $vals[1]);
                        $s = abs($vals[0]) + abs($vals[1]);
                        if ($d == 0) {
                                push @{$propoff{$f}}, 0;
                        } else {
                                push @{$propoff{$f}}, $d/$s/2;
                        }
                }
        }
}

foreach $f (@fields) {
        next unless defined $propoff{$f};
        $c = $s = 0; foreach (@{$propoff{$f}}) { $s += $_; $c++; }
        $av = ($c == 0 ? undef : $s/$c);
        $avpropoff{$f} = $av;
}

foreach $f (sort { $avpropoff{$a} <=> $avpropoff{$b} } keys %avpropoff) {
        print "$f $avpropoff{$f}\n";
}

__DATA__
# query used:
# tee bfl_master_check.txt; select * from bfl_master_test a join bfl_master b on (a.playerid=b.playerid and a.gameid=b.gameid) \G notee ;
