#
# $Id: ssh-key.sh,v 1.15 2012/11/27 00:48:32 phil Exp $
#
# generate a ssh key if one doesn't exist
#
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
#
# $Log: ssh-key.sh,v $
# Revision 1.15  2012/11/27 00:48:32  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.14  2012/08/10 23:49:10  phil
# Support hostbased authentication for ssh.  Inspired by Roy Dragseth.
#
# Revision 1.13  2012/06/26 22:45:45  clem
# Minor fix on file permission as pointed out by Ventre, Brian D. on 2012-06-14
# on the mailing list
#
# Revision 1.12  2012/05/06 05:48:39  phil
# Copyright Storm for Mamba
#
# Revision 1.11  2011/11/07 21:43:29  anoop
# Don't try to be too efficient or clever
#
# Revision 1.10  2011/08/22 23:44:00  anoop
# Cleaner re-implementation of creating ssh keys. Now supports tcsh correctly
#
# Revision 1.9  2011/08/06 14:56:25  phil
# more defensive about when to make hard link
#
# Revision 1.8  2011/08/05 22:26:06  anoop
# - Cleanup
# - Check for private key
# - Check UID: If root, create key without passphrase
# 	     If normal user, create key interactively
#
# Revision 1.7  2011/08/04 02:03:51  anoop
# Move creation of hard link to ssh public key
# from node file to profile.d startup script.
#
# Revision 1.6  2011/07/23 02:30:42  phil
# Viper Copyright
#
# Revision 1.5  2010/09/07 23:53:03  bruno
# star power for gb
#
# Revision 1.4  2009/05/01 19:07:05  mjk
# chimi con queso
#
# Revision 1.3  2008/10/18 00:55:58  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:41  mjk
# copyright storm on
#
# Revision 1.1  2007/08/13 19:31:00  bruno
# get the spec file out of rocks-config. this requires building a new
# package named : rocks-config-server
#
# Revision 1.8  2007/06/23 04:03:21  mjk
# mars hill copyright
#
# Revision 1.7  2006/09/11 22:47:05  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:09:28  mjk
# 4.2 copyright
#
# Revision 1.5  2005/10/19 12:59:49  bruno
# remove dead code that causes an error message on first login as root
#
# Revision 1.4  2005/10/12 18:08:34  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:02:14  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:21:50  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:43  mjk
# moved from core to base
#
# Revision 1.28  2005/01/06 16:12:39  bruno
# make sure /root/.ssh is readable by apache.
#
# fix for bug 102.
#
# Revision 1.27  2004/08/25 05:25:38  bruno
# move from ssh v1 to ssh v2
#
# (bug 17)
#
# Revision 1.26  2004/03/25 03:15:29  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.25  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.24  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.23  2003/05/21 18:57:31  mjk
# grid integration checkpoint
#
# Revision 1.22  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.21  2003/02/12 01:19:17  fds
# Dont need quotes around var.
#
# Revision 1.20  2003/02/12 01:18:21  fds
# INTERACTIVE can only be false or implied true. Need dodouble [[s around test.
#
# Revision 1.19  2003/02/11 17:52:12  bruno
# one more pass on the interactive stuff
#
# Revision 1.18  2003/02/11 17:10:24  bruno
# changed around the interactive stuff a bit.
#
# Revision 1.17  2003/02/10 23:42:16  fds
# A safer way to invoke ssh-host checking.
#
# Revision 1.16  2003/02/07 01:12:25  fds
# An additional check.
#
# Revision 1.15  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.14  2002/08/27 23:30:17  bruno
# removed SSL cert creation
#
# Revision 1.13  2002/05/07 22:53:50  bruno
# added '-t' flag for new version of ssh-keygen
#
# Revision 1.12  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.11  2001/05/09 20:17:13  bruno
# bumped copyright 2.1
#
# Revision 1.10  2001/04/10 14:16:27  bruno
# updated copyright
#
# Revision 1.9  2001/03/06 15:11:45  bruno
# if root user, then make sure ssh and cert permissions are right for
# cluster-dist
#
# Revision 1.8  2001/02/20 15:53:37  bruno
# rebuild kickstart files only once.
#
# Revision 1.7  2001/02/14 21:42:33  mjk
# Rebuild kickstart files after ss-genca
#
# Revision 1.6  2001/02/14 20:16:30  mjk
# Release 2.0 Copyright
#
# Revision 1.5  2001/02/14 19:43:28  mjk
# Also generate the SSL CA Certificate
#
# Revision 1.4  2001/02/06 21:10:22  bruno
# fixed the 'find' so it will automount /home/install/
#
# Revision 1.3  2001/02/02 18:34:09  bruno
# add auto freshing of kickstart files after root builds it's ssh-key
#
# Revision 1.2  2000/12/12 23:45:39  bruno
# tweaks to fix dumbass mistakes
#
# Revision 1.1  2000/12/12 23:36:49  bruno
# initial release

# Some constants
SSH_CMD="ssh-keygen -t rsa -f $HOME/.ssh/id_rsa -v"
SSH_KEY_LINK=/etc/ssh/authorized_keys/id_rsa.pub

# Function to check if we should autogen keys
do_autogen()
{
[ -f /etc/ssh/rocks_autogen_user_keys ] && return 1 || return 0
}

# Function to create ssh keys
create_key(){
echo
echo "It appears that you have not set up your ssh key."
echo "This process will make the files:"
echo "    " $HOME/.ssh/id_rsa.pub
echo "    " $HOME/.ssh/id_rsa
echo "    " $HOME/.ssh/authorized_keys
echo
# If root, create ssh key with blank passphrase
# Otherwise interact with user to ask passphrase
[ $UID -eq 0 ] && $SSH_CMD -N "" || $SSH_CMD

# Copy public key to authorized_keys file.
cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys

chmod 600 $HOME/.ssh/authorized_keys
chmod g-w $HOME
}

# Function to check existence of ssh key
check_key(){
[ -f $HOME/.ssh/id_rsa ] && return 0 || return 1
}

# Checks for hard link to root's ssh-key
check_hard_link(){
[ ! -f $SSH_KEY_LINK ] && return 1
[ `stat -c "%h" $SSH_KEY_LINK` -eq 2 ] && return 0 || return 1
}

# Creates hard link to root's ssh-key
create_hard_link(){
	d=`dirname $SSH_KEY_LINK`
	SSH_PUB_KEY=/root/.ssh/id_rsa.pub
	mkdir -p $d
	rm -rf $SSH_KEY_LINK
	echo "Creating hard link to $SSH_PUB_KEY in $d"
	ln $SSH_PUB_KEY $SSH_KEY_LINK
	chmod a+rx $d
	chmod a+r $SSH_KEY_LINK
}

# If we're a normal user, and the ssh-key exists, and
# we are supposed to autogen the key, then return
if [ $UID -ge 500 ]; then
	do_autogen || check_key || create_key
fi

# We need special handling of root. We -need- an ssh key pair
# to be able to bootstrap the 411 shared key, and the 
# ssh hosts keys kept in the sec_attr database.  
if [ $UID -eq 0 ]; then
	check_key || create_key
	check_hard_link || create_hard_link
fi
