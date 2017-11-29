#!/bin/sh
# This script uses the Rocks graph to set up central roll serving.
# good for a machine that was bootstrap0'ed

# $Id: bootstrap-central.sh,v 1.3 2012/11/27 00:48:00 phil Exp $
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
# $Log: bootstrap-central.sh,v $
# Revision 1.3  2012/11/27 00:48:00  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.2  2012/05/06 05:48:07  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/02/02 19:59:01  phil
# Enable simple setup of a central roll server on a bootstrap0'ed machine
#
#
# Define Some attributes

PublicHostname=`hostname`
PrivateNetwork=127.0.0.1
PrivateNetmask=255.0.0.0
PrivateNetwork=127.0.0.0
Info_ClusterName="$PublicHostname"
Info_ClusterContact="root@$PublicHostname"
Info_CertificateOrganization=local
Info_CertificateLocality="San Diego"
Info_CertificateState=CA
Info_CertificateCountry=US

MyAttrs="{'hostname':'$PublicHostname', 'HttpRoot':'/var/www/html','os':'linux', 'Kickstart_PublicHostname':'$PublicHostname', 'Kickstart_PrivateNetwork':'$PrivateNetwork', 'Kickstart_PrivateNetmask':'$PrivateNetmask', 'Kickstart_PrivateNetwork':'$PrivateNetwork', 'Info_ClusterName':'$Info_ClusterName', 'Info_ClusterContact':'$Info_ClusterContact', 'Info_CertificateOrganization':'$Info_CertificateOrganization', 'Info_CertificateLocality':'$Info_CertificateLocality',  'Info_CertificateState':'$Info_CertificateState', 'Info_CertificateCountry':'$Info_CertificateCountry'}"


# Extract the appropriate post sections into a script
tmpfile=$(/bin/mktemp)
/bin/cat nodes/ca.xml nodes/ssl.xml nodes/apache.xml nodes/central.xml | /opt/rocks/bin/rocks report post attrs="$MyAttrs"  > $tmpfile
if [ $? != 0 ]; then
        echo "FAILURE to create script for bootstrapping the Database"
	/bin/rm $tmpfile
        exit -1
fi

#
# Actually run the created script 
# 
/bin/sh $tmpfile
/bin/rm $tmpfile

if [ ! -d /var/www/html/install ]; then
	ln -s /export/rocks/install /var/www/html
fi
# Restart Httpd
echo Restarting HTTP
service httpd restart

# Don't forget to enable WWW on firewall
echo "==============================="
echo "You may need to set firewall rules"
echo "perhaps something like:"
echo "        iptables -I INPUT -p tcp --dport http --source 137.110.119.0/24 -j ACCEPT"

# And SELINUX
echo "==============================="
echo "You may need to turn off selinux"
echo "try 'echo 1 > selinux/enforce'"
