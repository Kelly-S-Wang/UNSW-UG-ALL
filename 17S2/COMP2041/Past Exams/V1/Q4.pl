#!/usr/bin/perl -w
while ($line = <STDIN>){
    @words = split(/ /,$line);
    foreach $word (@words){
        # if it is [0-9]\.[0-4] e.g. 3.0
        if ($word =~ /(.*[0-9]+)\.[0-4][0-9]*([^0-9]*)(\n)/){
            $word = $1.$2." ".$3;
        # if it is [0-9]\.[5-9] e.g. 3.7
        }elsif ($word =~ /(.*)([0-9]+)\.[5-9][0-9]*([^0-9]*)(\n)/){
            $word = $2;
            $word = int($word);
            $word += 1;
            $word = $1.$word.$3." ".$4
        }elsif ($word =~ /(.*)(\n)/) {
            $word=$1." ".$2;
        }else{
            $word.=" ";
        }
        print $word;
    }
}
