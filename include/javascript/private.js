/*
 * $Idi$
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		         version 6.2 (SideWinder)
 * 
 * Copyright (c) 2000 - 2014 The Regents of the University of California.
 * All rights reserved.	
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 * 
 * 1. Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 * 
 * 2. Redistributions in binary form must reproduce the above copyright
 * notice unmodified and in its entirety, this list of conditions and the
 * following disclaimer in the documentation and/or other materials provided 
 * with the distribution.
 * 
 * 3. All advertising and press materials, printed or electronic, mentioning
 * features or use of this software must display the following acknowledgement: 
 * 
 * 	"This product includes software developed by the Rocks(r)
 * 	Cluster Group at the San Diego Supercomputer Center at the
 * 	University of California, San Diego and its contributors."
 * 
 * 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
 * neither the name or logo of this software nor the names of its
 * authors may be used to endorse or promote products derived from this
 * software without specific prior written permission.  The name of the
 * software includes the following terms, and any derivatives thereof:
 * "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
 * the associated name, interested parties should contact Technology 
 * Transfer & Intellectual Property Services, University of California, 
 * San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
 * Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
 * 
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 * OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
 * IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 * @Copyright@
 * 
 * $Log: private.js,v $
 * Revision 1.3  2012/11/27 00:48:00  phil
 * Copyright Storm for Emerald Boa
 *
 * Revision 1.2  2012/05/06 05:48:09  phil
 * Copyright Storm for Mamba
 *
 * Revision 1.1  2012/03/13 06:03:13  phil
 * Support generic names for public and private interface on frontend
 *
 */

function check_private_ip()
{
	var doc = top.workarea.document;

	/*
	 * the user-input variables
	 */
	var PrivateAddress = doc.getElementsByName(
					'Kickstart_PrivateAddress')[0];

	return(check_ipaddr(PrivateAddress));
}

function process_private_eth(e)
{
	var doc = top.workarea.document;

	/*
	 * the user-input variables
	 */
	var PrivateAddress = doc.getElementsByName(
					'Kickstart_PrivateAddress')[0];
	var PrivateNetmask = doc.getElementsByName(
					'Kickstart_PrivateNetmask')[0];

	/*
	 * the hidden variables that will be populated by this function
	 */
	var PrivateNetwork = doc.getElementsByName(
					'Kickstart_PrivateNetwork')[0];
	var PrivateBroadcast = doc.getElementsByName(
					'Kickstart_PrivateBroadcast')[0];
	var PrivateNetmaskCIDR = doc.getElementsByName(
					'Kickstart_PrivateNetmaskCIDR')[0];
	var PrivateKickstartHost = doc.getElementsByName(
					'Kickstart_PrivateKickstartHost')[0];
	var PrivateNTPHost = doc.getElementsByName(
					'Kickstart_PrivateNTPHost')[0];
	var PrivateGateway = doc.getElementsByName(
					'Kickstart_PrivateGateway')[0];
	var PrivateDNSServers = doc.getElementsByName(
					'Kickstart_PrivateDNSServers')[0];
	var PrivateSyslogHost = doc.getElementsByName(
					'Kickstart_PrivateSyslogHost')[0];


	if (check_ipaddr(PrivateNetmask) == false) {
		return(false);
	}

	/*
	 * assign the easy ones
	 */
	PrivateKickstartHost.value = PrivateAddress.value;
	PrivateNTPHost.value = PrivateAddress.value;
	PrivateGateway.value = PrivateAddress.value;
	PrivateDNSServers.value = PrivateAddress.value;
	PrivateSyslogHost.value = PrivateAddress.value;

	/*
	 * now get the harder ones
	 */
	PrivateNetwork.value = getNetwork(PrivateAddress.value,
					PrivateNetmask.value); 
	PrivateBroadcast.value = getBroadcast(PrivateAddress.value,
					PrivateNetmask.value); 
	PrivateNetmaskCIDR.value = getNetmaskCIDR(PrivateNetmask.value); 

	return(true);
}


function generate_multicast(e)
{
	var doc = top.workarea.document;

	/*
	 * the user-input variables
	 */
	var Multicast = doc.getElementsByName('Kickstart_Multicast')[0];

	/*
	 * generate a random multicast address
	 *
	 * don't choose 224 or 232 (RFC 1700) for the first octet
	 */
	min = 225;
	max = 239;
	while (true) {
		a = Math.floor(Math.random() * (max - min + 1) + min);
		if (a != 232) {
			break;
		}
	}

	min = 1;
	max = 254;
	b = Math.floor(Math.random() * (max - min + 1) + min);
	c = Math.floor(Math.random() * (max - min + 1) + min);
	d = Math.floor(Math.random() * (max - min + 1) + min);
	
	Multicast.value = a + '.' + b + '.' + c + '.' + d;

	return(true);
}

