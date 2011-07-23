/*
 * $Id: sec_channel_server.c,v 1.3 2011/07/23 02:30:50 phil Exp $
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
 * $Log: sec_channel_server.c,v $
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

#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>

int *
sec_channel_ping_1_svc(struct svc_req *rqstp)
{
	static int  result;
	struct sockaddr_in *addr;
	char *ipaddr;
	int status;
	int pid;
	struct hostent *h;
	
	switch(pid = fork()){
		case -1:		/*Fork failed*/
			result = -1;
			break;

		case 0:			/* Child */

			addr = &rqstp->rq_xprt->xp_raddr;
			ipaddr = (char *)malloc(sizeof(char)*INET_ADDRSTRLEN);
			ipaddr = (char *)inet_ntop(AF_INET, &addr->sin_addr, ipaddr, INET_ADDRSTRLEN);
			h = (struct hostent *)gethostbyaddr(&addr->sin_addr, INET_ADDRSTRLEN, AF_INET);

			printf("%s\t%s\n", h->h_name, ipaddr);

			status = execl("/opt/rocks/bin/rocks", "rocks",
				"sync","host","sharedkey",h->h_name, NULL);
			exit(status);

		default:		/* Parent */
			result = 0;
			break;
		}

	return &result;
}
