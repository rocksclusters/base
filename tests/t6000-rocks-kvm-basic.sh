#!/bin/bash
#
# Test dhcpd.conf file creation 
#
                                                                                                                                                                    
test_description='Test basic kvm functionality


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
test_expect_success 'test KVM - steup test hosts (add cluster)' '
	ip=`rocks report nextip public` && test $? && test "$ip" && echo IP $ip &&
	rocks add cluster $ip 2 fe-name=test-host-0 cluster-naming=true
'


test_expect_success 'test KVM - list host vm' '
	rocks list host vm  > temp_out &&
	grep test-host-0 temp_out &&
	grep test-host-1 temp_out &&
	rocks list host vm showdisks=1 &&
	rocks list host vm status=1
'

test_expect_success 'test KVM - list cluster' '
	rocks list cluster test-host-0 > output &&
	test_line_count = 4 output
'

test_expect_success 'test KVM - report host vm config test memory' '
	rocks report host vm config test-host-1 > output &&
	memory=`echo -e "cat /domain/memory/text()" | xmllint  --shell output | tail -n-2| head -n-1` &&
	test $memory -gt 1045000
'

test_expect_success 'test KVM - report host vm config compute' '
	rocks set host interface subnet test-host-1 eth1 private &&
	rocks report host vm config test-host-1 > output &&
	xmllint output &&
	echo We have 2 interfaces for test-host-1 &&
	test `grep -c "\<interface\ " output ` -eq 2 &&
	virt-xml-validate output &&
	echo transform a compute into a frontend &&
	rocks set host installaction test-host-1 action="install vm frontend" &&
	rocks report host vm config test-host-1 > output &&
	xmllint output && 
	virt-xml-validate output
'

test_expect_success 'test KVM - report host vm config disablekvm interface' '
	rocks set host interface disablekvm test-host-1 eth1 True &&
	rocks list host interface disablekvm test-host-1 | grep True &&
	rocks report host vm config test-host-1 > output &&
	test `grep -c "<interface " output ` -eq 1 &&
        virt-xml-validate output
'

test_expect_success 'test KVM - report host vm config FE' '
	rocks report host vm config test-host-0 > output &&
	xmllint output &&
	gw=`rocks report host attr localhost attr=Kickstart_PublicGateway` &&
	test $? && test "$gw" &&
	grep "gateway=$gw" output
'

# my plugin are too stupid to generate valid libvirt xml so 
# skip the virt-xml-validate
python_path="/opt/rocks/lib/python2.6/site-packages/rocks/commands/report/host/vm/config/"
plugin_list="bootloader cpumem interface disk device global"
test_expect_success 'test KVM - report host vm config plugins' '
	for i in $plugin_list; do
		sed "s/%PLUGINNAME%/$i/" "$TEST_DIRECTORY"/t6000/plugin_device.py > $python_path/plugin_$i.py
	done &&
	rocks report host vm config test-host-0 > output &&
	echo test device &&
	grep -B 1 plugin_device output | head -1 | grep "</devices\>" &&
	echo test interface &&
	grep -B 1 plugin_interface output | head -1 | grep "</interface>" &&
	echo test disk &&
	grep -B 1 plugin_disk output | head -1 | grep "</disk>" &&
	for i in $plugin_list; do
		rm $python_path/plugin_$i.py*
	done

'

test_expect_success 'test KVM - dump host vm' '
	rocks dump host vm > output &&
	grep " test-host-0 " output &&
	grep " vm-test-host-0-0 " output &&
	grep " vm-test-host-0-1 " output
'


test_expect_success 'test KVM - teardown test hosts (remove host)' '
	rocks remove cluster test-host-0 &&
	rocks remove host test-host-1 &&
	rocks list host > temp_out &&
	!( rocks list host | grep "test-host-0\|test-host-1" ) &&
	true
'

test_done

