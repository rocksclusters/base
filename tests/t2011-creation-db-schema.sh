#!/bin/bash
#
# Test dhcpd.conf file creation 
#
                                                                                                                                                                    
test_description='Test creation of the database schema

Test the generation of a rocks database with the schema contained in 
node/database-schema.sh'

pushd `dirname $0` > /dev/null
export TEST_DIRECTORY=`pwd`
popd > /dev/null
. $TEST_DIRECTORY/test-lib.sh

NODES_DIR=$TEST_DIRECTORY/../nodes


attrs="{'os':'linux'}"

# need to hack the database-schema to create the tables 
# in our tempdb instead of the standard cluster db
test_expect_success 'test create db - setup' '
	/opt/rocks/mysql/bin/mysqladmin --defaults-extra-file=/root/.rocks.my.cnf --user=root  create tempdb &&
	test -f $NODES_DIR/database-schema.xml &&
	cat $NODES_DIR/database-schema.xml | \
		 rocks report post attrs="$attrs" | \
		sed "s|/opt/rocks/mysql/bin/mysql|echo |g" | \
		bash
'

test_expect_success 'test create db - test schema' '
	echo entering /tmp/tables.sql &&
	/opt/rocks/mysql/bin/mysql --defaults-extra-file=/root/.rocks.my.cnf \
		--user=root tempdb < /tmp/tables.sql &&
	echo entering /tmp/categories.sql &&
	/opt/rocks/mysql/bin/mysql --defaults-extra-file=/root/.rocks.my.cnf \
		--user=root tempdb < /tmp/categories.sql

'


test_expect_success 'test create db - tear down' '
	/opt/rocks/mysql/bin/mysqladmin --defaults-extra-file=/root/.rocks.my.cnf --user=root -f drop tempdb
'

test_done

