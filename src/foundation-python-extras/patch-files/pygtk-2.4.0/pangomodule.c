/* -*- Mode: C; c-basic-offset: 4 -*-
 * pygtk- Python bindings for the GTK toolkit.
 * Copyright (C) 1998-2003  James Henstridge
 *
 *   pangomodule.c: module wrapping the Pango library
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
 * USA
 */
#ifdef HAVE_CONFIG_H
#  include "config.h"
#endif
#include <stdio.h>
#include <Python.h>
#include <pygobject.h>

#include <pango/pango-font.h>

/* include any extra headers needed here */

void pypango_register_classes(PyObject *d);
void pypango_add_constants(PyObject *module, const gchar *strip_prefix);
extern PyMethodDef pypango_functions[];

DL_EXPORT(void)
initpango(void)
{
    PyObject *m, *d;

    /* perform any initialisation required by the library here */

    m = Py_InitModule("pango", pypango_functions);
    d = PyModule_GetDict(m);

    init_pygobject();

    pypango_register_classes(d);
    pypango_add_constants(m, "PANGO_");
    
    PyModule_AddObject(m, "SCALE_XX_SMALL",
		       PyFloat_FromDouble(PANGO_SCALE_XX_SMALL));
    PyModule_AddObject(m, "SCALE_X_SMALL",
		       PyFloat_FromDouble(PANGO_SCALE_X_SMALL));
    PyModule_AddObject(m, "SCALE_SMALL",
		       PyFloat_FromDouble(PANGO_SCALE_SMALL));
    PyModule_AddObject(m, "SCALE_MEDIUM",
		       PyFloat_FromDouble(PANGO_SCALE_MEDIUM));
    PyModule_AddObject(m, "SCALE_LARGE",
		       PyFloat_FromDouble(PANGO_SCALE_LARGE));
    PyModule_AddObject(m, "SCALE_X_LARGE",
		       PyFloat_FromDouble(PANGO_SCALE_LARGE));
    PyModule_AddObject(m, "SCALE_XX_LARGE",
		       PyFloat_FromDouble(PANGO_SCALE_LARGE));    
    PyModule_AddObject(m, "SCALE",
		       PyInt_FromLong(PANGO_SCALE));    

    /* add anything else to the module dictionary (such as constants) */

}
