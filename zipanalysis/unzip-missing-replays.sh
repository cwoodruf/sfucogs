#!/bin/sh
# these replays aren't yet in whoisrawlogs - for some reason the script skipped them
tgt=$HOME/unzipped
src=$HOME/Parsing/ReplaysInParts


for rar in 823_p17t6928ps802uujilo15pd0s3 Dionysos.556_p17lppogl21h98eot81j14ot0s1 MeteoRain_p18ai9lvm91jj9omq1fio1pqn1nce3 WifWaf_p18bbi7c2tradtet1dqr1t3414v63 LLAG_356_p17l2p4kstbecr3km0rblnlqv3
do
        cd $tgt
        mkdir -p $rar && cd $rar && unrar x $src/$rar.rar
done

for zip in Creative.929_p18sj3pc0915fi6s5uhk1gav1ri3 _p17n9dujsc1rm2c7pfqinl98sv3 WilliamX_p17n618tm214pv1lmk1lomim4124c3
do
        cd $tgt
        mkdir -p $zip && cd $zip && unzip $src/$zip.zip
done
