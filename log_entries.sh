#!/usr/bin/env bash

now=$(date +"%m_%d_%Y")
logfile="entries_$now.dat"

python2.7 manage.py getmodels >/dev/null 2>${logfile}
echo "Saved to file $logfile"