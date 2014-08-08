#!/usr/bin/env python

import sys

from ROOT import gROOT
gROOT.SetBatch(True)
gROOT.ProcessLine(".x /afs/cern.ch/user/t/tbird/lhcbstyle.C")

import ROOT
from ROOT import TFile, gDirectory, TLine
from ROOT import TCanvas, TChain, TH2D, lhcbName


directory = "/afs/cern.ch/user/t/tbird/cmtuser/Urania_v2r1/PIDCalib/PIDPerfScripts/scripts/python/PubPlots/"

plots = [
  #("ProbNN%s>",ROOT.kRed),
  ("DLL%s>",ROOT.kBlue),
  ]

final_hists = []
tc = TCanvas("tc", "tc",800,600)
tc.SetLogy(True)

tfs=[]

#strip = "20r1"
mag = "MagUp"

def getPlot(var,part,strip,mag):
  tfs.append( TFile(directory+"/PerfCurve_%sVsPi_Strip%s_%s_%s.root"%(part, strip, mag, var%(part.lower(),)), "OPEN"))
  p = tfs[-1].Get(part+"VsPi")
  return p

for strip in ["20r1","20"]:
  for part in ["e"]:
    axis = TH2D("axis","axis",10,.7,1.,10,0.001,.1)
    axis.SetStats(False)
    axis.GetXaxis().SetTitle(part+" efficiency")
    axis.GetYaxis().SetTitle("#pi mis-ID rate")
    tc.cd()
    axis.Draw()

    for i,(variable, colour) in enumerate(plots):
      print "Making plot",i,variable

      final_hists.append( getPlot(variable,part,strip,mag).Clone("misid_%i"%(i)) )

      #final_hists[-1].SetStats(False)
      #final_hists[-1].SetLogy(True)
      #final_hists[-1].GetYaxis().SetRangeUser(0.000001,0.2)
      #final_hists[-1].GetXaxis().SetRangeUser(0.,1.1)
      #final_hists[-1].GetYaxis().SetTitle("Fraction of tracks")
      #final_hists[-1].GetXaxis().SetTitle(title)
      final_hists[-1].SetMarkerColor(colour)
      final_hists[-1].SetLineColor(colour)

      if i is 0:
        tc.cd()
        final_hists[-1].Draw("same P")
      else:
        tc.cd()
        final_hists[-1].Draw("same P")

    lhcbName.Draw()
    
    tc.SaveAs("misid_%s_S%s_%s.pdf"%(part,strip,mag))
    tc.SaveAs("misid_%s_S%s_%s.png"%(part,strip,mag))
