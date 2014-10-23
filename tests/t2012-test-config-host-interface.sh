#!/bin/bash
#
# Test dhcpd.conf file creation
#

test_description='Test rocks config host interface

Test the command rocks config host interface'

. ./test-lib.sh



ip=`rocks report nextip private`
test_expect_success 'config host interface - set up tests' '
	rocks add host utest-0-0 membership=compute os=linux cpus=1 rack=0 rank=0 &&
	rocks add host interface utest-0-0 eth0 ip=$ip mac=F1:F1:F1:F1:F1:F1 subnet=private
'


test_expect_success 'config host interface - verify' '
	#adding virtual host with same name
	rocks config host interface utest-0-0 iface=eth0,eth1,eth2 \
		mac=F1:F1:F1:F1:F1:F0,F1:F1:F1:F1:F1:F1,F1:F1:F1:F1:F1:F2 \
		module=none,none,none flag=,ks, &&
	rocks list host interface utest-0-0 | grep eth1 | grep $ip
'


test_expect_success 'config host interface - tear down' '
	rocks remove host utest-0-0
'

test_done
