#!/usr/bin/env python

import sys
import re
import os
import math
import getopt
import ConfigParser
import string
import Atom
import QCTools

def main():
	atind=[]
	format='coord'
	outfile=None
	conv='None'
	
	try:
		(opts, args)=getopt.getopt(sys.argv[1:],'f:c:o:')
	except getopt.error, x:
		print  x
		sys.exit()
	for i in opts:
		if i[0] == '-f':
			format=i[1]
		elif i[0] == '-o':
			outfile=i[1]
			if len(args) == 1:  # has no list of atoms on cmd line
				cf=ConfigParser.ConfigParser()
				cf.read(outfile)
				if cf.has_section('geometry'):
					try:
						lst=cf.get('geometry', 'list')
					except:
						pass
					else:
						lst=string.split(lst)
						for i in lst:
							atind.append(string.atoi(i))
				del cf
		elif i[0] == '-c':
			conv=i[1]
			try:
				Atom._cfact[conv]
			except KeyError, x:
				print "Unknown conversion:", x
				sys.exit()
		
	dig=re.compile('[0-9]*$')
	ran=re.compile('[0-9]*-[0-9]*$')

	try:
		infile=args[0]
	except IndexError:
		print "No file!"
		sys.exit()
	del args[0]

	for i in args:
		if dig.match(i):
			try:
				val=string.atoi(i)
			except ValueError, x:
				print "Invalid coordinate!"
				sys.exit()
			atind.append(val)
		elif ran.match(i):
			val=string.split(i, '-', 1)
			try:
				val[0]=string.atoi(val[0])
				val[1]=string.atoi(val[1])
			except ValueError, x:
				print "Invalid coordinate!"
				sys.exit()
			for j in range(val[0],val[1]):
				atind.append(j)
		else:
			print "Error in atomlist!"
			sys.exit()
	if not atind:
		print "No atoms specified!"
		sys.exit()
	atind.append(atind[0]) # connect the ring...

	atlist=QCTools.readAtoms(infile, format)
	for i in atlist:
		i.setconv(conv)
	mean=meandist(atlist, atind)
	print "\n Mean bond length is:", mean
	rad=calcradius(mean, len(atind)-1)
	print " Mean geometrical radius is: %f" % rad
	alt=altrad(atlist, atind)
	print " Alternative geometrical radius is: %f\n" % alt[0]
	print " Geometrical center is: %s\n" % repr(alt[1])

	if outfile:
		if os.path.exists(outfile):
			f=open(outfile, 'r+')
		else:
			f=open(outfile, 'w+')
		
		str=f.read()
		try:
			idx=string.index(str,'[geometry]')
			print idx
		except ValueError:
			pass
		else:
			f.seek(0,0)
			f.write(str[:idx])
		
		lst=''
		for i in range(0, len(atind)-1):
			lst=lst+' '+repr(atind[i])
		
		f.write("\n[geometry]\n")
		f.write("list:          " + lst+'\n')
		f.write("meanbondl:     " + repr(mean)+ '\n')
		f.write("meanradius:    " + repr(rad)+ '\n')
		f.write("altradius:     " + repr(alt[0])+ '\n')
		f.write("center:        " + repr(alt[1])+ '\n')
		f.close()

def meandist(atlist, atind):
	mean=0
	n=0
	for i in atind[1:]:
		j=atind[n]
		n=n+1
		mean=mean+(atlist[i] % atlist[j]) # bond lenth
	return mean/n

def altrad(atlist, atind):
	x=0
	y=0
	z=0
	mean=0
	
	for i in atind[:-1]:
		x=x+atlist[i].coord[0]
		y=y+atlist[i].coord[1]
		z=z+atlist[i].coord[2]
	
	n=len(atind)-1
	c=(x/n, y/n, z/n)
	
	for i in atind[:-1]:
		mean=mean+(atlist[i] % c)
	
	return (mean/n, c)
		
def calcradius(mean, n):
	return (mean*n)/(2*math.pi)

if __name__ == '__main__':
	main()
