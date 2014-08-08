#!/usr/bin/env python

import sys

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT
from ROOT import TFile, gDirectory, TLine
from ROOT import TCanvas, TChain

gROOT.ProcessLine(".x lhcbStyle.C")

directory = "/afs/cern.ch/user/t/tbird/cmtuser/Urania_v2r1/PIDCalib/PIDPerfScripts/scripts/python/Plots/"

ncuts = 5
#cuts = [("e_ProbNNe>%s_All"%(str(0.5/(ncuts)+float(i)/(ncuts))), ROOT.kBlue + 2*i) for i in range(ncuts)]
cuts = [("e_DLLe>%s_All"%(str(j)), ROOT.kBlue + 2*i) for i,j in enumerate([-2,1,4,7,10,13])]
#cuts.reverse()

print "Using cuts:", cuts

plots = [
  ("P","p","20,0,100000","Probe electron momentum / MeV"),
  ("ETA","eta","20,1.5,5.0","#it{#eta}"),
  ("HasBremAdded","brem_added","2,0,2","Was a bremstrahlung photon added"),
  ("CaloRegion","calo_region","3,2,5","Calo Region"),
  ("nTracks","ntrack","20,0,500","Number of Tracks"),
  ("nSPDHits","nspd","20,0,500","Number of SPD Hits"),
  ]

#basiccuts = "{particle}_Probe == 1 && {particle}_ElectronTisTagged == 1 && {other}_Tag == 1"

hists = []
final_hists = []
keep = []
tc = TCanvas("tc", "tc",800,600)
#tc_full = TCanvas("tc_full", "tc_full",800,600)
#tc_cut = TCanvas("tc_cut", "tc_cut",800,600)

tfs=[]

def getPlot(var,plot):
  tfs.append( TFile(directory+"/PubPlots_e_as_e_Strip20r1_MagUp_PerfPlots_e_%s.root"%var, "OPEN"))
  p = tfs[-1].Get(plot)
  #tf.Close()
  return p
  
for i,(variable, name, binning,title) in enumerate(plots):
  print "Making plot",i,variable
  hists.append([])
  final_hists.append([])
  for j,(cut,colour) in enumerate(cuts):
    hists[i].append([])
    
    
    final_hists[i].append( getPlot(variable,cut).Clone("ratio_%i_%i"%(i,j)) )
    
    final_hists[i][j].SetStats(False)
    final_hists[i][j].GetYaxis().SetRangeUser(0.,1.09)
    final_hists[i][j].GetYaxis().SetTitle("Fraction of tracks")
    final_hists[i][j].GetXaxis().SetTitle(title)
    final_hists[i][j].SetMarkerColor(colour)
    final_hists[i][j].SetLineColor(colour)
    
    if j is 0:
      tc.cd()
      final_hists[i][j].Draw("e1")
      #tc_full.cd()
      #keep[-2].Draw()
      #tc_cut.cd()
      #keep[-1].Draw()
    else:
      tc.cd()
      final_hists[i][j].Draw("same e1")
      #tc_full.cd()
      #keep[-2].Draw("same")
      #tc_cut.cd()
      #keep[-1].Draw("same")
    
  tc.SaveAs("jpsiee_dataeff_dll_%s.pdf"%(name))
  tc.SaveAs("jpsiee_dataeff_dll_%s.png"%(name))
  
  #tc_full.SaveAs("jpsiee_full_%s.pdf"%(name))
  #tc_full.SaveAs("jpsiee_full_%s.png"%(name))
  
  #tc_cut.SaveAs("jpsiee_cut_%s.pdf"%(name))
  #tc_cut.SaveAs("jpsiee_cut_%s.png"%(name))


