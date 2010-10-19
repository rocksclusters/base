/* $Id: server.c,v 1.1 2010/10/19 23:06:29 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: server.c,v $
 * Revision 1.1  2010/10/19 23:06:29  mjk
 * c is hard
 *
 */

#include <stdio.h>
#include <string.h>
#include <syslog.h>
#include <assert.h>
#include <rpc/pmap_clnt.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <rocks/channel.h>
#include <rocks/hexdump.h>


#define DEBUG 1

extern void channel_prog_1(struct svc_req *rqstp, register SVCXPRT *transp);


int *
channel_ping_1_svc(struct svc_req *rqstp)
{
	static int  result = 1;

	assert(rqstp);
	syslog(LOG_INFO, "ping received");

	return &result;
} /* channel_ping_1_svc */


int *
channel_411_alert_1_svc(char *filename, unsigned long time, char *signature,
			struct svc_req *rqstp)
{
	static int	result = 1;
	static time_t	last = 0; /* time of last call */

	assert(filename);
	assert(rqstp);


	if ( time != last ) {
		result = 1;
		last   = time;

		syslog(LOG_INFO, "411_alert received");

#ifdef DEBUG
		syslog(LOG_DEBUG, "411_alert file=\"%s\" time=%ld sig=\"%s\"",
		       filename, time, signature);
#endif
	}
	else {
		syslog(LOG_INFO, "411_alert received (dup)");
		result++;	/* count number of dups */
	}

	return &result;
} /* channel_alert_1_svc */





int
main(int argc, char *argvp[])
{
	register SVCXPRT *transp;

	openlog("channeld", LOG_PID, LOG_LOCAL0);
	syslog(LOG_INFO, "starting service");

	pmap_unset(CHANNEL_PROG, CHANNEL_VERS);

	transp = svcudp_create(RPC_ANYSOCK);
	if ( !transp ) {
		syslog(LOG_ERR, "%s", "cannot create udp service.");
		exit(1);
	}

	if ( !svc_register(transp, CHANNEL_PROG, CHANNEL_VERS,
			   channel_prog_1, IPPROTO_UDP) )
	{
		syslog(LOG_ERR, "%s", 
		       "unable to register (CHANNEL_PROG, CHANNEL_VERS, udp)");
		exit(1);
	}

	transp = svctcp_create(RPC_ANYSOCK, 0, 0);
	if ( !transp ) {
		syslog(LOG_ERR, "%s", "cannot create tcp service.");
		exit(1);
	}

	if ( !svc_register(transp, CHANNEL_PROG, CHANNEL_VERS,
			   channel_prog_1, IPPROTO_TCP) ) 
	{
		syslog(LOG_ERR, "%s",
		       "unable to register (CHANNEL_PROG, CHANNEL_VERS, tcp)");
		exit(1);
	}

	svc_run();

	syslog(LOG_ERR, "%s", "svc_run returned");
	return -1;
} /* main */
