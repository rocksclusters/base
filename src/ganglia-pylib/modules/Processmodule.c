/*
 * Processmodule.c - Python extension module that reports the
 * top N processes by CPU usage.  
 *
 * Based on code from GNU's procps 2.0.7 package,
 * Copyright (C) 1996 Charles L. Blake, 1998 Michael K. Johnson,
 * and inherits the terms of the GNU Library General Public License.
 * Copyright 2002 Federico Sacerdoti <fds@sdsc.edu> and the UC 
 * Regents.
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		            version 5.0 (V)
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
 * gcc -fPIC -I/usr/include/python2.2 -c Processmodule.c
 * gcc -shared -Wl -o Processmodule.so Processmodule.o
 */

#include <Python.h>
#include <stdlib.h>
#include <stdio.h>
#include <pwd.h>
#include <sys/time.h>
#include <sys/types.h>
#include <dirent.h>
#include <sys/param.h>     /* for HZ */

#if defined __x86_64__
#include <sys/user.h>      /* for PAGE_SHIFT */
#else
#include <asm/page.h>      /* for PAGE_SHIFT */
#endif

#include <sys/stat.h>
#include <unistd.h>

/* useful macros */
#define bytetok(x)   (((x) + 512) >> 10)
#define pagetok(x)   ((x) << (PAGE_SHIFT - 10))

/* For funtions returning a pointer. */
#define myerror(message) \
    { PyErr_SetString(ErrorObject, message); return NULL; }

/* For funtions returning an integer. */
#define Myerror(message) \
    { PyErr_SetString(ErrorObject, message); return -1; }

static PyObject *ErrorObject;

struct process 
{
    char user[32];
    int pid;
    char name[64];
    float percent_cpu;
    long int utime;
    long int stime;
    long int starttime;
    float percent_mem;
    long int text;       /* Program text, bss memory size, in KB */
    long int data;      /* Program heap+stack size, in KB */
    long int shared;   /* Size of shared libs + IPC shm. */
    long int resident; /* The number of pages resident in core mem. */
    long int vm;       /* The number of pages allocated by Virtual Mem */
    long int major_faults;   /* Page faults requiring a read from disk */
};


/* Returns the interval between calls to this function, in seconds. */
static float
get_elapsed_time(void)
{
   struct timeval t;
   static struct timeval oldtime;
   struct timezone timez;
   float elapsed_time;

   gettimeofday(&t, &timez);
   elapsed_time = (t.tv_sec - oldtime.tv_sec)
      + (float) (t.tv_usec - oldtime.tv_usec) / 1000000.0;
   oldtime.tv_sec  = t.tv_sec;
   oldtime.tv_usec = t.tv_usec;

   return elapsed_time;
}


static long int
total_mem_kb(void)
{
   int len;
   FILE *meminfo;
   char buffer[2048], *p;
   long int memtotal;

   meminfo = fopen("/proc/meminfo", "r");
   if(!meminfo)
      return 0;

   len = fread(buffer, sizeof(char), sizeof(buffer)-1, meminfo);
   buffer[len] = '\0';
   fclose(meminfo);

   p = (char*) strstr( buffer, "MemTotal:" );
   if (!p)
      return 0;

   sscanf(p, "MemTotal: %lu ", &memtotal);
   return memtotal;
}


/* A more efficient, thread-safe pid->uid->username mapper. */
static void
pid2name(int pid, char *name)
{
   struct stat sb;
   char buffer[32];
   struct passwd *pw;
   int rc, uid;

   /* To insure a NULL string is returned on error. */
   *name='\0';

   sprintf(buffer, "/proc/%d", pid);

   rc=stat(buffer, &sb);
   if (rc<0) return;
   uid=sb.st_uid;

   pw=getpwuid(uid);
   if (!pw)
      sprintf(name,"%d",uid);
   else
      strcpy(name, pw->pw_name);

   /* Cannot free this? free(pw); */
}


static int
percent_cpu_sort (struct process *P, struct process *Q)
{
   if (P->percent_cpu < Q->percent_cpu) return 1;
   if (P->percent_cpu < Q->percent_cpu) return -1;
   return 0;
}


static void
read_proc(int pid, struct process *procs, int index)
{
	char filename[128];
	char line[512];
	FILE *stat, *statm;
	struct process *proc;
	char *tmp;
	int i, rc, n;
	long int resident, vmsize;

	proc = &procs[index];
	if (!proc) return;

	sprintf(filename, "/proc/%d/stat", pid);
	stat = fopen(filename, "r");
	if (!stat) {
		printf("WARNING: process %d could not be found.",pid);
		return;
	}
	fgets(line, sizeof(line), stat);
	fclose(stat);

	if (! *line) return;
	n=sscanf(line, 
		"%d (%s %*c %*d %*d %*d %*d %*d "  /* Start: pid, End: tgpid */
		"%*lu %*lu %*lu %lu %*lu " /* Start: flags, End: cmajflt */
		"%lu %lu %*ld %*ld %*ld "  /* Start: utime, End: priority */
		"%*ld %*lu %*ld %lu ",   /* Start: nice, End: starttime */
		&proc->pid, proc->name,
		&proc->major_faults,
		&proc->utime, &proc->stime,
		&proc->starttime);
	/* Remove the trailing ')' from the name */
	proc->name[strlen(proc->name)-1]='\0';

	/* Use the percent_cpu field to hold the number of new jiffies this
	 * process used since last time. */
	proc->percent_cpu = proc->utime + proc->stime - proc->percent_cpu;

	/* Get virtual memory statistics */
	sprintf(filename, "/proc/%d/statm", pid);
	statm = fopen(filename, "r");
	if (!statm) {
		printf("WARNING: process %d could not be found.",pid);
		return;
	}
	fgets(line, sizeof(line), statm);
	fclose(statm);

	if (! *line) return;
	/* The actual format is different than reported by the proc manpage.
		See /usr/src/linux/fs/proc/array.c.
		Size, Resident, Shared, Trs, Lrs, Drs, Dt */
	sscanf(line, "%lu %lu %lu %lu %*lu %*lu %*lu",
		&proc->vm, &proc->resident, &proc->shared, &proc->text);

	/* Data is defined as resident - shared. This may include text, and may
	 * not. Read-write heap pages are never shared. The stack is never
	 * shared. */ 
	proc->data = proc->resident - proc->shared;

	/* Convert to KB */
	proc->resident = pagetok(proc->resident);
	proc->text = pagetok(proc->text);
	proc->data = pagetok(proc->data);
	proc->shared = pagetok(proc->shared);
	proc->vm = pagetok(proc->vm);

}

/* Data is defined as resident - shared. This may include text, and may not.
Read-write heap pages are never shared. The stack is never shared.

Fork() calls will increase the number of shared pages because of copy-on-write
semantics. A page is "shared" if its reference count > 1. This figure counts
more than IPC shared memory pages.
*/

static PyObject *
ps (PyObject *self, PyObject *args)
{
	int pid, npids=0;
	int i=0, rval;
	int nprocs = 1;
	struct process *procs;      /* The top N processes by cpu usage */
	struct process *p;
	DIR *d;
	struct dirent *de;
	float delta;
	float sleeptime = 0.2;
	char s[64];
	PyObject *proc_list;
	PyObject *dict;

	/* How many processes do we report? */
	rval = PyArg_ParseTuple(args, "|if:ps",
				&nprocs, &sleeptime);
	if (!rval) return NULL;

	if (!(d = opendir ("/proc"))) {
		perror ("/proc"); exit (1);
	}
	/* First pass to see how many processes we have running */
	while (de = readdir (d))
		if (pid = atoi (de->d_name))
			npids++;
	procs = (struct process *) calloc(npids, sizeof(*procs));

	/* Second pass to populate our procs list */
	rewinddir(d);
	get_elapsed_time();
	i=0;
	while (de = readdir (d))
		if (pid = atoi (de->d_name)) {
			/* Insure no extra pids have been created since we
			 * counted. */
			if (i>=npids) break;
			read_proc(pid, procs, i);
			i++;
		}

	/* Sleep a bit so we don't grab all the %cpu while measuring it.
	 * Also improves the quality of measurements by increasing delta.
	 */ 
	usleep(sleeptime * 1e6);

	/* Third pass to calculate percent CPU */
	rewinddir(d);
	delta = get_elapsed_time();
	i=0;
	while (de = readdir (d))
		if (pid = atoi(de->d_name)) {
			/* Insure no extra pids have been created since we
			 * counted. */
			if (i>=npids) break;
			read_proc(pid, procs, i);
			i++;
		}
	closedir (d);

	/* Fill in the remaining process fields. */
	for (i=0; i<npids; i++) {
		p=&procs[i];
		/* Remember we have stored the new ticks of this process in
		 * p->percent_cpu. */
		p->percent_cpu = (p->percent_cpu * 100/HZ) / delta;
		if (p->percent_cpu > 99.9) p->percent_cpu=99.9;

		p->percent_mem = 100.0 * (p->resident / (float) total_mem_kb());
		if (p->percent_mem > 99.9) p->percent_mem=99.9;

		pid2name(p->pid, p->user);
	}

	/* Sort by %CPU */
	qsort(procs, npids, sizeof(*procs), (void*)percent_cpu_sort);

	/*printf("The top %d processes, sorted by %%CPU:\n", nprocs);*/
	proc_list = PyList_New(nprocs);

	for (i=0; i<nprocs; i++) {
		if (i>=npids) break;
		p=&procs[i];

		/* Keys meant to mirror 'ps' standard headers. All values
		are repored in KB. */
		dict = Py_BuildValue(
			"{s:i, s:s, s:s, s:f, s:f, s:l, s:l, s:l, s:l}",
			"PID", p->pid,
			"COMMAND", p->name,
			"USER", p->user,
			"%CPU", p->percent_cpu,
			"%MEM", p->percent_mem,
			"SIZE", p->text,
			"DATA", p->data,
			"SHARED", p->shared,
			"VM", p->vm
			);
		if (!dict) {
			free(procs);
			myerror("Could not create process dictionary");
		}

		PyList_SetItem(proc_list, i, dict);
	}
	free(procs);
	return proc_list;
}


static PyObject *
cpus (PyObject *self, PyObject *args)
{
    return Py_BuildValue("i", get_nprocs());
}

static PyObject *
hi (PyObject *self, PyObject *args)
{
    return Py_BuildValue("s", "hi mom");
}


/* Python Method Registration Table. */
static struct PyMethodDef Process_methods[] = {
   { "ps",  ps,  METH_VARARGS },
   { "cpus",  cpus,  METH_VARARGS },
   { "hi", hi, METH_VARARGS },
   { NULL, NULL }
};


void
initProcess()
{
   PyObject *m, *d;
   
   m = Py_InitModule("Process", Process_methods);
   
   /* Add "error" as a symbolic constant to this module. */
   d = PyModule_GetDict(m);
   ErrorObject = PyErr_NewException("Process.error", NULL, NULL);
   PyDict_SetItemString(d, "error", ErrorObject);
}





