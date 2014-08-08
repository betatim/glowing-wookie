#!/usr/bin/env python

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT, sys
from ROOT import TFile, gDirectory

if len(sys.argv) != 2:
  print sys.argv[0]+": takes one argument, the crop root file to open."
  sys.exit(2)

tf = TFile(sys.argv[1])
tf.cd("Optimised")

prefix = "plots/"

it = gDirectory.GetListOfKeys().MakeIterator()
while True:
  key = it.Next()
  if not key: 
    break
  obj = key.ReadObj()
  if not obj: 
    break
  obj.SaveAs(prefix+key.GetName().replace("<","").replace(">","")+".pdf")
  obj.SaveAs(prefix+key.GetName().replace("<","").replace(">","")+".png")


