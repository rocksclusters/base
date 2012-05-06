/*
 * $Id: clusterinfo.js,v 1.19 2012/05/06 05:48:09 phil Exp $
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		         version 5.5 (Mamba)
 * 		         version 6.0 (Mamba)
 * 
 * Copyright (c) 2000 - 2012 The Regents of the University of California.
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
 * $Log: clusterinfo.js,v $
 * Revision 1.19  2012/05/06 05:48:09  phil
 * Copyright Storm for Mamba
 *
 * Revision 1.18  2011/07/23 02:30:14  phil
 * Viper Copyright
 *
 * Revision 1.17  2010/11/29 18:38:56  bruno
 * need to flag the apostrophe as a 'bad character'.
 *
 * Revision 1.16  2010/09/07 23:52:46  bruno
 * star power for gb
 *
 * Revision 1.15  2009/05/01 19:06:48  mjk
 * chimi con queso
 *
 * Revision 1.14  2008/10/18 00:55:45  mjk
 * copyright 5.1
 *
 * Revision 1.13  2008/03/06 23:41:30  mjk
 * copyright storm on
 *
 * Revision 1.12  2007/06/23 04:03:18  mjk
 * mars hill copyright
 *
 * Revision 1.11  2006/09/11 22:47:00  mjk
 * monkey face copyright
 *
 * Revision 1.10  2006/08/18 18:25:51  bruno
 * more error detection in the screens
 *
 * Revision 1.9  2006/08/17 23:01:23  bruno
 * validate the fields that will be used to make a server certificate and
 * make sure the don't have a (") or a (/) character in them.
 *
 * make sure the Certificate Country is only two characters
 *
 * do better a IP address validation. in the previous code 10.0.-0.0 would
 * pass as a valid IP address because parseInt(-0) returned 0. make sure the
 * first character is a number.
 *
 * Revision 1.8  2006/08/10 00:09:24  mjk
 * 4.2 copyright
 *
 * Revision 1.7  2006/07/22 01:40:12  bruno
 * added validation functions to all screens
 *
 * Revision 1.6  2006/07/21 19:15:28  bruno
 * if the user doesn't select a partitioning scheme, then choose
 * the default (auto) for them.
 *
 * Revision 1.5  2006/07/11 21:17:55  bruno
 * screen cleanup
 *
 * Revision 1.4  2006/06/05 17:57:33  bruno
 * first steps towards 4.2 beta
 *
 * Revision 1.3  2006/03/22 19:39:20  bruno
 * new absolute web page naming structure
 *
 * Revision 1.2  2006/03/19 23:18:12  bruno
 * network validation screens
 *
 * Revision 1.1  2006/03/17 20:27:34  bruno
 * added clusterinfo screen validator and put on copyright
 *
 *
 */

function process_dns(e)
{
	var doc = top.workarea.document;
	var retval = true;

	/*
	 * the user-input variables
	 */
	var PublicHostname = doc.getElementsByName(
					'Kickstart_PublicHostname')[0];

	/*
	 * the hidden variables that will be populated by this function
	 */
	var PublicDNSDomain = doc.getElementsByName(
					'Kickstart_PublicDNSDomain')[0];
	var PrivateHostname = doc.getElementsByName(
					'Kickstart_PrivateHostname')[0];

	if (check_ssl(PublicHostname) == false) {
		retval = false;
	} else {
		if (check_fqdn(PublicHostname) == false) {
			retval = false;
		} else {		
			str = PublicHostname.value.split('.');

			PrivateHostname.value = str[0];

			PublicDNSDomain.value = '';
			for (i = 1 ; i < str.length ; ++i) {
				PublicDNSDomain.value += str[i];
		
				if (i != (str.length - 1)) {
					PublicDNSDomain.value += '.';
				}
			}
		}
	}

	if (retval == true) {
		/*
		 * valid input. make sure the color of the user data
		 * is set to 'normal'
		 */
		PublicHostname.setAttribute("class", "ProInput Padded");

		/*
		 * clear the status message
		 */
		top.status.printStatus('');
	}

	return(retval);
}


function trimSpace(str) {
	return str.replace(/^\s+/g, '').replace(/\s+$/g, '');
}


function check_ssl(field) {
	/*
	 * make sure the fields that will be used to make the
	 * SSL key have valid characters
	 */
	var retval = true;
	var badchar = '';

	field.value = trimSpace(field.value);

	if (field.value.search('"') > -1) {
		badchar = '"';
	} else if (field.value.search('/') > -1) {
		badchar = '/';
	} else if (field.value.search("'") > -1) {
		badchar = "'";
	}

	if (badchar != '') {
		field.setAttribute("class", "ProInputError Padded");

		msg = 'The character (' + badchar + ') is not valid.';
		top.status.printStatus(msg);

		retval = false;
	}

	/*
	 * an SSL field must have at least one non-whitespace character
	 */
	if (field.value.length < 1) {
		field.setAttribute("class", "ProInputError Padded");

		msg = 'The value must be at least one character.';
		top.status.printStatus(msg);

		retval = false;
	}

	return(retval);
}

function validate_certificate_country(e)
{
	var doc = top.workarea.document;
	var retval = true;

	/*
	 * the user-input variables
	 */
	var CertificateCountry = doc.getElementsByName(
					'Info_CertificateCountry')[0];

	if (check_ssl(CertificateCountry) == false) {
		retval = false;
	} else if (CertificateCountry.value.length != 2) {
		CertificateCountry.setAttribute(
			"class", "ProInputError Padded");

		msg = 'The Certificate Country must be ';
		msg += 'exactly two characters in length.';
		top.status.printStatus(msg);

		retval = false;
	}

	if (retval == true) {
		/*
		 * valid input. make sure the color of the user data
		 * is set to 'normal'
		 */
		CertificateCountry.setAttribute("class", "ProInput Padded");

		/*
		 * clear the status message
		 */
		top.status.printStatus('');
	}

	return(retval);
}

function validate_certificate_state(e)
{
	var doc = top.workarea.document;
	var retval = true;

	/*
	 * the user-input variables
	 */
	var field = doc.getElementsByName(
					'Info_CertificateState')[0];

	if (check_ssl(field) == false) {
		retval = false;
	}

	if (retval == true) {
		/*
		 * valid input. make sure the color of the user data
		 * is set to 'normal'
		 */
		field.setAttribute("class", "ProInput Padded");

		/*
		 * clear the status message
		 */
		top.status.printStatus('');
	}

	return(retval);
}

function validate_certificate_locality(e)
{
	var doc = top.workarea.document;
	var retval = true;

	/*
	 * the user-input variables
	 */
	var field = doc.getElementsByName(
					'Info_CertificateLocality')[0];

	if (check_ssl(field) == false) {
		retval = false;
	}

	if (retval == true) {
		/*
		 * valid input. make sure the color of the user data
		 * is set to 'normal'
		 */
		field.setAttribute("class", "ProInput Padded");

		/*
		 * clear the status message
		 */
		top.status.printStatus('');
	}

	return(retval);
}

function validate_certificate_organization(e)
{
	var doc = top.workarea.document;
	var retval = true;

	/*
	 * the user-input variables
	 */
	var field = doc.getElementsByName(
					'Info_CertificateOrganization')[0];

	if (check_ssl(field) == false) {
		retval = false;
	}

	if (retval == true) {
		/*
		 * valid input. make sure the color of the user data
		 * is set to 'normal'
		 */
		field.setAttribute("class", "ProInput Padded");

		/*
		 * clear the status message
		 */
		top.status.printStatus('');
	}

	return(retval);
}

function validate_cluster_name(e)
{
	var doc = top.workarea.document;
	var retval = true;

	/*
	 * the user-input variables
	 */
	var field = doc.getElementsByName(
					'Info_ClusterName')[0];

	if (check_ssl(field) == false) {
		retval = false;
	}

	if (retval == true) {
		/*
		 * valid input. make sure the color of the user data
		 * is set to 'normal'
		 */
		field.setAttribute("class", "ProInput Padded");

		/*
		 * clear the status message
		 */
		top.status.printStatus('');
	}

	return(retval);
}

