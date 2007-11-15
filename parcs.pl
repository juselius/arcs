#!/usr/local/bin/perl -w 
#
# Set q-atoms for PARCS calculations.
#
# Written by Jonas Juselius, 1998.
#
# $Id: parcs.pl,v 1.1.1.1 1999/03/08 12:30:07 jonas Exp $
#


if ( $#ARGV != 8 ) {
	usage();
}

$xstep = 0;
$ystep = 0;
$zstep = 0;
$n = 0;
$xa=0; $xb=0;
$ya=0; $yb=0;
$za=0; $zb=0;

for ($i=0; $i < 2; $i++ ) {
	if ( $ARGV[0] eq 'x' ) {
		shift;
		$xstep = $ARGV[0];
		shift;
		$n[$i]=$ARGV[0];
		shift;
		if ( $i == 0 ) {
			$xa = 1; $xb = 0;
		}
		else {
			$xb = 1; $xa = 0;
		}
	}
	elsif ( $ARGV[0] eq 'y' ) {
		shift;
		$ystep = $ARGV[0];
		shift;
		$n[$i]=$ARGV[0];
		shift;
		if ( $i == 0 ) {
			$ya = 1; $yb = 0;
		}
		else {
			$yb = 1; $ya = 0;
		}
	}
	elsif ( $ARGV[0] eq 'z' ) {
		shift;
		$zstep = $ARGV[0];
		shift;
		$n[$i]=$ARGV[0];
		shift;
		if ( $i == 0 ) {
			$za = 1; $zb = 0;
		}
		else {
			$zb = 1; $za = 0;
		}
	}
	else {
		usage();
	}
}

$x=$ARGV[0];
$y=$ARGV[1];
$z=$ARGV[2];

for ( $j=0; $j < $n[1]; $j++ ) {
	for ( $i=0; $i < $n[0]; $i++ ) {
		printf("%f  %f   %f   q\n", 
				$x+(($i*$xa+$j*$xb)*$xstep), 
				$y+(($i*$ya+$j*$yb)*$ystep), 
				$z+(($i*$za+$j*$zb)*$zstep));
	}
}
sub usage {
	print "usage: parcs.pl ax1 s1 n1 ax2 s2 n2 x y z\n";
	exit(0);
}
