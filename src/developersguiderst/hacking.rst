Hacking
-------

This is a hacking guide intended for developer and not for final users.

It tries to document some of the intricacies of the python 
library used which powers most of the logic behind Rocks.

Package distribution
====================

The Rocks python library is  distributed inside several subfolders:

* most of the rocks python library is now in ``src/rocks-pylib`` (this include
  rocks command line and many other tools)
* insert-ethers is under ``src/sql``
* kickstart.cgi setDbPartitions.cgi setPxeboot.cgi are under ``src/kickstart``
* rocks-console, big-red-button, gen_root_pw, rocks-db-perms, cluster-kill
  are under ``src/admin``


Rocks python library refactoring
================================

During the release cycle between Rocks 6.1 and 6.2 the python 
library underwent a major re-design in order to make the code 
more consistent and easier to extend. 

Listed here are some of the guiding principles followed during 
this re-design:

* *all connection* to the Rocks database must be created using the 
  class rocks.db.database.Database 
* most of the database manipulation must be done using the method 
  available in :class:`rocks.db.helper.Database` class (this class
  extend :class:`rocks.db.database.Database`).
  Some of the methods have already been moved here some are still 
  scattered in various location (e.g. a lot of them are still in 
  :class:`rocks.command`, ``rocks.sql``)
  The logic I followed is that if there are some *actions* on the 
  database which are generic enough that they might be needed in
  multiple location they should be placed inside 
  :class:`rocks.db.helper.Helper`, so all database logic is inside
  the package :mod:`rocks.db`
* all the ORM classes (which keeps mapping between DB table and
  python classes) are inside ``rocks.db.mappings.*``.
  The idea is to have one file per roll inside that folder. Obviously
  the base roll has most of the classes needed to play with DB.
  For this reason when updating or adding DB row it is easier to
  import all the modules with: ``from rocks.db.mappings.base import *``
* creating database table using directly SQL should be discouraged
  the new command ``rocks report databasesql`` can automatically
  generate SQL from a modules inside rocks.db.mappings.* (the
  base roll is not ready for that state yet). See KVM roll to see
  how to do it (``node/kvm-db.xml``). See KVM roll also on how to add
  generic functions to the rocks.db.helper.Database class
  (src/rocks-command/rocks/db/vmextend.py)



