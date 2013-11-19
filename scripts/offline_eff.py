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
likeSignCut = "x1_ID*x2_ID>0"

pipiPidCut = "x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNpi*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNk < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7"
trigPipiCut = "( Dst_L0HadronDecision_TOS == 1 ) && ( Dst_Hlt1TrackAllL0Decision_TOS == 1) && ( Dst_Hlt2Dst2PiD02PiPiDecision_TOS == 1 )"

emuPidCut = "x1_ProbNNe>0.45 && pi_ProbNNghost<0.05 && x2_ProbNNghost<0.05 && x2_ProbNNmu>0.3 && x2_ProbNNk<0.55 && pi_ProbNNpi>0.45 && x1_ProbNNk<0.8"
emuTrigCut = "Dst_L0MuonDecision_TOS == 1 && Dst_Hlt1TrackMuonDecision_TOS== 1 && (Dst_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 || Dst_Hlt2CharmHadD02HH_D02KPiDecision_TOS == 1 || Dst_Hlt2CharmHadD02HH_D02KKDecision_TOS == 1 )"

directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/"

inPath = "Demu_NTuple/Demu_NTuple"
outName = "Demu_NTuple"

config = {
  'pipi': {
    'infile' : directory+"mcpipi/strip_pipi.root",
    'precuts': combine_cuts([(trigPipiCut,True),(likeSignCut,False)]),
    'cuts'   : combine_cuts([(trigPipiCut,True),(pipiPidCut,True),(likeSignCut,False)]),
    'inPath' : "Demu_NTuple/Demu_NTuple",
  },
  'emu': {
    'infile' : directory+"mcemu/strip_emu.root",
    'precuts': combine_cuts([(emuTrigCut,True),(likeSignCut,False)]),
    'cuts'   : combine_cuts([(emuPidCut,True),(emuTrigCut,True),(likeSignCut,False)]),
    'inPath' : "Demu_NTuple/Demu_NTuple",
  },
}
  
  
def print_eff(config):
  sw = TStopwatch()
  sw.Start()

  print "Using dataset %s with cuts: %s"% (ds,config['cuts'])

  random.seed(112)

  inFile = TFile(config['infile'],"READ")

  inTree = inFile.Get(inPath)
  n_before = inTree.Draw("D0_M",config['precuts'])
  n_after = inTree.Draw("D0_M",config['cuts'])
  
  inFile.Close()
  
  print "Done! Offline selection is %.2f%% efficient." %(100.*float(n_after)/float(n_before))
  sw.Stop()
  sw.Print()


print_eff(config[ds])

