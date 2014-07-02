#!/bin/bash
#
# Test dhcpd.conf file creation 
#
                                                                                                                                                                    
test_description='Test insert-ether 

try to make some test on insert ether
'

pushd `dirname $0` > /dev/null
export TEST_DIRECTORY=`pwd`
popd > /dev/null
. $TEST_DIRECTORY/test-lib.sh


# real mac address from a SUN workstation with NVIDA NIC
magic_message1="May 22 16:12:18 `hostname` dhcpd: DHCPDISCOVER from 00:14:4f:80:de:00 via eth0: network 10.1.0.0/16: no free leases"
magic_message2="X_RHN_PROVISIONING_MAC_0: eth0 00:14:4f:80:de:00 none ks"



test_expect_success 'test insert-ether - set up' '
	which screen || (
	  echo We need screen for this test &&
	  yum --enablerepo base,update install screen ||
	  test_done
	)
'

test_expect_success 'test insert-ether - inset-host' '
	screen -d -m insert-ethers --basename utest-host --membership Compute 2> error  & 
	sleep 5 && 
	echo $magic_message1 >> /var/log/messages &&
	sleep 5 &&
	test_line_count -eq 0 error &&
	pgrep insert-ether 
'

test_expect_success 'test insert-ether - kickstart host' '
	testhostname=`rocks list host | grep utest-host` 
	test "$testhostname" &&
	testhostname=${testhostname%:*} &&
	test $testhostname &&
	echo the new hostname is "$testhostname" &&
	ip=`rocks list host interface $testhostname | grep private | awk "{print \\$4}"` &&
	test $ip &&
	interface=`rocks report host attr localhost attr=Kickstart_PrivateInterface` &&
	test $interface && 
	interface=$interface:5 &&
	echo Kickstarting on interface $interface ip $ip &&
	export interface hostname &&
	ifconfig $interface $ip up &&
	rocks list host interface $testhostname &&
	curl --interface $interface --header "$magic_message2" -o ks.cfg -k "https://`hostname`/install/sbin/kickstart.cgi?arch=x86_64&np=1" &&
	ifconfig $interface down &&
	test_line_count -ge 1000 ks.cfg
'

test_expect_success 'test insert-ether - check interface name of new hosts' '
	echo "Check interface name is set properly" &&
	rocks list host interface $testhostname | grep eth0 &&
	test_line_count -eq 0 error &&
	pgrep insert-ether
'


test_expect_success 'test insert-ether - tear down I' '
	rocks list host &&
	testhostname=`rocks list host | grep utest-host` &&
	test "$testhostname" &&
	testhostname=${testhostname%:*} &&
	test $testhostname &&
	insert-ethers --remove $testhostname &&
	! rocks list host $testhostname
'

test_expect_success 'test insert-ether - tear down II' '
	pkill insert-ether &&
	rm -f /var/lock/insert-ethers
'

test_done

