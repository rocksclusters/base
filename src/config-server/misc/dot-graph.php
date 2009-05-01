<?php
/* $Id: dot-graph.php,v 1.5 2009/05/01 19:07:05 mjk Exp $ */
#
# Dynamically creates an image of the Rocks Cluster Appliance
# graph.
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# Dont want users specifying their own malicious command via GET variables e.g.
# http://ganglia.mrcluster.org/graph.php?graph=blob&command=whoami;cat%20/etc/passwd
#

if($command)
	 {
		exit();
	 }

$landscape = escapeshellcmd(rawurldecode($HTTP_GET_VARS["landscape"]));
$size = escapeshellcmd(rawurldecode($HTTP_GET_VARS["size"]));
if (!$size) {
	$size = "66,58";
}
	

$format = "jpeg";

$command = "cd /export/rocks/install/; /opt/rocks/bin/rocks-dist ";
$command .= "--graph-draw-format $format --graph-draw-size $size --graph-draw-key ";
if ($landscape)
	$command .= "--graph-draw-landscape ";
$command .= "graph ";

# For debugging.
#echo "Command: $command<br>";

# Did we generate a command? Run it.
if($command)
 {
	/*Make sure the image is not cached*/
	header ("Expires: Mon, 26 Jul 1997 05:00:00 GMT");	// Date in the past
	header ("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT"); // always modified
	header ("Cache-Control: no-cache, must-revalidate");	// HTTP/1.1
	header ("Pragma: no-cache");				// HTTP/1.0
	if ($debug) {
		header ("Content-type: text/html");
		print "$command\n\n\n\n\n";
	 }
	else {
		header ("Content-type: image/$format");
		$fd = popen($command, "r");
		if (!$fd) return;
		
		while (!feof($fd))
			{
				$graph .= fread($fd, 2048);
			}
		pclose($fd);
		$len=strlen($graph);
		header("Content-length: $len");
		echo $graph;
	}
 }

?>

