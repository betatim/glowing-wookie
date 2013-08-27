#!/usr/bin/env python

from ROOT import TFile, TCanvas, gDirectory

tc = TCanvas("tc","tc",800,1200)
tc.Divide(1,2)

for mc_type in ["kpi", "pipi", "kk"]:
  tf = TFile("/afs/cern.ch/work/t/tbird/demu/ntuples/mc%s/strip_emu.root"%(mc_type))
  ntuple = tf.Get("Demu_NTuple/Demu_NTuple")

  ntuple.Draw("D0_M>>d0m_%s(100,1600,2000)"%(mc_type))
  d0m = gDirectory.Get("d0m_%s"%(mc_type))
  
  ntuple.Draw("Dst_M-D0_M>>dstm_%s(100,135,165)"%(mc_type))
  dstm = gDirectory.Get("dstm_%s"%(mc_type))
  
  tc.Clear()
  tc.Divide(1,2)
  tc.cd(1)
  d0m.Draw()
  tc.cd(2)
  dstm.Draw()
  
  tc.SaveAs("mass_%s.pdf"%(mc_type))
