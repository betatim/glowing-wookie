#!/usr/bin/env python


import ROOT
from ROOT import TFile, TCanvas, gROOT

gROOT.ProcessLine(".x lhcbstyle.C")


tf = TFile("fitResult.nominal.root")

c1 = tf.Get("FullData_BDT1_D0M_dstall_d0all")
c2 = tf.Get("FullData_BDT2_D0M_dstall_d0all")
c3 = tf.Get("FullData_BDT3_D0M_dstall_d0all")

chans = [c1,c2,c3]

tc = TCanvas("tc","tc",500,500)

for i,chan in enumerate(chans):
  chan.Draw()
  
  chan.GetXaxis().SetLabelFont(62)
  chan.GetXaxis().SetTitleFont(62)
  chan.GetXaxis().SetTitleOffset(1.1)
  chan.GetXaxis().SetTitle("D^{0} mass / MeV")
  
  chan.GetYaxis().SetLabelFont(62)
  chan.GetYaxis().SetTitleFont(62)
  chan.GetYaxis().SetTitleOffset(1.5)
  chan.GetYaxis().SetTitle("Candidates")

  tc.SaveAs("background_fit_BDT%i.pdf"%(i+1))