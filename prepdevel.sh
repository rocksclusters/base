#!/bin/bash
#
# This file should remain OS independent
# Bootstrap0: designed for "pristine" systems (aka no rocks)
# NOTE: This should not be used on ANY Rocks appliance. 
#
# $Id: prepdevel.sh,v 1.5 2012/11/27 00:48:00 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWindwer)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
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
# $Log: prepdevel.sh,v $
# Revision 1.5  2012/11/27 00:48:00  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/10/03 22:49:00  clem
# Make the code a little clearer
# No need to set lo twice
#
# Revision 1.3  2012/05/06 05:48:08  phil
# Copyright Storm for Mamba
#
# Revision 1.2  2012/04/24 18:47:03  phil
# Add rocks_version and rocks_version_major to attributes
#
# Revision 1.1  2012/04/05 20:59:24  phil
# Now call prepdevel.sh.
#
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

# 1. Create OS Roll and Latest Updates Roll from Mirror
# set the workdir
if [ -z "$WORKDIR" ]; then 
	TMPDIR=/tmp
else
	TMPDIR=$WORKDIR
fi

make -C OSROLL WORKDIR=$TMPDIR base updates

# 2. Create a fake bootstrap appliance, network, and host in the database
if [ `hostname | grep localhost` ] ; then
	# some built host (aka batlab) uses hostname == localhost
	# this confuses really all rocks command so let's avoid that
	MYNAME=develmachine
else
	MYNAME=`hostname -s`
fi

/opt/rocks/bin/rocks add distribution rocks-dist
/opt/rocks/bin/rocks add appliance bootstrap node=server
/opt/rocks/bin/rocks add host $MYNAME rack=0 rank=0 membership=bootstrap
/opt/rocks/bin/rocks add network private 127.0.0.1 netmask=255.255.255.255
/opt/rocks/bin/rocks add host interface $MYNAME lo subnet=private ip=127.0.0.1
/opt/rocks/bin/rocks add attr os `./_os` 

# 3. Add appliance types so that we can build the OS Roll
/opt/rocks/bin/rocks add attr Kickstart_DistroDir /export/rocks
/opt/rocks/bin/rocks add attr Kickstart_PrivateKickstartBasedir install
/opt/rocks/bin/rocks add appliance compute graph=default node=compute membership=Compute public=yes
/opt/rocks/bin/rocks add appliance nas graph=default node=nas membership=NAS\ Appliance public=yes
/opt/rocks/bin/rocks add appliance devel-server graph=default node=devel-appliance membership=Development\ Appliance public=yes
/opt/rocks/bin/rocks add appliance login graph=default node=login membership=Login public=yes
/opt/rocks/bin/rocks add attr rocks_version `/opt/rocks/bin/rocks report version`
/opt/rocks/bin/rocks add attr rocks_version_major `/opt/rocks/bin/rocks report version major=1`

# 4. Rest of packages for full build
if [ `./_os` == "linux" ]; then
        install_os_packages bootstrap-packages
fi


