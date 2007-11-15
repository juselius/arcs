import getopt
import sys
import os
import math
import string
import QCTools
import Const
import ConfigParser
import Lsf

# Global variables

title=''
R=1.0
fitfrom=5.00
B=1.00

# Exceptions
PltError='plt_error'

def main():
	global R, B, fitfrom, title
	optimize=0

	try:
		(opts, args)=getopt.getopt(sys.argv[1:], "t:r:f:b:s?h")
	except getopt.error, x:
		print x
		usage()
		sys.exit()

	try:
		datafile=args[0]
	except IndexError:
		usage()
	
	basename=QCTools.basename(datafile)
	if os.path.exists(datafile):
		arcsdat=QCTools.readData(datafile)
	else:
		print "No such file:", datafile
		sys.exit()

	ini=basename+'.ini'
	if os.path.exists(ini):
		inirest=readini(ini)
	else:
		inirest=''

	for i in opts:
		if i[0] == '-t':
			title = i[1]
		elif i[0] == '-f':
			fitfrom = string.atof(i[1])
		elif i[0] == '-r':
			R = string.atof(i[1])
		elif i[0] == '-b':
			B = string.atof(i[1])
		elif i[0] == '-s':
			optimize=1
		elif i[0] == '-?' or i[0] == '-h':
			usage()
	
	
	if optimize:
		fit, sv, lndata=optrad(arcsdat)
	else:
		lndata=lnarcs(arcsdat)
		fitz=setfitz(lndata)
		fit, sv=fitarcs(lndata, fitz)
	
	writedata(basename+'.ln', lndata)
	avgc=avgcurrent(arcsdat, basename+'.avg')
	I, dIdB, eb=calcarcs(fit[0])
	writeini(ini, fit[1], fit[0], sv, dIdB, eb, I, avgc, inirest)
	mkplots(basename, I, fit[1], fit[0], avgc)

#
# usage
#
############################################################

def usage():
	print "usage: arcs [ -t title] [-r radius] [-f fitfrom] [-b field] [-s] datafile"
	sys.exit()

#
# optrad
#
############################################################

def optrad(arcsdat):
	global R
	step=-0.1
	
	lndata=lnarcs(arcsdat)
	fitz=setfitz(lndata)
	fit, sv=fitarcs(lndata, fitz)

	for i in range(0, 500):
		if R > 30.0 or R < 0.1:
			print "INFO: Optimization of R diverged!"
			break
		if fit[1] > 1.5005:
			R=R-step
		elif fit[1] < 1.4995:
			R=R+step
		else:
			break
		lndata=lnarcs(arcsdat)
		fitz=setfitz(lndata)
		fit, sv=fitarcs(lndata, fitz)
		step=abs(fit[1]-1.5)
	
	return fit, sv, lndata

#
# readini
#
############################################################

def readini(ini):
	global title, R, B, fitfrom
	
	cf=ConfigParser.ConfigParser()
	cf.read(ini)
	
	if cf.has_section('arcs'):
		try:
			title=cf.get('arcs', 'title')
		except:
			print "Error in %s: title" % ini
		try:
			R=cf.getfloat('arcs', 'radius')
		except:
			print "Error in %s: R" % ini

		try:
			B=cf.getfloat('arcs', 'B')
		except:
			print "Error in  %s: B" % ini

		try:
			fitfrom=cf.getfloat('arcs', 'fitfrom')
		except:
			print "Error in  %s: fitfrom" % ini

#
#  Geometry section
#

	if cf.has_section('geometry'):
		mbl=0.0
		meanr=0.0
		altr=0.0
		center="(0.0, 0.0, 0.0)"
		list=''

		try:
			list=cf.get('geometry', 'list')
		except:
			print "Error in %s: list" % ini
		
		try:
			mbl=cf.getfloat('geometry', 'meanbondl')
		except:
			print "Error in %s: meanbondl" % ini
		
		try:
			meanr=cf.getfloat('geometry', 'meanradius')
		except:
			print "Error in %s: meanradius" % ini
		
		try:
			altr=cf.getfloat('geometry', 'altradius')
		except:
			print "Error in %s: altradius" % ini

		try:
			center=cf.get('geometry', 'center')
		except:
			print "Error in %s: center" % ini

		return (list, mbl, meanr, altr, center)
	
	return None

#
# avgcurrent
#
############################################################

def avgcurrent(data, oname):
	avgc=0.0
	sai=0.0
	Rau=R*Const.au2m
	avgdata=[]
		
	frm=data[0]
	for i in data:
		z=i[0]*Const.au2m
		dist=Rau**2/(Rau**2+z**2)**(1.5)
		bz=i[1]*B*1.0e-6
		ai=2.0*bz/Const.mu0/dist*1.0e9
		if abs(ai-sai) < 0.1:
			avgc=avgc+ai
		else:
			frm=i
		sai=ai
		avgdata.append([i[0], ai])

	avgc=avgc/(len(data)-data.index(frm))
	
	writedata(oname, avgdata)
	
	return avgc


#
# lnarcs
#
############################################################

def lnarcs(data):
	lndata=[]

	if data[len(data)-1][1] < 0.000:
		print "INFO: Inverting sequence."
		for i in data:
			i[1]=-1.0*i[1]
	
	for i in data:
		if i[1] < 0.00001:
			print "INFO: point %s skipped!" % str(i)
		else:
			lndata.append([math.log(R**2/(R**2+i[0]**2)), math.log(i[1])])
	
	return lndata


#
# writedata
#
############################################################

def writedata(ofile, data):
	try:
		f=open(ofile, 'w')
	except IOError:
		print "I/O error! Write error in file", ofile
	else:
		for i in data:
			out="%f      %f\n" % (i[0], i[1])
			f.write(out)
		f.close()


#
# fitarcs
#
############################################################

def fitarcs(data, fitz):
	x, res, rank, sv = Lsf.lsf(data[fitz-1:], (1, 1), 1)
	return x, sv


#
# setfiz
#
############################################################

def setfitz(data):
	fitz=math.log(R**2/(R**2+fitfrom**2))
	
	for i in data:
		if i[0] < fitz:
			return data.index(i)

#
# calcarcs
#
############################################################

def calcarcs(b):
	Rau=R*Const.au2m
	
	eb=math.exp(b)  # didb <=> mu0/2*dI/dB*1/R
	dIdB=2.0*eb*R*Const.au2m/Const.mu0
	I=2.0*eb*B*Rau*1.0e3/Const.mu0 # 1.0e3 = ppm*nano
	
	return I, dIdB, eb

#
# writeini
#
###########################################################

def writeini(ofile, a, b, sv, dIdB, eb, I, avgc, geo):
	z=str(math.log(R**2/(R**2+fitfrom**2)))
	
	try:
		f=open(ofile, 'w+')
	except IOError:
		print "I/O error! No .ini file will be written."
	else:
		f.write('[arcs]\n')
		f.write('title:   ' + title + '\n')
		f.write('radius:  ' + str(R) + '\n')
		f.write('fitfrom: ' + str(fitfrom) + '\n')
		f.write('B:       ' + str(B) + '\n\n')

		f.write('[fit]\n')
		f.write('fitz:    ' + z+ '\n')
		f.write('a:       ' + str(a) + '\n')
		f.write('b:       ' + str(b) + '\n')
		f.write('sv:      ' + str(sv) + '\n\n')

		f.write('[result]\n')
		f.write('dIdB:    ' + str(dIdB) + '\n')
		f.write('eb:      ' + str(eb) + '\n')
		f.write('I:       ' + str(I) + '\n')
		f.write('I.avg:   ' + str(avgc) + '\n')
		
		if geo:
			out="""
[geometry]
list:          %s
meanbondl:     %f
meanradius:    %f
altradius:     %f
center:        %s
""" % (geo[0], geo[1], geo[2], geo[3], geo[4])
			f.write(out)
		
		f.seek(0)
		print f.read()
		f.close()


#
# mkplots
#
###########################################################

def mkplots(bname, I, a, b, avgc):
	fitplt=bname + '-fit.plt'
	datplt=bname + '-dat.plt'
	avgplt=bname + '-avg.plt'
	
	fitps=bname + '-fit.ps'
	datps=bname + '-dat.ps'
	avgps=bname + '-avg.ps'
	
	try:
		mkfitplt(bname, I, a, b)
	except:
		pass
	else:
		os.system('gnuplot ' + fitplt + ' >/dev/null 2>&1')
		os.system('fixps.pl ' + fitps + ' >/dev/null 2>&1')
	
	try:	
		mkdatplt(bname)
	except:
		pass
	else:
		os.system('gnuplot ' + datplt + ' >/dev/null 2>&1')
		os.system('fixps.pl ' + datps + ' >/dev/null 2>&1')
	
	try:
		mkavgplt(bname, avgc)
	except:
		pass
	else:
		os.system('gnuplot ' + avgplt + ' >/dev/null 2>&1')
		os.system('fixps.pl ' + avgps + ' >/dev/null 2>&1')
		

#
# mkfitplt
#
###########################################################

def mkfitplt(bname, I, a, b):
	try:
		f=open(bname+'-fit.plt', 'w')
	except IOError:
		print "Write failed:", f.name
		raise PltError

	ps=bname+'-fit.ps'
	ln=bname+'.ln'

	out="""
set term postscript eps enhanced "Helvetica" 20
set output '%s'

set xrange [-6:0]
set yrange [-5:5]

set arrow from -6,0 to 0,0 nohead lt 2 lw 1
show arrow
set lmargin 7
set xlabel '{/=26 log(R^2/(R^2+z^2))}'
set ylabel '{/=26 log({/Symbol s})}'

set title "%s" font "Helvetica, 30"
set label "R = %.2f au" at  -5.7,4.0 font "Helvetica, 26"
set label " I = %.1f nA" at -5.67,3.3 font "Helvetica, 26"

a=%f
b=%f
f(x)=a*x+b

plot '%s' not pt 7, f(x) not lt 1
#pause -1

""" % (ps, title, R, I, a, b, ln)
	f.write(out)
	f.close()


#
# mkdatplt
#
###########################################################

def mkdatplt(bname):
	try:
		f=open(bname+'-dat.plt', 'w')
	except IOError:
		print "Write failed:", f.name
		raise PltError

	ps=bname+'-dat.ps'
	dat=bname+'.dat'

	out="""
set term postscript eps enhanced "Helvetica" 20
set output '%s'

set xrange [0:30]
set yrange [-1:35]

set arrow from 0,0 to 30,0 nohead
show arrow

set lmargin 7
set xlabel '{/=26 z}'
set ylabel '{/=26 {/Symbol s}}'

set title "%s" font "Helvetica, 30"

plot '%s' not pt 7
#pause -1
""" % (ps, title, dat)
	f.write(out)
	f.close()


#
# mkavgplt
#
###########################################################

def mkavgplt(bname, avgc):
	try:
		f=open(bname+'-avg.plt', 'w')
	except IOError:
		print "Write failed:", f.name
		raise PltError

	ps=bname+'-avg.ps'
	avg=bname+'.avg'

	out="""
set term postscript eps enhanced "Helvetica, 20"
set output '%s'

set xrange [0:30]
#set yrange [0:35]

set arrow from 0,%.2f to 30,%.2f nohead
show arrow

set lmargin 7
set xlabel '{/=26 z}'
set ylabel '{/=26 I}'

set title "%s" font "Helvetica, 30"

plot '%s' not pt 7
#pause -1
""" % (ps, avgc, avgc, title, avg)
	f.write(out)
	f.close()

