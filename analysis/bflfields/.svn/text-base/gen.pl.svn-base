#!/usr/bin/perl -n
# input is fields.txt
# run like: ./gen.pl fields.txt to generate a bunch of templates 
print;
chomp;
($f,$t) = split ",";
$txt = `grep -i $f MasterTableBuilderBFL_Final.m`;
die "remove file \Lfield_$f.py before starting!" if -f "\Lfield_$f.py";
open PY, "> \Lfield_$f.py" or die $!;
print PY <<PYTHON;
"""
defines behaviour of bfl master table field $f
"""

from bflmasterfield import MasterField

class Field$f(MasterField):
	def __init__(self, data):
		super(Field$f, self).__init__("$f", "$t", data)

	def calc(self):
		"""
		$txt
		"""
		return None # change me!

def instance(data):
	"""
	make an instance of Field$f and return it
	"""
	return Field$f(data)

PYTHON

