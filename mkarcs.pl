#!/usr/bin/env perl 
#
# Insert q-atoms into coord for ARCS calculations.
#
# Written by Jonas Juselius, 1999.
#
# $Id: mkarcs.pl,v 1.1.1.1 1999/03/08 12:30:07 jonas Exp $
#

if ( $#ARGV != 5 ) {
	usage();
}

$xstep = 0;
$ystep = 0;
$zstep = 0;

if ( $ARGV[0] eq 'x' ) {
	$xstep = 1;
}
elsif ( $ARGV[0] eq 'y' ) {
	$ystep = 1;
}
elsif ( $ARGV[0] eq 'z' ) {
	$zstep = 1;
}
elsif ( $ARGV[0] eq '-c' ) {
	$coords_only=1;
}
else {
	usage();
}

$step = $ARGV[1];
$N = $ARGV[2];
$x = $ARGV[3];
$y = $ARGV[4];
$z = $ARGV[5];

if ( $coords_only ) {
	for ( $i=0; $i < $N; $i++ ) {
		printf("%f \n", $x+$i*$step);
	}
}
else {
	for ( $i=0; $i < $N; $i++ ) {
		printf("%f  %f   %f q\n", 
				$x+$i*$step*$xstep, $y+$i*$step*$ystep, $z+$i*$step*$zstep);
	}
}

sub usage {
	print "usage: arcs.pl axis step N x y z\n";
	exit(0);
}
