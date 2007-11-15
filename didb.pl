#!/usr/local/bin/perl 

$mu0=12.56637061e-07;
$au2m=0.52917726e-10;


	open(INPUT, "<$ARGV[1]");
	$R = $ARGV[0];
	$R*=$au2m;

	while ( <INPUT> ) {
		if ( $_ =~ /^( |\t)*\#.*/ ) {
			next;
		}
			
		@_ = split;
		$sig=$_[1];
		$z=$_[0]*$au2m;
		
		$dbdi=(2.0*$sig*($R**2+$z**2)**(3/2))/($R**2*$mu0);
		
		printf("R= %6.2f r= %6.2f    dI/dB= %6.9f\n",$ARGV[0], $_[0], $dbdi);
	}

	close INPUT;
		
