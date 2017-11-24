#!/opt/rocks/bin/python
# Generate a cluster home page
# @copyright@
# @copyright@
import os
import subprocess
import os.path

template = """
<!DOCTYPE html>
<html>
<body>

<h1>
<img src="/images/rocks-logo.png" alt="Rocks Logo" width="139" height="139"
align="center"/>
Welcome to the %s cluster home page </h1>
<p> If <a href=\"http://ganglia.sourceforge.net\">ganglia</a> is
installed on your cluster, visit your <a href="/ganglia"> local monitoring 
instance</a> for information 
</p>

<p> You can <a href=\"/misc/dot-graph.php/\"> view your kickstart graph</a>

<p> The cluster contact is: %s</p>

<p> The <a href=\"http://www.rocksclusters.org\">Rocks rolls</a> installed are:
<ul>
%s
<ul>
</p>
<p> (C) 2003 - 2017 UC Regents </p>
</body>
</html>
"""

## The following are templates for listing the installed rolls
listtemplate="    <li>%s</li>\n"
withguide="%s (version %s) <a href=\"%s\">(roll usersguide)</a>"
withoutguide="%s (version %s)"
output=subprocess.check_output(["rocks","list","roll","output-header=no"]).replace(':','').split('\n')
rolls=filter(lambda x: len(x) > 0, map(lambda x: x.split(), output))

rollList=""
for r in rolls:
	uguidepath=os.path.join('/roll-documentation',r[0],r[1])
	fullpath="/var/www/html/" + uguidepath
	if os.path.exists(fullpath):
		listelem=withguide % (r[0],r[1],uguidepath)
	else:
		listelem=withoutguide % (r[0],r[1])

	rollList += listtemplate % listelem

contact = subprocess.check_output(["rocks","report","host", "attr", "localhost", "attr=Info_ClusterContact"]).strip()
clustername = subprocess.check_output(["rocks","report","host", "attr", "localhost", "attr=Info_ClusterName"]).strip()

print template % (clustername,contact,rollList)
