/*
 * $Id: misc-network.js,v 1.10 2011/07/23 02:30:14 phil Exp $
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		         version 5.4.3 (Viper)
 * 
 * Copyright (c) 2000 - 2011 The Regents of the University of California.
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
 * 	Development Team at the San Diego Supercomputer Center at the
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
 * $Log: misc-network.js,v $
 * Revision 1.10  2011/07/23 02:30:14  phil
 * Viper Copyright
 *
 * Revision 1.9  2010/09/07 23:52:46  bruno
 * star power for gb
 *
 * Revision 1.8  2009/05/01 19:06:48  mjk
 * chimi con queso
 *
 * Revision 1.7  2008/10/18 00:55:45  mjk
 * copyright 5.1
 *
 * Revision 1.6  2008/03/06 23:41:30  mjk
 * copyright storm on
 *
 * Revision 1.5  2007/06/23 04:03:18  mjk
 * mars hill copyright
 *
 * Revision 1.4  2006/09/11 22:47:00  mjk
 * monkey face copyright
 *
 * Revision 1.3  2006/08/17 23:01:23  bruno
 * validate the fields that will be used to make a server certificate and
 * make sure the don't have a (") or a (/) character in them.
 *
 * make sure the Certificate Country is only two characters
 *
 * do better a IP address validation. in the previous code 10.0.-0.0 would
 * pass as a valid IP address because parseInt(-0) returned 0. make sure the
 * first character is a number.
 *
 * Revision 1.2  2006/08/10 00:09:24  mjk
 * 4.2 copyright
 *
 * Revision 1.1  2006/07/22 01:40:12  bruno
 * added validation functions to all screens
 *
 *
 */

function check_gateway()
{
	var doc = top.workarea.document;
	var retval = true;

	/*
	 * the user-input variables
	 */
	var PublicGateway = doc.getElementsByName(
					'Kickstart_PublicGateway')[0];

	return(check_ipaddr(PublicGateway));
}

function check_dns()
{
	var doc = top.workarea.document;
	var retval = true;
	var i = 0;
	var hosts = new Array();

	/*
	 * the user-input variables
	 */
	var PublicDNSServers = doc.getElementsByName(
					'Kickstart_PublicDNSServers')[0];

	hosts = PublicDNSServers.value.split(',');

	for (i = 0; i < hosts.length; ++i) {
		if (convertToOctets(hosts[i]) == null) {
			PublicDNSServers.setAttribute("class",
						"ProInputError Padded");

			msg = '"' + hosts[i] + '"';
			msg += ' is not a valid IP address';
			top.status.printStatus(msg);

			retval = false;
			break;
		} else {
			PublicDNSServers.setAttribute("class",
						"ProInput Padded");

			/*
			 * clear the status message
			 */
			top.status.printStatus('');
		}
	}

	return(retval);
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

