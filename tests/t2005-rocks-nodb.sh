#!/bin/bash
#
# Test dhcpd.conf file creation 
#
                                                                                                                                                                    
test_description='Test command whicih should run without database connection

The command listed in this tests should be able to run with 
the mysql turned off
'

pushd `dirname $0` > /dev/null
export TEST_DIRECTORY=`pwd`
popd > /dev/null
. $TEST_DIRECTORY/test-lib.sh


node_name="attribute-node"
attr_name="test-attr"


# we need the site.attr in the following tests
test_expect_success 'test no db - set up tests' '
	rocks report host attr localhost > site.attr &&
	/etc/init.d/foundation-mysql stop
'

test_expect_success 'test no db - report' '
	rocks report version &&
	rocks report distro
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

rocks_version=`rocks report version`

test_expect_success 'test no db - rocks create distro' '
	rocks create distro rolls="kernel,$rocks_version base,$rocks_version" &&
	rm -rf rocks-dist
'

# this set of commands are run in anaconda in include/installclass/welcome_gui.py
# at installation time and they need to succede with the DB shut down
test_expect_success 'test no db - rocks list node xml root' '
	rocks list node xml root attrs=site.attrs > list_node_xml &&
	test_line_count -ge 5000 list_node_xml
'

test_expect_success 'test no db - rocks list host profile' '
	cat list_node_xml | rocks list host profile > list_host_profile &&
	test_line_count -ge 5000 list_host_profile
'

test_expect_success 'test no db - rocks list host installfile' '
	cat list_host_profile | rocks list host installfile section=kickstart > temp_file &&
	test_line_count -ge 5000 temp_file
'

NODES_DIR=$TEST_DIRECTORY/../nodes
# this command is run in boostrap0.sh
test_expect_success 'test no db - rocks report post' '
	/bin/cat $NODES_DIR/database.xml $NODES_DIR/database-schema.xml \
		$NODES_DIR/database-sec.xml | \
		/opt/rocks/bin/rocks report post \
		attrs="{\"hostname\":\"\", \"HttpRoot\":\"/var/www/html\",\"os\":\"linux\"}"\
		> script.sh &&
	test_line_count -ge 800 script.sh
'


test_expect_success 'test no db - tear down' '
	/etc/init.d/foundation-mysql start
'

test_done

