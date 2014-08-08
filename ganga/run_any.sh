#!/bin/bash

sleep_time=0
sleep_time_increment=600


if [ "$1" == "--test" ] ; then
  test=1
  shift
  echo "This is a test."
else
  test=0
  echo "Not a test, running for real... Are you sure?"
  sleep 3
fi

comment="$1"
shift
echo "Comment: $comment"
echo "Datasets: $*"



for decay in $* ; do
  if [ "${decay}" != "emu" ] ; then
    years="2011 2012"
  else
    years="2011-blinded 2011-unblinded"
  fi
  for year in `echo $years` ; do
    aspos=`expr index "$decay" as`
    if [ "${decay:0:2}" == "mc" ] ; then
      if [ $aspos != 0 ] ; then
        asend=$(($aspos+1))
        file="${decay:2:`echo $((aspos-3))`}-mc-${decay:`echo $asend`}strip.py"
      else
        file="${decay:2}-mc.py"
      fi
    else
      if [ $aspos != 0 ] ; then
        asend=$(($aspos+1))
        file="${decay:0:`echo $(($aspos-1))`}-data-${year}-${decay:`echo $asend`}strip.py"
        year=""
      else
        file="${decay}-data-${year}.py"
        year=""
      fi
    fi
    
    
    for mag in up down ; do
      if [ $test == 1 ] ; then
        echo sleep $sleep_time ganga $file $mag $year "$comment"
      else
        ( sleep $sleep_time ; ganga $file $mag $year "$comment" ) &
      fi
      sleep_time=$(($sleep_time + 600))
    done
  done
done

jobs

