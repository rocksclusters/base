/*
 * $Id: sec_channel.x,v 1.1 2011/04/11 22:41:49 anoop Exp $
 *
 * @Copyright@
 * @Copyright@
 *
 * $Log: sec_channel.x,v $
 * Revision 1.1  2011/04/11 22:41:49  anoop
 * RPC service that initiates transfer of shared 411 key
 *
 */

program SEC_CHANNEL{
	version SEC_CHANNEL_VERS{
		int SEC_CHANNEL_PING(void) = 1;
		} = 1;
} = 0x20000001;
