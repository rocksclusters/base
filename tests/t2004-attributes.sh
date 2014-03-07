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
		os=linux rack=10 rank=10 &&
	rocks list host 
'

# -- begin --  global
test_expect_success 'test attributes - global attributes' '
	rocks add attr $attr_name globa &&
	test `get_attr "$attr_name"` = "globa" &&
	rocks set attr $attr_name global &&
	test `get_attr "$attr_name"` = "global" &&
	test `get_host_attr localhost "$attr_name"` = "global" 
'
test_expect_success 'test attributes - global attributes add duplicate' '
	rocks add attr $attr_name global || true
'
test_expect_success 'test attributes - global attributes dump' '
	rocks dump attr | grep " $attr_name " 
'
# -- end -- global


# -- begin --  os
test_expect_success 'test attributes - os attributes' '
	rocks add os attr linux $attr_name os &&
	test `get_host_attr $node_name $attr_name` = "os" &&
	test `get_host_attr localhost $attr_name` = "os"
'
test_expect_success 'test attributes - os attributes add duplicate' '
	rocks add os attr linux $attr_name os2 || true
'
test_expect_success 'test attributes - os attributes set' '
	rocks set os attr linux $attr_name os2 &&
	test `get_host_attr $node_name ${attr_name}_old` = "os" &&
	test `get_host_attr $node_name ${attr_name} ` = "os2" &&
	rocks set os attr linux $attr_name os
'
test_expect_success 'test attributes - os attributes dump' '
        rocks dump os attr | grep " $attr_name " | grep os
'
# -- end -- os


# -- begin --  appliance
test_expect_success 'test attributes - appliance attributes' '
	rocks add appliance attr compute $attr_name appliance &&
	test `get_host_attr $node_name $attr_name` = "appliance" &&
	test `get_host_attr localhost $attr_name` = "os"
'
test_expect_success 'test attributes - appliance attributes add duplicate' '
	rocks add appliance attr compute $attr_name appliance2 || true
'
test_expect_success 'test attributes - appliance attributes set' '
	rocks set appliance attr compute $attr_name appliance2 &&
	test `get_host_attr $node_name ${attr_name}_old` = "appliance"
'
test_expect_success 'test attributes - appliance attributes dump' '
        rocks dump appliance attr | grep " $attr_name " | grep appliance
'
# -- end -- appliance


# -- begin --  host
test_expect_success 'test attributes - host attributes' '
	rocks add host attr $node_name $attr_name host &&
	test `get_host_attr $node_name $attr_name` = "host" &&
	test `get_host_attr localhost $attr_name` = "os"
'
test_expect_success 'test attributes - host attributes add duplicate' '
	rocks add host attr $node_name $attr_name host2 || true
'
test_expect_success 'test attributes - host attributes set' '
	rocks set host attr $node_name $attr_name host2 &&
	test `get_host_attr $node_name ${attr_name}_old` = "host" &&
	test `get_host_attr $node_name ${attr_name}` = "host2"
'
test_expect_success 'test attributes - host attributes dump' '
        rocks dump host attr | grep " $attr_name " | grep host2
'
# -- end -- host

test_expect_success 'test attributes - rocks report host attr' '
	rocks report host attr $node_name | grep "^$attr_name:" | grep host2
'

test_expect_success 'test attributes - tear down removing attribute' '
	rocks remove attr $attr_name &&
	rocks remove os attr $attr_name &&
	rocks remove appliance attr $attr_name &&
	rocks remove host attr $attr_name 
'

test_expect_success 'test attributes - tear down removing facke host' ' 
	rocks remove host $node_name
'

test_done

