#!/bin/bash
# Get an object from google drive (shared public). This uses the "uc" endpoint.
# usage:
#    gget.sh <objectid> [outputfile]
#	 if outputfile is not specified, the objectid is the outputfile
#
# requires:
#	curl
#	grep
#	sed
#
# example:
#    gget.sh 0B0LD0shfkvCRdk1NMVc1NlI2ZUk sage2-1.0.0.tar.bz2
#
# Note: this object has sha1sum
#    783ac71f01bde1c2d4abedf06cf43f99745e1d16  sage2-1.0.0.tar.bz2
#

## Clean up any left-overs
function cleanup
{
	if [ -f $COOKIE ]; then
		/bin/rm $COOKIE
	fi
	if [ -f $TMPFILE ]; then
		/bin/rm $TMPFILE
	fi
}
trap cleanup EXIT

### Download 
CWD=$(pwd)
COOKIE=$(mktemp --tmpdir=$CWD)
TMPFILE=$(mktemp --tmpdir=$CWD)
OBJECT=$1
if [ "x$2" != "x" ]; then
	OUTFILE=$2
else
	OUTFILE=$1
fi

## Retrieve the file
TEMPLATE="https://docs.google.com"
DLPATH="$TEMPLATE/uc?id=$OBJECT&export=download"
#wget -O $TMPFILE --save-cookie $COOKIE --load-cookie $COOKIE "$DLPATH"
curl -f --cookie-jar $COOKIE -o $TMPFILE -L "$DLPATH" 
## Handle the case where curl returned an error
if [ $? -ne 0 ]; then
	exit $?
fi

grep -q "confirm=" $TMPFILE
if [ $? -eq 0 ]; then
## We need to retry the download with the confirm code
	# echo  "Large Download ... retrying"
        REDIRECT=$(grep -o  'href="/uc?[[:alnum:][:punct:]]*confirm[[:alnum:][:punct:]]*"' $TMPFILE | sed -e 's#amp;##g' -e 's#href=##' -e 's#"##g')
	DLPATH="$TEMPLATE$REDIRECT"
	#wget -O $TMPFILE --save-cookie $COOKIE --load-cookie $COOKIE "$DLPATH"
	curl --cookie $COOKIE -o $TMPFILE -L "$DLPATH" 
fi
mv $TMPFILE $OUTFILE
