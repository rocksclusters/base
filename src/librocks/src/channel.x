/* $Id: channel.x,v 1.1 2010/10/19 01:04:01 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: channel.x,v $
 * Revision 1.1  2010/10/19 01:04:01  mjk
 * *** empty log message ***
 *
 */

program CHANNEL_PROG {
	version CHANNEL_VERS {
		int CHANNEL_PING(void) = 1;
		int CHANNEL_411_ALERT(string) = 2;
	} = 1;
} = 0xfeedface;

