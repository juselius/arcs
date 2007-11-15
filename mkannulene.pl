#!/usr/local/bin/perl -w

	if ( $#ARGV != 0 ) {
		print "usage: mkannulene.pl \{number of carbons\}\n";
		exit 1;
	}

	$annu = $ARGV[0];

	$PI = 3.14;
	$cc_dist = 2.70;
	$ch_dist = 2.08;
#	$cc_dist = 2.90; # phosphorus
#	$ch_dist = 2.08; # phosphorus

	$c_rad = (($annu+1)*$cc_dist)/(2.0*$PI);
	$h_rad = $c_rad+$ch_dist;
	$phi = 2.0*$PI/$annu;
	$ang = 0.0;
	
	print "\$coord\n";
	
	for ( $i=0; $i < $annu; $i++ ) {
		$ang = $i*$phi;
		$cx = $c_rad*sin($ang); 
		$cy = $c_rad*cos($ang);
		$hx = $h_rad*sin($ang); 
		$hy = $h_rad*cos($ang);
		printf("%6.4f    %6.4f  0.0000    c\n", $cx, $cy);
		printf("%6.4f    %6.4f  0.0000    h\n", $hx, $hy);
	}

	print "\$end\n";
