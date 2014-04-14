/* $Id: 411-alert.c,v 1.11 2012/11/27 00:48:08 phil Exp $
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		       version 6.1.1 (Sand Boa)
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
 * $Log: 411-alert.c,v $
 * Revision 1.11  2012/11/27 00:48:08  phil
 * Copyright Storm for Emerald Boa
 *
 * Revision 1.10  2012/08/09 23:16:48  clem
 * bug fix for the following problem:
 *
 * Centos 6.* libtirpc-0.2.1 are bugged cannot get return value from the server
 * https://bugzilla.redhat.com/show_bug.cgi?format=multiple&id=781880
 *
 * Revision 1.9  2012/05/06 05:48:18  phil
 * Copyright Storm for Mamba
 *
 * Revision 1.8  2011/07/23 02:30:24  phil
 * Viper Copyright
 *
 * Revision 1.7  2011/01/25 23:14:40  mjk
 * actually builds
 *
 * Revision 1.6  2010/11/04 02:20:15  anoop
 * Solaris compatibility fixes
 *
 * Revision 1.5  2010/10/21 22:03:18  mjk
 * - linux and solaris both send only .info and above to the frontend
 *   debug stays off the network
 * - changed syslog levels to debug (see above)
 * - proper wait return code handling with W* macros
 *
 * Revision 1.4  2010/10/21 20:51:17  mjk
 * - timestamp is now a timeval (microseconds)
 * - re-entry testing is done in 411-alert-handler using a pickle file for state
 * - more logging
 *
 * Looks good, but need to turn down the logging to keep the network quite.
 *
 * Revision 1.3  2010/10/21 16:59:45  mjk
 * more logging
 * copy the arg strings in case RPC is doing something odd
 *
 * Revision 1.2  2010/10/20 01:41:53  mjk
 * daemonized
 * calls out to python code for 411-listen
 *
 * Revision 1.1  2010/10/19 23:06:29  mjk
 * c is hard
 *
 */

#include <stdio.h>
#include <syslog.h>

#if defined (__SVR4) && defined (__sun)
#include <stdlib.h>
#include <strings.h>
#define PORTMAP
#endif

#include <rpc/rpc.h>
#include <rpc/pmap_clnt.h>
#include <sys/socket.h>
#include <netdb.h>
#include <time.h>
#include "channel.h"

static bool_t callback(caddr_t, struct sockaddr_in *);

int
main(int argc, char *argv[])
{
	int				result;
	channel_411_alert_1_argument	args;
	enum clnt_stat			status;
	struct timeval			tv;
	double				time;

	if (argc != 3) {
		fprintf(stderr, "usage: %s filename signature\n", argv[0]);
		exit(-1);
	}

	openlog("411-alert", LOG_PID, LOG_LOCAL0);

	gettimeofday(&tv, NULL);

	args.filename	= strdup(argv[1]);
	args.signature	= strdup(argv[2]);
	args.sec	= tv.tv_sec;
	args.usec	= tv.tv_usec;

	time = tv.tv_sec + (float)tv.tv_usec / 1e6;
	syslog(LOG_DEBUG, "call sent (file=\"%s\", time=%.6f)", args.filename, time);

	status = clnt_broadcast(CHANNEL_PROG, CHANNEL_VERS, CHANNEL_411_ALERT,
				(xdrproc_t)xdr_channel_411_alert_1_argument,
				(caddr_t)&args,
				(xdrproc_t)xdr_int, (caddr_t)&result,
				callback);

//Centos 6.* libtirpc-0.2.1 are bugged cannot get return value from the server
//https://bugzilla.redhat.com/show_bug.cgi?format=multiple&id=781880
#ifndef ROCKS6
	if ( status != RPC_SUCCESS ) {
		syslog(LOG_ERR, "call failed (%d)", status);
		return -1;
	}
#endif

	free(args.filename);
	free(args.signature);

	return 0;
} /* main */


/* callback
 *
 * Gets called for every completed RPC.  The 411_alert RPC counts
 * the number of times it has been called (using timestamp).  Once we have
 * heard fron a single host more than once return TRUE and stop
 * broadcasting.
 */

static bool_t
callback(caddr_t result, struct sockaddr_in *addr)
{
	struct hostent *he;
	int		count = *(int *)result;


	he = gethostbyaddr(&addr->sin_addr, sizeof(addr->sin_addr), 
			   addr->sin_family);

	if ( he ) {
		syslog(LOG_DEBUG, "call returned (host=%s, status=%d)", he->h_name, count);
	}
	else {
		syslog(LOG_ERR, "reply from unknown host");
		return 0;
	}

	/* 411-alert will return
	 *	 0 - file updated
	 *	 1 - duplicate request (file not fetched/updated)
	 *	-1 - system error
	 *
	 * Once a single duplicate has been detected stop the broadcast by returning 1.
	 */
	return (count > 0) ? 1 : 0;
} /* callback */

