#!/usr/bin/env python

import sys

#def usage():
  #print "This program takes exactly one argument, the data set which is to be divided."
  #print "Availble datasets: pipi"

#if len(sys.argv) != 1+1:
  #usage()
  #sys.exit(1)

#ds = str(sys.argv[1])

from ROOT import gROOT
gROOT.SetBatch(True)

import random
import subprocess
import ROOT

from math import fabs, pi

from ROOT import TFile, TStopwatch, gROOT, gDirectory, TLine
from ROOT import gROOT, TFile, TTreeFormula, TCanvas, TChain, THStack


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
#likeSignCut = "x1_ID*x2_ID>0"

#emuPidCut = "x1_BremMultiplicity == 0 && x1_ProbNNe>0.45 && pi_ProbNNghost<0.05 && x2_ProbNNghost<0.05 && x2_ProbNNmu>0.3 && x2_ProbNNk<0.55 && pi_ProbNNpi>0.45 && x1_ProbNNk<0.8"
emuPidCut = "x1_BremMultiplicity == 0"
emuTrigCut = "Dst_L0MuonDecision_TOS == 1 && Dst_Hlt1TrackMuonDecision_TOS== 1"# && (Dst_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 || Dst_Hlt2CharmHadD02HH_D02KPiDecision_TOS == 1 || Dst_Hlt2CharmHadD02HH_D02KKDecision_TOS == 1 )"

directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/"
#directory = "/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/"

variable = "D0_M"
ls = ""
  
chain = TChain("Demu_NTuple/Demu_NTuple")
#chain.Add(directory+"879/output/Demu_NTuple.root")
#chain.Add(directory+"880/output/Demu_NTuple.root")
#chain.Add(directory+"881/output/Demu_NTuple.root")
#chain.Add(directory+"882/output/Demu_NTuple.root")
#chain.Add(directory+"emu/strip_emu2011.root")
#chain.Add(directory+"emu/strip_emu2012.root")
#chain.Add(directory+"mckpi/strip_emu.root")
#chain.Add(directory+"lsdata.root") ; ls = "Ls"
chain.Add(directory+"mckk/strip_emu.root")
#chain.Add(directory+"mckpi/strip_emu.root")
#chain.Add(directory+"mcpipi/strip_emu.root")

plots = [
    #( ROOT.kCyan,   "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 0"%((ls,)*3) ),
    ( ROOT.kRed,    "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 0"%((ls,)*3) ),
    ( ROOT.kBlue,   "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 0"%((ls,)*3) ),
    ( ROOT.kYellow, "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 1"%((ls,)*3) ),
    ( ROOT.kMagenta,"Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 0"%((ls,)*3) ),
    ( ROOT.kOrange, "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 1"%((ls,)*3) ),
    ( ROOT.kGreen,  "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 1"%((ls,)*3) ),
    ( ROOT.kBlack,  "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 1"%((ls,)*3) ),
  ]


hists = []
tc = TCanvas("tc", "tc",800,600)
ts = THStack("thstack","")

for i,(colour, extra_cuts) in enumerate(plots):
  print "Making plot",i
  chain.Draw(variable+">>outhist%i(100,1550,2150)"%(i),combine_cuts([(emuTrigCut,True),(emuPidCut,True),(extra_cuts,True),]))
  hists.append(gDirectory.Get("outhist%i"%(i)))
  hists[i].SetFillColor(colour)

  hists[i].SetStats(False)
  hists[i].GetYaxis().SetTitle("Candidates")
  hists[i].GetXaxis().SetTitle("D^{0} Mass / MeV")
  ts.Add(hists[i])
  hists[i].Draw()
  tc.SaveAs("triggered_mass_%i.pdf"%(i))
  tc.SaveAs("triggered_mass_%i.png"%(i))
    
ts.Draw()
tc.SaveAs("triggered_mass.pdf")
tc.SaveAs("triggered_mass.png")


