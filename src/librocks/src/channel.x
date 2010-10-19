/* $Id: channel.x,v 1.2 2010/10/19 23:06:29 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: channel.x,v $
 * Revision 1.2  2010/10/19 23:06:29  mjk
 * c is hard
 *
 * Revision 1.1  2010/10/19 01:04:01  mjk
 * *** empty log message ***
 *
 */

program CHANNEL_PROG {
	version CHANNEL_VERS {
		int CHANNEL_PING(void) = 1;
		int CHANNEL_411_ALERT(string filename,
			unsigned long time, string signature) = 2;
	} = 1;
} = 0xfeedface;

