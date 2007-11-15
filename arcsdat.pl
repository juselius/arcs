#!/usr/bin/perl -w
#
# Extract ARCS data from control file.
#
# Written by Jonas Juselius, 1999.
#
# $Id: arcsdat.pl,v 1.1.1.1 1999/03/08 12:30:07 jonas Exp $
#

if ( $#ARGV > 0 ) {
	print "usage: arcsdat.pl [step]\n";
	exit;
}
elsif ( $#ARGV == 0 ) {
	$step=$ARGV[0];
}
else {
	$step=0.25;
}
	
if ( ! open(IN, "<control") ) {
	print "No control file!\n";
	exit;
}

$i=0.0;

while(<IN>) {
	if ( $_ =~/^ *[0-9]/) {
	@_ = split;
	if ( ($_[1] eq 'q') ) {
		printf("%f %f\n", $i, $_[3]);
		$i+=$step;
	}
	}
}

close(IN);
