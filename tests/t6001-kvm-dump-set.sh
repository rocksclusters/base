#!/bin/bash
#
# Test dhcpd.conf file creation 
#
                                                                                                                                                                    
test_description='Test kvm dump set commands (restore)

Test rocks set host vm, rocks dump host vm commands
'

pushd `dirname $0` > /dev/null
export TEST_DIRECTORY=`pwd`
popd > /dev/null
. $TEST_DIRECTORY/test-lib.sh



if ! rpm -q rocks-command-kvm > /dev/null
then
	skip_all='KVM roll not installed'
	test_done
fi


test_expect_success 'test KVM - steup test hosts (add host vm)' '
	rocks add host vm localhost compute name=test-host-1 num-macs=2
'

test_expect_success 'test KVM - test dump and set host cmd' '
	rocks dump host vm test-host-1 > dump &&
	rocks remove host vm test-host-1 &&
	bash dump &&
	rocks list host vm test-host-1 > temp_out &&
	test_line_count = 3 temp_out
'


test_expect_success 'test KVM - set host vm' '
	rocks set host vm test-host-1 mem=5535 &&
	rocks list host vm test-host-1 | grep 5535 > output &&
	test_line_count = 1 output &&
	test `awk "{print \\$2}" output` = 5535 &&
	rocks set host vm test-host-1 \
disk="file:/kvm/disks/test-host-1-0.vda,vda,virtio file:/kvm/disks/test-host-1-1.vda,vda,virtio" \
	disksize="67 28" &&
	rocks list host vm test-host-1 showdisks=1 > output &&
	test_line_count = 3 output &&
	grep "test-host-1-0.vda.*67" output &&
	grep "test-host-1-1.vda.*28" output
'
test_expect_success 'test KVM - set host vm cdrom' '
	rocks set host vm cdrom test-host-1 cdrom=/tmp/setup.iso &&
	rocks list host vm test-host-1 showdisks=1 > output &&
	grep /tmp/setup.iso output
'

test_expect_success 'test KVM - teardown test hosts (remove host)' '
	rocks remove host test-host-1 
'

test_done

