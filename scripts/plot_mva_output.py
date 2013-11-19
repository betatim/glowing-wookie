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
gROOT.SetBatch(True)

import random
import subprocess
import ROOT

from math import fabs, pi

from ROOT import TFile, TStopwatch, gROOT, gDirectory, TLine
from ROOT import gROOT, TFile, TTreeFormula, TCanvas, TChain, THStack


tc = TCanvas("tc", "tc",800,600)
f = TFile("/afs/cern.ch/user/t/tbird/emu/glowing-wookie/scripts/mva/d2emu-tmva.root")
tt = f.Get("TestTree")
tt.Draw("BDT_grad_30_120_7_1_5>>sig(100,-1,1)","classID==0")
sig = gDirectory.Get("sig")
tt.Draw("BDT_grad_30_120_7_1_5>>bkg(100,-1,1)","classID==1")
bkg = gDirectory.Get("bkg")

sig.Scale(1./sig.GetEntries())
bkg.Scale(1./bkg.GetEntries())

sig.SetTitle("")
sig.SetStats(False)
sig.GetXaxis().SetTitle("BDT Output")
sig.GetYaxis().SetTitleOffset(1.2)
sig.GetYaxis().SetTitle("Arb. Units")
bkg.SetLineColor(ROOT.kRed)

sig.Draw()
bkg.Draw("same")

tc.SaveAs("mva_output.pdf")
