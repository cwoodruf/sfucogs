#!/usr/bin/env python
"""
implements functions for defining normalized compression distance as described in:
http://ieeexplore.ieee.org.proxy.lib.sfu.ca/stamp/stamp.jsp?tp=&arnumber=1412045
"""
import zlib
import sys

level = 6
verbose = False

def dist(x, y):
	"""
	ncd = (C(x,y) - min{C(x),C(y)})/max{C(x),C(y)}

	where C(x) is the length of the compressed string
	of original string x

	find the NCD distance of two strings
	we'd expect strings that are equal will have NCD = 0
	and strings that represent a series of independent events
	to have NCD = 1

	"""
	Cx = float(len(zlib.compress(x, level)))
	Cy = float(len(zlib.compress(y, level)))
	Cxy = float(len(zlib.compress("{}{}".format(x,y))))
	min = Cx if Cx < Cy else Cy
	max = Cx if Cx > Cy else Cy
	NCD = (Cxy - min)/max
	if verbose:
		# print x[0:80]
		# print y[0:80]
		print "len x",len(x),"len y",len(y),"Cx",Cx,"Cy",Cy,"Cxy",Cxy,"min",min,"max",max
		print "NCD distance",NCD
	return NCD

if __name__ == '__main__':
	verbose = True
	# comparing two random strings of 117 characters was NCD =~ .7
	a1 = open(sys.argv[1], 'rb')
	a1str = a1.read()
	a1.close()
	a2 = open(sys.argv[2], 'rb')
	a2str = a2.read()
	a2.close()
	print dist(a1str, a2str)
