#!/bin/bash
#
# Test dhcpd.conf file creation 
#
# prerequisite none
#
#
# maxrun time 30 seconds



function testIt(){

	rocks report host dhcpd | rocks report script | bash
	/etc/init.d/dhcpd restart
	if [ "$?" != "0" ]; then
		echo ----  failing dhcpd.conf creation  -----
		rocks remove host test-0-0
		rocks remove host test-0-0-0
		exit -1
	fi

}

rocks add host test-0-0 membership=compute os=linux cpus=1 rack=0 rank=0
rocks add host interface test-0-0 eth0 ip=10.1.1.200 mac=F1:F1:F1:F1:F1:F1 subnet=private
rocks add host interface test-0-0 eth1  mac=F1:F1:F1:F1:F1:F2

testIt


#adding virtual host with same name
rocks add host test-0-0-0 membership=compute os=linux cpus=1 rack=0 rank=0
rocks add host interface test-0-0-0 eth0 ip=10.1.1.203 mac=F1:F1:F1:F1:F1:F5 subnet=private

testIt


rocks set host interface ip test-0-0 eth1 10.1.1.201
rocks set host interface subnet test-0-0 eth1 private

testIt


echo All test sucesfull cleaning DB
rocks remove host test-0-0
rocks remove host test-0-0-0


