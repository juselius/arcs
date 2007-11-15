#!/usr/bin/env python

from string import split

def getqcoord(buf):
	cc=[]
	for i in buf:
		try:
			x,y,z,e=split(i)
		except:
			continue
		if e == 'q':
			tmp=[]
#			tmp.append(x)
#			tmp.append(y)
			tmp.append(z)
			cc.append(tmp)
	return cc

def getq(buf, ret):
	k=0
	for i in buf:
		s=split(i)
		if len(s) == 6 and s[1] == 'q':
			ret[k].append(s[3])
			k=k+1
	return ret
	

def main():
	try:
		control=open('control', 'r')
		coord=open('coord', 'r')
		out=open('arcs.dat', 'w')
	except:
		print "Error in opening files!"
		exit(1)
	
	cc=getqcoord(coord.readlines())
	coord.close()
	cc=getq(control.readlines(), cc)
	control.close()
	
	for i in cc:
		#str="%s %s %s\n" % (i[0], i[1], i[2])
		str="%s %s\n" % (i[0], i[1])
		out.write(str)
	out.close()

if __name__=='__main__':
	main()
