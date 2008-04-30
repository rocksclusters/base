#! @PYTHON@
#
# $Id: add-extra-nic.py,v 1.13 2008/04/02 16:59:37 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# $Log: add-extra-nic.py,v $
# Revision 1.13  2008/04/02 16:59:37  bruno
# nuke dead commands
#
# put message in other commands that point the user to the appropriate rocks
# command-line command.
#
# Revision 1.12  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.11  2007/06/23 04:03:25  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:47:28  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:09:45  mjk
# 4.2 copyright
#
# Revision 1.8  2006/07/06 19:50:10  bruno
# for 'dump' command, print name of utility from argv -- that way, we can
# specify the full pathname when these tools are used during an installation
# and the path has not yet been initialized.
#
# Revision 1.7  2006/01/16 06:49:01  mjk
# fix python path for source built foundation python
#
# Revision 1.6  2005/10/12 18:08:46  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:02:25  mjk
# updated copyright
#
# Revision 1.4  2005/07/11 23:51:37  mjk
# use rocks version of python
#
# Revision 1.3  2005/05/24 21:22:00  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2005/05/23 23:59:24  fds
# Frontend Restore
#
# Revision 1.1  2005/03/01 02:03:17  mjk
# moved from core to base
#
# Revision 1.18  2005/02/16 06:03:50  phil
# Missing space on "--dump output"
#
# Revision 1.17  2005/02/09 22:41:31  phil
# Now sports a --dump and other command line features for building the networks
# table. Flags added: --no-modify == do not modify existing entry
#                     --dryrun == print the insert/update query but don't run
# Setting --option="None" will cause this to be NULL in the database. Option can
# be mac, ip, netmask, gateway, Name, Module
# If updating an entry and flag not specified on the command line, value in
# DB is used.
#
# Revision 1.16  2004/10/06 20:29:08  bruno
# fix for bug 48
#
# Revision 1.15  2004/08/16 22:20:05  bruno
# minor bug fix for when you specify a hostname on the command line
#
# Revision 1.14  2004/06/22 04:54:12  mjk
# - more anal formating for --list
# - fixed hostname output for --list
# - fixed update/insert decision (did not work for unused eth1 nics)
# - some minor cleanup
#
# Revision 1.13  2004/06/16 23:57:03  fds
# Added --no-update flag (good for batches)
#
# Revision 1.12  2004/06/16 21:37:32  fds
# Tweaks: delete works.
#
# Revision 1.11  2004/06/16 21:27:47  fds
# Checking for existance of interface: if not present do an insert, otherwise
# update. Needed for soft (tunnelling, etc) interfaces.
#
# Also transformed into a rocks.sql.application.
#
# Revision 1.10  2004/03/25 03:15:52  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.9  2004/03/04 19:57:49  bruno
# added gateway column to networks table -- it is populated by add-extra-nic
# and ConfigNetworks writes the GATEWAY field into the ifcfg file
#
# Revision 1.8  2004/02/06 00:43:55  fds
# Schema migration.
#
# Revision 1.7  2004/02/04 17:39:39  bruno
# on what interface do you want to install?
#
# Revision 1.6  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.5  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.4  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.3  2002/10/18 21:58:01  mjk
# remove +x bit
#
# Revision 1.2  2002/10/18 03:45:36  phil
# Insert,deleting,listing now work.
#
# Revision 1.1  2002/10/17 17:34:27  phil
# Manipulates the networks table for adding extra nics.
# Right now just just listing of contents
#
#
# add-extra-nic -- adds an entry to the networks table for a particular
# node.
#
# Synopsis
#	add-extra-nic --if=<if name> --ip=<ip addr> --netmask=<netmask> 
#		--gateway=<gateway>  --dump
#		[--del] [--db=<database>] [--user=user] 
#		[--pw=password] [node]
#       
#   example: add 192.168.2.10/24 to interface eth1 on node compute-0-0
#		with gateway 192.168.2.1
#
#   add-extra-nic -if eth1 --ip 192.168.2.10 --netmask 255.255.25.0 \
#		--gateway=192.168.2.1 compute-0-0
#

print 'add-extra-nic is no longer supported. please use:'
print '\n\trocks add host interface\n'

