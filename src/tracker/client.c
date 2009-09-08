#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <netinet/in.h>
#include "tracker.h"

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int
lookup(int sockfd, in_addr_t *tracker, char *file, tracker_info_t **info)
{
	struct sockaddr_in	send_addr, recv_addr;
	socklen_t		recv_addr_len;
	tracker_lookup_req_t	req;
	ssize_t			recvbytes;
	int			retval;
	int			infosize;
	char			buf[64*1024];

	bzero(&send_addr, sizeof(send_addr));
	send_addr.sin_family = AF_INET;

	/*
	 * all 'tracker' ip addresses are already in network byte order
	 */
	send_addr.sin_addr.s_addr = *tracker;
	send_addr.sin_port = htons(TRACKER_PORT);

	bzero(&req, sizeof(req));
	req.header.op = LOOKUP;
	req.header.length = sizeof(tracker_lookup_req_t);
	req.hash = hashit(file);

	tracker_send(sockfd, (void *)&req, sizeof(req),
		(struct sockaddr *)&send_addr, sizeof(send_addr));

	recv_addr_len = sizeof(recv_addr);
	recvbytes = tracker_recv(sockfd, (void *)buf, sizeof(buf),
		(struct sockaddr *)&recv_addr, &recv_addr_len);

{
	int	i;

	for (i = 0; i < recvbytes; ++i) {
		fprintf(stderr, "%02x ", (unsigned char)buf[i]);
	}
	fprintf(stderr, "\n");
}

	if (recvbytes > 0) {
		tracker_lookup_resp_t	*resp;

		resp = (tracker_lookup_resp_t *)buf;

		/*
		 * validate the packet
		 */
		if (resp->header.op != LOOKUP) {
			fprintf(stderr, "lookup:header op (%d) != (%d)\n",
				resp->header.op, LOOKUP);
			abort();
		}

		/*
		 * make sure numhashes is reasonable
		 */
		if ((resp->numhashes < 0) || (resp->numhashes > 64)) {
			fprintf(stderr, "lookup:numhashes (%d) is not between 0 and 64\n", resp->numhashes);
			abort();
		}

		/*
		 * get the size of the info structure
		 */
		infosize = resp->header.length - sizeof(tracker_lookup_resp_t);

		if ((*info = (tracker_info_t *)malloc(infosize)) == NULL) {
			fprintf(stderr, "lookup:malloc failed\n");
			abort();
		}

		memcpy(*info, resp->info, infosize);
		retval = resp->numhashes;
	} else {
		retval = 0;
	}

	return(retval);
}

int
get(in_addr_t *ip, char *filename)
{
	struct in_addr	in;

	in.s_addr = *ip;
	printf("get: get file (%s) from (%s)\n", filename, inet_ntoa(in));

	return(0);
}

int
register_hash(in_addr_t *ip, uint64_t hash)
{
	struct in_addr	in;

	in.s_addr = *ip;

	printf("register: registered hash (0x%lx) with tracker (%s)\n", hash,
		inet_ntoa(in));

	return(0);
}


int
init(uint16_t *num_trackers, in_addr_t **trackers, uint16_t *maxpeers,
	uint16_t *num_pkg_servers, in_addr_t **pkg_servers)
{
	size_t	size;

	/*
	 * the list of tracker(s)
	 */
	*num_trackers = 1;
	size = *num_trackers * sizeof(**trackers);

	if ((*trackers = malloc(size)) == NULL) {
		perror("init:malloc failed:");
		return(-1);
	}

	bzero(*trackers, size);
	(*trackers)[0] = inet_addr("10.1.1.1");

	/*
	 * set the maximum number of peers that should be registered with
	 * the tracker
	 */
	*maxpeers = 10;

	/*
	 * the list of package servers. if i can't get a package from a
	 * peer, then these are the servers that *always* have the package
	 */
	*num_pkg_servers = 1;
	size = *num_pkg_servers * sizeof(**pkg_servers);

	if ((*pkg_servers = malloc(size)) == NULL) {
		perror("init:malloc failed:");
		return(-1);
	}

	bzero(*pkg_servers, size);
	(*pkg_servers)[0] = inet_addr("10.1.1.1");

	return(0);
}

int
main(int argc, char **argv)
{
	uint16_t	num_trackers;
	in_addr_t	*trackers;
	uint16_t	maxpeers;
	uint16_t	num_pkg_servers;
	in_addr_t	*pkg_servers;
	uint16_t	i, j;
	tracker_info_t	*tracker_info, *infoptr;
	int		sockfd;
	int		info_count;
	char		success;
	char		*file;

	if (argc != 2) {
		fprintf(stderr, "usage: %s <filename>\n", argv[0]);
		exit(-1);
	}

	file = argv[1];

	if (init(&num_trackers, &trackers, &maxpeers, &num_pkg_servers,
			&pkg_servers) != 0) {
		fprintf(stderr, "main:init failed\n");
		exit(-1);
	}

	if ((sockfd = init_tracker_comm(0)) < 0) {
		fprintf(stderr, "main:init_tracker_comm failed\n");
		exit(-1);
	}

	for (i = 0 ; i < num_trackers; ++i) {
		struct in_addr	in;

		in.s_addr = trackers[i];

		info_count = lookup(sockfd, &trackers[i], file, &tracker_info);

		if (info_count > 0) {
			break;
		}
	}

	if (info_count == 0) {
		fprintf(stderr, "main:tracker_info is NULL\n");
		exit(-1);
	}

	success = 0;
	for (i = 0 ; i < info_count && !success; ++i) {
		infoptr = &tracker_info[i];

		fprintf(stderr, "info:hash (0x%x)\n", infoptr->hash);
		fprintf(stderr, "info:numpeers (%lld)\n", infoptr->numpeers);

		fprintf(stderr, "info:peers: ");
		for (j = 0 ; j < infoptr->numpeers; ++j) {
			struct in_addr	in;

			in.s_addr = infoptr->peers[j];
			fprintf(stderr, "%s\n", inet_ntoa(in));

			if (get(&infoptr->peers[j], file) == 0) {
				/*
				 * successful download, exit this loop
				 */
#ifdef	LATER
				success = 1;
				break;
#endif
			}
		}
	}

	if (success) {
		for (i = 0 ; i < num_trackers; ++i) {
			register_hash(&trackers[i], infoptr->hash);
		}
	}

	/*
	 * lookup() malloc'ed tracker_info
	 */
	free(tracker_info);

	free(trackers);
	return(0);
}

