# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.10 2012/05/06 05:48:44 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
# $Log: Makefile,v $
# Revision 1.10  2012/05/06 05:48:44  phil
# Copyright Storm for Mamba
#
# Revision 1.9  2011/07/23 02:30:46  phil
# Viper Copyright
#
# Revision 1.8  2010/09/10 18:23:44  bruno
# updated gmetric python interface to the latest ganglia API
#
# made the sge job reporting metric more efficient based on this new gmetric
# binding
#
# Revision 1.7  2010/09/07 23:53:07  bruno
# star power for gb
#
# Revision 1.6  2009/05/15 00:34:24  anoop
# Added some solaris support to ganglia-pylib
#
# Revision 1.5  2009/05/01 19:07:07  mjk
# chimi con queso
#
# Revision 1.4  2008/10/18 00:56:00  mjk
# copyright 5.1
#
# Revision 1.3  2008/05/20 01:04:29  anoop
# Made Makefiles more Solaris friendly
#
# Revision 1.2  2008/03/06 23:41:43  mjk
# copyright storm on
#
# Revision 1.1  2008/01/04 23:04:43  bruno
# moved ganglia-pylib and receptor from hpc to base roll
#
# Revision 1.10  2007/08/14 20:28:40  anoop
# Makefiles fitted so that compilation occurs without errors
# on Solaris
#
# Revision 1.9  2007/06/23 04:03:39  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:48:51  mjk
# monkey face copyright
#
# Revision 1.7  2006/09/05 21:59:16  anoop
# Main change -
#
# Modifications to a lot of XML files. I apologize if people feel that I've
# stepped on someone else's toes here, but right now, the MANPATH variable is
# causing a bit of a headache and needs to be rethought. So all additions to
# the MANPATH variable are done via the /etc/man.config file.
#
# Please do not write shell scripts and profile.d files setting the MANPATH variable present
# as this would override the /etc/man.config file, and most man pages will not be
# available to you.
#
# Smaller changes -
#
# Refreshing packages in the xena roll. Development of xena halted for the next few weeks atleast
# Change the python version number that ganglia-python uses.
# Note added to NCBI Blast regarding upgrades in the future.
#
# Revision 1.6  2006/08/10 00:10:55  mjk
# 4.2 copyright
#
# Revision 1.5  2006/01/23 20:00:18  bruno
# need foundation path to build gmon.Network module. necessary in order for
# kickstart.cgi to build kickstart files
#
# Revision 1.4  2005/10/12 18:09:45  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:03:22  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:22:48  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/12 00:30:43  fds
# Split ganglia-python into ganglia-pylib and ganglia-python. This pylib
# is not really ganglia specific, includes our Python modules coded in C.
#
# Revision 1.7  2004/03/25 03:15:03  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.6  2003/09/16 00:35:05  fds
# Made python version handling cleaner.
#
# Revision 1.5  2003/09/15 17:51:37  fds
# Builds as root
#
# Revision 1.4  2003/09/14 16:41:29  fds
# Added support for both simple and complex Python modules
# (those which need their own subdir).
#
# Revision 1.3  2003/08/27 23:10:55  mjk
# - copyright update
# - rocks-dist uses getArch() fix the i686 distro bug
# - ganglia-python spec file fixes (bad service start code)
# - found some 80col issues while reading code
# - WAN ks support starting
#
# Revision 1.2  2003/07/14 23:41:31  fds
# Python versioning is hard.
#
# Revision 1.1  2003/03/10 18:14:30  fds
# Makefile for python extension modules
#

RELEASE = 1
MODULES = $(wildcard *.c)
HEADERS = $(wildcard *.h)
# The default Python version.
PY.VERSION = 2.4

# The 411 service requires Python 2.1 or better.
PY_INCLUDE = /opt/rocks/include/python$(PY.VERSION)
GANGLIA_INCLUDE = /opt/ganglia/include

SRCDIRS = `find * -prune -type d ! -name "CVS" ! -name "."`

include $(OS).mk

modules:: these_modules
	for i in $(SRCDIRS) ; do \
		(cd $$i; $(MAKE) PY_INCLUDE=$(PY_INCLUDE) $@) ; \
	done

# The simple modules in this directory.
these_modules: $(MODULES:.c=.so)

%.so: %.c $(HEADERS)
	$(CC) $(CCOPTS) -g -I$(PY_INCLUDE) -I$(GANGLIA_INCLUDE) -c $<
	$(CC) -shared -o $@ $(<:.c=.o) -L/opt/rocks/lib -ldnet \
		-L/opt/ganglia/$(LIBARCH) -lganglia


clean::
	rm -f *.o *.so
	for i in $(SRCDIRS) ; do \
		(cd $$i; $(MAKE) $@) ; \
	done


