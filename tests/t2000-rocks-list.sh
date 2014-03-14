#!/bin/sh
#
# Luca Clementi
#

test_description='rocks list and dump commands

Tests all the lists and dump commands'


. ./test-lib.sh


test_expect_success 'rocks list appliance' '
	rocks list appliance
'

test_expect_success 'rocks list appliance' '
	rocks list appliance
'

test_expect_success 'rocks list appliance attr' '
	rocks list appliance attr
'

test_expect_success 'rocks list appliance route ' '
	rocks list appliance route 
'

test_expect_success 'rocks list appliance xml compute' '
	rocks list appliance xml compute
'

test_expect_success 'rocks list attr ' '
	rocks list attr 
'

test_expect_success 'rocks list bootaction ' '
	rocks list bootaction 
'

test_expect_success 'rocks list distribution ' '
	rocks list distribution 
'

test_expect_success 'rocks list firewall' '
	rocks list firewall
'

test_expect_success 'rocks list help' '
	rocks list help
'

test_expect_success 'rocks list host' '
	rocks list host
'

test_expect_success 'rocks list host alias ' '
	rocks list host alias 
'

test_expect_success 'rocks list host appliance ' '
	rocks list host appliance 
'

test_expect_success 'rocks list host attr' '
	rocks list host attr
'

test_expect_success 'rocks list host boot' '
	rocks list host boot
'

test_expect_success 'rocks list host firewall' '
	rocks list host firewall
'

test_expect_success 'rocks list host graph' '
	rocks list host graph
'

# I don't know what this file does
#test_expect_success 'rocks list host installfile section="kickstart"' '
#	rocks list host installfile section="kickstart"
#'

test_expect_success 'rocks list host interface' '
	rocks list host interface
'

test_expect_success 'rocks list host key' '
	rocks list host key
'

test_expect_success 'rocks list host membership' '
	rocks list host membership
'

test_expect_success 'rocks list host partition' '
	rocks list host partition
'

test_expect_success 'rocks list host profile localhost' '
	rocks list host xml localhost | rocks list host profile
'

test_expect_success 'rocks list host roll' '
	rocks list host roll
'

test_expect_success 'rocks list host route ' '
	rocks list host route 
'

test_expect_success 'rocks list host sec_attr' '
	rocks list host sec_attr
'

test_expect_success 'rocks list host xml' '
	rocks list host xml localhost
'

test_expect_success 'rocks list license ' '
	rocks list license 
'

test_expect_success 'rocks list membership' '
	rocks list membership
'

test_expect_success 'rocks list network' '
	rocks list network
'

test_expect_success 'rocks list node xml base' '
	rocks list node xml base
'

test_expect_success 'rocks list os attr' '
	rocks list os attr
'

test_expect_success 'rocks list os route ' '
	rocks list os route 
'

test_expect_success 'rocks list roll' '
	rocks list roll
'

test_expect_success 'rocks list roll command' '
	rocks list roll command
'

test_expect_success 'rocks list route ' '
	rocks list route 
'

test_expect_success 'rocks list sec_attr ' '
	rocks list sec_attr 
'

test_expect_success 'rocks list var' '
	rocks list var
'

test_expect_success 'rocks dump' '
	rocks dump
'

test_done
