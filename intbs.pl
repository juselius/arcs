#!/usr/bin/perl -w
#
# Calculate Biot-Savart curves for circular molecules.
#
# Written by Jonas Juselius, 1999.
#
# $Id: intbs.pl,v 1.1.1.1 1999/03/08 12:30:07 jonas Exp $
#

if ( $#ARGV != 2 ) {
	print("usage: integ a b I\n");
	exit(1);
}

$c1 = $ARGV[0];
$c2 = $ARGV[1];
$I = $ARGV[2]/2;

$n = 1000;
$PI = 3.141592554;
#$mu = 12.56637061e-07;

#*ff = f3;
*ff = f2;

for ( $i=0; $i < 121; $i++ ) {
	$z = $i*0.25;
	$ii = integrate(0, 2*$PI, $n);
	printf("%f   %f\n", $z, $ii);
}

#*ff = f3;
#$ii = integrate(0, 2*$PI, $n);
#print "II = $ii\n";

sub integrate {
	local ($a, $b, $n, $tot, $h, $i);

	$a=$_[0];
	$b=$_[1];
	$n=$_[2];
	
	$h = ($b-$a)/$n;
	$tot=0.5*(ff($a)+ff($b));

	for ($i=1; $i < $n; $i++) {
		$tot += ff($a+$i*$h);
	}

	$tot *= $h;
}

sub f1 {
	local ( $t );
	$t = $_[0];
	$f1=$c1*$c2/($c1**2*sin($t)**2+$c2**2*cos($t)**2+$z**2)**1.5;
}

sub f2 {
	local ( $t );
	$t = $_[0];
	$f2=$I*$c1*$c2/(($c2**2-$c1**2)*sin($t)**2+$c1**2+$z**2)**1.5;
}

sub f3 {
	local ( $t, $R );
	$t = $_[0];
	$R=2.35;
	$I=30.5/2;
	$f3=$I*$R**2/($R**2+$z**2)**1.5;
}
