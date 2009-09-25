/*
 * $Id: tracker-client.c,v 1.3 2009/09/25 21:02:04 bruno Exp $
 *
 * @COPYRIGHT@
 * @COPYRIGHT@
 *
 * $Log: tracker-client.c,v $
 * Revision 1.3  2009/09/25 21:02:04  bruno
 * got prediction code in
 *
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
#include <stdarg.h>
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
extern int send_done(int, in_addr_t *);
extern void logmsg(const char *, ...);

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
	logmsg("doheaders : ");
	logmsg(ptr);
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

#ifdef	DEBUG
	logmsg("outputfile:filename (%s)\n", filename);
#endif

	while (!done) {
		ssize_t	i;

		if ((sizeof(buf) + bytesread) > totalbytes) {
			count = totalbytes - bytesread;
		} else {
			count = sizeof(buf);
		}

		if ((i = read(fd, buf, count)) < 0) {
			logmsg("outputfile:read failed: errno (%d)\n", errno);
			done = 1;
			continue;
		}

		/*
		 * output the buffer on stdout
		 */
		fwrite(buf, i, 1, stdout);

		bytesread += i;

#ifdef	DEBUG
		logmsg("outputfile:bytesread (%d), totalbytes (%d)\n",
			bytesread, totalbytes);
#endif

		if (bytesread >= totalbytes) {
			done = 1;
		}
	}

	fflush(stdout);
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
	logmsg("URL : ");
	logmsg(url);
	logmsg("\n");
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
		logmsg("HTTP RANGE: ");
		logmsg(range);
		logmsg("\n");
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

#ifdef	DEBUG
		logmsg("getlocal:file (%s)\n", filename);
#endif

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

#ifdef	DEBUG
	logmsg("getremote: get file (%s) from (%s)\n", filename, inet_ntoa(in));
#endif

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
		logmsg("getremote:fopen():failed\n");
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
		logmsg("getremote:curl_easy_setopt():failed:(%d)\n", curlcode);
		return(-1);
	}

	if ((curlcode = curl_easy_setopt(curlhandle, CURLOPT_HEADERFUNCTION,
			doheaders)) != CURLE_OK) {
		logmsg("getremote:curl_easy_setopt():failed:(%d)\n", curlcode);
		return(-1);
	}

	if ((curlcode = curl_easy_setopt(curlhandle, CURLOPT_WRITEFUNCTION,
			dobody)) != CURLE_OK) {
		logmsg("getremote:curl_easy_setopt():failed:(%d)\n", curlcode);
		return(-1);
	}

	if (makeurl("http://", filename, inet_ntoa(in), url, sizeof(url)) != 0){
		logmsg("getremote:makeurl():failed:(%d)", errno);
		return(-1);
	}

	if (downloadfile(curlhandle, url, NULL) != 0) {
		logmsg("getremote:downloadfile():failed\n");

		/*
		 * don't return on failure here. we still need
		 * to do some cleanup
		 */
		status = HTTP_NOT_FOUND;
	}

	/*
	 * cleanup curl
	 */
	curl_easy_cleanup(curlhandle);

	fflush(file);
	fclose(file);

#ifdef	DEBUG
	logmsg("getremote:status (%d)\n", status);
#endif

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

void
write_prediction_info(tracker_info_t *infoptr, int info_count)
{
	FILE	*file;
	int	len;
	int	i;

	/*
	 * the first entry in the tracker info is the entry that we
	 * explicitly asked for. all remaining entries are the predictions.
	 */
	if ((info_count <= 1) || (infoptr == NULL)) {
		return;
	}

	if ((file = fopen("/tracker.predictions", "w")) == NULL) {
		/*
		 * don't worry if this fails. it is just prediction data, it
		 * is not critical
		 */
		return;
	}

	/*
	 * skip the first entry
	 */
	infoptr = (tracker_info_t *)((char *)infoptr + sizeof(tracker_info_t) +
		(sizeof(infoptr->peers[0]) * infoptr->numpeers));

	for (i = 1 ; i < info_count ; ++i) {

#ifdef	DEBUG
		logmsg("prediction info\n");
		logmsg("info:hash (0x%lx)\n", infoptr->hash);
		logmsg("info:numpeers (%d)\n", infoptr->numpeers);
#endif
		
		len = sizeof(tracker_info_t) +
			(sizeof(infoptr->peers[0]) * infoptr->numpeers);

		if (fwrite(infoptr, 1, len, file) < len) {
			logmsg("write_prediction_info:fwrite:errno (%d)\n",
				errno);
		}

#ifdef	DEBUG
		logmsg("info:peers:\n");

		for (i = 0 ; i < infoptr->numpeers; ++i) {
			struct in_addr	in;

			in.s_addr = infoptr->peers[i];
			logmsg("\t%s\n", inet_ntoa(in));
		}
#endif

		/*
		 * move the infoptr to the next entry
		 */
		infoptr = (tracker_info_t *)((char *)infoptr + len);
	}

	fclose(file);
}

int
getprediction(uint64_t hash, tracker_info_t **info)
{
	FILE		*file;
	struct stat	statbuf;
	tracker_info_t	*p;
	size_t		readbytes;
	int		offset, size, len;
	int		retval;
	char		*buf;

#ifdef	DEBUG
	logmsg("getprediction:hash (0x%016lx)\n", hash);
#endif

	if (stat("/tracker.predictions", &statbuf) != 0) {
		return(0);
	}	

	if ((file = fopen("/tracker.predictions", "r")) == NULL) {
		return(0);
	}

	if ((buf = malloc(statbuf.st_size)) == NULL) {
		fclose(file);
		return(0);
	}

	if ((readbytes = fread(buf, 1, statbuf.st_size, file)) < len) {
		free(buf);
		fclose(file);
		return(0);
	}

	offset = 0;
	retval = 0;

	while (offset < statbuf.st_size) {
		p = (tracker_info_t *)((char *)buf + offset);	

		size = sizeof(tracker_info_t) +
			(sizeof(p->peers[0]) * p->numpeers);

		if (p->hash == hash) {
			/*
			 * found a prediction for this hash
			 */
			if ((*info = (tracker_info_t *)malloc(size)) != NULL) {
				memcpy(*info, p, size);
				retval = 1;
			}

			break;
		}

		offset += size;
	}

	free(buf);
	fclose(file);

	return(retval);
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

	/*
	 * see if there is a prediction for this file
	 */
	tracker_info = NULL;
	info_count = getprediction(hash, &tracker_info);

#ifdef	DEBUG
	if (info_count == 0) {
		logmsg("trackfile:pred miss (0x%016lx)\n", hash);
	} else {
		logmsg("trackfile:pred hit (0x%016lx)\n", hash);
	}
#endif

	if (info_count == 0) {
		/*
		 * no prediction. need to ask a tracker for peer info for
		 * this file.
		 */
		for (i = 0 ; i < num_trackers; ++i) {
#ifdef	DEBUG
			struct in_addr	in;

			in.s_addr = trackers[i];
			logmsg("trackfile:sending lookup to tracker (%s)\n",
				inet_ntoa(in));
#endif
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

		/*
		 * write the prediction info to a file	
		 */
		write_prediction_info(tracker_info, info_count);
	}

	success = 0;
	infoptr = tracker_info;
	if ((info_count > 0) && (infoptr->hash == hash)) {
#ifdef	DEBUG
		logmsg("getfile:hash (0x%lx)\n", infoptr->hash);
		logmsg("getfile:numpeers (%d)\n", infoptr->numpeers);

		logmsg("getfile:peers:\n");

		for (i = 0 ; i < infoptr->numpeers; ++i) {
			struct in_addr	in;

			in.s_addr = infoptr->peers[i];
			logmsg("\t%s\n", inet_ntoa(in));
		}
#endif
		/*
		 * randomly shuffle the peers
		 */
		if (shuffle(infoptr->peers, infoptr->numpeers) != 0) {
			/*
			 * not a critical error, but it should be logged
			 */
			fprintf(stderr, "getfile:shuffle:failed\n");
		}

#ifdef	DEBUG
		fprintf(stderr, "getfile:peers:after shuffle: ");

		for (i = 0 ; i < infoptr->numpeers; ++i) {
			struct in_addr	in;

			in.s_addr = infoptr->peers[i];
			fprintf(stderr, "%s\n", inet_ntoa(in));
		}
#endif
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

		if (!success) {
			/*
			 * unable to download the file from a peer, need to
			 * get it from one of the package servers
			 */
			for (i = 0 ; i < num_pkg_servers ; ++i) {
				if (getremote(filename, &pkg_servers[i], range)
						== 0) {
					success = 1;
					break;
				}
			}
		}

		if (success) {
			tracker_info_t	info[1];

			bzero(info, sizeof(info));

			info[0].hash = infoptr->hash;
			info[0].numpeers = 0;

			for (i = 0 ; i < num_trackers; ++i) {
				register_hash(sockfd, &trackers[i], 1, info);
			}
		}
	}

	/*
	 * lookup() and getprediction() mallocs tracker_info
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

#ifdef	DEBUG
	logmsg("main:getting file (%s)\n", filename);
#endif

	/*
	 * if the file is local, just read it off the disk, otherwise, ask
	 * the tracker where the file is
	 */
	if (getlocal(filename, range) != 0) {
		if (trackfile(filename, range) != 0) {
			senderror(404, "File not found", 0);
		}
	}

#ifdef	DEBUG
	logmsg("main:done:file (%s)\n\n", filename);
#endif

	return(0);
}

