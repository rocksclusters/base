#!/bin/bash
#
# Various networking tests
#
# prerequisite none
#
                          
                                                                                                                                                                    
test_description='rocks networking commands

Test some basic networking command with rocks command line'


. ./test-lib.sh

test_expect_success setup '

	# create test interface
	rocks add network testzz 10.199.0.0 255.255.0.0 dnszone=test mtu=1600 servedns=true &&
	rocks add host interface localhost eth37 mac=16:77:6e:c0:00:03 ip=10.199.1.1 subnet=testzz &&
	rocks add host interface localhost eth47 mac=16:77:6e:c0:00:04
'

test_expect_success 'rocks set host interface wrong ip' '
	# set ip addresses
	test_must_fail rocks set host interface ip localhost eth37 ip=10.199.1.a &&
	test_must_fail rocks set host interface ip localhost eth37 ip=10.199.1.2.1
'

test_expect_success 'rocks set host interface ip' '
	rocks set host interface ip localhost eth37 ip=10.199.1.3 &&
	rocks report host interface localhost | grep 10.199.1.3 &&
	rocks set host interface ip localhost eth47 ip=10.199.1.4 &&
	# interface without subnet does not get reported
	!( rocks report host interface localhost | grep 10.199.1.4)
'
#
## test bonded interface
#rocks add host bonded localhost channel=bond0 ip=10.5.1.3 network=test interfaces=eth3,eth4 || failIt "unable to create the bonded interface"
#rocks report host interface localhost | grep bond0 || failIt "unable to report bond0 interface"
#
#

test_expect_success 'teardown rocks networking' '
	# tear down the tests interface
	#rocks remove host interface localhost bond0
	rocks remove host interface localhost eth37 &&
	rocks remove host interface localhost eth47 &&
	rocks remove network testzz
	
'

test_done

