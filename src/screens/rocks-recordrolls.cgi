#!/opt/rocks/bin/python

import os
#
# make sure we use the native python path
#
os.environ['PYTHONPATH'] = ''

import os.path
import string
import cgi
import re
import rocks.sql
import rocks.file
import rocks.installcgi
import rocks.roll


class App(rocks.sql.Application):

	def __init__(self):
		rocks.sql.Application.__init__(self)

		self.installcgi = rocks.installcgi.InstallCGI()

		self.debug = open('/tmp/rocks-recordrolls.debug', 'w')

		return


	def urlLoad(self, url):
		out = '<html>'
		out += '<head>'

		out += '<script language="JavaScript">'
		out += 'function loadit(url) {'
		out += '\tparent.rolls.location.href = url;'
		out += '\ttop.selected.document.selectedform.submit();'
		out += '}'
		out += '</script>'

		out += '<body onLoad=loadit("%s"); >' % (url)
		out += '</body>'

		out += '</head>'
		out += '</html>'

		print 'Content-type: text/html'
		print 'Content-length: %d' % (len(out))
		print ''
		print out
		return
		

        def run(self):
		rollList = []

		try:
			#
			# if there is an existing rolls.xml file:
			#	- read it
			# 	- initialize rollList with it
			#	- nuke it
			#
			cmd = 'mv /tmp/rolls.xml /tmp/r.xml > /dev/null 2>&1'
			os.system(cmd)

			generator = rocks.roll.Generator()
			generator.parse('/tmp/r.xml')

			rollList = generator.rolls
		except:
			pass

		file = open('/tmp/r.xml', 'w')
		file.write('<rolls>\n')

		form = cgi.FieldStorage()

		if form.has_key('rollurl'):
			rollurl = form['rollurl'].value
		else:
			rollurl = ''

		if form.has_key('diskid'):
			diskid = form['diskid'].value
		else:
			diskid = ''

		self.debug.write('diskid %s\n' % (diskid))

		for name in form.keys():
			#
			# get the newly selected rolls
			#
			if form[name].value == 'on':
				#
				# the format of the selected rolls are:
				#
				#	name,version,arch
				#
				self.debug.write('name (%s)\n' % (name))
				self.debug.write('rollurl (%s)\n' % (rollurl))

				s = string.split(name, ',')
				if len(s) < 2:
					continue

				self.debug.write('s (%s)\n' % (s))

				rollname = s[0]
				rollver = s[1]
				rollarch = s[2]

				roll = (rollname, rollver, rollarch,
					rollurl, diskid)

				if roll not in rollList:
					rollList.append(roll)
					self.installcgi.getKickstartFiles(roll)

		for roll in rollList:
			#
			# rewrite rolls.xml
			#
			(rollname, rollver, rollarch, rollurl, diskid) = roll

			str = '<roll\n'
			str += '\tname="%s"\n' % (rollname)
			str += '\tversion="%s"\n' % (rollver)
			str += '\tarch="%s"\n' % (rollarch)
			str += '\turl="%s"\n' % (rollurl)
			str += '\tdiskid="%s"\n' % (diskid)
			str += '/>'

			file.write('%s\n' % (str))

		file.write('</rolls>\n')
		file.close()

		#
		# this makes the creation of /tmp/rolls.xml an atomic
		# operation. we need this because rocks-buildscreens is
		# testing for the existence of /tmp/rolls.xml and we don't
		# want it to start parsing before /tmp/rolls.xml is completely
		# written
		#
		os.system('mv /tmp/r.xml /tmp/rolls.xml')

		self.debug.close()

		self.urlLoad('/tmp/updates/opt/rocks/screens/rolls.html')

		return

app = App()
app.run()

