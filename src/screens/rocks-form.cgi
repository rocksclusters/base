#!/opt/rocks/bin/python

import os
#
# make sure we use the native python path
#
os.environ['PYTHONPATH'] = ''

import cgi
import rocks.sql
import rocks.password

class App(rocks.sql.Application):

	def __init__(self):
		rocks.sql.Application.__init__(self)
		return


	def buildSiteAttrs(self):
		file = open('/tmp/site.attrs', 'w')

		form = cgi.FieldStorage()
		for name in form.keys():
			xmlname = name
			xmlvalue = form[name].value

			#
			# special cases for the root password
			#
			if xmlname == 'Private_PureRootPassword':
				#
				# encrypt the root password
				#

				enc=rocks.password.Enc()
				str = 'Kickstart_PrivateRootPassword:%s' \
					% enc.enc_crypt(xmlvalue)
				file.write('%s\n' % (str))
				continue
			elif xmlname == 'Confirm_Private_PureRootPassword':
				#
				# skip this one
				#
				continue
			elif xmlname == 'Server_Partitioning':
				#
				# special case for partitioning
				#
				partfile = open('/tmp/user_partition_info', 'w')
				partfile.write('rocks %s\n' % xmlvalue)
				partfile.close()
			elif xmlname == 'Kickstart_PrivateHostname':
				#
				# need to set the 'hostname' attribute
				#
				file.write('hostname:%s\n' % (xmlvalue))

			str = '%s:%s' % (xmlname, xmlvalue)
			file.write('%s\n' % (str))

		#
		# add the rocks_version attribute
		#
		cmd = '/opt/rocks/bin/rocks report version'
		for line in os.popen(cmd).readlines():
			file.write('rocks_version:%s\n' % line[:-1])

		#
		# add the os attribute
		#
		file.write('os:linux\n')

		file.close()
		return


	def killBrowser(self):
		cmd = 'killall firefox-bin'
		os.system(cmd)
		return


        def run(self):
		self.buildSiteAttrs()
		self.killBrowser()
		return

##
## main
##
app = App()
app.run()

