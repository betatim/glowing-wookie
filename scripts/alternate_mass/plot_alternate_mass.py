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

from ROOT import TFile, TStopwatch, gROOT, gDirectory, TLine, gPad
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


variable = "sqrt({m1}*{m1}+{m2}*{m2}+2*(sqrt(0.511*0.511+(x1_PX*x1_PX+x1_PY*x1_PY+x1_PZ*x1_PZ))*sqrt(105.6*105.6+(x2_PX*x2_PX+x2_PY*x2_PY+x2_PZ*x2_PZ))-(x1_PX*x2_PX+x1_PY*x2_PY+x1_PZ*x2_PZ)))"
variable = "sqrt({m1}*{m1}+{m2}*{m2}+2*(sqrt({m1}*{m1}+x1_PE*x1_PE)*sqrt({m2}*{m2}+x2_PE*x2_PE)-(x1_PX*x2_PX+x1_PY*x2_PY+x1_PZ*x2_PZ)))"
ls = ""

pi = 139.6
k  = 493.7
mu = 105.6
e  = 0.511
d  = 1864.84

chain = TChain("Demu_NTuple/Demu_NTuple")

#directory = "/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/"
#chain.Add(directory+"879/output/Demu_NTuple.root")
#chain.Add(directory+"880/output/Demu_NTuple.root")
#chain.Add(directory+"881/output/Demu_NTuple.root")
#chain.Add(directory+"882/output/Demu_NTuple.root")
#chain.Add(directory+"920/output/Demu_NTuple.root")

directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/"
#chain.Add(directory+"emu/strip_emu2011.root")
#chain.Add(directory+"emu/strip_emu2012.root")
#chain.Add(directory+"mckpi/strip_emu.root")
#chain.Add(directory+"lsemu/strip_emu.root") ; ls = "Ls"
#chain.Add(directory+"mckk/strip_emu.root")
#chain.Add(directory+"mckpi/strip_emu.root")
#chain.Add(directory+"mcpipi/strip_emu.root")
chain.Add(directory+"mcemu/strip_emu.root")

plots = [
    ##( ROOT.kCyan,   "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 0"%((ls,)*3) ),
    #( ROOT.kRed,    "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 0"%((ls,)*3) ),
    #( ROOT.kBlue,   "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 0"%((ls,)*3) ),
    #( ROOT.kYellow, "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 1"%((ls,)*3) ),
    #( ROOT.kMagenta,"Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 0"%((ls,)*3) ),
    #( ROOT.kOrange, "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 1"%((ls,)*3) ),
    #( ROOT.kGreen,  "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 0 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 1"%((ls,)*3) ),
    #( ROOT.kBlack,  "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KPi%sDecision_TOS == 1 && Dst_Hlt2CharmHadD02HH_D02KK%sDecision_TOS == 1"%((ls,)*3) ),
    #( ROOT.kRed,  "Dst_Hlt2CharmHadD02HHXDst_hhXDecision_TOS == 1 " ),
    ( ROOT.kRed,   "Dst_Hlt2CharmHadD02HH_D02PiPi%sDecision_TOS == 1"%(ls) ),
  ]


lines = []
hists = []
tc = TCanvas("tc", "tc",800,600)

for hypname,m1,m2 in [("kk",k,k),("gg",0.,0.),("emu",e,mu),("mue",mu,e),("kpi",k,pi),("pik",pi,k),("pipi",pi,pi),("std","x1_M","x2_M"),]:
#for hypname,m1,m2 in [("mue",mu,e),("std","x1_M","x2_M"),("kk",k,k),("emu",e,mu)]:
  ts = THStack("thstack_%s"%(hypname),"thstack_%s"%(hypname))

  for i,(colour, extra_cuts) in enumerate(plots):
    print "Making plot",i, hypname, [m1,m2]
    print variable.format(m1=m1,m2=m2)
    chain.Draw(variable.format(m1=m1,m2=m2)+">>outhist_%s_%i(100,1550,2150)"%(hypname,i),combine_cuts([(emuTrigCut,True),(emuPidCut,True),(extra_cuts,True),]))
    hist = gDirectory.Get("outhist_%s_%i"%(hypname,i))
    hist.SetFillColor(colour)

    hist.SetStats(False)
    hist.GetYaxis().SetTitle("Candidates")
    hist.GetXaxis().SetTitle("D^{0} Mass / MeV")
    ts.Add(hist)
    hist.Draw()
    hists.append(hist)
    tc.SaveAs("triggered_mass_%s_hyp_%i.pdf"%(hypname,i))
    tc.SaveAs("triggered_mass_%s_hyp_%i.png"%(hypname,i))
      
  ts.Draw()
  
  #print (d,0,d,ts.GetMaximum())
  lines.append(TLine(d,0,d,ts.GetMaximum()))
  lines[-1].SetLineColor(ROOT.kRed)
  lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
  lines[-1].Draw("same")
  
  tc.SaveAs("triggered_mass_%s_hyp.pdf"%(hypname,))
  tc.SaveAs("triggered_mass_%s_hyp.png"%(hypname,))




