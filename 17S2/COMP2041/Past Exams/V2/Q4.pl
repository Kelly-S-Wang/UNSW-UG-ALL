#!/usr/bin/perl -w
while ($line = <>){
    # start with 00 then add 12 and put am at end
    if ($line =~ /(.*\s)00(:\d\d:\d\d)(\s.*)/){
        $line = $1."12".$2."am".$3;
    # start with 12 then put pm at end
    } elsif ($line =~ /(.*\s)(12)(:\d\d:\d\d)(.*)/){
        $line = $1.$2.$3."pm".$4;
    # start with 13-23 then subtract 12 and put pm at end
    } elsif ($line =~ /(.*\s)(1[3-9]|2[0-3])(:\d\d:\d\d)(\s.*)/){
        $num = int ($2);
        $num = $num-12;
        $line= $1.$num.$3."pm".$4;
    #       print "24 hour is ".$num."\n";
    } elsif ($line =~ /(.*\s)(0[1-9]|1[01])(:\d\d:\d\d)(\s.*)/){
        $line = "$1".$2.$3."am"."$4";
        #print "before: $1\n";
        #print "num: $2\n";
        #print "time: $3\n";
        #print "after:$4\n";


    }
    print $line."\n";
}
