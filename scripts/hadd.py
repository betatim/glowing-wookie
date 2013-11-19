#!/usr/bin/env python

import sys
import subprocess
import ROOT
from ROOT import TFile

to_merge = [
 # ##{ # this is really loose
 #   ##"up"   : None,
 #   ##"down" : 145,
 #   ##"strip": "emu",
 #   ##"data" : "emu",
 #   ##"mc"   : True
 # ##},
 # ##{ # no triggers
 #   ##"up"   : 92,
 #   ##"down" : 91,
 #   ##"strip": "emu",
 #   ##"data" : "emu",
 #   ##"mc"   : True
 # ##},
 # #{ # constraind D* vert + trig
 # #  "up"   : 186,
 # #  "down" : 188,
 # #  "strip": "emu",
 # #  "data" : "emu",
 # #  "mc"   : True
 # #},
 # #{ # constraind D* vert + trig
 #   #"up"   : 187,
 #   #"down" : 189,
 #   #"strip": "mcmatch",
 #   #"data" : "emu",
 #   #"mc"   : True
 # #},
  #{ # cc_biased
    #"up"   : 319,
    #"down" : 320,
    #"strip": "emu",
    #"data" : "cc",
    #"mc"   : True
  #},
 # { # MC2012
 #   "up"   : 296,
 #   "down" : 297,
 #   "strip": "emu",
 #   "data" : "emu",
 #   "mc"   : True
 # },
 # { # MC2012
 #   "up"   : 309,
 #   "down" : 310,
 #   "strip": "kpi",
 #   "data" : "kpi",
 #   "mc"   : True
 # },
 # #{ # constraind D* vert + trig
 #   #"up"   : 229,
 #   #"down" : 230,
 #   #"strip": "emu",
 #   #"data" : "kpi",
 #   #"mc"   : True
 # #},
 # #{ # constraind D* vert + trig
 #   #"up"   : 231,
 #   #"down" : 232,
 #   #"strip": "emu",
 #   #"data" : "kk",
 #   #"mc"   : True
 # #},
 # #{ # constraind D* vert + trig
 #   #"up"   : 233,
 #   #"down" : 234,
 #   #"strip": "emu",
 #   #"data" : "pipi",
 #   #"mc"   : True
 # #},
 # #{ # constraind D* vert + trig
 #   #"up"   : 235,
 #   #"down" : 236,
 #   #"strip": "emu",
 #   #"data" : "mumu",
 #   #"mc"   : True
 # #},
 # #{
 #   #"up"   : 94,
 #   #"down" : 93,
 #   #"strip": "emu",
 #   #"data" : "pipi",
 #   #"mc"   : True
 # #},
 # #{
 #   #"up"   : 96,
 #   #"down" : 95,
 #   #"strip": "emu",
 #   #"data" : "mumu",
 #   #"mc"   : True
 # #},
 # #{
 #   #"up"   : 98,
 #   #"down" : 99,
 #   #"strip": "pipi",
 #   #"data" : "emu",
 #   #"mc"   : True
 # #},
 # ##{# no triggers
 #   ##"up"   : 100,
 #   ##"down" : 99,
 #   ##"strip": "pipi",
 #   ##"data" : "pipi",
 #   ##"mc"   : True
 # ##},
 # #{  # constraind D* vert + trig
 #   #"up"   : 191,
 #   #"down" : 192,
 #   #"strip": "pipi",
 #   #"data" : "pipi",
 #   #"mc"   : True
 # #},
 # {  # more trigger lines
 #   "up"   : 315,
 #   "down" : 316,
 #   "strip": "pipi",
 #   "data" : "pipi",
 #   "mc"   : True
 # },
 # #{
 #   #"up"   : 102,
 #   #"down" : 101,
 #   #"strip": "mumu",
 #   #"data" : "mumu",
 #   #"mc"   : True
 # #},
 # 
 # ##{
 #   ##"up"   : 126,
 #   ##"down" : 125,
 #   ##"strip": "emu",
 #   ##"data" : "emu",
 #   ##"mc"   : False
 # ##},
 # #{
 # #  "up"   : 207,
 # #  "down" : 208,
 # #  "strip": "emu",
 # #  "data" : "emu",
 # #  "mc"   : False
 # #},
 # { # more trigger lines
 #  "up"   : 299,
 #  "down" : 300,
 #  "strip": "emu2012",
 #  "data" : "emu",
 #  "mc"   : False
 # },
 # { # more trigger lines
 #  "up"   : 298,
 #  "down" : 305,
 #  "strip": "emu2011",
 #  "data" : "emu",
 #  "mc"   : False
 # },
 # ##{ # no lumi info
 #   ##"up"   : 148,
 #   ##"down" : 147,
 #   ##"strip": "pipi",
 #   ##"data" : "pipi",
 #   ##"mc"   : False
 # ##},
 # #{
 # #  "up"   : 194,
 # #  "down" : 195,
 # #  "strip": "pipi",
 # #  "data" : "pipi",
 # #  "mc"   : False
 # #},
 # { # more trigger lines
 #  "up"   : 303,
 #  "down" : 304,
 #  "strip": "pipi2012",
 #  "data" : "pipi",
 #  "mc"   : False
 # },
 # { # more trigger lines
 #  "up"   : 301,
 #  "down" : 302,
 #  "strip": "pipi2011",
 #  "data" : "pipi",
 #  "mc"   : False
 # },
 # { # more trigger lines
 #  "up"   : 313,
 #  "down" : 314,
 #  "strip": "kpi2012",
 #  "data" : "kpi",
 #  "mc"   : False
 # },
 { # more trigger lines
  "up"   : 311,
  "down" : 312,
  "strip": "kpi2011",
  "data" : "kpi",
  "mc"   : False
 },
]

directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/"
gangadir  = "/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/"

path = "Demu_NTuple/Demu_NTuple"

for config in to_merge:
  data_type = ("mc" if config['mc'] else "") + config['data']
  dir_name = directory + data_type + "/"
  
  files = []
  for magnet_polarity in ["up", "down"]:
    if config[magnet_polarity] is None:
      print "Skipping %s %s" % (data_type, config['strip'])
      continue
    files.append("%i/*/output/Demu_NTuple.root" % (config[magnet_polarity]))
  fn = dir_name + ("strip_%s.root" % config['strip'])
  file_list = ""
  for f in files: file_list += f + " " 
  subprocess.call("cd %s ; time hadd -f %s %s " % (gangadir, fn, file_list), shell=True)
  








