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

function get_free_ip(){
	# dummy function to get a free public IP
	# full of limitation but most of the time works
	rocks list host interface | awk '{if ( $2 == "public" ) {print $5}}' > usedIP
	lastip=`sort usedIP | tail -1`
	IFS='.' read -a array <<< "$lastip"
	number=${array[3]}
	while true; do
		number=$(( $number + 1 ))
		if [ ! "$number" ]; then 
			return 1
		fi
		if [ $number -ge 255 ]; then
			return 1
		fi
		newip=`echo ${array[0]}.${array[1]}.${array[2]}.$number`
		if ! grep $newip usedIP > /dev/null; then
			echo $newip
			return 0
		fi
	done

}

test_expect_success 'test KVM - steup test hosts (add host vm)' '
	rocks add host vm localhost compute name=test-host-1 num-macs=2
'
test_expect_success 'test KVM - steup test hosts (add cluster)' '
	ip=`get_free_ip` && test $? && test "$ip" &&
	rocks add cluster $ip 0 fe-name=test-host-0 cluster-naming=true
'


test_expect_success 'test KVM - list host vm' '
	rocks list host vm  > temp_out &&
	grep test-host-0 temp_out &&
	grep test-host-1 temp_out &&
	rocks list host vm showdisks=1 &&
	rocks list host vm status=1
'

test_expect_success 'test KVM - report host vm config compute' '
	rocks report host vm config test-host-1 > output &&
	xmllint output &&
	rocks set host installaction test-host-1 action="install vm frontend" &&
	rocks report host vm config test-host-1 > output &&
	xmllint output
'

test_expect_success 'test KVM - report host vm config FE' '
	rocks report host vm config test-host-0 > output &&
	xmllint output &&
	gw=`rocks report host attr localhost attr=Kickstart_PublicGateway` &&
	test $? && test "$gw" &&
	grep "gateway=$gw" output
'

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

test_expect_success 'test KVM - teardown test hosts (remove host)' '
	rocks remove cluster test-host-0 &&
	rocks remove host test-host-1 &&
	rocks list host > temp_out &&
	!( rocks list host | grep "test-host-0\|test-host-1" ) &&
	true
'

test_done

