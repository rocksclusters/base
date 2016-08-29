#! /bin/bash
#
/usr/lib/rpm/pythondeps.sh --requires | sed -e '/\/usr\/local\/bin\/python/d' 

