#! /opt/rocks/bin/python
#
# Code for handling the new conditional attributes for both the graph
# edges and nodes.
#
# The old style arch/os/release attributes are still supported in the
# new code.
#
# @Copyright@
# @Copyright@
#
# $Log: cond.py,v $
# Revision 1.1  2008/12/23 01:18:09  mjk
# missed one
#

import string
import UserDict


class _CondEnv(UserDict.UserDict):
	"""This is a special dictionary that rather than throwing
	an exception when an item is not found it just returns None.  It is
	used to create a special local() environment where all unresolved
	variables evaluate to None.  This allows condintional expressions
	that refer to non-existent attributes to evaluate to False."""
	
	def __getitem__(self, key):
		try:
			val = UserDict.UserDict.__getitem__(self, key)
		except:
			return None

		# Try to convert value to a boolean
		
		if val.lower() in [ 'on', 'true', 'yes', 'y' ]:
			return True
		if val.lower() in [ 'off', 'false', 'no', 'n' ]:
			return False

		# Try to convert value to an integer
		try:
			return int(val)
		except ValueError:
			pass

		# Try to convert value to a float
		try:
			return float(val)
		except ValueError:
			pass

		# Everything else is returned as a string
		
		return val
		

def CreateCondExpr(archs, oses, releases, cond):
	"""Build a boolean expression from the old Rocks style
	arch, os, and release conditionals along with the new style
	generic cond XML tag attribute.

	ARCHS	= comma separated list of architectures
	OSES	= comma separated list of oses
	RELEASES	= command separated list of Rocks releases
	COND	= boolean expression in Python syntax

	The resulting expression string is the AND and all the above, where
	the ARCHS, OSES, and RELEASES are also ORed.

	The purposes is to build a single Python expression that can
	evaluate the old style "arch=", "os=", "release=" attributes along
	with the new generic "cond=" attributes.  The means that the following
	XML tags are equivalent:

	<edge from="foo" to="base" arch="i386"/>
	<edge from="foo" to="base" cond="arch=='i386'"/>
	"""

	exprs = []
    
	if archs:
		list = []		# OR of architectures
		for arch in string.split(archs, ','):
			list.append('arch=="%s"' % arch.strip())
		exprs.append(string.join(list, ' or '))

	if oses:
		list = []		# OR of OSes
		for os in string.split(oses, ','):
			list.append('os=="%s"' % os.strip())
		exprs.append(string.join(list, ' or '))

	if releases:
		list = []		# OR of releases
		for release in string.split(releases, ','):
			list.append('release=="%s"' % release.strip())
		exprs.append(string.join(list, ' or '))

	if cond:
		exprs.append(cond)	# AND of the above and the generic cond

	return string.join(exprs, ' and ')


    
def EvalCondExpr(cond, attrs):
	"""Tests the conditional expression.  The ATTRS dictionary is use to
	build the Python local() dictional (local vars) and the COND
	expression is evaluated in using these variables.  In other words,
	for every key-value pair in the ATTRS dictionary a Python variable
	is created, this allows the COND expression to directly refer to
	all the attributes as variables.
	"""
			
	if not cond:
		return True

	env = _CondEnv()
	for (k,v) in attrs.items():
		env[k] = v
		
	return eval(cond, globals(), env)
