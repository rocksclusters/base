#!/bin/bash
#
# Test dhcpd.conf file creation 
#
# prerequisite none
#
#
# maxrun time 30 seconds

ScriptName=$0


function failIt(){

	echo  ---- failing $ScriptName ----
	echo  reason: $1
	exit 1
}


# create test interface
rocks add network test 10.5.0.0 255.255.0.0 dnszone=test mtu=1600 servedns=true
rocks add host interface localhost eth3 mac=16:77:6e:c0:00:03 ip=10.5.1.1 subnet=test
rocks add host interface localhost eth4 mac=16:77:6e:c0:00:04

# set ip addresses
rocks set host interface ip localhost eth3 ip=10.5.1.a && failIt "incorrect IP address did not fail"
rocks set host interface ip localhost eth3 ip=10.5.1.3 || failIt "unable to set ip address"
rocks report host interface localhost | grep 10.5.1.3 || failIt "unable to report ip address"

# test bonded interface
rocks add host bonded localhost channel=bond0 ip=10.5.1.3 network=test interfaces=eth3,eth4 || failIt "unable to create the bonded interface"
rocks report host interface localhost | grep bond0 || failIt "unable to report bond0 interface"

# tore down the tests interface
echo -e 'All tests were successful\nCleaning DB'
rocks remove host interface localhost bond0
rocks remove host interface localhost eth3
rocks remove host interface localhost eth4
rocks remove network test


