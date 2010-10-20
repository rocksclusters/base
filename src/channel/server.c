/* $Id: server.c,v 1.2 2010/10/20 01:41:53 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: server.c,v $
 * Revision 1.2  2010/10/20 01:41:53  mjk
 * daemonized
 * calls out to python code for 411-listen
 *
 * Revision 1.1  2010/10/19 23:06:29  mjk
 * c is hard
 *
 */

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <syslog.h>
#include <assert.h>
#include <rpc/pmap_clnt.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <rocks/channel.h>
#include <rocks/hexdump.h>


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
	int		status;

	assert(filename);
	assert(rqstp);

	if ( time != last ) {
		result = 1;
		last   = time;

		syslog(LOG_INFO, "411_alert received (file=\"%s\")", filename);

		switch ( pid=fork() ) {
		case -1:
			syslog(LOG_ERR, "%s", "cannot fork");
			result = -1;
			break;
		case 0:			/* child process */
			execl("/opt/rocks/sbin/411-listen", "411-listen",
			      filename, tile, signature, NULL);
		default:		/* parent process */
			waitpid(pid, &status, 0);
		}
 
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

#ifndef DEBUG
        switch ( fork() ) {
	case -1:
		syslog(LOG_ERR, "%s", "cannot fork");
		exit(1);
	case 0:			/* child process */
		break;
	default:		/* parent process */
		return 0;
	}
 
        close(STDIN_FILENO);
        close(STDOUT_FILENO);
        close(STDERR_FILENO);

        setsid();		/* start a new session */
#endif

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
