#!/opt/rocks/bin/python
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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



import inspect
import os
import sqlalchemy

import rocks.commands
import rocks.db.mappings


#
# dump mysql code
#
def dump(sql, *multiparams, **params):
    print sql.compile(dialect=engine.dialect), ';'

engine = sqlalchemy.create_engine('mysql://', strategy='mock', executor=dump)

class Command(rocks.commands.report.command):
	"""
	Output the database DDL SQL to create the given module tables.


	<arg type='string' name='component'>
	output the database configuration of the given component name
	the component are fetched from rocks.db.mappings.&lt;componentname&gt;
	</arg>

	<param optional='1' type='bool' name='droptable'>
	If this parameters is true this command will drop the tables
	before creating it (it will wipe all the data from it).
	Default is false.
	</param>

	<example cmd='report databasesql base'>
	print out the SQL for the base roll
	</example>
	"""

	def run(self, params, args):

		(droptable, ) = self.fillParams([('droptable','false'), ])
		droptable=self.str2bool(droptable)
	
		if len(args) != 1:
			self.abort('must supply one component name')
		component = args[0]
	

		new_tables = []
		try:
			mod = __import__('rocks.db.mappings.' + component, 
					fromlist=[''])
		except ImportError:
			self.abort("module %s does not exists in "
					"rocks.db.mappings" % component)

		from sqlalchemy.ext.declarative.api import DeclarativeMeta
		from rocks.db.mappings.base import RocksBase

		for name, table in inspect.getmembers(mod):
			if type(table) is DeclarativeMeta and \
				issubclass(table, RocksBase):
				# table is a ORM table declaration (sqlalchemy)
				new_tables.append(table.__table__)

		base = rocks.db.mappings.base.Base
		if droptable:
			base.metadata.drop_all(engine, tables=new_tables)
		base.metadata.create_all(engine, tables=new_tables)


		# extra sql files
		extra_sql_path = os.path.join(rocks.db.mappings.__path__[0], 
					component + ".sql")
		if os.path.exists(extra_sql_path):
			f = open(extra_sql_path)
			print f.read()
			f.close()

	
RollName = "base"


