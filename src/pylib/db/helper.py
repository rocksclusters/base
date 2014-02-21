

import rocks.db.database
from rocks.db.mappings.base import *
from sqlalchemy import or_

class DatabaseHelper(rocks.db.database.Database):
	"""This class extend the Database class with a set of helper method 
	which returns object from the rocks.db.mappings classes

	These methods will replace the old methods in rocks.command.__init__"""

	def __init__(self):
		# we need to call the super class constructor
		super(DatabaseHelper, self).__init__()
		self._appliances_list = None


	def getNodesfromNames(self, names=None, managed_only=0):
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
		"""

		# Handle the simple case first and just return a complete
		# list of hosts in the cluster if no list of names was
		# provided

		list = []
		if not names:
			
			list = self.getSession().query(Node)

			# If we're looking for managed nodes only, filter out
			# the unmanaged ones using host attributes
			if managed_only:
				raise Exception('Managed node are no implemented yet')
				#managed_list = []
				#for hostname in list:
				#	if self.db.getHostAttr(hostname, 
				#		'managed') == 'true':
				#		managed_list.append(hostname)
				#return managed_list
			return list

		
		# we start with a false clause and then we add with OR all the other condition
		# while parsing the various names
		clause = sqlalchemy.sql.expression.false()
		query = self.getSession().query(Node)

		for name in names:
			if name.find('select') == 0:    # SQL select
				#TODO fix this
				self.execute(name)
				return self.fetchall()
			elif name.find('%') >= 0:	# SQL % pattern
				clause = or_(clause, Node.Name.like(name))
			elif name.startswith('rack'):
				# this is racks
				racknumber = int(name[4:])
				clause = or_(clause, Node.Rack == racknumber) #TODO exclude frontend

			elif name in self.getAppliancesListText():
				# it is an appliance
				query = query.join(Membership).join(Appliance)
				clause = or_(clause, Appliance.Name == name)
			else:			   
				# it is a host name
				clause = or_(clause, Node.Name == name)
				#import pdb; pdb.set_trace()
		
		# now we register the query on the table Node and append all our clauses on OR
		query = query.filter(clause)
		return query


	def getAppliancesListText(self):
		"""return a list of all the appliances names

		This query is run only once. If it is called multiple times it will return 
		always the same results"""
		if self._appliances_list:
			return self._appliances_list
		else:
			# first time we invoke it, run the query and cache the results
			self._appliances_list = \
				[a.Name for a in self.getSession().query(Appliance.Name)]
			return self._appliances_list


	def getHostname(self, hostname=None):
		"""Returns the name of the given host as referred to in
		the database.  This is used to normalize a hostname before
		using it for any database queries."""

		raise Exception('getHostname is not implemented yet')
		# this is old code
		
		# Look for the hostname in the database before trying
		# to reverse lookup the IP address and map that to the
		# name in the nodes table.  This should speed up the
		# installer w/ the restore roll

		arghostname = hostname 

		if hostname and self.database:
			rows = self.execute("""select * from nodes where
				name='%s'""" % hostname)
			if rows:
				return hostname

		if not hostname:					
			hostname = socket.gethostname()
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

		if not addr:
			if self.database:
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
				
				Abort('cannot resolve host "%s"' % hostname)
					
		
		if addr == '127.0.0.1': # allow localhost to be valid
			if arghostname == None:
				# break out of recursive loop
				return 'localhost'
			else:
				return self.getHostname()
			
		if self.database:
			# Look up the IP address in the networks table
			# to find the hostname (nodes table) of the node.
			#
			# If the IP address is not found also see if the
			# hostname is in the networks table.  This last
			# check handles the case where DNS is correct but
			# the IP address used is different.
			rows = self.execute('select nodes.name from '
				'networks,nodes where '
				'nodes.id=networks.node and ip="%s"' % (addr))
			if not rows:
				rows = self.execute('select nodes.name ' 
					'from networks,nodes where '
					'nodes.id=networks.node and '
					'networks.name="%s"' % (hostname))
				if not rows:
					Abort('host "%s" is not in cluster'
						% hostname)
			hostname, = self.fetchone()

		return hostname


	def checkHostname(self, hostname):
		"""check that the given host name is valid

		it checks that the hostname is not already used and
		that it is not a appliance name and is not in the form of
		rack<number>"""

		if hostname in self.getHostnames():
			self.abort('host "%s" exists' % hostname)

		nodes = rocks.clusterdb.Nodes(self.db)
		msg = nodes.checkNameValidity(hostname)
		if msg :
			# if multiple lines we keep on the first
			self.abort(msg.split('\n')[0])
		return

	def getHostAttribute(self, node):
		"""return """
		


