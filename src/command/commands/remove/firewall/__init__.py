# $Id: __init__.py,v 1.10 2012/11/27 00:48:20 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# Revision 1.10  2012/11/27 00:48:20  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.9  2012/05/06 05:48:29  phil
# Copyright Storm for Mamba
#
# Revision 1.8  2011/07/23 02:30:33  phil
# Viper Copyright
#
# Revision 1.7  2011/06/07 22:16:11  anoop
# Bug fix
#
# Revision 1.6  2011/06/03 16:27:59  phil
# Update to new firewall schema
#
# Revision 1.5  2010/11/19 16:15:17  bruno
# fix to remove a firewall rule with 'all' as its 'network' or 'output-network'
#
# Revision 1.4  2010/09/07 23:52:57  bruno
# star power for gb
#
# Revision 1.3  2010/05/11 22:28:16  bruno
# more tweaks
#
# Revision 1.2  2010/05/07 23:13:33  bruno
# clean up the help info for the firewall commands
#
# Revision 1.1  2010/04/30 22:07:16  bruno
# first pass at the firewall commands. we can do global and host level
# rules, that is, we can add, remove, open (calls add), close (also calls add),
# list and dump the global rules and the host-specific rules.
#
#

import rocks.commands

class command(rocks.commands.CategoryArgumentProcessor,
	rocks.commands.remove.command):
	pass

class Command(command):
	"""
	Remove a named firewall rule

	<arg type='string' name='category=index' optional='1'>
	[global,os,appliance,host]=index.

	Specify which version of rulename to remove
	os=linux, appliance=login, or host=compute-0-0.
        global, global=, and global=global all refer
        to the global category.

	cannot be wildcarded. Specifying just a rulename defaults to the global
	category
	</arg>

	<arg type='stringe' name='rulename'>
	The particular rule to remove. Cannot be wildcarded
	</arg>

	<example cmd='remove firewall global ZZDRACONIAN'>
	Remove the rule named ZZDRACONIAN from the global category
	</example>

	<example cmd='remove firewall appliance=compute MYRULE'>
	Remove the rule named MYRULE from compute appliances
	</example>

	<related>list firewall</related>
	<related>list host firewall</related>

	"""


	def run(self, params, args):

                (args, rulename) = self.fillPositionalArgs(('rulename',))
		if params.has_key('@ROCKSPARAM0'):
			args.append(params['@ROCKSPARAM0'])

		indices =  self.getCategoryIndices(args, wildcard=0)
	
		if rulename is None:
			self.abort("no rulename specified")
	
		for category,catindex in indices:
			try:
				nrows=self.db.execute("""DELETE FROM firewalls 
					 WHERE rulename='%s' AND category=mapCategory('%s')
					AND catindex=mapCategoryIndex('%s','%s') """ % 
					(rulename, category, category, catindex)) 
				if nrows == 0:
					raise notFound
			except:
				self.abort("Rule '%s' not found for %s=%s" % (rulename,category,catindex))
	


