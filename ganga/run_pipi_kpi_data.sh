#!/bin/bash

sleep_time=0
sleep_time_increment=600

for year in 2011 2012 ; do
  for decay in pipi kpi ; do
    for mag in up down ; do
      ( sleep $sleep_time ; ganga ${decay}-data-${year}.py $mag "rerun data for new triggers" ) &
      sleep_time=$(($sleep_time + 600))
    done
  done
done



