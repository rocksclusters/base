#!/bin/bash
#
# Test dhcpd.conf file creation 
#
                                                                                                                                                                    
test_description='Test screen generation

The scren should run without DB connection and without libraries 
'

pushd `dirname $0` > /dev/null
export TEST_DIRECTORY=`pwd`
popd > /dev/null
. $TEST_DIRECTORY/test-lib.sh


out_dir=/tmp/updates/opt/rocks/screens


# we need the site.attr and a bunch of other stuff in the following tests
#
# we save the current distro so we don't have to re-create it
# this is just to save some time since rocks-buildscreens will 
# recreate a distro with only the base roll active
test_expect_success 'test buildscreens - set up tests' '
	rocks report host attr localhost > /tmp/site.attr &&
	cp "$TEST_DIRECTORY"/t2007/interfaces /tmp &&
	cp "$TEST_DIRECTORY"/t2007/rolls.xml /tmp &&
	if [ ! -f /opt/rocks/screens/rocks-buildscreens ] ; then 
		yum install rocks-screens
	fi &&
	mkdir -p $out_dir &&
	/etc/init.d/foundation-mysql stop && 
	mv /export/rocks/install/rocks-dist /export/rocks/install/orig-rocks-dist
'

# TODO: we should remove shared mysql libraries during this tests
#       but since we are a little lazy and this is a corner case we don't do it
# /opt/rocks/mysql/lib/libmysqlclient.a
# /opt/rocks/mysql/lib/libmysqlclient.so
# /opt/rocks/mysql/lib/libmysqlclient.so.18
# /opt/rocks/mysql/lib/libmysqlclient.so.18.1.0
# /opt/rocks/mysql/lib/libmysqlclient_r.a
# /opt/rocks/mysql/lib/libmysqlclient_r.so
# /opt/rocks/mysql/lib/libmysqlclient_r.so.18
# /opt/rocks/mysql/lib/libmysqlclient_r.so.18.1.0


test_expect_success 'test buildscreens - rocks-buildscreens' '
	/opt/rocks/screens/rocks-buildscreens > output &&
	test -f $out_dir/screens.html &&
	test_line_count -ge 2000 $out_dir/screens.html
'

test_expect_success 'test buildscreens - tear down' '
	/etc/init.d/foundation-mysql start &&
	rm -rf /export/rocks/install/rocks-dist &&
	mv /export/rocks/install/orig-rocks-dist /export/rocks/install/rocks-dist
'

test_done

