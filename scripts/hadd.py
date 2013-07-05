#!/usr/bin/env python

import sys
import subprocess

to_merge = [
  {
    "up"   : None,
    "down" : 145,
    "strip": "emu",
    "data" : "emu",
    "mc"   : True
  },
  {
    "up"   : 94,
    "down" : 93,
    "strip": "emu",
    "data" : "pipi",
    "mc"   : True
  },
  {
    "up"   : 96,
    "down" : 95,
    "strip": "emu",
    "data" : "mumu",
    "mc"   : True
  },
  {
    "up"   : 98,
    "down" : 99,
    "strip": "pipi",
    "data" : "emu",
    "mc"   : True
  },
  {
    "up"   : 100,
    "down" : 99,
    "strip": "pipi",
    "data" : "pipi",
    "mc"   : True
  },
  {
    "up"   : 102,
    "down" : 101,
    "strip": "mumu",
    "data" : "mumu",
    "mc"   : True
  },
  
  {
    "up"   : 126,
    "down" : 125,
    "strip": "emu",
    "data" : "emu",
    "mc"   : False
  },
  {
    "up"   : 148,
    "down" : 147,
    "strip": "pipi",
    "data" : "pipi",
    "mc"   : False
  },
]

directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/"
gangadir  = "/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/"

for config in to_merge:
  data_type = ("mc" if config['mc'] else "") + config['data']
  dir_name = directory + data_type + "/"
  
  for magnet_polarity in ["up", "down"]:
    if config[magnet_polarity] is None:
      print "Skipping %s %s %i %s" % (data_type, config['strip'], magnet_polarity)
      continue
    file_name = dir_name + "strip_%s_%s.root" % (config['strip'], magnet_polarity)
    print "hadding %s %s %i %s" % (data_type, config['strip'], config[magnet_polarity], magnet_polarity)
    subprocess.call("cd %s/%i/output ; hadd -f %s ../*/output/Demu_NTuple.root" % (gangadir, config[magnet_polarity], file_name), shell=True)
  
  
  








