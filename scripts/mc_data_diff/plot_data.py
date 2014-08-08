#!/usr/bin/env python

import sys

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT
from ROOT import TFile, gDirectory, TLine
from ROOT import TCanvas, TChain

gROOT.ProcessLine(".x lhcbStyle.C")

directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/"

data_name = "emu/strip_emu2011_unblind.root"
mc_name = "mcemu/pid_emu.root"

plots = [
  ("nTracks","ntrack","50,0,500","Number of Tracks"),
  ("nSPDHits","nspd","50,0,1000","Number of SPD Hits"),
  ]

colours = [
    ROOT.kBlue,
    ROOT.kBlack,
    ROOT.kRed,
  ]

hists = []
final_hists = []
keep = []
tc = TCanvas("tc", "tc",800,600)

tfs=[]

data_file = TFile.Open(directory+data_name)
data_tree = data_file.Get("Demu_NTuple/Demu_NTuple")

mc_file = TFile.Open(directory+mc_name)
mc_tree = mc_file.Get("subTree")
  
for i,(variable, name, binning,title) in enumerate(plots):
  print "Making plot",i,variable
  hists.append([])
  final_hists.append([])
    
  mc_tree.Draw("%s>>mc_%s(%s)"%(variable,name,binning))
  final_hists[i].append( gDirectory.Get("mc_%s"%(name,)) )
  
  if name == "nTracks":
    mc_tree.Draw("%s_Scaled>>mc_%s_scale(%s)"%(variable,name,binning))
    final_hists[i].append( gDirectory.Get("mc_%s_scale"%(name,)) )
  else:
    mc_tree.Draw("%s*1.28>>mc_%s_scale(%s)"%(variable,name,binning))
    final_hists[i].append( gDirectory.Get("mc_%s_scale"%(name,)) )
  
  data_tree.Draw("%s>>data_%s(%s)"%(variable,name,binning))
  final_hists[i].append( gDirectory.Get("data_%s"%(name,)) )
  
  for j,(plot) in enumerate(final_hists[i]):
    colour = colours[j]
    plot.SetStats(False)
    plot.GetYaxis().SetRangeUser(0.,1.09)
    plot.GetYaxis().SetTitle("Fraction of tracks")
    plot.GetXaxis().SetTitle(title)
    plot.SetMarkerColor(colour)
    plot.SetLineColor(colour)
    plot.Sumw2()
    plot.Scale(1./plot.GetEntries())
    
    print plot.GetName(), plot.GetMean(), plot.GetMeanError()
    
    if j is 0:
      tc.cd()
      plot.Draw("e1")
    else:
      tc.cd()
      plot.Draw("same e1")
    
  tc.SaveAs("data_mc_diff_%s.pdf"%(name))
  tc.SaveAs("data_mc_diff_%s.png"%(name))
  
  #tc_full.SaveAs("jpsiee_full_%s.pdf"%(name))
  #tc_full.SaveAs("jpsiee_full_%s.png"%(name))
  
  #tc_cut.SaveAs("jpsiee_cut_%s.pdf"%(name))
  #tc_cut.SaveAs("jpsiee_cut_%s.png"%(name))


