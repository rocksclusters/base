#!/bin/bash
#
# Test kickstart.cgi script
#
                                                                                                                                                                    
test_description='Test the kickstart.cgi python script 

TODO: add more test: 1. test the ohter cgi functionalities 2. test real kickstart generation
'

pushd `dirname $0` > /dev/null
export TEST_DIRECTORY=`pwd`
popd > /dev/null
. $TEST_DIRECTORY/test-lib.sh

hostname=`hostname`


# on a standard frontend this should always return 
# a wan kickstart which should be more that 40 line 
# and contains wan.xml
test_expect_success 'test kickstart.cgi - test' '
	wget -O ks.cfg --no-check-certificate "https://`hostname`/install/sbin/kickstart.cgi?arch=x86_64&np=1" &&
	test_line_count -ge 40 ks.cfg && 
	grep wan.xml ks.cfg
'

test_done

