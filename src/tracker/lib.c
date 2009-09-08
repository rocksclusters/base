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

uint64_t
hashit(char *ptr)
{
	uint64_t	hash = 0;
	int		c;

	/*
	 * SDBM hash function
	 */

	while (c = *ptr++) {
		hash = c + (hash << 6) + (hash << 16) - hash;
	}

	return hash;
}

int
tracker_send(int sockfd, void *buf, size_t len, struct sockaddr *to,
	socklen_t tolen)
{
	int	flags = 0;

	sendto(sockfd, buf, len, flags, (struct sockaddr *)to, tolen);

	return(0);
}

ssize_t
tracker_recv(int sockfd, void *buf, size_t len, struct sockaddr *from,
	socklen_t *fromlen)
{
	int	flags = 0;

	return(recvfrom(sockfd, buf, len, flags, from, fromlen));
}

int
init_tracker_comm(int port)
{
	struct sockaddr_in	client_addr;
	int			sockfd;

	if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
		perror("init_tracker_comm:socket failed:");
		return(-1);
	}

	/*
	 * bind the socket so we can send from it
	 */
	bzero(&client_addr, sizeof(client_addr));
	client_addr.sin_family = AF_INET;
	client_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	client_addr.sin_port = htons(port);

	if (bind(sockfd, (struct sockaddr *)&client_addr,
			sizeof(client_addr)) < 0) {
                perror("init_tracker_comm:bind failed:");
		close(sockfd);
                return(-1);
	}

	return(sockfd);
}

