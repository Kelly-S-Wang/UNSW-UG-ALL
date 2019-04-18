#!/usr/bin/perl -w
while ($line = <>){
    while ($line =~ /^(.*)<!([^>]*)>(.*)$/){
            $line = $1.`$2`.$3;
    }
    while ($line =~ /^(.*)<([^>]*)>(.*)$/){
            $line = $1.`cat $2`.$3;
    }
    print $line."\n";
}
