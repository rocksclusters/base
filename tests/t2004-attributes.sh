#!/bin/bash
#
# Test dhcpd.conf file creation 
#
                                                                                                                                                                    
test_description='Test attributes manipulation

Test various attributes manipulations'

pushd `dirname $0` > /dev/null
export TEST_DIRECTORY=`pwd`
popd > /dev/null
. $TEST_DIRECTORY/test-lib.sh


node_name="attribute-node"
attr_name="test-attr"

get_attr(){
	rocks list attr | grep "^$1:" | awk "{print \$2}";
}

get_host_attr(){
	rocks list host attr $1 | grep " $2 " | awk "{print \$3}";
}


test_expect_success 'test attributes - set up tests' '
	/opt/rocks/bin/rocks add host $node_name cpus=1 membership=compute\
		os=linux rack=10 rank=10
'

test_expect_success 'test attributes - global attributes' '
	rocks add attr $attr_name globa &&
	test `get_attr "$attr_name"` = "globa" &&
	rocks set attr $attr_name global &&
	test `get_attr "$attr_name"` = "global" &&
	test `get_host_attr localhost "$attr_name"` = "global" 
'
# rocks dump attr | grep " $attr_name "

test_expect_success 'test attributes - global attributes add duplicate' '
	rocks add attr $attr_name global || true
'

test_expect_success 'test attributes - global attributes dump' '
	rocks dump attr | grep " $attr_name " 
'

test_expect_success 'test attributes - host attributes' '
	rocks add host attr $node_name $attr_name host &&
	test `get_host_attr $node_name $attr_name` = "host" &&
	test `get_host_attr localhost $attr_name` = "global"
'

test_expect_success 'test attributes - host attributes add duplicate' '
	rocks add host attr $node_name $attr_name host2 || true
'

test_expect_success 'test attributes - host attributes dump' '
        rocks dump host attr | grep " $attr_name "
'

test_expect_success 'test attributes - tear down' '
	rocks remove attr $attr_name &&
	rocks remove host attr $attr_name &&
	rocks remove host $node_name
'

test_done

