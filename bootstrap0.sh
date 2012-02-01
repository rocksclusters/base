#!/bin/bash
#
# This file should remain OS independent
# Bootstrap0: designed for "pristine" systems (aka no rocks)
# NOTE: This should not be used on ANY Rocks appliance. 
#
# $Id: bootstrap0.sh,v 1.9 2012/02/01 19:59:50 phil Exp $
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
# $Log: bootstrap0.sh,v $
# Revision 1.9  2012/02/01 19:59:50  phil
# add foundation-python-setuptools.  Source rocks-binaries.sh at the appropriate place
#
# Revision 1.8  2012/01/04 22:51:29  phil
# Reverse last two steps. Can't use install_os_packages macro until the
# buildhost  is in the database
#
# Revision 1.7  2011/11/07 22:34:40  phil
# add the default distro
#
# Revision 1.6  2011/11/04 20:41:30  phil
# full pathnames for no ambiguity
#
# Revision 1.5  2011/11/03 22:48:15  phil
# More packages for non-Rocks build system bootstrap
#
# Revision 1.4  2011/11/03 21:03:13  phil
# Small tweaks and typo.
#
# Revision 1.3  2011/11/02 21:10:54  phil
# Some tweaks and updates to bootstrap0 so that bootstrap works properly
#
# Revision 1.2  2011/11/02 16:43:38  phil
# In bootstrap0, create an OS and Updates roll after the Rocks database is up and running.
#
# Revision 1.1  2011/11/02 05:08:56  phil
# First take on bootstrap0. Packages, command line and processing to
# bring up the rocks database on a non-Rocks installed host.
# Also reworked generation of post sections to work more like Solaris:
# Each post section now creates a shell script with the desired interpreter.
# Report post command creates a shell script from the post section of a
# (set of) node xml files.
#
#

. src/devel/devel/src/roll/etc/bootstrap-functions.sh

# 0. directory structure
# 
if [ ! -d /export/rocks/install ]; then
	mkdir -p /export/rocks/install
fi

# 1. other system packages (need similar for solaris)
if [ `./_os` == "linux" ]; then
	yum -y install rpm-build rpm-devel gcc gcc-c++ ncurses-devel swig glib2 glib2-devel openssl-devel pygobject2 pygobject2-devel cairo cairo-devel createrepo apr apr-devel expat-devel
	# packages required to build anaconda on 6
	yum -y install e2fsprogs-devel isomd5sum-devel libarchive-devel libXxf86misc-devel libblkid-devel libnl-devel newt-devel pykickstart slang-devel NetworkManager-devel NetworkManager-glib-devel iscsi-initiator-utils-devel device-mapper-devel
fi

# 2. Foundation Packages
compile_and_install foundation-mysql
compile_and_install foundation-python
compile_and_install foundation-python-setuptools
compile_and_install foundation-libxml2
compile_and_install foundation-python-xml
compile_and_install foundation-python-extras
compile_and_install foundation-rcs

# 3. Rocks  config, pylib, and kickstart, commands  
compile admin 
install rocks-admin
compile config
install rocks-config
compile pylib
install rocks-pylib
compile kickstart
install rocks-kickstart
compile command
install rocks-command

# 4. Make sure we have updated paths
. /etc/profile.d/rocks-binaries.sh

# 5. Bootstrap the database
tmpfile=$(/bin/mktemp)
/bin/cat nodes/database.xml nodes/database-schema.xml nodes/database-sec.xml | /opt/rocks/bin/rocks report post attrs="{'hostname':'', 'HttpRoot':'/var/www/html','os':'linux'}"  > $tmpfile
if [ $? != 0 ]; then
	echo "FAILURE to create script for bootstrapping the Database"
	exit -1
fi
/bin/sh $tmpfile
/bin/rm $tmpfile

# 6. Create OS Roll and Latest Updates Roll from Mirror
make -C OSROLL base updates

# 7. Create a fake bootstrap appliance, network, and host in the database
MYNAME=`hostname`
/opt/rocks/bin/rocks add distribution rocks-dist
/opt/rocks/bin/rocks add appliance bootstrap node=server
/opt/rocks/bin/rocks add host $MYNAME rack=0 rank=0 membership=bootstrap
/opt/rocks/bin/rocks add network private 127.0.0.1 netmask=255.255.255.255
/opt/rocks/bin/rocks add host interface $MYNAME lo subnet=private ip=127.0.0.1

# 8. Rest of packages for full build
if [ `./_os` == "linux" ]; then
        install_os_packages bootstrap-packages
fi


