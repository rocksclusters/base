/*
 * $Id: sec_channel_server.c,v 1.9 2012/11/27 00:48:43 phil Exp $
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
 * $Log: sec_channel_server.c,v $
 * Revision 1.9  2012/11/27 00:48:43  phil
 * Copyright Storm for Emerald Boa
 *
 * Revision 1.8  2012/08/04 06:34:29  phil
 * Have nodes ask to have their secure attributes set as well as the 411 shared
 * key.
 *
 * Revision 1.7  2012/05/06 05:48:48  phil
 * Copyright Storm for Mamba
 *
 * Revision 1.6  2012/03/01 22:19:11  phil
 * Use sigaction instead of signal.
 * Setting signal process in the child process of sec_channel_svc is not needed.
 *
 * Revision 1.5  2011/08/19 06:04:38  anoop
 * - Added debugging support.
 * - Does not create zombie processes anymore
 *
 * Revision 1.4  2011/08/04 02:02:47  anoop
 * Use ip address instead of hostname. This way, failure
 * during host lookup does not screw with request.
 *
 * Revision 1.3  2011/07/23 02:30:50  phil
 * Viper Copyright
 *
 * Revision 1.2  2011/04/20 05:55:04  anoop
 * Fixed server to daemonize itself
 *
 * Revision 1.1  2011/04/11 22:41:50  anoop
 * RPC service that initiates transfer of shared 411 key
 *
 */


#include "sec_channel.h"
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <signal.h>

#include <netinet/in.h>
#include <netdb.h>
#include <tcpd.h>

#include <syslog.h>


/*
 * returns nonzero if tcpd/libwrap allows this connection
 * returns 0 if tcpd/libwrap denies this connection
 */
int 
tcpd_allowed(struct svc_req *rqstp)
{
	static char remhost[1024];
	int result;

	assert(rqstp);
	assert(rqstp->rq_xprt);

	/* get the hostname from the IP */
	result = getnameinfo((struct sockaddr *) &(rqstp->rq_xprt->xp_raddr), 
	                     rqstp->rq_xprt->xp_addrlen, remhost, 1024, 
			     NULL, 0, 0);

	/* stop here if getnameinfo blew up */
	if( result && result != EAI_AGAIN && result != EAI_NONAME ) {
		syslog(LOG_DEBUG,"getnameinfo(%s) failed: %s",
		       inet_ntoa(rqstp->rq_xprt->xp_raddr.sin_addr),
		       strerror(result));
		return 0;
	}

	/* do the libwrap check */
	result = hosts_ctl(SERVICE_NAME, remhost,
	                   inet_ntoa(rqstp->rq_xprt->xp_raddr.sin_addr),
		           STRING_UNKNOWN);
	if ( result ) return result; 
       
	/* report failures */
	syslog(LOG_DEBUG,"hosts_ctl(\"%s\",%s,%s) rejected connection",
	       SERVICE_NAME, remhost,
  	       inet_ntoa(rqstp->rq_xprt->xp_raddr.sin_addr));
 
       return 0;
} /* tcpd_allowed */


int *
sec_channel_ping_1_svc(int *argp, struct svc_req *rqstp)
{
	static int  result;
	struct sockaddr_in *addr;
	char *ipaddr;
	int status;
	int pid;

	/* libwrap check - stop as soon as possible if we shouldn't talk to
	 * this host. 
	 */
	if(!tcpd_allowed(rqstp)) 
	{
		result = 0;
		return &result; 
	}

	switch(pid = fork()){
		case -1:		/*Fork failed*/
			result = -1;
			return &result;

		case 0:			/* Child */
			break;
		default:		/* Parent */
			result = 0;
			return &result;
	}
	
	addr = &rqstp->rq_xprt->xp_raddr;
	ipaddr = (char *)malloc(sizeof(char)*INET_ADDRSTRLEN);
	ipaddr = (char *)inet_ntop(AF_INET, &addr->sin_addr, ipaddr, INET_ADDRSTRLEN);

	syslog(LOG_DEBUG, "Received request from %s", ipaddr);
	fprintf(stderr, "Received request from %s\n", ipaddr);
	if (*argp == 0)
		status = execl("/opt/rocks/bin/rocks", "rocks",
			"sync","host","sharedkey",ipaddr, NULL);
	else
		status = execl("/opt/rocks/bin/rocks", "rocks",
			"sync","host","sec_attr",ipaddr, NULL);
	exit(status);
}
