#!/bin/bash
#
# Test kickstart.cgi script
#
                                                                                                                                                                    
test_description='Test kickstart syntax and generation

'

pushd `dirname $0` > /dev/null
export TEST_DIRECTORY=`pwd`
popd > /dev/null
. $TEST_DIRECTORY/test-lib.sh

hostname=`hostname`

rocks_build=/export/rocks/install/rocks-dist/x86_64/build

test_expect_success 'test rocks KS syntax - set up' '
	cp $TEST_DIRECTORY/t2009/test.xml $rocks_build/graphs/default/test.xml &&
	cp $TEST_DIRECTORY/t2009/test1.xml $rocks_build/nodes/test1.xml &&
	cp $TEST_DIRECTORY/t2009/test2.xml $rocks_build/nodes/test2.xml &&
	cp $TEST_DIRECTORY/t2009/test3.xml $rocks_build/nodes/test3.xml &&
	rocks list node xml test1
'

test_expect_success 'test rocks KS syntax  - file tag' '
	rocks list node xml test1 |rocks report post | bash &&
	echo test1.xml &&
	grep ciao /tmp/test1file &&
	grep localhost /tmp/test1file &&
	touch /tmp/RCS/test1file,v &&
	! grep ciao /tmp/test2file &&
	grep localhost /tmp/test1file &&
	echo test2.xml &&
	grep local /tmp/test2pipe &&
	grep local /tmp/test2pipesamefile &&
	echo test3.xml &&
	touch /tmp/RCS/test2pipe,v &&
	test ! -f /tmp/RCS/test3simplefile,v &&
	grep simple /tmp/test3simplefile &&
	grep Rocks /tmp/test3-release 
'


test_expect_success 'test rocks KS syntax - tear down' '
	rm $rocks_build/graphs/default/test.xml &&
	rm $rocks_build/nodes/test1.xml &&
	rm $rocks_build/nodes/test2.xml &&
	rm $rocks_build/nodes/test3.xml &&
	rm -rf /tmp/RCS/ &&
	rm /tmp/test1file &&
	rm /tmp/test2file &&
	rm /tmp/test2pipe &&
	rm /tmp/test2pipesamefile &&
	rm /tmp/test3simplefile &&
	rm /tmp/test3-release
'

test_done

