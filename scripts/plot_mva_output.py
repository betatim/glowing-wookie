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
gROOT.ProcessLine(".x lhcbstyle.C")
gROOT.SetBatch(True)

import ROOT
from ROOT import TFile, gDirectory, TLine, TCanvas, gPad
from wookie import config as wookie_config

to_plot = [
  ("emu2011unblind",False,ROOT.kGray,wookie_config.datasets["fitteremu2011unblind"],""),
  ("emu2011blind",False,ROOT.kBlack,wookie_config.datasets["fitteremu2011blind"],""),

  ("mcemu2011",False,ROOT.kRed,wookie_config.datasets["mcfitteremu2011"],""),
  ("mcemu2012",True,ROOT.kRed+2,wookie_config.datasets["mcfitteremu2012"],""),

  ("pipi2011",False,ROOT.kGreen,wookie_config.datasets["fitterpipi2011"],"abs(Del_Mass-145.5)<0.5 && abs(D0_Mass-1867.5)<15"),
  ("pipi2012",False,ROOT.kGreen+2,wookie_config.datasets["fitterpipi2012"],"abs(Del_Mass-145.5)<0.5 && abs(D0_Mass-1867.5)<15"),

  #("kpi2011",False,ROOT.kBlue,wookie_config.datasets["fitterkpi2011"],"abs(Del_Mass-145.5)<0.5 && abs(D0_Mass-1867.5)<15"),
  #("kpi2012",False,ROOT.kBlue+2,wookie_config.datasets["fitterkpi2012"],"abs(Del_Mass-145.5)<0.5 && abs(D0_Mass-1867.5)<15"),

  ]

nSplit = 3


def integrate_plot(plot):
  total = 0
  bin_num = 0
  while bin_num < plot.GetNbinsX()+2:
    total += plot.GetBinContent(bin_num)
    plot.SetBinContent(bin_num,total)
    bin_num += 1

tc = TCanvas("tc", "tc",800,600)

files = []
hists = []
lines = []
splits = []

for name,split,colour,file_obj,cut in to_plot:
  print "Plotting", name
  files.append(TFile(file_obj["file"]))
  #files[-1].ls()
  tt = files[-1].Get(file_obj["tree"])
  #print tt
  tt.Draw("BDT_ada>>h_%s(100,-1,1)"%(name),cut)
  hist = gDirectory.Get("h_%s"%(name))

  if split:
    integrated_hist = hist.Clone("h_int_%s"%(name))
    integrate_plot(integrated_hist)

    total = integrated_hist.GetEntries()
    max_val = hist.GetMaximum()

    i = 1.
    while int(i)<(nSplit):
      bin_num = 0
      while bin_num < integrated_hist.GetNbinsX()+2:
        bin_val = integrated_hist.GetBinContent(bin_num)
        if bin_val > float(total)*i/float(nSplit):
          splits.append((integrated_hist.GetBinCenter(bin_num),colour))
          break
        bin_num += 1
      i += 1.

  hist.Scale(1./hist.GetEntries())
  hist.SetStats(False)
  hist.GetXaxis().SetTitle("BDT Output")
  hist.GetYaxis().SetDecimals(True)
  #hist.GetYaxis().SetTitleOffset(1.2)
  hist.GetYaxis().SetTitle("Arb. Units")
  hist.SetLineColor(colour)
  hists.append(hist)

for i,(hist) in enumerate(hists):
  if i == 0:
    hist.Draw()
  else:
    hist.Draw("same")

tc.Update()

for split,colour in splits:
  print "line:", (split,0., split,gPad.GetUymax()*0.9)
  lines.append(TLine(split,0., split,gPad.GetUymax()*0.9))
  lines[-1].SetLineColor(colour)
  lines[-1].Draw("same")

tc.SaveAs("mva_output.png")
tc.SaveAs("mva_output.pdf")
