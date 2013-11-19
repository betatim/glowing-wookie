#!/usr/bin/env python

import sys

def usage():
  print "This program takes exactly one argument, the data set which is to be divided."
  print "Availble datasets: pipi"

if len(sys.argv) != 1+1:
  usage()
  sys.exit(1)

ds = str(sys.argv[1])

from ROOT import gROOT
#gROOT.SetBatch(True)

import random
import subprocess
import ROOT

from math import fabs, pi

from ROOT import TFile, TStopwatch, gROOT, gDirectory, TLine
from ROOT import gROOT, TFile, TTreeFormula, TCanvas


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

nSplit = 3
variable = "BDT_ada"

config = {
  'pipi': {
    'infile' : directory+"mcpipi/mva_pipi_fitter.root",
    'inPath' : "subTree",
  },
  'emu': {
    'infile' : directory+"mcemu/mva_emu_fitter.root",
    'inPath' : "subTree",
  },
}
  
  
def integrate_plot(plot):
  total = 0
  bin_num = 0
  while bin_num < plot.GetNbinsX()+2:
    total += plot.GetBinContent(bin_num)
    plot.SetBinContent(bin_num,total)
    bin_num += 1
  
  
def print_split(config,nSplit,variable):
  sw = TStopwatch()
  sw.Start()

  tc = TCanvas("tc", "tc",1000,600)
  tc.Divide(2,1)
  tc.cd(1)

  print "Using dataset %s and varible %s with %i splits"% (ds, variable, nSplit)

  inFile = TFile(config['infile'],"READ")

  inTree = inFile.Get(config['inPath'])
  inTree.Draw(variable+">>outhist(-1,1,1000)")
  orig = gDirectory.Get("outhist")
  plot = orig.Clone()
  integrate_plot(plot)
  
  total = plot.GetEntries()
  max_val = orig.GetMaximum()
  
  splits = []
  i = 1.
  
  while int(i)<(nSplit):
    bin_num = 0
    while bin_num < plot.GetNbinsX()+2:
      bin_val = plot.GetBinContent(bin_num)
      if bin_val > float(total)*i/float(nSplit):
	splits.append(plot.GetBinCenter(bin_num))
	break
      bin_num += 1
    i += 1.
    
  orig.Draw()
  tc.cd(2)
  plot.Draw()
  tc.cd(1)
  lines = []
  for split in splits:
    lines.append(TLine(split,0., split,max_val))
    lines[-1].Draw()
  
  tc.cd(2)
  for split in splits:
    lines.append(TLine(split,0., split,total))
    lines[-1].Draw()
    
  tc.SaveAs("spliter_%s_%s.pdf" % (variable,nSplit))
  
  inFile.Close()
  
  print "Done! Splits are:", splits
  sw.Stop()
  sw.Print()


print_split(config[ds],nSplit,variable)

