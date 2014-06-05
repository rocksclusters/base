# Rocks python library 

This readme tries to document some of the intricacies of the python 
library used which powers most of the logic behind Rocks.

## Package distribution

The Rocks python library is distributed inside several RPM package.
(_Should we try to reduce the number of packages/subdirectory?_)

* rocks.command is under src/commands
* rocks is under src/pylib


The command line python scripts are inside:

* rocks is under src/commands
* insert-ethers is under src/sql
* kickstart.cgi setDbPartitions.cgi setPxeboot.cgi is under src/kickstart
* rocks-console, big-red-button, gen_root_pw, rocks-db-perms, cluster-kill
  are under src/admin


## Rocks python library refactoring

During the release cycle between Rocks 6.1 and 6.2 the python 
library underwent a major re-design in order to make the code 
more consistent and easier to extend. 

Listed here are some of the guiding principles followed during 
this re-design:

* _all connection_ to the Rocks database must be created using the 
  class rocks.db.database.Database 
* most of the database manipulation must be done using the method 
  available in rocks.db.helper.Database class (this class extend 
  rocks.db.database.Database). 
  Some of the methods have already been moved here some are still 
  scattered in various location (e.g. a lot of them are still in 
  rocks.command.*, rocks.sql rocks.clusterdb)
  If there are some _actions_ on the database which are 
  generic enough that they might be needed in some other modules
  they should be placed inside rocks.db.helper.Database, so all 
  database logic is inside the package rocks.db
* you can use the ORM classes created in rocks.db.mappings.base.*
  to play around with database (especially for update and insert)

 
