/* $Id: 411-alert.c,v 1.3 2010/10/21 16:59:45 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 * 
 * $Log: 411-alert.c,v $
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
#include <rpc/rpc.h>
#include <rpc/pmap_clnt.h>
#include <sys/socket.h>
#include <netdb.h>
#include <time.h>
#include <rocks/channel.h>

static bool_t callback(caddr_t, struct sockaddr_in *);

int
main(int argc, char *argv[])
{
	int				result;
	channel_411_alert_1_argument	args;
	enum clnt_stat			status;


	if (argc != 3) {
		fprintf(stderr, "usage: %s filename signature\n", argv[0]);
		exit(-1);
	}

	openlog("411-alert", LOG_PID, LOG_LOCAL0);

	args.filename	= strdup(argv[1]);
	args.time	= time(NULL);
	args.signature	= strdup(argv[2]);

	syslog(LOG_INFO, "call sent (file=\"%s\", time=%ld)", args.filename, args.time);

	status = clnt_broadcast(CHANNEL_PROG, CHANNEL_VERS, CHANNEL_411_ALERT,
				(xdrproc_t)xdr_channel_411_alert_1_argument,
				(caddr_t)&args,
				(xdrproc_t)xdr_int, (caddr_t)&result,
				callback);
	if ( status != RPC_SUCCESS ) {
		syslog(LOG_ERR, "call failed (%d)", status);
		return -1;
	}

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
		syslog(LOG_INFO, "call returned %s:%d",
		       he->h_name, count);
	}
	else {
		syslog(LOG_ERR, "reply from unknown host");
		return 0;
	}

	return (count > 1) ? 1 : 0;

} /* callback */

