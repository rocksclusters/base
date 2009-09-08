#include <stdint.h>
#include <netinet/in.h>

/*
 * hard-coded stuff
 */

#define	TRACKER_PORT	9632


/*
 * message structures
 */

typedef struct {
	uint16_t	op;
	uint16_t	length;
	char		reserved[4];
} tracker_header_t;

/*
 * tracker message types
 */
#define	LOOKUP		1
#define	REGISTER	2
#define	UNREGISTER	3


/*
 * LOOKUP messages
 */

typedef struct {
	tracker_header_t	header;
	uint64_t		hash;
} tracker_lookup_req_t;

typedef struct {
	uint64_t	hash;
	uint16_t	numpeers;
	char		pad[2];
	in_addr_t	peers[0];
} tracker_info_t;

typedef struct {
	tracker_header_t	header;
	uint32_t		numhashes;
	tracker_info_t		info[0];
} tracker_lookup_resp_t;


/*
 * REGISTER messages
 */

/*
 * this is flexible enough to be able to register multiple files (hashes) or
 * register multiple files for multiple other peers
 */
typedef struct {
	tracker_header_t	header;
	uint32_t		numhashes;
	tracker_info_t		info[0];
						/* this really is an array */
} tracker_register_t;

/* there is no response to a 'register' message */

/*
 * UNREGISTER messages
 */

/*
 * this is flexible enough to be able to unregister multiple files (hashes) or
 * register multiple files for multiple other peers
 */
typedef struct {
	tracker_header_t	header;
	uint32_t		numhashes;
	tracker_info_t		info[0];
						/* this really is an array */
} tracker_unregister_t;

typedef struct {
	tracker_header_t	header;
} tracker_unregister_resp_t;


/*
 * prototypes
 */
extern uint64_t hashit(char *);
extern int tracker_send(int, void *, size_t, struct sockaddr *, socklen_t);
extern ssize_t tracker_recv(int, void *, size_t, struct sockaddr *,
	socklen_t *);
extern int init_tracker_comm(int);

