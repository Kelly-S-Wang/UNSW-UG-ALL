#!/usr/bin/perl -w
while ($line = <>){          # COULD USE @input = <STDIN>; instead
    push (@input, $line);
}

foreach $line (@input){
    if ($line =~ /^#([0-9]+)/){
        $num = int($1)-1;
        print $input[$num];

    }else{
        print $line;
    }
}
