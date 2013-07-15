#!/usr/bin/env python

import sys
from math import sqrt

import ROOT
from ROOT import TFile

tf= False
if len(sys.argv)>1:
  tf = TFile(sys.argv[1])
else:
  tf = TFile("/home/thomas/pipi_NTuple.root")

lumi_tuple = tf.Get("GetIntegratedLuminosity/LumiTuple")

lumi_tot = 0.
lumi_err = 0.

for data_file in lumi_tuple:
  #print data_file.IntegratedLuminosity, "+/-", data_file.IntegratedLuminosityErr
  lumi_tot += data_file.IntegratedLuminosity
  le = data_file.IntegratedLuminosityErr
  lumi_err +=  le * le
  
print "Total:", lumi_tot, "+/-", sqrt(lumi_err),"nb"

