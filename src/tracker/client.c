#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <time.h>
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
fprintf(stderr, "lookup:retval (%d)\n", retval);
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
	fprintf(stderr, "get: get file (%s) from (%s)\n", filename,
		inet_ntoa(in));

	return(0);
}

int
register_hash(int sockfd, in_addr_t *ip, uint32_t numhashes,
	tracker_info_t *info)
{
	struct sockaddr_in	send_addr;
	tracker_register_t	*req;
	struct in_addr		in;
	int			len, infolen;
	int			i;

	bzero(&send_addr, sizeof(send_addr));
	send_addr.sin_family = AF_INET;

	/*
	 * the ip address is already in network byte order
	 */
	send_addr.sin_addr.s_addr = *ip;
	send_addr.sin_port = htons(TRACKER_PORT);

	infolen = 0;
	for (i = 0 ; i < numhashes ; ++i) {
		infolen += sizeof(tracker_info_t) +
			(info[i].numpeers * sizeof(*(info[i].peers)));
	}

	len = sizeof(tracker_register_t) + infolen;

	if ((req = (tracker_register_t *)malloc(len)) == NULL) {
		fprintf(stderr, "register_hash:malloc failed\n");
		return(-1);
	}

	bzero(req, len);
	req->header.op = REGISTER;
	req->header.length = len;

	req->numhashes = numhashes;

fprintf(stderr, "infolen (%d)\n", infolen);

	memcpy(req->info, info, infolen);

	tracker_send(sockfd, (void *)req, len, 
		(struct sockaddr *)&send_addr, sizeof(send_addr));

	in.s_addr = *ip;
	fprintf(stderr,
		"register: registered hash (0x%016lx) with tracker (%s)\n",
		info->hash, inet_ntoa(in));

	free(req);
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
shuffle(in_addr_t *peers, uint16_t numpeers)
{
	in_addr_t	temp;
	int		i, j;
	
	if (numpeers < 2) {
		/*
		 * nothing to shuffle
		 */
		return(0);
	}

	srand(time(NULL));

	for (i = 0 ; i < numpeers - 1 ; ++i) {
		j = i + rand() / (RAND_MAX / (numpeers - i) + 1);

		temp = peers[j];
		peers[j] = peers[i];
		peers[i] = temp;
	}

	return(0);
}

