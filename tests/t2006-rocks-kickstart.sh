#!/bin/bash
#
# Test kickstart.cgi script
#
                                                                                                                                                                    
test_description='Test the kickstart.cgi python script 

it also test that the generated file can be properly 
translated into a valid anaconda kickstart file
'

pushd `dirname $0` > /dev/null
export TEST_DIRECTORY=`pwd`
popd > /dev/null
. $TEST_DIRECTORY/test-lib.sh

hostname=`hostname`


# on a standard frontend this should always return 
# a wan kickstart which should be more that 40 line 
# and contains wan.xml
test_expect_success 'test kickstart.cgi - wan kickstart' '
	wget -O ks.cfg --no-check-certificate "https://`hostname`/install/sbin/kickstart.cgi?arch=x86_64&np=1" &&
	test_line_count -ge 40 ks.cfg && 
	grep wan.xml ks.cfg
'


# we create a fake host and we assign its ip as an alias to our
# private interface so we can fake some kickstart request from this host
#
#TODO verify this IP does not already exists
fakeIP=10.1.1.200
interface=`rocks report host attr localhost attr=Kickstart_PrivateInterface`

test_expect_success 'test kickstart.cgi - local kickstart setup interface' '
	test $interface &&
	ifconfig $interface:5 $fakeIP up
'
interface=$interface:5

test_expect_success 'test kickstart.cgi - local kickstart non existent host' '
	curl --interface $interface -o ks.cfg   -k "https://`hostname`/install/sbin/kickstart.cgi?arch=x86_64&np=1"
	test_line_count -ge 1 ks.cfg &&
	grep KickstartError ks.cfg &&
	grep $fakeIP ks.cfg
'

test_expect_success 'test kickstart.cgi - kickstart setup fake host' '
	rocks add host test-0-0 membership=compute os=linux cpus=1 rack=0 rank=0 &&
	rocks add host interface test-0-0 eth0 ip=$fakeIP mac=F1:F1:F1:F1:F1:F1 subnet=private
'


test_expect_success 'test kickstart.cgi - kickstart fake host CGI' '
	curl --interface $interface -o ks.xml -k "https://`hostname`/install/sbin/kickstart.cgi?arch=x86_64&np=1"
	test_line_count -ge 100 ks.xml
'

rversion=`rocks report version`
rversion=RHEL${rversion:0:1}

test_expect_success 'test kickstart.cgi - kickstart fake host kickstart generation kgen' '
	/etc/init.d/foundation-mysql stop &&
	cat ks.xml | /opt/rocks/bin/rocks list host profile 2> /tmp/kgen.debug | \
	/opt/rocks/bin/rocks list host installfile section=kickstart > ks.cfg 2>> /tmp/kgen.debug &&
	/usr/bin/ksvalidator -v $rversion -e ks.cfg &&
	cat /tmp/kgen.debug &&
	test_line_count -eq 0 /tmp/kgen.debug
	
'

test_expect_success 'test kickstart.cgi - local kickstart tear down' '
	/etc/init.d/foundation-mysql start &&
	rocks remove host test-0-0 &&
	ifconfig $interface down
'

test_done

