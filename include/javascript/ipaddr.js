/*
 * $Id: ipaddr.js,v 1.9 2008/10/18 00:55:45 mjk Exp $
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		           version 5.1  (VI)
 * 
 * Copyright (c) 2000 - 2008 The Regents of the University of California.
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
 * $Log: ipaddr.js,v $
 * Revision 1.9  2008/10/18 00:55:45  mjk
 * copyright 5.1
 *
 * Revision 1.8  2008/03/06 23:41:30  mjk
 * copyright storm on
 *
 * Revision 1.7  2007/06/23 04:03:18  mjk
 * mars hill copyright
 *
 * Revision 1.6  2006/09/11 22:47:00  mjk
 * monkey face copyright
 *
 * Revision 1.5  2006/08/17 23:01:23  bruno
 * validate the fields that will be used to make a server certificate and
 * make sure the don't have a (") or a (/) character in them.
 *
 * make sure the Certificate Country is only two characters
 *
 * do better a IP address validation. in the previous code 10.0.-0.0 would
 * pass as a valid IP address because parseInt(-0) returned 0. make sure the
 * first character is a number.
 *
 * Revision 1.4  2006/08/10 00:09:24  mjk
 * 4.2 copyright
 *
 * Revision 1.3  2006/07/22 01:40:12  bruno
 * added validation functions to all screens
 *
 * Revision 1.2  2006/03/17 20:27:34  bruno
 * added clusterinfo screen validator and put on copyright
 *
 *
 */

function convertToOctets(ipAddr)
{
	var	octets = ipAddr.split('.');
	var	x = new Array();

	if (octets.length != 4) {
		return(null);
	}

	for (i = 0 ; i < 4 ; ++i) {
		/*
		 * make sure the first character is a number
		 */
		a = octets[i].search('[0-9]+');
		if (a != 0) {
			return(null);
		}

		/*
		 * a clever hack to convert a string to a number
		 */
		x[i] = octets[i] * 1;

		if (isNaN(x[i]) || (x[i] < 0) || (x[i] > 255)) {
			return(null);
		}
	}

	return(x);
}

function check_ipaddr(ipAddr)
{
	var	retval = true;

	if (convertToOctets(ipAddr.value) == null) {
		ipAddr.setAttribute("class", "ProInputError Padded");

		msg = '"' + ipAddr.value + '"';
		msg += ' is not a valid IP address';
		top.status.printStatus(msg);

		retval = false;
	} else {
		ipAddr.setAttribute("class", "ProInput Padded");

		/*
		 * clear the status message
		 */
		top.status.printStatus('');
	}

	return(retval);
}

function getNetwork(ipAddr, ipNetmask)
{
	/*
	 * return ipAddr 'and' ipNetmask
	 */
	var	a = convertToOctets(ipAddr);
	var	b = convertToOctets(ipNetmask);
	var	ipNetwork = '';

	if ((a == null) || (b == null)) {
		return(null);
	}

	for (i = 0 ; i < 4 ; ++i) {
		ipNetwork += (a[i] & b[i]);

		if (i != 3) {
			ipNetwork += '.';
		}
	}

	return(ipNetwork);
}

function getBroadcast(ipAddr, ipNetmask)
{
	/*
	 * return ipNetwork 'or' the bitwise not of ipNetmask
	 */
	var	a = convertToOctets(ipAddr);
	var	b = convertToOctets(ipNetmask);
	var	ipBroadcast = '';
	var	x = 0;

	if ((a == null) || (b == null)) {
		return(null);
	}

	for (i = 0 ; i < 4 ; ++i) {
		
		/*
		 * this is needed becuase all bitwise functions are
		 * performed on signed numbers and i don't see how to
		 * force a number to be unsigned
		 */
		x = ((a[i] & 0x000000ff) | ((~b[i]) & 0x000000ff));
/*
		if (x < 0) {
			x = ~x;
		}
*/
		ipBroadcast += x;

		if (i != 3) {
			ipBroadcast += '.';
		}
	}

	return(ipBroadcast);
}

function getNetmaskCIDR(ipNetmask)
{
	/*
	 * count the number of sequential one's in the netmask
	 */
	var	a = convertToOctets(ipNetmask);
	var	x = 0;
	var	count = 0;
	var	done = 0;

	if (a == null) {
		return(null);
	}

	for (i = 0 ; i < 4 && !done; ++i) {

		x = parseInt(a[i]);

		for (j = 0; j < 8 && !done; ++j) {
			if (x & 0x80) {
				count += 1;
			} else {
				done = 1;
			}
			x = x << 1;
		}
	}

	return(count);
}

