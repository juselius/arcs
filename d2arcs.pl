#!/usr/bin/perl -w
#
# Find point of inflection in arcs data. 
# d^2/dx^2 = y_{-1}-2y_0+y_{1}
#

$n=0;

open(IN,"<$ARGV[0]");

while (<IN>) {
	if ( $_ =~ /^[ \t]*([0-9]|\.[0-9])/ ) {
		@_=split;
		$x[$n]=$_[0];
		$y[$n]=$_[1];
		$n++;
	}
}

$infl=1;

for ( $i=0; $i < $n-3; $i++) {
	$d2=$y[$i]-2*$y[$i+1]+$y[$i+2];
	
	if ( $d2*$infl < 0 ) {
		$infl*=-1;
		printf("Inflextion at %5.3f %5.3f\n", $x[$i+1], $d2);
	}
}

