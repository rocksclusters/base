#!/opt/rocks/bin/python
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
#
# Encodes a comma-separated list of compute node names, using 
# a shorthand suggested by MPD. A pattern is used to tell the 
# encoder where to compress the list.
#
# Example 1:
# Pattern: "compute-0-%d"
#
# Encoding:
# compute-0-0 compute-0-1 compute-0-2 -> compute-0-%d:0-2
#
# Example 2:
# Pattern: "compute-0-%d"
#
# Encoding:
# compute-0-0 compute-0-2 compute-0-3 ->
#	compute-0-%d:0,2-3
#
# Example 3 (harder):
# Pattern: "compute-%d-%d"
#
# Encoding:
# compute-0-0 compute-0-1 compute-1-0 compute-1-1 ->
#	compute-0-%d:0-1 compute-1-%d:0-1
#
# This encoder expands on MPDs idea by allowing
# an arbitrary number of %d wildcards in the pattern.
#
# It also factors out duplicates (for SMPs):
#
# compute-0-0 compute-0-0 compute-0-1 compute-0-1 compute-0-2 ->
#	2*compute-0-%d:0-1 compute-0-%d:2-2
#
# Intended for use the Rocks ganglia-queue reporting module for Greceptor,
# as it will shorten the size of monitoring messages significantly.
#
# Original author: Federico Sacerdoti <fds@sdsc.edu> (2002).
#
# $Log: encoder.py,v $
# Revision 1.7  2012/05/06 05:48:44  phil
# Copyright Storm for Mamba
#
# Revision 1.6  2011/07/23 02:30:46  phil
# Viper Copyright
#
# Revision 1.5  2010/09/07 23:53:07  bruno
# star power for gb
#
# Revision 1.4  2009/05/01 19:07:07  mjk
# chimi con queso
#
# Revision 1.3  2008/10/18 00:56:00  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:43  mjk
# copyright storm on
#
# Revision 1.1  2008/01/04 23:04:43  bruno
# moved ganglia-pylib and receptor from hpc to base roll
#
# Revision 1.9  2007/06/23 04:03:39  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:48:50  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:10:55  mjk
# 4.2 copyright
#
# Revision 1.6  2006/06/30 12:26:31  bruno
# moved all ganglia python code in hpc roll to point to the rocks foundation
# python
#
# Revision 1.5  2005/10/12 18:09:44  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:22  mjk
# updated copyright
#
# Revision 1.3  2005/05/24 21:22:48  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2005/04/27 19:04:09  fds
# Much more powerful. Works with many different appliances, and only relies on
# 'prefix-X-Y' naming assumption.
#
#

import sys
import re
import types
from string import find,split,index,join


class Encoder:
	"""Encodes a space-delimited name list into a mpd-style compact form.
	Assumes the names are in the form name-X-Y where X and Y are integers.
	Will silently ignore names not in this format, as well as any suffix after
	the X-Y name component."""
	

	def __init__(self, dummy=""):
		self.tightlist = []


	def sorter(self, a, b):
		"Sorts list to find all possible ranges. Used by encodeOne."

		A = a[1]
		B = b[1]
		if (A<B): return -1
		if (A==B): return 0
		if (A>B): return 1


	def encodeOne(self, namelist, prefix):
		"""Encodes the name list, given a static prefix (with no vars).
		namelist is a true python list, not a string."""

		if not prefix: return

		ranges = []
		# Sort the list to get find all possible ranges
		namelist.sort(self.sorter)

		low="undefined"
		high=0
		for dummy, i in namelist:
			if low=="undefined":
				# Prime the pump.
				low=i
				high=i
			elif i == high + 1:
				# Does this element fall in a range?
				high = i
			else:
				# We have a finished range.
				ranges.append("%d-%d" % (low,high))
				low = i
				high = i
		# Executed after loop finishes if no exceptions occured.
		else:
			if low != "undefined":
				# The final range
				ranges.append("%d-%d" % (low,high))

		# The encoded list in MPD form.
		return "%s%%d:%s" % (prefix, join(ranges,","))


	def splitList(self, namelist):
		"""Splits list into ones containing the same prefix.
		Returns a dict of lists."""

		prefixpat = re.compile('.*(\d+)-(\d+)')
		
		lists = {}
		for name in namelist:
			m = prefixpat.search(name)
			if m:
				x, y = map(int, m.groups())
				prefix = name[:m.start(2)]
				if prefix not in lists: 
					lists[prefix] = []
				lists[prefix].append((x,y))
			#else:
				#print "warning - skipping name", name

		return lists
		
		
	def findRepeats(self, indexlist):
		"""Factors out repeats. Returns a dict with key='repeat count',
		value='list of names'. """

		unique={}
		seen={}
		for coord in indexlist:
			if coord not in seen:
				# I love python: you can hash on a tuple.
				seen[coord] = 1
			else:
				seen[coord] += 1
				continue

		for coord in seen.keys():
			count = seen[coord]
			if count not in unique:
				unique[count] = [coord]
			else:
				unique[count].append(coord)

		return unique


	def encode(self, namelist, dummy=None):
		"""Takes a list of hostnames and returns a compacted version of the
		name list."""

		if type(namelist) == types.StringType:
			namelist = split(namelist, " ")

		self.tightlist = []

		prefixlist = self.splitList(namelist)
		
		for prefix, indexlist in prefixlist.items():
			#print prefix, indexlist
		
			unique = self.findRepeats(indexlist)
			#print "Unique:", unique

			for count in unique:
				element = self.encodeOne(unique[count], prefix)
				if count>1:
					self.tightlist.append("%d*%s" %
						(count, element))
				else:
					self.tightlist.append(element)
						
								
		return join(self.tightlist, " ")


	def decode(self, namelist):
		"""Decodes an encoded list of names. Does not respect original
		name ordering."""

		wholelist=[]

		if type(namelist) == types.StringType:
			namelist = split(namelist, " ")
			if not len(namelist): return

		for name in namelist:
			# Set count and name prefix.
			a=find(name,"*")
			b=find(name,"%d")
			if b<0: 
				end = len(name)
			else:
				end = b
			if a<0:
				prefix = name[:end]
				count = 1
			else:
				prefix = name[a+1:end]
				count = int(name[:a])

			# No reason to go on if we have no %d.
			if b<0:
				fullname = prefix
				wholelist.extend([fullname]*count)
				continue

			# Note there can be multiple ranges!
			ranges = split(name[b+3:],",")
			for r in ranges:
				limits = split(r,"-")
				if len(limits) == 2:
					low, high = map(int, limits)
					domain = range(low, high+1)
				else:
					domain = map(int, limits)
				for n in domain:
					fullname = "%s%s" % (prefix,n)
					wholelist.extend([fullname]*count)

		return join(wholelist," ")

