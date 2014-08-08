#!/usr/bin/env python

import sys

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT
from ROOT import TFile, gDirectory, TLine
from ROOT import TCanvas, TChain

gROOT.ProcessLine(".x lhcbStyle.C")

directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/mcjpsiee/"
#directory = "/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/"
  
chain = TChain("JpsieeKFromBTuple/CalibPID")
chain.Add(directory+"PIDCalib_MagDown.root")
chain.Add(directory+"PIDCalib_MagUp.root")

ncuts = 5
#cuts = [("{particle}_ProbNNe>"+str(0.5/(ncuts)+float(i)/(ncuts)), ROOT.kBlue + 2*i) for i in range(ncuts)]
cuts = [("{particle}_PIDe>%s"%(str(j)), ROOT.kBlue + 2*i) for i,j in enumerate([-2,1,4,7,10,13])]
#cuts.reverse()

print "Using cuts:", cuts

plots = [
  ("{particle}_P","p","20,0,100000","Probe electron momentum / MeV"),
  ("{particle}_ETA","eta","20,1.5,5.0","#it{#eta}"),
  ("{particle}_BremMultiplicity>0","brem_added","2,0,2","Was a bremstrahlung photon added"),
  ("{particle}_BremMultiplicity","brem_multiplicity","3,0,3","Number of photons"),
  ("{particle}_CaloRegion","calo_region","3,2,5","Calo Region"),
  ("nTracks","ntrack","20,0,500","Number of Tracks"),
  ("nSPDHits","nspd","20,0,500","Number of SPD Hits"),
  ]

basiccuts = "{particle}_Probe == 1 && {particle}_ElectronTisTagged == 1 && {other}_Tag == 1"

particles = [
  ("PositiveProbe",{"particle":"e0", "other":"e1"}), 
  ("NegativeProbe",{"particle":"e1", "other":"e0"}),
  ]

hists = []
final_hists = []
keep = []
tc = TCanvas("tc", "tc",800,600)
tc_full = TCanvas("tc_full", "tc_full",800,600)
tc_cut = TCanvas("tc_cut", "tc_cut",800,600)

for i,(variable, name, binning,title) in enumerate(plots):
  print "Making plot",i,variable
  hists.append([])
  final_hists.append([])
  for j,(cut,colour) in enumerate(cuts):
    hists[i].append([])
    for k,(pname,pnames) in enumerate(particles):
      print "Drawing",variable,cut.format(**pnames),pname
      chain.Draw(variable.format(**pnames)+">>fullhist_%i_%i_%s(%s)"%(i,j,pname,binning),basiccuts.format(**pnames))
      hists[i][j].append(gDirectory.Get("fullhist_%i_%i_%s"%(i,j,pname)))
      chain.Draw(variable.format(**pnames)+">>cuthist_%i_%i_%s(%s)"%(i,j,pname,binning),basiccuts.format(**pnames)+"&&"+cut.format(**pnames))
      hists[i][j].append(gDirectory.Get("cuthist_%i_%i_%s"%(i,j,pname)))
      
    full_hist = hists[i][j][0].Clone()
    full_hist.Add(hists[i][j][2])
    full_hist.Sumw2()
    cut_hist = hists[i][j][1].Clone()
    cut_hist.Add(hists[i][j][3])
    cut_hist.Sumw2()
    
    keep.append(full_hist)
    keep.append(cut_hist)
    
    final_hists[i].append( cut_hist.Clone("ratio_%i_%i"%(i,j)) )
    final_hists[i][j].Divide(cut_hist, full_hist, 1., 1., "b")
    
    final_hists[i][j].SetStats(False)
    final_hists[i][j].GetYaxis().SetRangeUser(0.,1.09)
    final_hists[i][j].GetYaxis().SetTitle("Fraction of tracks")
    final_hists[i][j].GetXaxis().SetTitle(title)
    final_hists[i][j].SetMarkerColor(colour)
    final_hists[i][j].SetLineColor(colour)
    
    if j is 0:
      tc.cd()
      final_hists[i][j].Draw("e1")
      tc_full.cd()
      keep[-2].Draw()
      tc_cut.cd()
      keep[-1].Draw()
    else:
      tc.cd()
      final_hists[i][j].Draw("same e1")
      tc_full.cd()
      keep[-2].Draw("same")
      tc_cut.cd()
      keep[-1].Draw("same")
    
  tc.SaveAs("jpsiee_dll_eff_%s.pdf"%(name))
  tc.SaveAs("jpsiee_dll_eff_%s.png"%(name))
  
  tc_full.SaveAs("jpsiee_dll_full_%s.pdf"%(name))
  tc_full.SaveAs("jpsiee_dll_full_%s.png"%(name))
  
  tc_cut.SaveAs("jpsiee_dll_cut_%s.pdf"%(name))
  tc_cut.SaveAs("jpsiee_dll_cut_%s.png"%(name))


