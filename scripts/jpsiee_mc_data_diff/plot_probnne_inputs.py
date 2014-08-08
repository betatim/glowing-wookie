#!/usr/bin/env python

import sys, os, itertools

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT
from ROOT import TFile, gDirectory, TLine
from ROOT import TCanvas, TChain, TH1F

gROOT.ProcessLine(".x lhcbStyle.C")

from array import array

#mc_dir = "/afs/cern.ch/work/t/tbird/"
#mc_tree = "ANNPID.Tuple/annInputs"
#mc_files = [
  #"Reco14-0.root"
#]

mc_dir = "root://castorlhcb.cern.ch//castor/cern.ch/user/j/jonrob/ProtoParticlePIDtuples/MC12-Binc-nu2.5/"
mc_tree = "ANNPID.Tuple/annInputs"
mc_files = [ "Reco14-%i.root" % (i) for i in range(100) ]

mc_files = mc_files[0:10]

data_dir = "/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/"
data_tree = "JpsieeKFromBTuple/CalibPID"
data_files = list(itertools.chain.from_iterable([ ["%i/%i/output/PID_Modes.root" % (j,i) for j in [1472,1473]] for i in range(260) ]))


tag_cut = "{particle}_Tag==1"
probe_cut = "{particle}_Probe==1 && {particle}_ElectronTisTagged==1"
data_cut = "Jpsi_M>2700 && Jpsi_M<3150 && (Bu_M-Jpsi_M)>2150 && (Bu_M-Jpsi_M)<2200"
mc_cut = "1"
mc_fromb_cut = "MCFromB==1 && TrackPt>500 && TrackP>3000"

colours = [
    ROOT.kBlack, #Data
    ROOT.kRed,   #MC
    ROOT.kRed+3, #MC from B
  ]
markers = [
    None,     #Data
    ROOT.kOpenCircle,     #MC
    ROOT.kOpenTriangleUp, #MC from B
  ]

plots = [
  ("TrackP","{particle}_P","50,0,100000","Momentum / MeV"),
  ("TrackPt","{particle}_PT","50,0,10000","Transverse momentum / MeV"),
  ("TrackChi2PerDof","{particle}_TTTI_TRACK_CHI2NDOF","50,0,3","Track #Chi^{2}/NDOF"),
  ("TrackNumDof","{particle}_TTTI_TRACK_NDOF","40,10,50","Track NDOF"),
  ("TrackLikelihood","{particle}_TTTI_TRACK_Likelihood","40,-40,0","Track Likelihood"),
  ("TrackGhostProbability","{particle}_TTTI_TRACK_GhostProb","50,0,1","Track Ghost Probability"),
  ("TrackFitMatchChi2","{particle}_TTTI_TRACK_MatchCHI2","60,0,60","Track Match #Chi^{2}"),
  ("TrackCloneDist","{particle}_TTTI_TRACK_CloneDist","20,-10,10","Track Clone Dist"),
  #("TrackFitVeloChi2",
  #("TrackFitVeloNDoF",
  #("TrackFitTChi2",
  #("TrackFitTNDoF",
  ("RichUsedAero","{particle}_TTD_UsedRichAerogel","2,0,2","Used Rich Areogel?"),
  ("RichUsedR1Gas","{particle}_TTD_UsedRich1Gas","2,0,2","Used Rich1 Gas?"),
  ("RichUsedR2Gas","{particle}_TTD_UsedRich2Gas","2,0,2","Used Rich2 Gas?"),
  #  ("RichAboveElThres","{particle}_TTD_RichAboveElThres","2,0,2","Above RICH electron threshold?"),
  ("RichAboveMuThres","{particle}_TTD_RichAboveMuThres","2,0,2","Above RICH muon threshold?"),
  #  ("RichAbovePiThres","{particle}_TTD_RichAbovePiThres","2,0,2","Above RICH pion threshold?"),
  ("RichAboveKaThres","{particle}_TTD_RichAboveKaThres","2,0,2","Above RICH kaon threshold?"),
  #  ("RichAbovePrThres","{particle}_TTD_RichAbovePrThres","2,0,2","Above RICH proton threshold?"),
  ("RichDLLe","{particle}_TTD_RichDLLe","100,-80,80","RICH DLLe"),
  ("RichDLLmu","{particle}_TTD_RichDLLmu","100,-80,80","RICH DLLmu"),
  ("RichDLLk","{particle}_TTD_RichDLLk","100,-80,80","RICH DLLk"),
  ("RichDLLp","{particle}_TTD_RichDLLp","100,-80,80","RICH DLLp"),
  ("RichDLLbt","{particle}_TTD_RichDLLbt","100,-80,80","RICH DLLbt"),
  ("MuonBkgLL","{particle}_TTD_MuonBkgLL","100,-10,10","MuonBkgLL"),
  ("MuonMuLL","{particle}_TTD_MuonMuLL","100,-10,10","MuonMuLL"),
  ("MuonIsMuon","{particle}_TTD_isMuon","2,0,2","Is muon?"),
  ("MuonNShared","{particle}_TTD_MuonNShared","10,0,10","Muon N Shared"),
  ("InAccMuon","{particle}_TTD_InAccMuon","2,0,2","In muon acceptance?"),
  ("MuonIsLooseMuon","{particle}_TTD_isMuonLoose","2,0,2","Is loose muon?"),
  ("EcalPIDe","{particle}_TTD_EcalPIDe","50,-5,5","ECAL PIDe"),
  ("EcalPIDmu","{particle}_TTD_EcalPIDmu","50,-5,5","ECAL PIDmu"),
  ("HcalPIDe","{particle}_TTD_HcalPIDe","50,-5,5","HCAL PIDe"),
  ("HcalPIDmu","{particle}_TTD_HcalPIDmu","50,-5,5","HCAL PIDmu"),
  ("PrsPIDe","{particle}_TTD_PrsPIDe","50,-5,5","PRS PIDe"),
  ("InAccBrem","{particle}_TTD_InAccBrem","2,0,2","In brem acceptance?"),
  ("BremPIDe","{particle}_TTD_BremPIDe","50,-5,5","Brem PIDe"),
  ("VeloCharge","{particle}_TTD_VeloCharge","2,0,2","Velo charge")
]

tc = TCanvas("tc", "tc",800,600)

mc_chain = TChain(mc_tree)
for f in mc_files:
  #if os.path.isfile(mc_dir + f):
  mc_chain.Add(mc_dir + f)
print "mc chain:", mc_chain.GetEntries()

data_chain = TChain(data_tree)
for f in data_files:
  if os.path.isfile(data_dir + f):
    data_chain.Add(data_dir + f)
print "data chain:", data_chain.GetEntries()


def overflow_hist(h):
   # This function paint the histogram h with an extra bin for overflows
   nx = h.GetNbinsX()+2
   xbins = array('f', [0]*(nx+2))
   for i in xrange(nx):
     xbins[i+1] = h.GetBinLowEdge(i+1)
   xbins[0] = (xbins[1]-h.GetBinWidth(1))
   xbins[nx] = (xbins[nx-1]+h.GetBinWidth(nx))
   tempName = h.GetName()+"_withOverFlow"
   # Book a temporary histogram having ab extra bin for overflows
   htmp = TH1F(tempName, h.GetTitle(), nx, xbins)
   # Reset the axis labels
   htmp.SetXTitle(h.GetXaxis().GetTitle())
   htmp.SetYTitle(h.GetYaxis().GetTitle())
   # Fill the new hitogram including the extra bin for overflows
   for i in xrange(nx+2):
     htmp.SetBinContent(i+1,h.GetBinContent(i))
     #htmp.SetBinError(i+1,h.GetBinError(i))
     #htmp.Fill(htmp.GetBinCenter(i+1), h.GetBinContent(i))
   # Fill the underflows
   htmp.Fill(h.GetBinLowEdge(1)-1, h.GetBinContent(0))
   # Restore the number of entries
   htmp.SetEntries(h.GetEntries()+h.GetBinContent(0)+h.GetBinContent(nx+1))
   # FillStyle and color
   htmp.SetFillStyle(h.GetFillStyle())
   htmp.SetFillColor(h.GetFillColor())
   htmp.Sumw2()
   return htmp
 
def find_max(plots):
  max_val = 0.
  for p in plots:
    for i in xrange(p.GetNbinsX()+2):
      if p.GetBinContent(i) > max_val:
        max_val = p.GetBinContent(i)
  return max_val
    

def mc_plot(variable,name,binning,cut=""):
  if cut == "":
    cut = "(%s)"%(mc_cut)
  else:
    cut = "(%s) && (%s)"%(mc_cut, cut)
  #name = "mc_hist_%s"%(variable)
  mc_chain.Draw("%s>>%s(%s)"%(variable,name,binning),cut)
  plot = gDirectory.Get(name)
  return plot

def data_plot(variable,name,binning,tag,probe,cut=""):
  if cut == "":
    cut = "(%s) && (%s) && (%s)"%(data_cut, tag_cut.format(particle=tag), probe_cut.format(particle=probe))
  else:
    cut = "(%s) && (%s) && (%s) && (%s)"%(data_cut, tag_cut.format(particle=tag), probe_cut.format(particle=probe), cut)
  data_chain.Draw("%s>>%s(%s)"%(variable.format(particle=probe),name,binning),cut)
  plot = gDirectory.Get(name)
  return plot

for i,(mc_var, data_var, binning,title) in enumerate(plots):
  print "Making hist", i, mc_var, data_var

  e0_hist = data_plot(data_var,"e0_hist_%s"%(mc_var),binning,"e0","e1")
  print "data hist e0:", e0_hist.GetEntries()
  e0_hist = overflow_hist(e0_hist)
  e1_hist = data_plot(data_var,"e1_hist_%s"%(mc_var),binning,"e1","e0")
  print "data hist e1:", e1_hist.GetEntries()
  e1_hist = overflow_hist(e1_hist)

  e_hist = e0_hist.Clone("e_hist_%s"%(mc_var))
  e_hist.Add(e1_hist)
  e_hist.Scale(1./e_hist.GetEntries())
  print "data hist:", e_hist.GetEntries()


  mc_hist = mc_plot(mc_var,mc_var,binning)
  print "mc hist:", mc_hist.GetEntries()
  mc_hist = overflow_hist(mc_hist)
  mc_hist.Scale(1./mc_hist.GetEntries())

  mc_fromb_hist = mc_plot(mc_var,mc_var+"_fromb",binning,mc_fromb_cut)
  print "mc_fromb hist:", mc_fromb_hist.GetEntries()
  mc_fromb_hist = overflow_hist(mc_fromb_hist)
  mc_fromb_hist.Scale(1./mc_fromb_hist.GetEntries())
  
  plots = [e_hist,mc_hist,mc_fromb_hist]
  
  ymax = find_max(plots)

  for i, (plot, colour, marker) in enumerate(zip(plots,colours,markers)):

    plot.SetStats(False)
    plot.GetYaxis().SetRangeUser(0.,ymax*1.1)
    plot.GetYaxis().SetTitle("Fraction of tracks")
    plot.GetXaxis().SetTitle(title)
    plot.SetMarkerColor(colour)
    if marker != None:
      plot.SetMarkerStyle(marker)
    plot.SetLineColor(colour)

    if i is 0:
      plot.Draw("e1")
    else:
      plot.Draw("e1 same")

  tc.SaveAs("probnne_input_%s.pdf"%(mc_var))
  tc.SaveAs("probnne_input_%s.png"%(mc_var))


