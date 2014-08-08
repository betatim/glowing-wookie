#!/usr/bin/env python

from ROOT import gROOT
gROOT.ProcessLine(".x /afs/cern.ch/user/t/tbird/lhcbstyle.C")

import ROOT
from ROOT import TFile, TCanvas

tc = TCanvas("tc","tc",800,600)

tfs = []
tfs.append( TFile.Open("PlotCalibDistribution_e_ETA_Strip20_MagDown_100binspi_ETA.root") )
tfs.append( TFile.Open("PlotCalibDistribution_e_ETA_Strip20_MagDown_emu2012e_ETA.root") )

hist_calib_100 = tfs[-2].Get("e_ETA_All")
hist_calib_std = tfs[-1].Get("e_ETA_All")

tfs.append( TFile.Open("PlotRefDistribution_e_ETA_100binse_ETA_2012.root") )
tfs.append( TFile.Open("PlotRefDistribution_e_ETA_emu2012e_ETA_2012.root") )

hist_ref_100 = tfs[-2].Get("e_ETA")
hist_ref_std = tfs[-1].Get("e_ETA")

tfs.append( TFile.Open("PubPlots_e_as_e_Strip20_MagDown_emu2012e_ETA.root") )

hist_calib_eff = tfs[-1].Get("e_HasBremAdded==1_All")

hist_calib_100.Scale( 1./hist_calib_100.GetMaximum() )
hist_calib_std.Scale( 1./hist_calib_std.GetMaximum() )
hist_ref_100.Scale( 1./hist_ref_100.GetMaximum() )
hist_ref_std.Scale( 1./hist_ref_std.GetMaximum() )


hist_calib_100.GetYaxis().SetTitle("Arb. Scale")
hist_calib_100.GetXaxis().SetTitle("Pseudorapidity, #eta")
hist_calib_100.Draw("HIST")
hist_calib_std.SetLineColor(ROOT.kRed)
hist_calib_std.Draw("HIST SAME")

name = "calib_eta"
tc.SaveAs("example_%s.pdf"%name)
tc.SaveAs("example_%s.png"%name)


hist_ref_100.GetYaxis().SetTitle("Arb. Scale")
hist_ref_100.GetXaxis().SetTitle("Pseudorapidity, #eta")
hist_ref_100.Draw("HIST")
hist_ref_std.SetLineColor(ROOT.kRed)
hist_ref_std.Draw("HIST SAME")

name = "ref_eta"
tc.SaveAs("example_%s.pdf"%name)
tc.SaveAs("example_%s.png"%name)


hist_calib_eff.GetYaxis().SetRangeUser(0.,1.)
hist_calib_eff.Draw("e1")

name = "eff_hasbrem_eta"
tc.SaveAs("example_%s.pdf"%name)
tc.SaveAs("example_%s.png"%name)

