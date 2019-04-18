#!/usr/bin/perl -w
$name = "";
$fine = 0;
while (1){
    print "Enter student name: ";
    $name = <STDIN>;
    last if !defined $name;
    chomp $name;
    print "Enter library fine: ";
    $fine = <STDIN>;
    $total{$name}+= int($fine);
}
$largest = -1;
$expel = "";
foreach $student (keys %total){
    if ($total{$student}>$largest){
            $expel = $student;
            $largest = $total{$student};
    }
}

print "Expel $expel whose library fines total \$$largest\n";
