/* $Id: server.c,v 1.14 2012/11/27 00:48:08 phil Exp $
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		         version 6.2 (SideWindwer)
 * 		         version 7.0 (Manzanita)
 * 
 * Copyright (c) 2000 - 2017 The Regents of the University of California.
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
 * $Log: server.c,v $
 * Revision 1.14  2012/11/27 00:48:08  phil
 * Copyright Storm for Emerald Boa
 *
 * Revision 1.13  2012/05/06 05:48:18  phil
 * Copyright Storm for Mamba
 *
 * Revision 1.12  2011/07/23 02:30:24  phil
 * Viper Copyright
 *
 * Revision 1.11  2011/01/25 23:20:24  anoop
 * hexdump and -Wall are linux only
 *
 * Revision 1.10  2011/01/25 23:14:40  mjk
 * actually builds
 *
 * Revision 1.9  2011/01/25 21:58:51  mjk
 * - Move all RPC stuff from librocks to here
 * - Handle case of Solaris naming server side functions different than
 *   Linux.
 *
 * Revision 1.8  2011/01/21 20:08:46  anoop
 * Solaris build fixes
 *
 * Revision 1.7  2010/11/04 02:20:15  anoop
 * Solaris compatibility fixes
 *
 * Revision 1.6  2010/10/21 22:03:18  mjk
 * - linux and solaris both send only .info and above to the frontend
 *   debug stays off the network
 * - changed syslog levels to debug (see above)
 * - proper wait return code handling with W* macros
 *
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

#if defined (__linux__)
#include <rpc/pmap_clnt.h>
#endif

#if defined (__SVR4) && defined (__sun)
#define PORTMAP
#include <rpc/rpc.h>
#include <stdlib.h>
int _rpcpmstart;
#endif

#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include "channel.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <tcpd.h>

void writePidFile(char * pidfile, int pid)
{
	if (pidfile == NULL) return;
	int f;
	char outbuf[128];
	f = open(pidfile,O_CREAT | O_WRONLY);
	if (f <= 0) return;
	sprintf(outbuf,"%d",pid);
	outbuf[sizeof(outbuf)-1] = '\0';
	write(f,outbuf,strlen(outbuf));
	close(f);
}
extern void channel_prog_1(struct svc_req *rqstp, register SVCXPRT *transp);

/* 
 * Linux adds a _svc to the server side RPC functions and Solaris does not.
 */

#if defined(__linux__)
# define RPC_SERVICE(a)   a ## _svc
#else
# define RPC_SERVICE(a)   a
#endif

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
RPC_SERVICE(channel_ping_1)(struct svc_req *rqstp)
{
	/* return 0 so RPC doesn't get upset */
	static int  result = 0;

	assert(rqstp);
	syslog(LOG_DEBUG, "ping received");

	/* libwrap check - stop as soon as possible if we shouldn't talk to
	 * this host. 
	 */
	if(!tcpd_allowed(rqstp)) 
	{
		result = 0;
		return &result; 
	}

	syslog(LOG_DEBUG, "ping received, socket %d clnt %s:%d", 
	       rqstp->rq_xprt->xp_sock,
	       inet_ntoa(rqstp->rq_xprt->xp_raddr.sin_addr),
	       ntohs(rqstp->rq_xprt->xp_raddr.sin_port));

	return &result;
} /* channel_ping_1_svc */


int *
RPC_SERVICE(channel_411_alert_1)(char *filename, char *signature, 
				 u_long sec, u_int usec, struct svc_req *rqstp)
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

	/* libwrap check - stop as soon as possible if we shouldn't talk to 
	 * this host.
	 */
	if ( !tcpd_allowed(rqstp) )
	{
		result = 0;
		return &result;
	}

	syslog(LOG_DEBUG, "411_alert received (file=\"%s\", time=%.6f)", filename, time);

	switch ( pid=fork() ) {
	case -1:
		syslog(LOG_ERR, "%s", "cannot fork");
		result = -1;
		break;
	case 0:			/* child process */
		sprintf(sec_string, "%lu", sec);
		sprintf(usec_string, "%u", usec);
		status = execl("/opt/rocks/sbin/411-alert-handler", "411-alert-handler",
		      filename, signature, sec_string, usec_string, NULL);
		syslog(LOG_ERR, "411-alert-handler could not run (%s)", strerror(errno));
		exit(-1);
	default:		/* parent process */
		waitpid(pid, &status, 0);
		if ( WIFEXITED(status) ) {
			result = WEXITSTATUS(status);
		}
		else {		/* child crashed */
			result = -1;
		}
	}

	syslog(LOG_DEBUG, "411_alert processed (file=\"%s\", time=%.6f, status=%d)",
	       filename, time, result);

	return &result;
} /* channel_alert_1_svc */





int
main(int argc, char *argv[])
{
	char c;
	int debug = 0;
	char * pidfile = NULL;
	int pid;
	register SVCXPRT *transp;

	openlog(SERVICE_NAME, LOG_PID, LOG_LOCAL0);
	syslog(LOG_INFO, "starting service");

#if defined (__SVR4) && defined (__sun)
	_rpcpmstart = 0;
#endif

	while ((c=getopt(argc,argv,"dp:")) != -1)
	{
		switch(c)
		{
			case 'd': debug = 1;
				  break;
			case 'p': pidfile = optarg;
				  break;
			default:  break;
		}
	}
#ifndef DEBUG
        switch ( (pid=fork()) ) {
	case -1:
		syslog(LOG_ERR, "%s", "cannot fork");
		exit(1);
	case 0:			/* child process */
		break;
	default:		/* parent process */
		if (debug) fprintf(stderr,"pidfile is %s\n", pidfile);
		writePidFile(pidfile,pid);
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
