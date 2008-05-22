#! @PYTHON@

import os
#
# make sure we use the native python path
#
os.environ['PYTHONPATH'] = ''

import os.path
import string
import cgi
import rocks.sql
import rocks.util
import rocks.installcgi
import rocks.roll


class App(rocks.sql.Application):

	def __init__(self):
		rocks.sql.Application.__init__(self)
		self.installcgi = rocks.installcgi.InstallCGI()

		self.os = os.uname()[0].lower()
		self.generator = rocks.roll.Generator()		
		self.generator.setArch(self.getArch())
		self.generator.setOS(self.os)

		return


	def writeSiteXML(self):
		file = open('/tmp/site.xml', 'w')

		file.write('<kickstart>\n')

		#
		# set the language
		#
		cmdline = open('/proc/cmdline', 'r')
		args = string.split(cmdline.readline())
		cmdline.close()

		#
		# the default language
		#
		lang = 'en_US'
		langsupport = 'en_US'

		for arg in args:
			if arg.count('lang='):
				a = string.split(arg, '=')
				if len(a) > 1 and a[1] == 'ko':
					lang = 'ko_KR'
					langsupport = string.join([
						'ko_KR.UTF-8',
						'ko_KR',
						'ko',
						'en_US.UTF-8',
						'en_US'
						])

		file.write('<var name="Kickstart_Lang" ')
		file.write('val="%s"/>\n' % (lang))
		file.write('<var name="Kickstart_Langsupport" ')
		file.write('val="%s"/>\n' % (langsupport))

		#
		# set networking info
		#
		if os.path.exists('/tmp/netinfo-rocks'):
			netinfo = open('/tmp/netinfo-rocks', 'r')
			for line in netinfo.readlines():
				file.write(line)
			netinfo.close()

		file.write('</kickstart>\n')

		file.close()
		return


	def buildScreens(self):
		cmd = '/opt/rocks/bin/rocks report distro'
		for line in os.popen(cmd).readlines():
			distrodir = line[:-1]
		dir = distrodir

		#
		# now use rocks-dist to extract all the kickstart
		# files from their RPMs and place them into a distro
		# that we can use 'kpp' on.
		#
		pwd = os.getcwd()
		os.chdir(dir)

		#
		# need a .popt 
		#
		self.installcgi.createPopt(dir)

		#
		# rebuild the distro 
		#
		self.installcgi.rebuildDistro(self.generator.rolls)

		nativearch = rocks.util.getNativeArch()
		builddir = '%s/rocks-dist/%s/build' % (distrodir, nativearch)

		isbasicSiteXML = 0
		if os.path.exists('%s/nodes/site.xml' % (builddir)):
			#
			# if the user supplied the restore roll, then grab the
			# site.xml from the distro
			#
			os.system('cp %s/nodes/site.xml /tmp/' % (builddir))
		else:
			#
			# write a basic site.xml file
			#
			self.writeSiteXML()
			isbasicSiteXML = 1

		#
		# build the screens
		#
		os.chdir(builddir)

		cmd = '/opt/rocks/sbin/kpp root '
		cmd += '| /opt/rocks/sbin/screengen > '
		cmd += '/tmp/updates/opt/rocks/screens/screens.html '
		cmd += '2> /tmp/screens.debug'
		os.system(cmd)

		os.chdir(pwd)

		#
		# if a basic site.xml file was created (this site.xml
		# has networking info in it), then remove it after the
		# screens.html is created.
		#
		# the purpose of the basic site.xml is to provide default
		# networking info that was gathered from the first text-based
		# screen that asked for networking info.
		#
		# then, by removing this basic site.xml file, the installer
		# will know to build a 'real' site.xml by starting the
		# browser and asking the user for cluster variable info.
		#
		if isbasicSiteXML:
			os.system('rm -f /tmp/site.xml')

		return


        def run(self):
		import time

		filename = '/tmp/rolls.xml'

		#
		# wait for /tmp/rolls.xml to be completely written
		#
		steps = 10
		while steps > 0:
			if os.path.exists(filename):
				steps = 0
			else:
				time.sleep(1)
				steps -= 1

		self.generator.parse(filename)

		self.buildScreens()
		return


app = App()
app.run()

