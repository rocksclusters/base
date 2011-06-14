#
# $Id: hostselections.py,v 1.1 2011/06/14 23:12:13 phil Exp $ 
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# $Log: hostselections.py,v $
# Revision 1.1  2011/06/14 23:12:13  phil
# if insert-ethers actually called rocks add host, wouldn't need this redundant code. Added and already slated for removal.
#

import rocks.sql
from syslog import syslog

class Plugin(rocks.sql.InsertEthersPlugin):
	"Set up host selections for Rocks 5.4.3"

	def added(self, nodename, id):
		"""Only essential services should restart every time a 
		node is added or removed"""

		# get the osname and the membership from the db

		query = """SELECT m.name FROM 
			nodes JOIN memberships m on nodes.membership=m.id 
			WHERE nodes.name='%s'""" % nodename
		self.app.execute(query)
		membership = self.app.fetchone()[0]

		self.app.execute("""SELECT value FROM
		 	nodes n JOIN node_attributes attr on attr.node=n.id 
			WHERE n.name='%s' and Attr='os' """ % nodename) 

		osname, = self.app.fetchone()
		
		## Now execute the hostselection inserts
		## XXFIXME:  This mirrors what rocks add host does. 

		self.app.execute("""INSERT INTO catindex(Name,Category)

			VALUES('%s',mapCategory('host'))""" % nodename)

		# And then make the Default category selections for this host
		self.app.execute("""INSERT INTO hostselections(Host,
			Category, Selection) VALUES (
			mapCategoryIndex('host','%s'), mapCategory('global'),
			mapCategoryIndex('global','global')) """ % nodename)
		self.app.execute("""INSERT INTO hostselections(Host,
			Category, Selection) VALUES (
			mapCategoryIndex('host','%s'), mapCategory('os'),
			mapCategoryIndex('os','%s')) """ % (nodename,osname))
		self.app.execute("""INSERT INTO hostselections(Host,
			Category, Selection) VALUES (
			mapCategoryIndex('host','%s'), mapCategory('appliance'),
			mapCategoryIndex('appliance',
			(SELECT a.name FROM memberships m JOIN appliances a ON m.appliance=a.id AND m.name='%s')))""" 
				% (nodename,membership))
		self.app.execute("""INSERT INTO hostselections(Host,
			Category, Selection) VALUES (
			mapCategoryIndex('host','%s'), mapCategory('host'),
			mapCategoryIndex('host','%s'))""" % (nodename,nodename))

		m =  "insert-ethers - add plugin (hostselections) for  " + nodename
		syslog(m)
