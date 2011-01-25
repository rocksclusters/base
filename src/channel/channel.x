/* $Id: channel.x,v 1.1 2011/01/25 22:33:50 mjk Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: channel.x,v $
 * Revision 1.1  2011/01/25 22:33:50  mjk
 * for anoop
 *
 * Revision 1.3  2010/10/21 20:51:17  mjk
 * - timestamp is now a timeval (microseconds)
 * - re-entry testing is done in 411-alert-handler using a pickle file for state
 * - more logging
 *
 * Looks good, but need to turn down the logging to keep the network quite.
 *
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
		int CHANNEL_411_ALERT(string filename, string signature,
				      unsigned long sec, unsigned usec) = 2;
	} = 1;
} = 0xfeedface;

