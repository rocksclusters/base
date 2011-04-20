/*
 * $Id: sec_channel_server.c,v 1.2 2011/04/20 05:55:04 anoop Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: sec_channel_server.c,v $
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
