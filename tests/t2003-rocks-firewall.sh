#!/bin/bash
#
# Test dhcpd.conf file creation 
#
                                                                                                                                                                    
test_description='Test creation of dhcpd.conf

Test the generation of dhcpd.conf with some basic network configuration '

. ./test-lib.sh


test_firewall="TEST-FIREWALL-RULE-DELETEME"


test_expect_success 'test firewall - insert host rules' '
	/opt/rocks/bin/rocks add firewall	\
		host=localhost network=all	\
		service="372" protocol="tcp" action="REJECT"	\
		chain="INPUT" flags="--sport 1024:65535" rulename="A9994-$test_firewall" rulesrc="system" &&
	/opt/rocks/bin/rocks add firewall	\
		host=localhost network=private	\
		service="372" protocol="udp" action="REJECT"	\
		chain="INPUT" flags="--sport 1024:65535" rulename="A9995-$test_firewall" rulesrc="system"
'

test_expect_success 'test firewall - insert global rules' '
	/opt/rocks/bin/rocks add firewall global network=all service="all" flags="-i lo"\
		protocol="all" action="ACCEPT" chain="INPUT" rulename="A9996-$test_firewall" rulesrc="system" &&
	/opt/rocks/bin/rocks add firewall global network=public service="ssh" \
		protocol="tcp" action="ACCEPT" chain="INPUT" \
		flags="-m state --state NEW" rulename="A9997-$test_firewall" rulesrc="system"
'

test_expect_success 'test firewall - insert appliance rules' '
	/opt/rocks/bin/rocks add firewall appliance=login network=all service="3333" \
		protocol="tcp" action="REJECT" chain="INPUT" \
		comment="This is a unit test on firewall" rulename="A9998-$test_firewall" rulesrc="system"
'

test_expect_success 'test firewall - insert rule with attribute' '
	/opt/rocks/bin/rocks add firewall host=localhost chain=INPUT \
		flags="-m state --state NEW --source &Kickstart_PublicNetwork;/&Kickstart_PublicNetmask;" \
		protocol=tcp service=https action=ACCEPT network=public rulename="A9999-$test_firewall" rulesrc="system"
'

test_expect_success 'test firewall - insert duplicate rule' '
        /opt/rocks/bin/rocks add firewall appliance=login network=all service="3333" \
                protocol="tcp" action="REJECT" chain="INPUT" \
                comment="This is a unit test on firewall" rulename="A9998-$test_firewall" rulesrc="system" || true
'


test_expect_success 'test firewall - list rules' '
	/opt/rocks/bin/rocks list firewall &&
	/opt/rocks/bin/rocks list firewall host=localhost &&
	/opt/rocks/bin/rocks list firewall appliance=login 
'


attr="{'Kickstart_PublicNetwork':'123.111.111.0', 'Kickstart_PublicNetmask':'255.255.255.0'}"

test_expect_success 'test firewall - report rules' '
	/opt/rocks/bin/rocks report host firewall localhost | \
		/opt/rocks/bin/rocks report script \
		attrs="$attr"  > test.sh &&
	grep 123.111.111.0 test.sh
'


test_expect_success 'test firewall - tear down' '
	rocks remove firewall host=localhost A9994-$test_firewall &&
	rocks remove firewall host=localhost A9995-$test_firewall &&
	rocks remove firewall global A9996-$test_firewall &&
	rocks remove firewall global A9997-$test_firewall &&
	rocks remove firewall appliance=login A9998-$test_firewall &&
	rocks remove firewall host=localhost A9999-$test_firewall 
'

test_done

