#!/usr/bin/env python
import sys

if len(sys.argv) != 2:
  sys.exit("This program takes one argument, mode to plot")

import ROOT
from ROOT import gROOT
gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError +20
gROOT.ProcessLine(".x lhcbstyle.C")


from ROOT import TFile, TCanvas

mode = sys.argv[1]

tf = TFile("fitResult.%s.root"%mode)

c1 = tf.Get("FullData_BDT1_D0M_dstall_d0all")
c2 = tf.Get("FullData_BDT2_D0M_dstall_d0all")
c3 = tf.Get("FullData_BDT3_D0M_dstall_d0all")

tc = TCanvas("tc","tc",500,500)
for cat in ["BDT1","BDT2","BDT3","PiPi"]:
  for mass in ["D0M", "DelM"]:
    plotname = "FullData_%s_%s_delall_d0all"%(cat,mass)
    plot = tf.Get(plotname)
    
    if not plot:
      print plotname, "not found"
      continue
    else:
      print plotname
      
    plot.Draw()
    
    plot.GetXaxis().SetLabelFont(62)
    plot.GetXaxis().SetTitleFont(62)
    plot.GetXaxis().SetTitleOffset(1.1)
    
    if mass is "D0M":
      plot.GetXaxis().SetTitle("D^{0} mass / MeV")
      if cat is "PiPi":
        plot.GetXaxis().SetRangeUser(1826.,1920.)
    elif mass is "DelM":
      plot.GetXaxis().SetTitle("D* - D^{0} mass / MeV")
    
    plot.GetYaxis().SetLabelFont(62)
    plot.GetYaxis().SetTitleFont(62)
    plot.GetYaxis().SetTitleOffset(2.0)
    plot.GetYaxis().SetTitle("Candidates")

    tc.SaveAs("plots/%s_%s_%s.pdf"%(mode,cat,mass))
