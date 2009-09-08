#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include "tracker.h"

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int	count = 0;

/*
 * this assumes infoptr points to real storage
 */
int
getpeers(uint64_t hash, tracker_info_t *infoptr)
{
	int	i;

if (count == 0) {
	infoptr->numpeers = 1;
	
	for (i = 0 ; i < infoptr->numpeers ; ++i) {
		/*
		 * inet_addr() returns a value in network byte order
		 */
		infoptr->peers[i] = inet_addr("10.1.1.1");
	}
} else {
	infoptr->numpeers = 2;
	
	for (i = 0 ; i < infoptr->numpeers ; ++i) {
		/*
		 * inet_addr() returns a value in network byte order
		 */
		if (i == 0) {
			infoptr->peers[i] = inet_addr("10.1.1.2");
		} else {
			infoptr->peers[i] = inet_addr("10.1.1.3");
		}
	}
}

	++count;

	return(infoptr->numpeers);
}

void
dolookup(int sockfd, uint64_t hash, struct sockaddr_in *from_addr)
{
	tracker_lookup_req_t	*req;
	tracker_lookup_resp_t	*resp;
	tracker_info_t		*infoptr;
	uint16_t		numpeers;
	size_t			len;
	int			i, j;
	int			flags;
	char			buf[64*1024];

	resp = (tracker_lookup_resp_t *)buf;
	resp->header.op = LOOKUP;

	/*
	 * keep a running count for the length of the data
	 */
	len = sizeof(tracker_lookup_resp_t);

	/*
	 * look up info for this hash
	 * XXX - this will need to be dynamic
	 */
	resp->numhashes = 2;
	
	infoptr = (tracker_info_t *)resp->info;
	for (i = 0 ; i < resp->numhashes ; ++i) {
		infoptr->hash = hash;

		len += sizeof(tracker_info_t);

		if (getpeers(hash, infoptr) < 0) {
			fprintf(stderr, "dolookup:getpeers failed\n");
			abort();
		}

fprintf(stderr, "numpeers (%d)\n", infoptr->numpeers);
fprintf(stderr, "len before (%d)\n", len);
		len += (sizeof(infoptr->peers[0]) * infoptr->numpeers);
fprintf(stderr, "len after (%d)\n", len);

#ifdef	LATER
		/*
		 * lookup the number of peers for this hash
		 * XXX - this will need to be dynamic
		 */
		infoptr->numpeers = 1;
		
		for (j = 0 ; j < infoptr->numpeers ; ++j) {
			/*
			 * inet_addr() returns a value in network byte order
			 */
			infoptr->peers[j] = inet_addr("10.1.1.1");

			len += sizeof(infoptr->peers[j]);
		}
#endif


		/*
		 * advance infoptr to the next 'hash' info
		 */
		infoptr = (tracker_info_t *)
			(&(infoptr->peers[infoptr->numpeers]));
	}

	resp->header.length = len;

{
	int	i;

	for (i = 0; i < len; ++i) {
		fprintf(stderr, "%02x ", (unsigned char)buf[i]);
	}
	fprintf(stderr, "\n");
}

	flags = 0;
	sendto(sockfd, buf, len, flags, (struct sockaddr *)from_addr,
		sizeof(*from_addr));

	return;
}

int
main()
{
	struct sockaddr_in	send_addr, from_addr;
	socklen_t		from_addr_len;
	ssize_t			recvbytes;
	int			sockfd;
	char			buf[64*1024];
	char			done;

	if ((sockfd = init_tracker_comm(TRACKER_PORT)) < 0) {
		fprintf(stderr, "main:init_tracker_comm:failed\n");
		abort();
	}

	done = 0;
	while (!done) {
		from_addr_len = sizeof(from_addr);
		recvbytes = tracker_recv(sockfd, buf, sizeof(buf),
			(struct sockaddr *)&from_addr, &from_addr_len);

		if (recvbytes > 0) {
			tracker_header_t	*p;

			p = (tracker_header_t *)buf;

			switch(p->op) {
			case LOOKUP:
				{
					tracker_lookup_req_t	*req;

					req = (tracker_lookup_req_t *)buf;
					dolookup(sockfd, req->hash, &from_addr);
				}
				break;

			case REGISTER:
				break;

			case UNREGISTER:
				break;

			default:
				fprintf(stderr, "Unknown op (%d)\n", p->op);
				abort();
				break;
			}
		}
	}
}

