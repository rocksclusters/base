#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include "tracker.h"

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

hash_table_t	*hash_table = NULL;

int
init_hash_table(int size)
{
	int		len;

	len = sizeof(hash_table_t) + (size * sizeof(hash_info_t));

	if ((hash_table = malloc(len)) == NULL) {
		perror("init_hash_table:malloc failed:");
		return(-1);
	}
	
	bzero(hash_table, len);
	hash_table->size = size;
	hash_table->head = 0;
	hash_table->tail = -1;

	return(0);
}

void
print_peers(hash_info_t *hashinfo)
{
	struct in_addr	in;
	int		i;

	for (i = 0 ; i < hashinfo->numpeers ; ++i) {
		in.s_addr = hashinfo->peers[i];
		fprintf(stderr, "\t%s\n", inet_ntoa(in));
	}
}

void
print_hash_table()
{
	int	i;

fprintf(stderr, "head: (%d)\n", hash_table->head);
fprintf(stderr, "tail: (%d)\n", hash_table->tail);

	if (hash_table->head >= hash_table->tail) {
		for (i = hash_table->head ;
				(i >= hash_table->tail) && (i >= 0) ; --i) {

			fprintf(stderr, "entry[%d] : hash (0x%lx)\n", i,
				hash_table->entry[i].hash);

			print_peers(&hash_table->entry[i]);
		}
	} else {
		for (i = hash_table->head ; i >= 0 ; --i) {
			fprintf(stderr, "entry[%d] : hash (0x%lx)\n", i,
				hash_table->entry[i].hash);

			print_peers(&hash_table->entry[i]);
		}

		for (i = (hash_table->size - 1) ;
				(i >= hash_table->tail) && (i >= 0) ; --i) {

			fprintf(stderr, "entry[%d] : hash (0x%lx)\n", i,
				hash_table->entry[i].hash);

			print_peers(&hash_table->entry[i]);
		}
	}

	return;
}

/*
 * 'size' is the number of new entries to be added to the table
 */
int
grow_hash_table(int size)
{
	uint32_t	oldsize = hash_table->size;
	uint32_t	newsize = size + hash_table->size;
	int		len;

	len = sizeof(hash_table_t) + (newsize * sizeof(hash_info_t));

fprintf(stderr, "grow_hash_table:enter:size (%d)\n", hash_table->size);
fprintf(stderr, "grow_hash_table:enter:head (%d)\n", hash_table->head);
fprintf(stderr, "grow_hash_table:enter:tail (%d)\n", hash_table->tail);

fprintf(stderr, "grow_hash_table:before\n\n");
print_hash_table();

	if ((hash_table = realloc(hash_table, len)) == NULL) {
		perror("grow_hash_table:realloc failed:");
		return(-1);
	}

	/*
	 * create an initialized space in the new table for the new entries.
	 * these new entries are being 'spliced' into the middle of the table
	 * starting at 'head'.
	 * 
	 * need to move the entries from the table head down to the end of
	 * the old table into the last part of the new table.
	 */
	memcpy(&hash_table->entry[oldsize],
		&hash_table->entry[hash_table->head],
			size * sizeof(hash_info_t));
	
	/*
	 * initialize the new entries
	 */
	bzero(&hash_table->entry[hash_table->head], size * sizeof(hash_info_t));

	hash_table->size = newsize;
	hash_table->tail = hash_table->tail + size;

fprintf(stderr, "grow_hash_table:exit:size (%d)\n", hash_table->size);
fprintf(stderr, "grow_hash_table:exit:head (%d)\n", hash_table->head);
fprintf(stderr, "grow_hash_table:exit:tail (%d)\n", hash_table->tail);

fprintf(stderr, "grow_hash_table:after\n\n");
print_hash_table();

	return(0);
}

hash_info_t *
newentry()
{
	if (hash_table->tail != -1) {
		++hash_table->head;
		if (hash_table->head == hash_table->size) {
			hash_table->head = 0;
		}
	}

	if (hash_table->head == hash_table->tail) {
		if (grow_hash_table(HASH_TABLE_ENTRIES) != 0) {
			fprintf(stderr, "newentry:grow_hash_table:failed\n");
			return(NULL);
		}
	}

	/*
	 * when the first entry is allocated on a newly initialized table,
	 * tail will be -1. in this case, set tail to 0.
	 */
	if (hash_table->tail == -1) {
		hash_table->tail = 0;
	}

	return(&hash_table->entry[hash_table->head]);
}

int
addpeer(hash_info_t *hashinfo, in_addr_t *peer)
{

{
	struct in_addr	in;

	in.s_addr = *peer;
	fprintf(stderr, "addpeer:adding peer (%s) for hash (0x%016lx)\n",
		inet_ntoa(in), hashinfo->hash);
}

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
getpeers(uint64_t hash)
{
	int	i;

	for (i = 0 ; i < hash_table->size; ++i) {

fprintf(stderr, "getpeers:entry [%i] hash (0x%016lx)\n", i,
	hash_table->entry[i].hash);

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
dolookup(int sockfd, uint64_t hash, struct sockaddr_in *from_addr)
{
	tracker_lookup_resp_t	*resp;
	tracker_info_t		*respinfo;
	hash_info_t		*hashinfo;
	size_t			len;
	int			i;
	int			flags;
	char			buf[64*1024];

fprintf(stderr, "dolookup:enter:hash (0x%lx)\n", hash);

	resp = (tracker_lookup_resp_t *)buf;
	resp->header.op = LOOKUP;

	/*
	 * keep a running count for the length of the data
	 */
	len = sizeof(tracker_lookup_resp_t);

fprintf(stderr, "len (%d)\n", (int)len);

	/*
	 * look up info for this hash
	 */
	respinfo = (tracker_info_t *)resp->info;
	respinfo->hash = hash;

	len += sizeof(tracker_info_t);

fprintf(stderr, "len (%d)\n", (int)len);

	if ((hashinfo = getpeers(hash)) != NULL) {
		/*
		 * copy the hash info into the response buffer
		 */
		respinfo->hash = hashinfo->hash;
		respinfo->numpeers = 0;

		for (i = 0 ; i < hashinfo->numpeers ; ++i) {
			/*
			 * don't copy in address of requestor
			 */
			if (hashinfo->peers[i] == from_addr->sin_addr.s_addr) {
				continue;
			}

			respinfo->peers[i] = hashinfo->peers[i];
			++respinfo->numpeers;
		}

fprintf(stderr, "resp info numpeers (%d)\n", respinfo->numpeers);

		len += (sizeof(respinfo->peers[0]) * respinfo->numpeers);

fprintf(stderr, "len (%d)\n", (int)len);

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

fprintf(stderr, "dolookup:exit:hash (0x%lx)\n", hash);

	return;
}

void
register_hash(char *buf, struct sockaddr_in *from_addr)
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
fprintf(stderr, "register_hash:enter:hash (0x%lx)\n", reqinfo->hash);

if (hash_table->tail != -1) {
	fprintf(stderr, "register_hash:hash_table:before\n\n");
	print_hash_table();
}

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

fprintf(stderr, "register_hash:numpeers:1 (0x%d)\n", numpeers);

		/*
		 * scan the list for this hash.
		 */
		if ((hashinfo = getpeers(reqinfo->hash)) != NULL) {
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
			if ((hashinfo = newentry()) == NULL) {
				fprintf(stderr, "addentry:failed\n");
				abort();
			}

			hashinfo->hash = reqinfo->hash;
			hashinfo->numpeers = 0;

			for (j = 0 ; j < numpeers ; ++j) {
				addpeer(hashinfo, &peers[j]);
			}

		}
fprintf(stderr, "register_hash:hash_table:after\n\n");
print_hash_table();
fprintf(stderr, "register_hash:exit:hash (0x%lx)\n", reqinfo->hash);
	}
}

int
main()
{
	struct sockaddr_in	from_addr;
	socklen_t		from_addr_len;
	ssize_t			recvbytes;
	int			sockfd;
	char			buf[64*1024];
	char			done;

	if ((sockfd = init_tracker_comm(TRACKER_PORT)) < 0) {
		fprintf(stderr, "main:init_tracker_comm:failed\n");
		abort();
	}

	if (init_hash_table(HASH_TABLE_ENTRIES) != 0) {
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
					dolookup(sockfd, req->hash, &from_addr);
				}
				break;

			case REGISTER:
				register_hash(buf, &from_addr);
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

	return(0);
}

