/*
 * Networkmodule.c - Python extension module that reports the
 * the IP addresses of activated network interfaces. This
 * is suprisingly hard to do with standard UNIX tools.
 *
 * Copyright 2002 Federico Sacerdoti <fds@sdsc.edu> and the UC 
 * Regents.
 *
 * "Active Ingredients" from libdnet-1.7:
 * 
 * Copyright (c) 2000-2003 Dug Song <dugsong@monkey.org>
 * All rights reserved, all wrongs reversed.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The names of the authors and copyright holders may not be used to
 *    endorse or promote products derived from this software without
 *    specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,
 * INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
 * AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
 * THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 * ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		           version 5.1  (VI)
 * 
 * Copyright (c) 2000 - 2008 The Regents of the University of California.
 * All rights reserved.	
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 * 
 * 1. Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 * 
 * 2. Redistributions in binary form must reproduce the above copyright
 * notice unmodified and in its entirety, this list of conditions and the
 * following disclaimer in the documentation and/or other materials provided 
 * with the distribution.
 * 
 * 3. All advertising and press materials, printed or electronic, mentioning
 * features or use of this software must display the following acknowledgement: 
 * 
 * 	"This product includes software developed by the Rocks(r)
 * 	Cluster Group at the San Diego Supercomputer Center at the
 * 	University of California, San Diego and its contributors."
 * 
 * 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
 * neither the name or logo of this software nor the names of its
 * authors may be used to endorse or promote products derived from this
 * software without specific prior written permission.  The name of the
 * software includes the following terms, and any derivatives thereof:
 * "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
 * the associated name, interested parties should contact Technology 
 * Transfer & Intellectual Property Services, University of California, 
 * San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
 * Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
 * 
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 * OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
 * IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 * @Copyright@
 *
 *
 * Compile like this:
 * gcc -fPIC -I/usr/include/python2.2 -c Networkmodule.c
 * gcc -shared -Wl -o Networkmodule.so Networkmodule.o \
 *   intf.o addr.o addr-utils.o strlcpy.o
 */

#include <Python.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include "dnet.h"
#include "dnet/eth.h"

/* For funtions returning a pointer. */
#define myerror(message) \
    { PyErr_SetString(ErrorObject, message); return NULL; }

/* For funtions returning an integer. */
#define Myerror(message) \
    { PyErr_SetString(ErrorObject, message); return -1; }

static PyObject *ErrorObject;

/* This function only populates the first (primary) IP
 * address for an interface. We can extend this to include
 * aliases later if necessary.
 */
static int
interfaces_callback(const struct intf_entry *entry, void *arg)
{
	PyObject *dict = (PyObject*) arg;
	char * name;
	char ip[64];
	int rc;


	/* Interface must be up */
	if (! (entry->intf_flags & INTF_FLAG_UP) )
		return 0;

	name = (char*) entry->intf_name;
	addr_ntop((const struct addr*) &entry->intf_addr, (char*) ip, (size_t) 64);
	if (!ip) Myerror("Could not find IP address for interface");

	rc = PyDict_SetItemString(dict, name, PyString_FromString(ip));
	if (rc<0) Myerror("adding to dictionary didn't work");

	/* printf("Adding interface %s: %s\n", name, ip); */

	return 0;
}



/* Returns a dictionary with Network Interface information:
 * dict["interface name (eth0)"] = "ip address"
 */

static PyObject *
interfaces(PyObject *self, PyObject *args)
{
	intf_t *intf;
	PyObject *dict;
	struct intf_entry *entry = NULL;

	dict = PyDict_New();
	if (!dict) return NULL;

	intf = intf_open();
	intf_loop( intf, interfaces_callback, (void*) dict );
	intf_close(intf);

	if (!dict) myerror("Could not read any net interfaces");

	return dict;
}


/* netcmp(a,b) returns 0 if IP address a is in the
 * same network as b, 1 otherwise.
 */

static PyObject *
netcmp(PyObject *self, PyObject *args)
{
	char *astr;
	char *bstr;
	struct addr a;
	struct addr b;
	int rval;
	int cmp = 0;
	struct intf_entry *entry = NULL;

	rval = PyArg_ParseTuple(args, "ss:netcmp",
					&astr, &bstr);

	if (!rval) return NULL;
	
	/* printf("Got addresses %s, %s\n", astr, bstr); */

	rval = addr_pton(astr, &a);
	if (rval<0)
			myerror("Could not read first address");

	rval = addr_pton(bstr, &b);
	if (rval<0)
			myerror("Could not read second address");

	cmp = addr_cmp(&a, &b);

	return Py_BuildValue("i", cmp);
}


static PyObject *
hi (PyObject *self, PyObject *args)
{
    return Py_BuildValue("s", "hi mom");
}


static PyObject *
ethernet_aton(PyObject *self, PyObject *args)
{
	char *nstr;
	char *astr;
	int asize;
	eth_addr_t eth_a;
	int rval;
	struct intf_entry *entry = NULL;

	rval = PyArg_ParseTuple(args, "s#:eth_aton",
					&astr, &asize);

	if (!rval) return NULL;
	
	/* printf("Got addresses %s, %s\n", astr, bstr); */

	rval = eth_aton(astr, &eth_a);
	if (rval<0)
		myerror("Could not convert address");

	return Py_BuildValue("s#", (char*) &eth_a, ETH_ADDR_LEN);
}


static PyObject *
ethernet_ntoa(PyObject *self, PyObject *args)
{
	char *nstr;
	char *astr;
	eth_addr_t eth_a;
	int rval;
	int nsize;
	struct intf_entry *entry = NULL;

	rval = PyArg_ParseTuple(args, "s#:eth_ntoa",
					&nstr, &nsize);

	if (!rval) return NULL;
	
	/* printf("Got addresses %s, %s\n", astr, bstr); */
	if (nsize != ETH_ADDR_LEN)
		myerror("Address is wrong length");

	memcpy(&eth_a, nstr, nsize);

	astr = eth_ntoa(&eth_a);
	if (!astr)
		myerror("Could not convert address");

	return Py_BuildValue("s", astr);
}


/* Python Method Registration Table. */
static struct PyMethodDef Network_methods[] = {
   { "interfaces",  interfaces,  METH_VARARGS },
   { "netcmp",  netcmp,  METH_VARARGS },
   { "eth_aton", ethernet_aton, METH_VARARGS },
   { "eth_ntoa", ethernet_ntoa, METH_VARARGS },
   { "hi", hi, METH_VARARGS },
   { NULL, NULL }
};


void
initNetwork()
{
   PyObject *m, *d;
   
   m = Py_InitModule("Network", Network_methods);
   
   /* Add "error" as a symbolic constant to this module. */
   d = PyModule_GetDict(m);
   ErrorObject = PyErr_NewException("Network.error", NULL, NULL);
   PyDict_SetItemString(d, "error", ErrorObject);
}





