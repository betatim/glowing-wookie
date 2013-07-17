#!/usr/bin/env python

import sys
import subprocess
import ROOT
from ROOT import TFile

to_merge = [
  #{ # this is really loose
    #"up"   : None,
    #"down" : 145,
    #"strip": "emu",
    #"data" : "emu",
    #"mc"   : True
  #},
  #{ # no triggers
    #"up"   : 92,
    #"down" : 91,
    #"strip": "emu",
    #"data" : "emu",
    #"mc"   : True
  #},
  { # constraind D* vert + trig
    "up"   : 186,
    "down" : 188,
    "strip": "emu",
    "data" : "emu",
    "mc"   : True
  },
  { # constraind D* vert + trig
    "up"   : 187,
    "down" : 189,
    "strip": "mcmatch",
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
  #{# no triggers
    #"up"   : 100,
    #"down" : 99,
    #"strip": "pipi",
    #"data" : "pipi",
    #"mc"   : True
  #},
  {  # constraind D* vert + trig
    "up"   : 191,
    "down" : 192,
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
  #{ # no lumi info
    #"up"   : 148,
    #"down" : 147,
    #"strip": "pipi",
    #"data" : "pipi",
    #"mc"   : False
  #},
  {
    "up"   : 194,
    "down" : 195,
    "strip": "pipi",
    "data" : "pipi",
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
    file_name_temp = dir_name + "strip_%s_%s_temp.root" % (config['strip'], magnet_polarity)
    file_name      = dir_name + "strip_%s_%s.root" % (config['strip'], magnet_polarity)
    files.append(file_name)
    
    print "hadding %s %s %i %s" % (data_type, config['strip'], config[magnet_polarity], magnet_polarity)
    subprocess.call("cd %s/%i/output ; time hadd -f %s ../*/output/Demu_NTuple.root" % (gangadir, config[magnet_polarity], file_name_temp), shell=True)
  
    subprocess.call("cd %s ; time SimpleToolsColumnMaker.exe %s %s %s %s %s" % (directory, file_name_temp, path, ("1" if magnet_polarity is "up" else "0"), "MagPol", file_name), shell=True)
    
    tmp_tf = TFile(file_name_temp)
    dst_tf = TFile(file_name, "UPDATE")
    dst_tf.cd()
    dst_tf.mkdir("GetIntegratedLuminosity")
    dst_tf.cd("GetIntegratedLuminosity")
    
    lumi = tmp_tf.Get("GetIntegratedLuminosity/LumiTuple").Clone("LumiTuple")
    lumi.Write("LumiTuple")
    
    dst_tf.Write()
    dst_tf.Close()
    tmp_tf.Close()
    
    subprocess.call("echo rm %s" % (file_name_temp), shell=True)
    
  file_name = dir_name + "strip_%s.root" % (config['strip'])
  file_list = ""
  for f in files: file_list += f + " " 
  subprocess.call("cd %s ; time hadd -f %s %s ; echo rm %s" % (dir_name, file_name, file_list, file_list), shell=True)
  








