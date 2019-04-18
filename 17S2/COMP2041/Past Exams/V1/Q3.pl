#!/usr/bin/perl -w
foreach $element (@ARGV){
    if ($words{$element}){

    } else {
		print $element." ";
        $words{$element} = 1;
	}
}
print "\n";
