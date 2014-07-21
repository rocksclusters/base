#!/bin/bash
#
# Test dhcpd.conf file creation 
#
                                                                                                                                                                    
test_description='Test airboss

Airboss integration tests
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


test_expect_success 'test airboss - steup' '
	ip=`rocks report nextip public` && test $? && test "$ip" && echo IP $ip &&
	rocks add cluster $ip 2 fe-name=test-host-0 cluster-naming=true container-hosts=localhost &&
	rocks create keys key=/tmp/private.key passphrase=no > /tmp/public.key &&
	rocks add host key test-host-0 key=/tmp/public.key &&
	rocks list host key test-host-0 &&
	rocks list host key test-host-0 > output &&
	test_line_count -ge 6 output
'

test_expect_success 'test airboss - list host macs' '
	rocks list host macs test-host-0 key=/tmp/private.key status=1 > output &&
	test_line_count -eq 4 output &&
	rocks add host alias test-host-0 foo &&
	rocks list host macs foo key=/tmp/private.key &&
	echo serial test &&
	for i in `seq 1 15`; do rocks list host macs test-host-0 key=/tmp/private.key; done &&
	echo parallel test &&
	for i in `seq 1 15`; do rocks list host macs test-host-0 key=/tmp/private.key & done &&
	wait
'

test_expect_success 'test airboss - set host cdrom' '
	touch /tmp/isotest.iso &&
	rocks set host cdrom test-host-0 cdrom=/tmp/isotest.iso key=/tmp/private.key &&
	rocks list host vm test-host-0 showdisks=1|grep isotest.iso &&
	rocks set host cdrom test-host-0 cdrom=none key=/tmp/private.key &&
	! rocks list host vm test-host-0 showdisks=1|grep isotest.iso &&
	test_must_fail rocks set host cdrom test-host-0 cdrom=n  key=/tmp/private.key
'

# we turn on the virtual machine only if the processor supports it
test_expect_success 'test airboss - power on and off' '
	if  grep "svm\|vmx" /proc/cpuinfo  ; then
		rocks set host power vm-test-host-0-0 action=on key=/tmp/private.key &&
		ps auxf|grep kvm | grep vm-test-host-0-0 &&
		rocks set host power vm-test-host-0-0 action=off key=/tmp/private.key &&
		! ps auxf|grep kvm | grep vm-test-host-0-0
	fi
'

test_expect_success 'test airboss - teardown test' '
	rm -f /tmp/public.key /tmp/private.key &&
	rocks remove cluster test-host-0
'

test_done

