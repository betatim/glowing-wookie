#!/usr/bin/env python

import sys

def usage():
  print "This program takes exactly one argument, the data set which the offline selection is to be measured."
  print "Availble datasets: pipi"

if len(sys.argv) != 1+1:
  usage()
  sys.exit(1)

ds = str(sys.argv[1])

from ROOT import gROOT
gROOT.SetBatch(True)

import random
import subprocess
import ROOT

from math import fabs, pi

from ROOT import TFile,TStopwatch,gROOT,gDirectory
from ROOT import gROOT,TFile,TTreeFormula


def combine_cuts(cuts):
  ret = ""
  last_cut = len(cuts) - 1
  for cut_number,(cut,positive) in enumerate(cuts):
    if positive:
      ret += "(%s)" % cut
    else:
      ret += "!(%s)" % cut
      
    #if cut_number is not 0:
    if cut_number is not last_cut:
      ret += "&&"
        
  return ret



cuts = ""
pipiPidCut = "x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNpi*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNk < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7"
likeSignCut = "x1_ID*x2_ID>0"

directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/"

inPath = "Demu_NTuple/Demu_NTuple"
outName = "Demu_NTuple"

config = {
  #'pipi': {
    #'infile' : directory+"pipi/strip_pipi.root",
    #'outfile': directory+"pipi/strip_pipi_fitter.root",
    #'cuts'   : combine_cuts([(pipiPidCut,True),(likeSignCut,False)]),
  #},
  'mcpipi': {
    'infile' : directory+"mcpipi/strip_pipi.root",
    'outfile': directory+"mcpipi/strip_pipi_fitter.root",
    'cuts'   : combine_cuts([(pipiPidCut,True),(likeSignCut,False)]),
  },
}
  
  
def print_eff(config):
  sw = TStopwatch()
  sw.Start()

  print "Using dataset %s with cuts: %s"% (ds,config['cuts'])

  random.seed(112)

  inFile = TFile(config['infile'],"READ")

  inTree = inFile.Get(inPath)
  n_before = inTree.Draw("D0_M","")
  n_after = inTree.Draw("D0_M",config['cuts'])
  
  inFile.Close()
  
  print "Done! Offline selection is %.2f%% efficient." %(100.*float(n_after)/float(n_before))
  sw.Stop()
  sw.Print()


print_eff(config[ds])

