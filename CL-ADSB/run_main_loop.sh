#!/usr/bin/env bash

echo 'CL-ADSB tool runner script.'
echo
echo 'You must be in the same directory as cl_adsb.py for this to work'
echo

if [ "$#" -ne 1 ]
then
  echo 'No argument supplied'
  echo 'Use:'
  echo '     ./run_main_loop.sh t'
  echo '     t .... seconds to sleep between refreshes'
  exit 1
fi


while true
 do
  clear
  date
  python cl_adsb.py -c -m
  sleep $1
 done
