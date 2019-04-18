#!/usr/bin/perl -w
$file = $ARGV[0];
$word = $ARGV[1];
if (@ARGV != 2){
    die"Usage: <file> <string>";
}
open F, "<$file" or die "cannot open $file";
while ($line = <F>){
    if ($line =~ /$word/){
            $line =~ s/$word/($word)/g;
    }
    print $line;
}
