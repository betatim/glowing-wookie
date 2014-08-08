#!/usr/bin/env python

from ROOT import gROOT
gROOT.ProcessLine(".x lhcbstyle.C")
gROOT.SetBatch(True)

import ROOT
from ROOT import TFile, TCanvas, gDirectory

from wookie import config as wookie_config

tc = TCanvas("tc","tc",800,600)

to_plot = [
  ("nTracks",wookie_config.datasets["mcpidemu2011"],ROOT.kBlack,2),
  ("nTracks_Scaled",wookie_config.datasets["mcpidemu2011"],ROOT.kBlack,1),
  ("nTracks",wookie_config.datasets["pidemu2011unblind"],ROOT.kRed,1),
  ]

plots = []
tfs = []

for i, (var, ds, colour, style) in enumerate(to_plot):
  tfs.append(TFile(ds["file"]))
  tree = tfs[-1].Get(ds["tree"])
  tree.Draw("%s>>hist_%i(100,0,500)"%(var,i))
  plot = gDirectory.Get("hist_%i"%(i))
  plot.Scale(1./plot.GetEntries())
  plot.SetLineColor(colour)
  plot.SetLineStyle(style)
  plot.GetYaxis().SetTitle("Events")
  plot.GetYaxis().SetDecimals(True)
  plot.GetYaxis().SetTitleOffset(1.05)
  plot.GetXaxis().SetTitle("Number of tracks")
  plots.append(plot)

for i,(plot) in enumerate(plots):
  opts = "" if i==0 else "same"
  print i,opts
  plot.Draw(opts)

tc.SaveAs("ntracks.png")
tc.SaveAs("ntracks.pdf")
