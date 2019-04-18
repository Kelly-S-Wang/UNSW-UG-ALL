#!/usr/bin/perl -w
while ($line = <>){
    if ($line =~ /(.*\|)(.*)\,([^\|]*)(\|.*)/){
            $line = $1.$3." ".$2.$4;
    }
    print $line."\n";
}
