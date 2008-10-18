#! @PYTHON@
#
# $Id: labels.py,v 1.8 2008/10/18 00:56:01 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# $Log: labels.py,v $
# Revision 1.8  2008/10/18 00:56:01  mjk
# copyright 5.1
#
# Revision 1.7  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.6  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.5  2007/05/30 22:56:29  anoop
# subnet support
#
# Revision 1.4  2006/09/11 22:47:20  mjk
# monkey face copyright
#
# Revision 1.3  2006/08/10 00:09:39  mjk
# 4.2 copyright
#
# Revision 1.2  2006/05/31 23:19:13  anoop
# Removed spec file dependency. Modified Makefiles to reflect this. Changed all
# python and cgi scripts to use the system default rocks rather than hardcoding
# the path
#
# Revision 1.1  2006/05/31 23:02:24  anoop
# Moving the labels report to the base roll from the hpc roll
#
# Revision 1.8  2006/01/16 06:49:11  mjk
# fix python path for source built foundation python
#
# Revision 1.7  2005/10/12 18:09:47  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:03:24  mjk
# updated copyright
#
# Revision 1.5  2005/08/08 21:25:00  mjk
# foundation
#
# Revision 1.4  2005/05/24 21:22:49  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/05/23 23:55:28  fds
# Fixed recent checkin log
#
# Revision 1.2  2005/05/23 23:52:44  fds
# Frontend Restore
#
# Revision 1.1  2005/02/17 04:16:56  bruno
# moved source to the hpc roll
#
# Revision 1.10  2004/10/16 03:56:27  fds
# Really fits Avery 5260 now.
#
# Revision 1.9  2004/05/13 19:08:33  bruno
# added MAC address -- thanks to jess becker of northwestern
#
# Revision 1.8  2004/03/25 03:15:44  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.7  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.6  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.5  2003/02/26 02:08:33  fds
# Made principle names larger, and tweaked layout to sit better in label.
#
# Revision 1.4  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.3  2003/02/06 20:52:38  bruno
# multi-sheet printing
#
# Revision 1.2  2003/02/06 20:00:38  bruno
# added more verbage to web site info
#
# Revision 1.1  2003/02/04 05:18:18  bruno
# initial release
#
#

import rocks.reports.base


class Report(rocks.reports.base.ReportBase):
    
	def head(self):
		print "\\documentclass[24pt]{article}"
		print "\\oddsidemargin -1.0in"
		print "\\evensidemargin -1.0in"
		print "\\marginparwidth 0pt"
		print "\\marginparsep 0pt"
		print "\\topmargin -0.50in"
		print "\\headsep 0pt"
		print "\\headheight 0pt"
		print "\\textwidth  8in"
		print "\\textheight 10.5in"

		print "\\usepackage{graphicx}"

		print "\\renewcommand{\\baselinestretch}{1.0}"
		print "% use this to adjust space between rows"
		print "\\renewcommand{\\arraystretch}{2.8}"

		print "% use this to adjust space between columns"
		print "\\renewcommand{\\tabcolsep}{6.0mm}"

		print "\\begin{document}"

		print "\\centering"

		print "\\begin{tabular}{lll}"
	

	def label(self, clustername, nodename, mac, membership):

		if membership == "Frontend":
			address = self.sql.\
				getGlobalVar('Kickstart','PublicAddress')
		else:
			address = mac

		print "\\begin{picture}(170,62.5)(1,1)"

		print "\\put(1,1){\\framebox(170,62.5){}}"

		print "\\put(4,56){Cluster:}"
		print "\\put(4,46){\\large \\textbf{%s}}" % (clustername)

		print "\\put(4,32){Node:}"
		print "\\put(4,20){\\large \\textbf{%s}}" % (nodename)

		print "\\put(4,12) {\\tiny \\textbf{Addr:}}" 
		print "\\put(4,4) {\\small \\textbf{%s}}" % (address)

		print "\\put(110,56){\\small \\textbf{\\textit{Powered By}}}"
		print "\\put(110,5){\\includegraphics[scale=0.4]{./rocks.png}}"

		print "\\end{picture}"


	def foot(self):
		print "\\end{tabular}"

		print "\\end{document}"


	def run(self):
		#
		# print out the .tex header
		#
		self.head()

		#
		# get the cluster name
		#
		clustername = ''
		try:
			clustername = self.sql.getGlobalVar('Info','ClusterName')
		except:
			pass

		self.execute('select nodes.name, networks.mac, '
			'memberships.name from nodes, networks, memberships, subnets '
			'where nodes.site=0 and networks.node = nodes.id '
			'and subnets.name="private" and networks.subnet=subnets.id '
			'and nodes.membership = memberships.id '
			'order by nodes.rack,nodes.rank')

		rows = 1
		columns = 1 

		for row in self.fetchall():
                	if not row[0]:
				continue
			self.label(clustername, row[0], row[1], row[2])

			if (columns % 3) == 0:
				print "\\\\"
				rows = rows + 1
			else:
				print "&"

			columns = columns + 1

			if rows == 11:
				print "\\end{tabular}"
				print '\\newpage'
				print "\\begin{tabular}{lll}"
				rows = 1
				columns = 1

		self.foot()
