# $Id: __init__.py,v 1.17 2012/05/06 05:48:24 phil Exp $
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
# $Log: __init__.py,v $
# Revision 1.17  2012/05/06 05:48:24  phil
# Copyright Storm for Mamba
#
# Revision 1.16  2011/07/23 02:30:29  phil
# Viper Copyright
#
# Revision 1.15  2010/09/07 23:52:53  bruno
# star power for gb
#
# Revision 1.14  2009/05/01 19:06:57  mjk
# chimi con queso
#
# Revision 1.13  2008/10/18 00:55:49  mjk
# copyright 5.1
#
# Revision 1.12  2008/08/19 19:33:33  bruno
# a MAC address is now a valid key to look up a host.
#
# also, one more tweak to get the 'output-col' flag working
#
# Revision 1.11  2008/08/18 22:16:50  bruno
# fix for 'output-col' and 'rocks list var'
#
# Revision 1.10  2008/03/14 20:54:34  bruno
# make sure all header/column comparisons are based on lowercase names
#
# Revision 1.9  2008/03/12 22:25:11  bruno
# dear mason,
#
# there are rocks commands that don't provide a 'header' parameter, yet, and
# here's the funny part, they still expect output.
#
# with love, greg. :-)
#
# Revision 1.8  2008/03/06 23:41:36  mjk
# copyright storm on
#
# Revision 1.7  2008/03/06 23:12:55  mjk
# Added column level filtering of output for list commands.
#
# New params
#   output-header=BOOL
#   output-col=NAME,NAME,...
#
# Now can turn off the header line with output-header=no and can select
# which columns get printed with output-col.  For example:
#
# rocks list roll output-col=arch output-header=no
#
# Will just print the arch (not even roll name) for all the rolls on the
# cluster.
#
# TODO: Where to document, not going to touch every list command!
#
# Revision 1.6  2007/06/19 16:42:41  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.5  2007/06/07 21:23:04  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#

import string
import rocks.commands

class command(rocks.commands.Command):
	MustBeRoot = 0

	def __init__(self, database):
		rocks.commands.Command.__init__(self, database)
		self.outputCols	= []

	def outputRow(self, list):
		if len(self.outputCols) > 0:
			l = []
			for i in range(0, len(list)):
				if self.outputCols[i + self.startOfLine]:
					l.append(list[i])
		else:
			l = list
		return string.join(l, ' ')

	def endOutput(self, header=[], padChar='-', trimOwner=1):
                """Pretty prints the output list buffer."""

		showHeader	= 1

		showCols = []
		for c in header:
			showCols.append(c.lower())
			
		for key in self._params.keys():
			if key == 'output-header':
				showHeader = self.str2bool(self._params[key])
			elif key == 'output-col':
				showCols = []
				for col in self._params[key].split(','):
					showCols.append(col.lower())

		self.outputCols = []
		for c in header:
			if c.lower() in showCols:
				self.outputCols.append(True)
			else:
				self.outputCols.append(False)
		if not showHeader:
			header = []
		rocks.commands.Command.endOutput(self, 
			header, padChar, trimOwner)
