/* $Id: server.c,v 1.5 2010/10/21 20:51:17 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: server.c,v $
 * Revision 1.5  2010/10/21 20:51:17  mjk
 * - timestamp is now a timeval (microseconds)
 * - re-entry testing is done in 411-alert-handler using a pickle file for state
 * - more logging
 *
 * Looks good, but need to turn down the logging to keep the network quite.
 *
 * Revision 1.4  2010/10/21 16:59:45  mjk
 * more logging
 * copy the arg strings in case RPC is doing something odd
 *
 * Revision 1.3  2010/10/20 21:12:34  mjk
 * works
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
#include <unistd.h>
#include <string.h>
#include <syslog.h>
#include <assert.h>
#include <errno.h>
#include <rpc/pmap_clnt.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/wait.h>
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
channel_411_alert_1_svc(char *filename, char *signature, u_long sec, u_int usec,
			struct svc_req *rqstp)
{
	static int	result = 0;
	double		time = (float)usec / 1e6 + (double)sec;
	char		sec_string[32];
	char		usec_string[32];
	int		pid;
	int		status;

	assert(filename);
	assert(signature);
	assert(time > 0);
	assert(rqstp);

	syslog(LOG_INFO, "411_alert received (file=\"%s\", time=%.6f)", filename, time);

	switch ( pid=fork() ) {
	case -1:
		syslog(LOG_ERR, "%s", "cannot fork");
		result = -1;
		break;
	case 0:			/* child process */
		sprintf(sec_string, "%lu", sec);
		sprintf(usec_string, "%u", usec);
		status = execl("/opt/rocks/sbin/411-alert-handler", "411-alert-handler",
		      filename, signature, &sec_string, &usec_string, NULL);
		syslog(LOG_ERR, "411-alert-handler could not run (%s)", strerror(errno));
		exit(-1);
	default:		/* parent process */
		waitpid(pid, &result, 0);
	}

	syslog(LOG_INFO, "411_alert processed (file=\"%s\", time=%.6f, status=%d)",
	       filename, time, result);

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
