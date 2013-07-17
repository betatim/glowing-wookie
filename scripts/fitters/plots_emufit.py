#!/usr/bin/env python


import ROOT
from ROOT import TFile, TCanvas, gROOT

gROOT.ProcessLine(".x lhcbstyle.C")


tf = TFile("emufit.root")

c1 = tf.Get("channel1")
c2 = tf.Get("channel2")
c3 = tf.Get("channel3")

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

  tc.SaveAs("signal_fit_BDT%i.pdf"%(i+1))