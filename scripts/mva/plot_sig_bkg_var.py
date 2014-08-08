#/usr/bin/env python

import sys
if len(sys.argv) < 4:
  sys.exit("needs more args")
  
var = sys.argv[1]
var_min = float(sys.argv[2])
var_max = float(sys.argv[3])

from ROOT import gROOT
gROOT.ProcessLine(".x ../lhcbstyle.C")
gROOT.SetBatch(True)

from wookie import config as wookie_config

import ROOT
from ROOT import TFile, TCanvas, gDirectory

tc = TCanvas("tc","tc",800,600)

print wookie_config.datasets["pipi2011"]
print wookie_config.datasets["emu2011unblind"]

sigf = TFile.Open(wookie_config.datasets["pipi2011"]["file"])
sigt = sigf.Get(wookie_config.datasets["mcemu2011"]["tree"])
sigt.Draw("%s>>sigh(100,%f,%f)"%(var,var_min,var_max),"abs(Dst_DTF_D0_M-1865)<15 && abs(Dst_DTF_Dst_M-Dst_DTF_D0_M-145.5)<0.5")
sigh = gDirectory.Get("sigh")

bkgf = TFile.Open(wookie_config.datasets["pipi2011"]["file"])
bkgt = bkgf.Get(wookie_config.datasets["emu2011unblind"]["tree"])
bkgt.Draw("%s>>bkgh(100,%f,%f)"%(var,var_min,var_max))
bkgh = gDirectory.Get("bkgh")

sigh.Scale(1./sigh.GetEntries())
bkgh.Scale(1./bkgh.GetEntries())

sigh.SetLineColor(ROOT.kRed)
bkgh.SetLineColor(ROOT.kBlack)
#sigh.Draw("")
#bkgh.Draw("same")
bkgh.Draw("")
sigh.Draw("same")

for c in "!/\\\"&*()-_=+":
  var = var.replace(c,"_")

tc.SaveAs("SigBkg_%s.pdf"%var)
tc.SaveAs("SigBkg_%s.png"%var)

