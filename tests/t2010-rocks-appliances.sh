#!/bin/bash
#
# Test kickstart.cgi script
#
                                                                                                                                                                    
test_description='Test rocks appliance commands

test various aspects of rocks appliance related commands
'

pushd `dirname $0` > /dev/null
export TEST_DIRECTORY=`pwd`
popd > /dev/null
. $TEST_DIRECTORY/test-lib.sh

hostname=`hostname`

rocks_build=/export/rocks/install/rocks-dist/x86_64/build

test_expect_success 'test rocks appliance - add routes' '
	rocks add appliance route nas 10.1.1.0 10.1.1.1 netmask=255.255.255.0 &&
	! rocks add appliance route compute nas 10.1.1.0 10.1.1.1 netmask=255.255.255.0 &&
	test `rocks list appliance route | grep 10.1.1.1  | wc -l` == "1" &&
	rocks add appliance route compute 10.1.1.0 10.1.1.1 netmask=255.255.255.0 &&
	test `rocks list appliance route | grep 10.1.1.1  | wc -l` == "2"
'

test_expect_success 'test rocks appliance - add routes' '
	/opt/rocks/bin/rocks add appliance test-appliance  membership='test-appliance' &&
	/opt/rocks/bin/rocks set appliance attr test-attr managed false &&
	rocks list appliance test-appliance
'


test_expect_success 'test rocks appliance - tear down' '
	rocks remove appliance test-appliance &&
	rocks remove appliance route nas 10.1.1.0 &&
	rocks remove appliance route compute 10.1.1.0 &&
	test `rocks list appliance route | grep 10.1.1.1  | wc -l` == "0"
'


test_done

