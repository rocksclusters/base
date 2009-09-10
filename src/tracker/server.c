#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include "tracker.h"

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

hash_table_t *
init_hash_table(int size)
{
	hash_table_t	*hash_table;
	int		len;

	len = sizeof(hash_table_t) + (size * sizeof(hash_info_t));

	if ((hash_table = malloc(len)) == NULL) {
		perror("init_hash_table:malloc failed:");
		return(NULL);
	}
	
	bzero(hash_table, len);
	hash_table->size = size;

	return(hash_table);
}

int
addpeer(hash_info_t *hashinfo, in_addr_t *peer)
{
	if (hashinfo == NULL) {
		fprintf(stderr, "addpeer:hashinfo NULL\n");
		return(-1);
	}

	if (hashinfo->peers) {
		if ((hashinfo->peers = realloc(hashinfo->peers,
			(hashinfo->numpeers + 1) * sizeof(*peer))) == NULL) {

			fprintf(stderr, "addpeer:realloc failed\n");
			return(-1);
		}
	} else {
		if ((hashinfo->peers = malloc(sizeof(*peer))) == NULL) {
			fprintf(stderr, "addpeer:malloc failed\n");
			return(-1);
		}
	}

	memcpy(&hashinfo->peers[hashinfo->numpeers], peer, sizeof(*peer));
	++hashinfo->numpeers;
		
	return(0);
}


/*
 * this assumes infoptr points to real storage
 */
hash_info_t *
getpeers(hash_table_t *hash_table, uint64_t hash)
{
	int	i;

	for (i = 0 ; i < hash_table->size; ++i) {
		if (hash_table->entry[i].hash == hash) {
			fprintf(stderr, "getpeers:hash (0x%016lx) found\n",
				hash);
			return(&hash_table->entry[i]);
		}
	}

	/*
	 * the hash is not in the table
	 */
	fprintf(stderr, "getpeers:hash (0x%016lx) not found\n", hash);
	return(NULL);
}

void
dolookup(int sockfd, hash_table_t *hash_table, uint64_t hash,
	struct sockaddr_in *from_addr)
{
	tracker_lookup_resp_t	*resp;
	tracker_info_t		*respinfo;
	hash_info_t		*hashinfo;
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

fprintf(stderr, "len (%d)\n", len);

	/*
	 * look up info for this hash
	 */
	respinfo = (tracker_info_t *)resp->info;
	respinfo->hash = hash;

	len += sizeof(tracker_info_t);

fprintf(stderr, "len (%d)\n", len);

	if ((hashinfo = getpeers(hash_table, hash)) != NULL) {
		/*
		 * copy the hash info into the response buffer
		 */
		respinfo->hash = hashinfo->hash;
		respinfo->numpeers = hashinfo->numpeers;
		memcpy(respinfo->peers, hashinfo->peers,
			(sizeof(hashinfo->peers[0]) * hashinfo->numpeers));

fprintf(stderr, "hash info numpeers (%d)\n", hashinfo->numpeers);

		len += (sizeof(hashinfo->peers[0]) * hashinfo->numpeers);
fprintf(stderr, "len (%d)\n", len);

	} else {
		respinfo->numpeers = 0;
	}

	resp->numhashes = 1;

fprintf(stderr, "resp info numpeers (%d)\n", respinfo->numpeers);
		
#ifdef	LATER
	/*
	 * XXX - this is where we would fill in 'predictive' info
	 */

	/*
	 * advance respinfo to the next 'hash' info
	 */
	respinfo = (tracker_info_t *)
		(&(respinfo->peers[respinfo->numpeers]));

	++resp->numhashes;
#endif

	resp->header.length = len;

	fprintf(stderr, "send buf: ");
	dumpbuf((char *)resp, len);

	flags = 0;
	sendto(sockfd, buf, len, flags, (struct sockaddr *)from_addr,
		sizeof(*from_addr));

	return;
}

int
register_hash(hash_table_t *hash_table, char *buf,
	struct sockaddr_in *from_addr)
{
	tracker_register_t	*req = (tracker_register_t *)buf;
	hash_info_t		*hashinfo;
	tracker_info_t		*reqinfo;
	uint16_t		numpeers;
	in_addr_t		dynamic_peers[1];
	in_addr_t		*peers;
	int			i, j, k;

	for (i = 0; i < req->numhashes; ++i) {
		reqinfo = &req->info[i];

		if (reqinfo->numpeers == 0) {
			/*
			 * no peer specified. dynamically determine
			 * the peer IP address from the host who
			 * sent us the message
			 */
			numpeers = 1;
			dynamic_peers[0] = from_addr->sin_addr.s_addr;
			peers = dynamic_peers;
		} else {
			numpeers = reqinfo->numpeers;
			peers = reqinfo->peers;
		}

		/*
		 * scan the list for this hash.
		 */
		if ((hashinfo = getpeers(hash_table, reqinfo->hash)) != NULL) {
			/*
			 * this hash is already in the table, see if this peer
			 * is already in the list
			 */
			for (j = 0 ; j < numpeers ; ++j) {
				int	found = 0;
		
				for (k = 0 ; k < hashinfo->numpeers ; ++k) {
					if (peers[j] == hashinfo->peers[k]) {
						found = 1;
						break;
					}
				}

				if (!found) {
					addpeer(hashinfo, &peers[j]);
				}
			}
		} else {
			/*
			 * if not, then add this hash to the end of the list
			 */
			if (hash_table->head < hash_table->size) {
				hashinfo = &hash_table->entry[hash_table->head];
				hashinfo->hash = reqinfo->hash;
				++hash_table->head;
			} else {
				fprintf(stderr, "no free entry in table\n");
				abort();
			}

			for (j < 0 ; j < numpeers ; ++j) {
				addpeer(hashinfo, &peers[j]);
			}
		}
	}
}

int
main()
{
	struct sockaddr_in	send_addr, from_addr;
	socklen_t		from_addr_len;
	ssize_t			recvbytes;
	hash_table_t		*hash_table;
	int			sockfd;
	char			buf[64*1024];
	char			done;

	if ((sockfd = init_tracker_comm(TRACKER_PORT)) < 0) {
		fprintf(stderr, "main:init_tracker_comm:failed\n");
		abort();
	}

	if ((hash_table = init_hash_table(HASH_TABLE_ENTRIES)) == NULL) {
		fprintf(stderr, "main:init_hash_table:failed\n");
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
					dolookup(sockfd, hash_table, req->hash,
						&from_addr);
				}
				break;

			case REGISTER:
				register_hash(hash_table, buf, &from_addr);
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

