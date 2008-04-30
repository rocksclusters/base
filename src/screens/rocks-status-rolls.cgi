#!/opt/rocks/bin/python

import os
#
# make sure we use the native python path
#
os.environ['PYTHONPATH'] = ''

import re
import string
import rocks.sql
import rocks.roll

class App(rocks.sql.Application):

	def __init__(self):
		rocks.sql.Application.__init__(self)

		self.rollList = []
		return


	def sendHelp(self):
		out = '<html>'
		out += '<head>'

		out += '<script language="JavaScript">'
		out += 'function loadit(url) {'
		out += '\tparent.selected.location.href = url;'
		out += '}'
		out += '</script>'

		url = '/tmp/updates/opt/rocks/screens/selected.html'
		out += '<body onLoad=loadit("%s"); >' % (url)
		out += '</body>'

		out += '</head>'
		out += '</html>'

		print 'Content-type: text/html'
		print 'Content-length: %d' % (len(out))
		print ''
		print out
		return


	def sendResponse(self):
		out = '<html>'
		out += '<head>'
		out += '<link rel="stylesheet" type="text/css" '
		out += 'href="common.css" />'
		out += '</head>'

		out += '<body class="ProBackground">'
		out += '<h2 class="ProTitle"> Selected Rolls </h2>'

		out += '<center>'
		out += '<table border cellpadding=3 cellspacing=0>'

		out += '<tr align=center>'
		out += '<td class="ProTitle">Roll Name</td>'
		out += '<td class="ProTitle">Version</td>'
		out += '<td class="ProTitle">Arch</td>'
		out += '<td class="ProTitle">Id</td>'
		out += '</tr>'

		for roll in self.rollList:
			(name, version, arch, url, diskid) = roll

			out += '<tr align=center>'

			out += '<td class="ProStatusText">'
			out += '%s' % (name)
			out += '</td>'

			out += '<td class="ProStatusText">'
			out += '%s' % (version)
			out += '</td>'

			out += '<td class="ProStatusText">'
			out += '%s' % (arch)
			out += '</td>'

			out += '<td class="ProStatusText">'
			d = string.split(diskid, ' - ')
			if len(d) > 1:
				out += '%s' % (d[1])
			else:
				if diskid == '':
					out += 'Net'
				else:
					out += '%s' % (diskid)
			out += '</td>'

			out += '</tr>'

		out += '</table>'
		out += '</center>'

		out += '<form name="selectedform" method="post"'
		out += 'action="/tmp/updates/opt/rocks/screens/'
		out += 'rocks-status-rolls.cgi">'
		out += '</form>'

		out += '</body>'
		out += '</html>'

		print 'Content-type: text/html'
		print 'Content-length: %d' % (len(out))
		print ''
		print out

		return


        def run(self):
		try:
			import time

			filename = '/tmp/rolls.xml'

			#
			# if /tmp/r.xml exists, then rocks-recordrolls.cgi
			# is busy processing the users request for rolls. in
			# this case, we'll wait for rocks-recordrolls.cgi to
			# complete -- it is done when /tmp/rolls.xml exists
			#
			if os.path.exists('/tmp/r.xml') or \
						os.path.exists(filename):
				steps = 10
				while steps > 0:
					if os.path.exists(filename):
						steps = 0
					else:
						time.sleep(0.5)
						steps -= 1

				generator = rocks.roll.Generator()
				generator.parse(filename)
				self.rollList = generator.rolls

		except:
			pass

		if self.rollList != []:
			self.sendResponse()
		else:
			self.sendHelp()

		return


app = App()
app.run()

