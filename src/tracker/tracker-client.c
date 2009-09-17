/*
 * $Id: tracker-client.c,v 1.2 2009/09/17 20:12:49 bruno Exp $
 *
 * @COPYRIGHT@
 * @COPYRIGHT@
 *
 * $Log: tracker-client.c,v $
 * Revision 1.2  2009/09/17 20:12:49  bruno
 * lots of good stuff:
 *  - expandable, circular hash table
 *  - clients randomly shuffle their peer list
 *  - skip to next peer if download of peer fails
 *
 * Revision 1.1  2009/09/15 21:52:13  bruno
 * closer
 *
 * Revision 1.2  2009/09/02 21:11:45  bruno
 * save the file locally. if it exists, then don't ask for it over the
 * network, just stream the file from the local disk
 *
 * Revision 1.1  2009/08/28 21:49:53  bruno
 * the start of the "most scalable installer in the universe!"
 *
 *
 */

#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdint.h>
#include <limits.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <curl/curl.h>
#include <httpd/httpd.h>
#include <netinet/in.h>
#include "tracker.h"
#include <sys/socket.h>
#include <arpa/inet.h>

extern int init(uint16_t *, in_addr_t **, uint16_t *, uint16_t *, in_addr_t **);
extern int lookup(int, in_addr_t *, char *, tracker_info_t **);
extern int register_hash(int, in_addr_t *, uint32_t, tracker_info_t *);
extern int shuffle(in_addr_t *, uint16_t);


int	status = HTTP_OK;

int
getargs(char *forminfo, char *filename, char *serverip)
{
	char	*ptr;

	/*
	 * help out sscanf by putting in a blank for '&'
	 */
	if ((ptr = strchr(forminfo, '&')) == NULL) {
		/*
		 * XXX - log an error
		 */
		return(-1);
	}

	*ptr = ' ';

	if (sscanf(forminfo, "filename=%4095s serverip=%15s", filename,
			serverip) != 2) {
		/*
		 * XXX - log an error
		 */
		return(-1);
	}

	return(0);
}

#ifdef	DEBUG
void
logdebug(char *msg)
{
	FILE	*file;

	if ((file = fopen("/tmp/tracker-client.debug", "a+")) != NULL) {
		fprintf(file, "%s", msg);
		fclose(file);
	}

	return;
}
#endif


size_t
doheaders(void *ptr, size_t size, size_t nmemb, void *stream)
{
	int	httpstatus;

	/*
	 * look for HTTP status code. if it is not 200, then set the status
	 * to -1 (this tells us not to output any data).
	 */
	if ((status >= HTTP_OK) && (status <= HTTP_MULTI_STATUS)) {
		if (sscanf(ptr, "HTTP/1.1 %d", &httpstatus) == 1) {
			status = httpstatus;
		}
	}

#ifdef	LATER
	if ((status >= HTTP_OK) && (status <= HTTP_MULTI_STATUS)) {
		fwrite(ptr, size, nmemb, stdout);
	}
#endif

#ifdef	DEBUG
	logdebug("doheaders : ");
	logdebug(ptr);
#endif
	
	return(size * nmemb);
}

size_t
dobody(void *ptr, size_t size, size_t nmemb, void *stream)
{
	if ((status >= HTTP_OK) && (status <= HTTP_MULTI_STATUS)) {
		fwrite(ptr, size, nmemb, stream);
	}

	return(size * nmemb);
}

void
senderror(int http_error_code, char *msg, int other_error_code)
{
	/*
	 * HTTP/1.1 <errorcode> <error name>
	 *	
	 *	e.g., "HTTP/1.1 404 Not Found"
	 *	
	 */
        printf("HTTP/1.1 %d\n", http_error_code);

        printf("Content-type: text/plain\n");
        printf("Status: %d\n\n", http_error_code);
        printf("%s\n", msg);
        printf("other error code (%d)\n", other_error_code);
}

int
makeurl(char *header, char *filename, char *serverip, char *url,
	int url_max_size)
{
	int	length;

	/*
	 * +2 is for null terminator and (potential) added '/' character
	 */
	length = strlen(header) + strlen(serverip) + strlen(filename) + 2;

	if (length > url_max_size) {
		return(-1);
	}

	sprintf(url, "%s%s", header, serverip);

	if (filename[0] != '/') {
		sprintf(url, "%s/", url);
	}

	sprintf(url, "%s%s", url, filename);

	return(0);
}

int
outputfile(char *filename, char *range)
{
	struct stat	statbuf;
	off_t		offset;
	size_t		lastbyte;
	size_t		totalbytes;
	size_t		bytesread;
	size_t		count;
	int		fd;
	char		buf[128*1024];
	char		done;

	/*
	 * make sure the file exists
	 */
	if (stat(filename, &statbuf) != 0) {
		return(-1);
	}

	/*
	 * if a range is supplied, then we need to calculate the offset
	 * and total number of bytes to read
	 */
	if (range != NULL) {

		/*
		 * there are three cases:
		 *
		 *	1) there is no 'offset' supplied. this means read from
		 *	   the beginning of the file (offset 0).
		 *
		 *	2) there is no 'last byte' supplied. this means read
		 *	   to the end of the file
		 *
		 *	3) both 'offset and 'last byte' are supplied.
		 */
		if (range[0] == '-') {
			/*
			 * case 1
			 */
			sscanf(range, "-%d", (int *)&lastbyte);
			offset = 0;
		} else if (range[strlen(range) - 1] == '-') {
			/*
			 * case 2
			 */
			sscanf(range, "%d-", (int *)&offset);
			lastbyte = statbuf.st_size;
		} else {
			/*
			 * case 3
			 */
			sscanf(range, "%d-%d", (int *)&offset,
				(int *)&lastbyte);
		}

		totalbytes = (lastbyte - offset) + 1;

	} else {
		offset = 0;
		totalbytes = statbuf.st_size;
	}

	if ((fd = open(filename, O_RDONLY)) < 0) {
		return(-1);
	}

	if (offset > 0) {
		if (lseek(fd, offset, SEEK_SET) < 0) {
			return(-1);
		}
	}

	/*
	 * output the HTTP headers
	 */
	if (range != NULL) {
		printf("HTTP/1.1 %d\n", HTTP_PARTIAL_CONTENT);
	} else {
		printf("HTTP/1.1 %d\n", status);
	}

	printf("Content-Type: application/octet-stream\n");
	printf("Content-Length: %d\n", (int)totalbytes);
	printf("\n");

	bytesread = 0;
	done = 0;
	while (!done) {
		ssize_t	i;

		if ((sizeof(buf) + bytesread) > totalbytes) {
			count = totalbytes - bytesread;
		} else {
			count = sizeof(buf);
		}

		if ((i = read(fd, buf, count)) < 0) {
			/*
			 * log an error
			 */
			done = 1;
			continue;
		}

		/*
		 * output the buffer on stdout
		 */
		fwrite(buf, i, 1, stdout);

		bytesread += i;

		if (bytesread >= totalbytes) {
			done = 1;
		}
	}

	close(fd);
	return(0);
}

int
downloadfile(CURL *curlhandle, char *url, char *range)
{
	CURLcode	curlcode;

	if ((curlcode = curl_easy_setopt(curlhandle, CURLOPT_URL, url)) !=
			CURLE_OK) {
		fprintf(stderr, "downloadfile:curl_easy_setopt():failed:(%d)\n",
			curlcode);
		return(-1);
	}

#ifdef	DEBUG
	logdebug("URL : ");
	logdebug(url);
	logdebug("\n");
#endif

	if (range != NULL) {
		if ((curlcode = curl_easy_setopt(curlhandle, CURLOPT_RANGE,
				range)) != CURLE_OK) {
			fprintf(stderr,
				"downloadfile:curl_easy_setopt():failed:(%d)\n",
				curlcode);
			return(-1);
		}
#ifdef	DEBUG
		logdebug("HTTP RANGE: ");
		logdebug(range);
		logdebug("\n");
#endif
	}

	if ((curlcode = curl_easy_perform(curlhandle)) != CURLE_OK) {
		fprintf(stderr,
			"downloadfile:curl_easy_perform():failed:(%d)\n",
			curlcode);
		return(-1);
	}

	return(0);
}

int
createdir(char *path)
{
	struct stat	buf;
	char		*ptr;
	char		*lastptr;
	char		done = 0;

	if (strlen(path) == 0)
		return(0);

	if (path[0] != '/') {
		return(0);
	}

	lastptr = &path[1];

	while (!done) {
		if ((ptr = index(lastptr, '/')) == NULL) {
			done = 1;
			continue;
		}

		*ptr = '\0';

		if (stat(path, &buf) != 0) {
			if (mkdir(path, 0755) != 0) {
				return(-1);
			}
		}

		*ptr = '/';

		lastptr = ptr + 1;
		if (lastptr >= (path + strlen(path))) {
			done = 1;
		}
	}

	/*
	 * we've created all the parent directories, now create the
	 * last directory
	 */
	if (mkdir(path, 0755) != 0) {
		return(-1);
	}

	return(0);
}

int
getlocal(char *filename, char *range)
{
	struct stat	buf;

	if (stat(filename, &buf) == 0) {
		status = HTTP_OK;

		if (outputfile(filename, range) != 0) {
			fprintf(stderr, "outputfile():failed:(%d)\n", errno);
			return(-1);
		}
	} else {
		return(-1);
	}

	return(0);
}

int
getremote(char *filename, in_addr_t *ip, char *range)
{
	CURL		*curlhandle;
	CURLcode	curlcode;
	struct in_addr	in;
	struct stat	buf;
	FILE		*file;
	char		url[PATH_MAX];
	char		*dir;
	char		*ptr;

	in.s_addr = *ip;

fprintf(stderr, "getremote: get file (%s) from (%s)\n",
	filename, inet_ntoa(in));

	status = HTTP_OK;

	/*
	 * we know the file is not on the local hard disk (because getlocal()
	 * is called before this function), so try to download the file
	 * from a peer
	 */

	/*
	 * make sure the destination directory exists
	 */
	if ((dir = strdup(filename)) != NULL) {
		if ((ptr = rindex(dir, '/')) != NULL) {
			*ptr = '\0';
			if (stat(dir, &buf) != 0) {
				createdir(dir);
			}
		}

		free(dir);
	}

	/*
	 * make a 'http://' url and get the file.
	 */
	if ((file = fopen(filename, "w")) == NULL) {
		fprintf(stderr, "getremote:fopen():failed\n");
		return(-1);
	}

	/*
	 * initialize curl
	 */
	if ((curlhandle = curl_easy_init()) == NULL) {
		return(-1);
	}

#ifdef	DEBUG
	curl_easy_setopt(curlhandle, CURLOPT_VERBOSE, 1);
#endif

	/*
	 * tell curl to save it to disk (save it to the file pointed
	 * to by 'file'
	 */
	if ((curlcode = curl_easy_setopt(curlhandle, CURLOPT_WRITEDATA,
			file)) != CURLE_OK) {
		fprintf(stderr, "getremote:curl_easy_setopt():failed:(%d)\n",
			curlcode);
		return(-1);
	}

	if ((curlcode = curl_easy_setopt(curlhandle, CURLOPT_HEADERFUNCTION,
			doheaders)) != CURLE_OK) {
		fprintf(stderr, "getremote:curl_easy_setopt():failed:(%d)\n",
			curlcode);
		return(-1);
	}

	if ((curlcode = curl_easy_setopt(curlhandle, CURLOPT_WRITEFUNCTION,
			dobody)) != CURLE_OK) {
		fprintf(stderr, "getremote:curl_easy_setopt():failed:(%d)\n",
			curlcode);
		return(-1);
	}

	if (makeurl("http://", filename, inet_ntoa(in), url, sizeof(url)) != 0){
		fprintf(stderr, "getremote:makeurl():failed:(%d)", errno);
		return(-1);
	}

	if (downloadfile(curlhandle, url, NULL) != 0) {
		fprintf(stderr, "getremote:downloadfile():failed\n");

		/*
		 * don't return on failure here. we still need
		 * to do some cleanup
		 */
		status = HTTP_NOT_FOUND;
	}

	fclose(file);

fprintf(stderr, "getremote:status (%d)\n", status);

	/*
	 * cleanup curl
	 */
	curl_easy_cleanup(curlhandle);

	/*
	 * we downloaded the file from a peer, so read it and output it
	 * to stdout
	 */
	if ((status >= HTTP_OK) && (status <= HTTP_MULTI_STATUS)) {
		if (outputfile(filename, range) != 0) {
			fprintf(stderr, "outputfile():failed:(%d)\n", errno);
			return(-1);
		}
	} else {
		/*
		 * on a failure, a zero-byte length file will be
		 * left on the disk -- this is because of the fopen().
		 * remove this zero-length file.
		 */
		unlink(filename);
		return(-1);	
	}

	return(0);
}

int
trackfile(char *filename, char *range)
{
	uint64_t	hash;
	uint16_t	num_trackers;
	in_addr_t	*trackers;
	uint16_t	maxpeers;
	uint16_t	num_pkg_servers;
	in_addr_t	*pkg_servers;
	uint16_t	i;
	tracker_info_t	*tracker_info, *infoptr;
	int		sockfd;
	int		info_count;
	char		success;

	hash = hashit(filename);

	if (init(&num_trackers, &trackers, &maxpeers, &num_pkg_servers,
			&pkg_servers) != 0) {
		fprintf(stderr, "main:init failed\n");
		return(-1);
	}

	if ((sockfd = init_tracker_comm(0)) < 0) {
		fprintf(stderr, "main:init_tracker_comm failed\n");
		return(-1);
	}

	tracker_info = NULL;
	for (i = 0 ; i < num_trackers; ++i) {
		struct in_addr	in;

		in.s_addr = trackers[i];

		info_count = lookup(sockfd, &trackers[i], filename,
			&tracker_info);

		if (info_count > 0) {
			break;
		}

		/*
		 * lookup() mallocs space for 'tracker_info', so need to
		 * free it here since we'll call lookup() again in the
		 * next iteration
		 */
		if (tracker_info != NULL) {
			free(tracker_info);
			tracker_info = NULL;
		}
	}

	success = 0;
	if ((info_count > 0) && (tracker_info[0].hash == hash)) {
		infoptr = &tracker_info[0];

		fprintf(stderr, "info:hash (0x%lx)\n", infoptr->hash);
		fprintf(stderr, "info:numpeers (%d)\n", infoptr->numpeers);

		fprintf(stderr, "info:peers: ");

		for (i = 0 ; i < infoptr->numpeers; ++i) {
			struct in_addr	in;

			in.s_addr = infoptr->peers[i];
			fprintf(stderr, "%s\n", inet_ntoa(in));
		}

		/*
		 * randomly shuffle the peers
		 */
		if (shuffle(infoptr->peers, infoptr->numpeers) != 0) {
			/*
			 * not a critical error, but it should be logged
			 */
			fprintf(stderr, "trackfile:shuffle:failed\n");
		}

		fprintf(stderr, "info:peers:after shuffle: ");

		for (i = 0 ; i < infoptr->numpeers; ++i) {
			struct in_addr	in;

			in.s_addr = infoptr->peers[i];
			fprintf(stderr, "%s\n", inet_ntoa(in));
		}

		for (i = 0 ; i < infoptr->numpeers; ++i) {
			if (getremote(filename, &infoptr->peers[i], range)
					== 0) {

				/*
				 * successful download, exit this loop
				 */
				success = 1;
				break;
			}
		}
	}

	if (!success) {
		/*
		 * unable to download the file from a peer, need to get it
		 * from one of the package servers
		 */
		for (i = 0 ; i < num_pkg_servers ; ++i) {
			if (getremote(filename, &pkg_servers[i], range) == 0) {
				success = 1;
				break;
			}
		}
	}

	if (success) {
		tracker_info_t	info[1];

		bzero(info, sizeof(info));

		info[0].hash = hash;
		info[0].numpeers = 0;

		for (i = 0 ; i < num_trackers; ++i) {
			register_hash(sockfd, &trackers[i], 1, info);
		}
	}

	/*
	 * lookup() mallocs tracker_info
	 */
	if (tracker_info != NULL) {
		free(tracker_info);
	}	

	/*
	 * init() mallocs trackers
	 */
	free(trackers);

	if (success) {
		return(0);
	}

	return(-1);
}

int
main()
{
	char	*forminfo;
	char	*range;
	char	filename[PATH_MAX];
	char	serverip[16];

	bzero(filename, sizeof(filename));
	bzero(serverip, sizeof(serverip));

	if ((forminfo = getenv("QUERY_STRING")) == NULL) {
		senderror(500, "No QUERY_STRING", errno);
		return(0);
	}

	if ((range = getenv("HTTP_RANGE")) != NULL) {
		char	*ptr;

		if ((ptr = strchr(range, '=')) != NULL) {
			range = ptr + 1;
		}
	}

	if (getargs(forminfo, filename, serverip) != 0) {
		senderror(500, "getargs():failed", errno);
		return(0);
	}

	/*
	 * if the file is local, just read it off the disk, otherwise, ask
	 * the tracker where the file is
	 */
	if (getlocal(filename, range) != 0) {
		if (trackfile(filename, range) != 0) {
			senderror(404, "File not found", 0);
		}
	}

	return(0);
}

