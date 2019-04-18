#!/usr/bin/perl -w
$V = {};
foreach $arg (@ARGV){
    $V{$arg}++;

}
$highestcount = 0;
foreach $arg (@ARGV){
    if (int($highestcount)== 0){
        $highest = $arg;
        $highestcount = $V{$arg};
    } elsif ($highestcount < int($V{$arg})){
        $highest = $arg;
        #print $highest."\n";
    }
}
print $highest."\n";
