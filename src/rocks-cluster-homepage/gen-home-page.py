#!/opt/rocks/bin/python
# Generate a cluster home page
# @copyright@
# @copyright@
import os
import subprocess
import os.path
import sys
from operator import itemgetter

def colInfo(r):
        uguidepath=os.path.join('/roll-documentation',r[0],r[1])
        fullpath="/var/www/html/" + uguidepath
        if os.path.exists(fullpath):
                listelem=withguide % (r[0],r[1],uguidepath)
        else:
                listelem=withoutguide % (r[0],r[1])
        return  listelem

template = """
<!DOCTYPE html>
<html>
<head>
<style>
h2 { color: #016c93; }
.title {color: #0190c4; font-weight: bold;}
.cr {color: #7b8599; font-weight: bold;}
.tcolor { background-color: #e7efff;}
</style>
</head>
<body>

<table>
  <tr>
    <td valign="top">
      <img src="/images/rocks-logo.png" alt="Rocks Logo" width="100" />
    </td>
    <td>
      <h2>Welcome to the <i>%s</i> cluster home page</h2>
      <font class="title"><h3>Cluster Information</h3></font>
      <ul>
        <li><a href="/ganglia">Local ganglia monitoring instance</a> (if ganglia roll is installed)</li>
        <li><a href=\"/misc/dot-graph.php/\">Cluster kickstart graph</a>
        <li>Cluster contact: %s</li>
      </ul>
      <p>Visit <a href=\"http://www.rocksclusters.org\">Rocks Website</a> for latest news and updates </p>
    </td>
  </tr>
</table>

<table class="tcolor">
<tr><th colspan="4" bgcolor=""><font class="title"><h3>Installed Rolls</h3></font></th></tr>
%s
</table>

<p class="cr">(C) Copyright 2003 - 2017 UC Regents</p>

</body>
</html>
"""

## The following are templates for listing the installed rolls
withguide = "<td>&emsp;%s</td><td>(v.%s)&emsp;<a href=\"%s\">roll usersguide</a>&emsp;</td>"
withoutguide = "<td>&emsp;%s</td><td>(v.%s)</td>"

output = subprocess.check_output(["rocks","list","roll","output-header=no"]).replace(':','').split('\n')
rolls = filter(lambda x: len(x) > 0, map(lambda x: x.split(), output))
rolls = sorted(rolls, key=itemgetter(0))

all=len(rolls)
rows=len(rolls)/2
rollList=""
i = 0
while i <= rows :
    second = i+rows
    if second <= all-1  :
       if i == rows:
           col2 = colInfo(rolls[second])
           rollList += "<tr>\n<td colspan='2'> </td>\n%s</tr>\n" % (col2)
       else:
           col1 = colInfo(rolls[i])
           col2 = colInfo(rolls[second])
           rollList += "<tr>\n%s%s</tr>\n" % (col1, col2)
    i += 1

contact = subprocess.check_output(["rocks","report","host", "attr", "localhost", "attr=Info_ClusterContact"]).strip()
clustername = subprocess.check_output(["rocks","report","host", "attr", "localhost", "attr=Info_ClusterName"]).strip()

print template % (clustername,contact,rollList)
