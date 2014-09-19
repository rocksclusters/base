#! /opt/rocks/bin/python
#
# @Copyright@
# 
#                               Rocks(r)
#                        www.rocksclusters.org
#                        version 5.6 (Emerald Boa)
#                        version 6.1 (Emerald Boa)
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
#       "This product includes software developed by the Rocks(r)
#       Cluster Group at the San Diego Supercomputer Center at the
#       University of California, San Diego and its contributors."
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


import socket
import rocks.db.database
import rocks
import rocks.util
import string

from rocks.db.mappings.base import *
from sqlalchemy import or_, and_


attr_postfix = "_old"


class DatabaseHelper(rocks.db.database.Database):
	"""This class extend the Database class with a set of helper method 
	which returns object from the rocks.db.mappings classes

	These methods will replace the old methods in rocks.command.__init__"""

	def __init__(self):
		# we need to call the super class constructor
		super(DatabaseHelper, self).__init__()
		# cache for the list of appliances
		self._appliances_list = None
		# cache for the attributes
		self._attribute = None
		# cache for frontend name
		self._frontend = None
		# dictionary to cache attributes
		self._cacheAttrs = {}


	def getListHostnames(self):
		"""Return a list of string containing all the current hostnames"""
		list = self.getSession().query(Node.name).all()
		return [item for item, in list]


	def getNodesfromNames(self, names=None, managed_only=0, preload=[]):
		"""Expands the given list of names to valid set of Node entries.
		A name can be a hostname, IP address, our group (membership name), 
		or a MAC address. Any combination of these is valid.
		If the names list is empty a list of all Node in the cluster
		is returned.

		The following groups are recognized:

		rackN - All non-frontend host in rack N
		appliancename - All appliances of a given type (e.g. compute)
		select ... - an SQL statement that returns a list of hosts

		The 'managed_only' flag means that the list of hosts will
		*not* contain hosts that traditionally don't have ssh login
		shells (for example, the following appliances usually don't
		have ssh login access: 'Ethernet Switches', 'Power Units',
		'Remote Management')

		The 'preload' list contains the relationships which should be 
		preloaded to avoid sub-query when accessing related tables.
		If you need to access node.membership.name (the node membership 
		name) you should pass preload=['membership'] to preload the 
		membership table 
		(http://docs.sqlalchemy.org/en/latest/orm/loading.html)
		"""

		# Handle the simple case first and just return a complete
		# list of hosts in the cluster if no list of names was
		# provided


		list = []
		if not names:
			
			list = self.getSession().query(Node)
			for i in preload:
				list = list.options(sqlalchemy.orm.joinedload(i))
			list = list.all()

			# If we're looking for managed nodes only, filter out
			# the unmanaged ones using host attributes
			if managed_only:
				managed_list = []
				for hostname in list:
					if self.getHostAttr(hostname,
						'managed') == 'true':
						managed_list.append(hostname)
				return managed_list
			return list

		
		# we start with a false clause and then we add with OR all the other condition
		# while parsing the various names
		clause = sqlalchemy.sql.expression.false()
		query = self.getSession().query(Node)

		for name in names:
			if name.find('select ') == 0:    # SQL select
				self.execute(name)
				nodes = [i for i, in self.fetchall()]
				clause = or_(clause, Node.name.in_(nodes))
			elif name.find('%') >= 0:	# SQL % pattern
				clause = or_(clause, Node.name.like(name))
			elif name.startswith('rack'):
				# this is racks
				racknumber = int(name[4:])
				query = query.join(Membership).join(Appliance)
				clause = or_(clause, Node.rack == racknumber)
				clause = and_(clause, Appliance.name != 'frontend')
			elif name in self.getAppliancesListText():
				# it is an appliance
				query = query.join(Membership).join(Appliance)
				clause = or_(clause, Appliance.name == name)
			else:			   
				# it is a host name
				clause = or_(clause, Node.name == self.getHostname(name))
				#import pdb; pdb.set_trace()
		
		# now we register the query on the table Node and append all our clauses on OR
		query = query.filter(clause)
		for i in preload:
			query = query.options(sqlalchemy.orm.joinedload(i))
		return query.all()


	def getAppliancesListText(self):
		"""return a list of all the appliances names

		This query is run only once. If it is called multiple times it will return 
		always the same results"""
		if self._appliances_list:
			return self._appliances_list
		else:
			# first time we invoke it, run the query and cache the results
			self._appliances_list = \
				[a.name for a in self.getSession().query(Appliance.name)]
			return self._appliances_list


	def getApplianceNames(self, args=None, preload=[]):
		"""Returns a list of rocks.db.mappings.base.Appliance instance
		 from the database.
		For each arg in the ARGS list find all the appliance
		names that match the arg (assume SQL regexp).  If an
		arg does not match anything in the database we Abort.  If the
		ARGS list is empty return all appliance names.
		"""
                clause = sqlalchemy.sql.expression.false()
                query = self.getSession().query(Appliance)

		if not args:
			args = [ '%' ] # find all appliances
		for arg in args:
			clause = or_(clause, Appliance.name.like(arg))
		query = query.filter(clause)

		for i in preload:
			query = query.options(sqlalchemy.orm.joinedload(i))

		return query


	def getFrontendName(self):
		"""return the frontend name and caches it"""
		if self._frontend :
			return self._frontend

		self._frontend = self.getCategoryAttr('global', 'global', \
				'Kickstart_PrivateHostname')
		return self._frontend



	def getHostname(self, hostname=None):
		"""Returns the name of the given host as referred to in
		the database.  This is used to normalize a hostname before
		using it for any database queries."""

		# this is old code taken from rocks.commands.Database.getHostname
		# TODO it should be improved and remove the original
		
		# Look for the hostname in the database before trying
		# to reverse lookup the IP address and map that to the
		# name in the nodes table.  This should speed up the
		# installer w/ the restore roll

		arghostname = hostname 

		if hostname:
			rows = self.execute("""select * from nodes where
				name='%s'""" % hostname)
			if rows:
				return hostname

		if not hostname:					
			hostname = socket.gethostname().split('.')[0]
		try:

			# Do a reverse lookup to get the IP address.
			# Then do a forward lookup to verify the IP
			# address is in DNS.  This is done to catch
			# evil DNS servers (timewarner) that have a
			# catchall address.  We've had several users
			# complain about this one.  Had to be at home
			# to see it.
			#
			# If the resolved address is the same as the
			# hostname then this function was called with
			# an ip address, so we don't need the reverse
			# lookup.
			#
			# For truly evil DNS (OpenDNS) that have
			# catchall servers that are in DNS we make
			# sure the hostname matches the primary or
			# alias of the forward lookup Throw an Except,
			# if the forward failed an exception was
			# already thrown.


			addr = socket.gethostbyname(hostname)
			if not addr == hostname:
				(name, aliases, addrs) = socket.gethostbyaddr(addr)
				if hostname != name and hostname not in aliases:
					raise NameError

		except:
			if hostname == 'localhost':
				addr = '127.0.0.1'
			else:
				addr = None

		if not addr and self.conn:
			self.execute("""select name from nodes
				where name="%s" """ % hostname)
			if self.fetchone():
				return hostname

			#
			# let's check if the name is an alias
			#
			row = self.execute("""select n.name
					from nodes n, aliases ali
					where n.id = ali.node
					and ali.name='%s'""" % hostname)

			if row == 1:
				(hostname, ) = self.fetchone()
				return hostname

			#
			# see if this is a MAC address
			#
			self.execute("""select nodes.name from
				networks,nodes where
				nodes.id = networks.node and
				networks.mac = '%s' """ % (hostname))
			try:
				hostname, = self.fetchone()
				return hostname
			except:
				pass

			#
			# see if this is a FQDN. If it is FQDN,
			# break it into name and domain.
			#
			n = hostname.split('.')
			if len(n) > 1:
				name = n[0]
				domain = string.join(n[1:], '.')
				cmd = 'select n.name from nodes n, '	+\
					'networks nt, subnets s where '	+\
					'nt.subnet=s.id and '		+\
					'nt.node=n.id and '		+\
					's.dnszone="%s" and ' % (domain)+\
					'(nt.name="%s" or n.name="%s")'  \
					% (name, name)

				self.execute(cmd)
			try:
				hostname, = self.fetchone()
				return hostname
			except:
				pass

			# Check if the hostname is a basename
			# and the FQDN is in /etc/hosts but
			# not actually registered with DNS.
			# To do this we need lookup the DNS
			# search domains and then do a lookup
			# in each domain.  The DNS lookup will
			# fail (already has) but we might
			# find an entry in the /etc/hosts
			# file.
			#
			# All this to handle the case when the
			# user lies and gives a FQDN that does
			# not really exist.  Still a common
			# case.
			
			try:
				fin = open('/etc/resolv.conf', 'r')
			except:
				fin = None
			if fin:
				domains = []
				for line in fin.readlines():
					tokens = line[:-1].split()
					if len(tokens) > 0 and tokens[0] == 'search':
						domains = tokens[1:]
				for domain in domains:
					try:
						name = '%s.%s' % (hostname, domain)
						addr = socket.gethostbyname(name)
						hostname = name
						break
					except:
						pass
				if addr:
					return self.getHostname(hostname)

				fin.close()

			# TODO add phils execption to this
			raise rocks.util.HostnotfoundException(\
				'cannot resolve host "%s"' % hostname)
				
		
		if addr == '127.0.0.1': # allow localhost to be valid
			if arghostname == None:
				# break out of recursive loop
				return 'localhost'
			else:
				return self.getHostname()
			
		# Look up the IP address in the networks table
		# to find the hostname (nodes table) of the node.
		#
		# If the IP address is not found also see if the
		# hostname is in the networks table.  This last
		# check handles the case where DNS is correct but
		# the IP address used is different.
		if self.conn:
			rows = self.execute('select nodes.name from '
				'networks,nodes where '
				'nodes.id=networks.node and ip="%s"' % (addr))
			if not rows:
				rows = self.execute('select nodes.name ' 
					'from networks,nodes where '
					'nodes.id=networks.node and '
					'networks.name="%s"' % (hostname))
				if not rows:
					raise rocks.util.HostnotfoundException(\
						'host "%s" is not in cluster' % hostname)
			hostname, = self.fetchone()

		return hostname



	def checkHostnameValidity(self, hostname):
		"""check that the given host name is valid

		it checks that the hostname:
		- it does not contain any .
		- it is not already used
		- it is not a appliance name
		- it is not in the form of rack<number>
		- it is not an alias
		- it is not a mac address
		"""

		# they can not be in the form of rack<number>
		if '.' in hostname:
			raise rocks.util.CommandError('Hostname %s can not contains any dot.'
					% hostname)
		msg = ''
		if hostname.startswith('rack'):
			number = hostname.split('rack')[1]
			try:
				int(number)
				msg = ('Hostname %s can not be in the form ' \
					+ 'of rack<number>.\n') % hostname
				msg += 'Select a different hostname.'
			except ValueError:
				pass
		if msg:
			raise rocks.util.CommandError(msg)

		# they can not be equal to any appliance name
		if hostname in self.getAppliancesListText():
			msg = 'Hostname %s can not be equal to an appliance'\
				' name.\n' % (hostname)
			msg += 'Select a different hostname.'
			raise rocks.util.CommandError(msg)

		# check the name is not already in use in the DB
		try:
			# TODO maybe this is not the proper function to check this
			# it does too many tests we just need hostname IP and MAC
			host = self.getHostname(hostname)
			if host:
				msg = 'Node %s already exists.\n' % hostname
				msg += 'Select a different hostname, cabinet '
				msg += 'and/or rank value.'
		except (rocks.util.HostnotfoundException, NameError):
			# good! Host does not exist
			return
		raise rocks.util.CommandError(msg)



	def getCategoryIndex(self, category_name, category_index):
		"""given a category name and a category index it returns the correspondying
		object if the category_index does not exist it will be created

		All category are created at boot time"""

		session = self.getSession()
		try:
			return session.query(Category, Catindex)\
				.join(Category.catindexes)\
				.filter(Category.name==category_name, Catindex.name==category_index)\
				.one()
		except sqlalchemy.orm.exc.NoResultFound:
			# we need to create the catindex element
			cat = Category.loadOne(session, name=category_name)
			catindex = Catindex(name=category_index, category=cat)
			session.add(catindex)
			return (cat, catindex)

	def addCategoryAttr(self, category_name, catindex_name, attr, value):
		"""general function to add an attribute to the DB given a category
		and a catindex"""

		(cat, catindex) = self.getCategoryIndex(category_name, catindex_name)

		newAttr = Attribute(attr=attr, value=value, category=cat, catindex=catindex)
		return newAttr


	def setCategoryAttr(self, category_name, catindex_name, attr, value):
		"""general function which set an attribute value for a given 
		category and catindex"""

		session = self.getSession()

		(cat, catindex) = self.getCategoryIndex(category_name, \
					catindex_name)

		try:
			old_attr = Attribute.loadOne(session, attr=attr, \
					category=cat, catindex=catindex)

		except sqlalchemy.orm.exc.NoResultFound:
			# new attr, it should have been add but let's do it anyway
			#TODO
			new_attr = Attribute(attr=attr, value=value, category=cat, \
					catindex=catindex)
			session.add(new_attr)
			return

		old_value = old_attr.value
		old_attr.value = value
		# somebody will need to run commit

		if not attr.endswith(attr_postfix):
			self.setCategoryAttr(category_name, catindex_name, \
				attr + attr_postfix, old_value)


	def getCategoryAttrs(self, category_name, catindex_name):
		"""Given a category name and a category index it returns all the
		attribute in that group"""

		session = self.getSession()

		(cat, catindex) = self.getCategoryIndex(category_name, \
				catindex_name)

		return Attribute.load(session, category=cat, catindex=catindex)


	def getCategoryAttr(self, category_name, catindex_name, attr_name):
		"""Given a category name and a category index name and an attribute
		name it return its value or null if it does not exist"""

		session = self.getSession()

		(cat, catindex) = self.getCategoryIndex(category_name, \
				catindex_name)

		try:
			attr = Attribute.loadOne(session, attr=attr_name, \
					category=cat, catindex=catindex)
			return attr.value

		except sqlalchemy.orm.exc.NoResultFound:
			return None


	def removeCategoryAttr(self, category_name, catindex_name, attribute_name):

		session = self.getSession()

		(cat, cat_index) = self.getCategoryIndex(category_name, catindex_name)

		session.query(Attribute).filter(Attribute.attr == attribute_name, \
				Attribute.category==cat, \
				Attribute.catindex==cat_index).delete()

		session.query(Attribute).filter(Attribute.attr == \
				(attribute_name + attr_postfix), \
				Attribute.category==cat, \
				Attribute.catindex==cat_index).delete()


	def getHostAttrs(self, hostname, showsource=False):
		"""it returns a dictionary of {attr_name1 : (value1), attr_name2: (value2)}
		for a given hostname. In the dictionary it resolve the attributes values
		following their precendencei. If showsource is True the returned attr will
		contains an extra field with the attribute type"""

		session = self.getSession()

		if isinstance(hostname, str):
			# to support legacy getHostAttr which works with string
			(appliance, membership, node) = \
				session.query(Appliance.name, Membership.name, Node)\
					.join(Node.membership)\
					.join(Membership.appliance)\
					.filter(Node.name == hostname).one()

		elif isinstance(hostname, Node):
			node = hostname
			hostname = node.name

			# TODO
			(appliance, membership) = \
				session.query(Appliance.name, Membership.name)\
					.join(Membership.appliance)\
					.filter(Membership.ID == node.membership_ID).one()

		else:
			assert False, "hostname must be either a string with a hostname or a Node"

		attrs = {}
		if showsource:
			attrs['hostname']	= (hostname, 'I')
			attrs['rack']		= (str(node.rack), 'I')
			attrs['rank']		= (str(node.rank), 'I')
			attrs['appliance']	= (appliance, 'I')
			attrs['membership']	= (membership, 'I')

		else:
			attrs['hostname']	= hostname
			attrs['rack']		= str(node.rack)
			attrs['rank']		= str(node.rank)
			attrs['appliance']	= appliance
			attrs['membership']	= membership

		for (attr, value, type) in self.conn.execute(text(sql_attribute_query),\
				host=hostname):
			if showsource:
				attrs[attr]     = (value, type)
			else:
				attrs[attr]     = value

		# TODO cache attributes tables for speed
		# self._cacheAttrs[node.name] = attrs
		return attrs


	def getHostAttr(self, hostname, attr):
		"""like getHostAttrs but it returns the value of the given attr """
		return self.getHostAttrs(hostname).get(attr)




# this query will get all the attribute for a particular host
# the inner select (which goes in the table sub) finds all
# the attr name and maximum precedence (called maxprec)
# corresponding to a host. The outer select will then fetch
# the value for each given attr name and maxprec
#
# this query should be substituted with the tuple
# (host, host)
sql_attribute_query = """
select a.attr, a.value, UPPER(SUBSTRING(c.Name, 1, 1)) as category
from attributes a, resolvechain r, categories c, hostselections hs,
  (select attr, max(precedence) as maxprec
   from attributes a, resolvechain r, hostselections hs
   where a.category = r.category and a.category = hs.category
     and a.catindex = hs.selection and hs.host = :host
     group by attr) as sub
where a.attr = sub.attr and a.category = r.category
 and sub.maxprec = r.precedence and a.category = hs.category 
 and a.catindex = hs.selection and c.id = hs.category
 and hs.host = :host;
"""
