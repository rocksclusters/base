#!/bin/bash
#
# Script to parse the non-text sources metadata file and download
# the required files to build a roll from our web repo
#
# Please note: this script is non-destructive, it wont replace
# files that already exist, regardless of their state, allowing you
# to have work-in-progress content that wont get overwritten.
#

if [ ! "$SURL" ]; then
	# rocksclusters download base URL
	SURL="https://googledrive.com/host/0B0LD0shfkvCRRGtadUFTQkhoZWs"
fi

pn=$(basename `pwd`)
f=.${pn}.metadata


if [ ! -e ${f} ] ||  [ ! -d .git ]; then
  echo 'You need to run this from inside a sources git repo'
  exit 1
fi

while read a; do
  fsha=$( echo ${a}  | cut -f1 -d\ )
  fname=$( echo ${a} | cut -f2 -d\ )
  if [ ${fsha} = "da39a3ee5e6b4b0d3255bfef95601890afd80709" ]; then
    # zero byte file
    touch ${fname}
  else
    if [ ! -e ${fname} ]; then
      url=${SURL}/${pn}/`basename ${fname}`
      curl "$url" -o ${fname}
      if [ "$?" != "0" ]; then
          echo "Error download from URL $url"
          exit 1
      fi

      echo "${fsha}  ${fname}" | sha1sum -c --status;
      if [ "$?" != "0" ]; then 
          echo "Checksum error for file ${fname}"
          exit 1
      fi
    else
      echo "${fname} exists. skipping"
    fi
  fi
done < ${f}

