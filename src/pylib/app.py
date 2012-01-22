#! /opt/rocks/bin/python
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# $Log: app.py,v $
# Revision 1.15  2012/01/22 05:28:47  phil
# Have version reported by app object be the same at the rocks version it is built on
#
# Revision 1.14  2011/07/23 02:30:48  phil
# Viper Copyright
#
# Revision 1.13  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.12  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.11  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.9  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:47:22  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:40  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:48:59  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.3  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.2  2005/05/24 21:21:57  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 00:22:08  mjk
# moved to base roll
#
# Revision 1.38  2004/10/19 00:19:28  mjk
# oh so wrong, getopt is too hard
#
# Revision 1.36  2004/08/26 00:07:01  fds
# More reliable error detection when running rocks apps
#
# Revision 1.35  2004/08/11 22:37:51  fds
# Tweak
#
# Revision 1.34  2004/08/11 22:26:11  fds
# Tweak
#
# Revision 1.33  2004/08/11 21:12:53  fds
# Command line options always win
#
# Revision 1.32  2004/08/11 19:23:30  fds
# --rcfile option for Greg
#
# Revision 1.31  2004/05/25 01:54:05  fds
# Multiple mirror support for rocks-dist parser. Comparator used to ensure we
# do not read the same mirror twice, a danger when multiple rocks-distrc files
# are in the lookup path.
#
# Revision 1.30  2004/04/28 21:05:44  fds
# Rocks-dist optimization for cross-kickstarting. Do not need the awkward
# --genhdlist flag anymore.
# o Will automatically find the native genhdlist executable, but
# o requires the native dist be made first.
#
# Revision 1.29  2004/03/25 03:15:47  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.28  2003/10/16 20:06:37  fds
# Fixed some architecture issues.
#
# Revision 1.27  2003/10/02 20:04:00  fds
# Setting arch type for self.distro in kickstart.Application. Added
# DistRPMList exception to getRPM so we can choose the correct kernel
# in dist.py. Small changes to app.py.
#
# Revision 1.26  2003/10/01 22:58:12  bruno
# don't convert the key
#
# Revision 1.25  2003/10/01 22:50:19  bruno
# convert all attributes from unicode to ascii
#
# Revision 1.24  2003/10/01 02:11:15  bruno
# fixes for anaconda 9
#
# Revision 1.23  2003/09/30 22:12:33  fds
# Ensure caller args are always processed last, even
# when parseRC has been previously invoked.
#
# Revision 1.22  2003/09/24 19:25:04  fds
# RCbase can now be explicitly specified.
#
# Revision 1.21  2003/09/17 00:43:33  fds
# Could not find any reason this crazyness is there.
#
# Revision 1.20  2003/09/04 17:37:49  fds
# Fixed RC file value ordering, and null option attributes.
#
# Revision 1.19  2003/08/26 22:44:20  mjk
# - File tag now takes "expr" attribute (command evaluation)
# - Conversion of old code to file tags
# - Added media-server (used to be server)
# - Killed replace-server on the hpc roll
# - Updated Server database membership (now a media-server)
# - Added Public field to the membership table
# - Insert-ethers only allows a subset of memberships (Public ones) to be
#   inserted.
# - Added getArch() to Application class
# - Kickstart trinity (kcgi,kpp,kgen) all updated self.arch initial value
#
# Revision 1.18  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.17  2003/08/15 21:07:26  mjk
# - RC files only built one per directory (fixed)
# - Default CGI arch is native (used to be i386)
# - Added scheduler,nameservices to rocksrc.xml
# - insert-ethers know what scheduler and nameservice we use
# - I forget what else
#
# Revision 1.16  2003/08/06 21:17:52  mjk
# - Added rocksrc base XML config file
# - Backed out of file.py tabs vs. spaces bogus fix
# - Moved mkdir from spec into makefile
#
# Revision 1.15  2003/08/05 21:10:50  mjk
# applet support
#
# Revision 1.14  2003/07/07 16:25:07  mjk
# IA64 redux
#
# Revision 1.13  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.12  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.11  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.10  2002/02/21 21:33:28  bruno
# added new copyright
#
# Revision 1.9  2001/10/24 20:23:32  mjk
# Big ass commit
#
# Revision 1.7  2001/06/27 22:32:17  mjk
# - Added pssh.py module
# - Application now work when the HOME env var is not set
#
# Revision 1.6  2001/05/09 20:17:21  bruno
# bumped copyright 2.1
#
# Revision 1.5  2001/05/08 21:08:23  mjk
# --sdsc was coded backwards (don't know when this happened)
#
# Revision 1.4  2001/05/04 22:58:53  mjk
# - Added 'cdrom' command, and CDBuilder class.
# - CDBuilder uses RedHat's source to parse the hdlist/comps file so we can
#   trim the set of RPMs on our CD.
# - Weekend!
#
# Revision 1.3  2001/04/27 01:08:50  mjk
# - Created working 7.0 and 7.1 distibutions (in same tree even)
# - Added symlink() method to File object.  Trying to get the File object
#   to make the decision on absolute vs. relative symlinks.  So far we are
#   absolute everywhere.
# - Still missing CD making code.  Need to figure out how to read to
#   comps files using RedHat's anaconda python code.  Then we can decide
#   which RPMs can go on the second CD based on what is required in the
#   kickstart files.
#
# Revision 1.2  2001/04/18 01:20:38  mjk
# - Added build.py, util.py modules
#
# - Getting closer.  I'm happy with the object model for building
# mirrors, and this will extend well to build the distributions.
#
# - Seriously needs a design document.
#
# Revision 1.1  2001/04/17 02:27:59  mjk
# Time for an initial checkin.  Datastructure and general layout of the
# code is correct.  Still need comparison code for File and RPM objects.
#

import os
import sys
import string
import getopt
import types
import rocks.util
import xml
from xml.sax import saxutils
from xml.sax import handler
from xml.sax import make_parser
from xml.sax._exceptions import SAXParseException

class Application:

    def __init__(self, argv=None):

        # Applets (code in the kickstart graph) doesn't pass sys.argv
        # so pick it up anyway to keep everything working.
        
        if not argv:
            argv = sys.argv
            
        self.args		= []
	self.caller_args	= argv[1:]
        self.usage_command	= os.path.basename(argv[0])
        self.usage_name		= 'Application'
        self.usage_version	= 0
        self.rcfileHandler      = RCFileHandler
        self.rcfileList		= []
	self.rcForce		= []

        self.projectName	 = 'rocks'
        self.projectVersionName  = 'base'
        self.projectVersionMajor = '@VERSION_MAJOR@'
        self.projectVersionMinor = '@VERSION_MINOR@'
        self.projectVersionMicro = '@VERSION_MICRO@'
        

        self.getopt		= rocks.util.Struct()
        self.getopt.s		= [ 'h' ]
        self.getopt.l		= [ 'help',
                                    'list-rcfiles',
                                    'list-project-info',
				    'rcfile='
				    ]

        # Unset our locale
	try:
        	del os.environ['LANG']
	except KeyError:
		pass

        
    def run(self):
        sys.exit(-1)

    def projectInfo(self):
        return [ self.projectName,
                 self.projectVersionName,
                 int(self.projectVersionMajor),
                 int(self.projectVersionMinor),
                 int(self.projectVersionMicro) ]

    def getArgs(self):
        return self.args

    def setArgs(self, list):
        self.args = list


    def parseArgs(self, rcbase=None):
        """Parses the command line arguments and all the relevant
        resource-control (RC) files for this application. The usage_command
        (generally argv[0]) will determine which the name of our rcfile,
        unless overrided with the rcbase argument."""

	# Save any existing options
	args = self.getArgs()

	# First pass to get rcfiles specified on the cmd line
	self.setArgs(self.caller_args)
        self.parseCommandLine(rcfile=1)

	# Parse Resource Control files
	self.setArgs([])
        if not rcbase:
            rcbase = self.usage_command
        self.parseRC(rcbase)
	for rc in self.rcForce:
		self.parseRCFile(rc, rcbase)

	# Command line options always win
        self.setArgs(args + self.args + self.caller_args)
        self.parseCommandLine()


    def parseRC(self, rcbase, section=None):
        rcfile  = rcbase + 'rc'

        if not section:
            section = rcbase

        # Where we look for resource-control files. First in 
        # the default 'etc' location, then HOME, finally in this dir.
        # We use data from all three, such that later rc files take 
        # precedence.

        dirList = [ os.path.join(os.sep,'opt', self.projectName, 'etc') ]
        if os.environ.has_key('HOME'):
            dirList.append(os.environ['HOME'])
        dirList.append('.')

        # Look for both hidden and visible rc files.
        for dir in dirList:
            self.parseRCFile(os.path.join(dir, '.' + rcfile), section)
            self.parseRCFile(os.path.join(dir, rcfile), section)


    def parseRCFile(self, filename, section):
        if os.path.isfile(filename) and filename not in self.rcfileList:
            #print "Parsing:", filename
            self.rcfileList.append(filename)
            file = open(filename, 'r')
            parser  = make_parser()
            handler = self.rcfileHandler(self)
            if section:
                handler.setSection(section)
            parser.setContentHandler(handler)
            try:
                parser.parse(file)
            except SAXParseException, msg:
                print filename, "XML parse exception: ", msg
            file.close()
            

    def parseCommandLine(self, rcfile=0):
    	"""Calls getopt to parse the command line flags. In
	rcfile mode we just get --rcfile options."""

        short = ''
        for e in self.getopt.s:
            if type(e) == types.TupleType:
                short = short + e[0]
            else:
                short = short + e
        long = []
        for e in self.getopt.l:
            if type(e) == types.TupleType:
                long.append(e[0])
            else:
                long.append(e)
        try:
            opts, args = getopt.getopt(self.args, short, long)
        except getopt.GetoptError, msg:
	    sys.stderr.write("error - %s\n" % msg)
            self.usage()
            sys.exit(1)

	for c in opts:
		if rcfile:
			if c[0] != "--rcfile":
				continue
		self.parseArg(c)

	if not rcfile:
        	self.args = args


    def parseArg(self, c):
        if c[0] in ('-h', '--help'):
            self.help()
            sys.exit(0)
        elif c[0] == '--list-rcfiles':
            print self.rcfileList
            sys.exit(0)
        elif c[0] == '--list-project-info':
            print self.projectInfo()
            sys.exit(0)
	elif c[0] == '--rcfile':
		self.rcForce.append(c[1])
        else:
            return 0
        return 1
    
    def usage(self):

        if os.environ.has_key('COLUMNS'):
            cols = os.environ['COLUMNS']
        else:
            cols = 80

        list = [ 'Usage: ', self.usage_command, ' ' ]
        
        # Build string of argument-free short options.
        s = '[-'
        for e in self.getopt.s:
            if len(e) == 1:
                s = s + e
        s = s + ']'
        if len(s) == 3:
            s = ''
        list.append(s)

        # Add the argument short options to the above string
        for e in self.getopt.s:
            if type(e) == types.TupleType:
                v = e[0]
                h = e[1]
            else:
                v = e
                h = 'arg'
            if len(v) != 1:
                list.append(' [-' + v[:-1] + ' ' + h + ']')

        # Add argument-free long options
        for e in self.getopt.l:
            if type(e) == types.TupleType:
                v = e[0]
            else:
                v = e
            if v[len(v)-1] != '=':
                list.append(' [--' + v + ']')

        # Add argument long options
        for e in self.getopt.l:
            if type(e) == types.TupleType:
                v = e[0]
                h = e[1]
            else:
                v = e
                h = 'arg'
            if v[len(v)-1] == '=':
                list.append(' [--' + v[:-1] + ' ' + h + ']')

        list.append(self.usageTail())

        # Print the usage, word wrapped to the correct screen size.
        print self.usage_name, '- version', self.usage_version
        l = 0
        s = ''
        for e in list:
            if l + len(e) <= cols:
                s = s + e
                l = l + len(e)
            else:
                print s
                l = len(e)
                s = e
        if s:
            print s


    def help(self):
        self.usage()


    def usageTail(self):
        return ''


    def getArch(self):
	return rocks.util.getNativeArch()



class RCFileHandler(rocks.util.ParseXML):

    def __init__(self, application):
        rocks.util.ParseXML.__init__(self, application)
        self.foundSection = 0
        self.section	  = self.app.usage_command

    def setSection(self, section):
        self.section = section

    def startElement(self, name, attrs):
        #
        # need to convert all the attributes to ascii strings.
        # starting in python 2, the xml parser puts the attributes in
        # unicode which causes problems with rocks apps classes, specifically
        # those that append path names found in the attributes to the sys.path
        #
        newattrs = {}
        for (aname, avalue) in attrs.items():
            newattrs[aname] = str(attrs[aname])

        if self.foundSection:
            rocks.util.ParseXML.startElement(self, name, newattrs)
        elif name == self.section:
            self.startElementSection(name, newattrs)

    def endElement(self, name):
        if self.foundSection and name == self.foundSection:
            self.endElementSection(name)
        if self.foundSection:
            rocks.util.ParseXML.endElement(self, name)

    def getOptions(self):
        return self.options


    # <section parent="base">

    def startElementSection(self, name, attrs):
        parent = attrs.get('parent')
        if parent:
            self.app.parseRC(parent, parent)
        self.foundSection = 1

    def endElementSection(self, name, attrs):
        self.foundSection = 0
    
    # <usage>

    def startElement_usage(self, name, attrs):
        usageName    = attrs.get('name')
        usageVersion = attrs.get('version')

        if usageName:
            self.app.usage_name = usageName
        if usageVersion:
            self.app.usage_version = usageVersion
        
    # <option>

    def startElement_option(self, name, attrs):
        argName  = attrs.get('name')
        # Will return None if value is not present.
        argValue = attrs.get('value')

        list = self.app.getArgs()
        
        if len(argName) > 1:
            flag = '--' + argName

            # We differentiate between empty values and
            # no value at all.
            if argValue is not None:
                list.append('%s=%s' % (flag, argValue))
            else:
                list.append(flag)
        else:
            flag = '-' + argName
            if argValue:
                list.append('%s %s' % (flag, argValue))
            else:
                list.append(flag)
        
        self.app.setArgs(list)


    # <project>

    def startElement_project(self, name, attrs):
        self.app.projectName = attrs.get('name')
        self.app.projectVersionName = attrs.get('versionName')
        self.app.projectVersionMajor = attrs.get('versionMajor')
        self.app.projectVersionMinor = attrs.get('versionMinor')
        self.app.projectVersionMicro = attrs.get('versionMicro')
