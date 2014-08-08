#!/usr/bin/env python

from ROOT import gROOT, gStyle
gROOT.SetBatch(True)
gROOT.ProcessLine(".x /afs/cern.ch/user/t/tbird/lhcbstyle.C")
gStyle.SetOptStat("ouRMe")

from math import sqrt
from ROOT import TFile, TCanvas, gDirectory

tf =  TFile.Open("/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/1920/output/fitResultsTree.toy.root")
#tf =  TFile.Open("/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/1924/output/fitResultsTree.toy.root")

tree = tf.Get("RooFitResultsTree")

tc = TCanvas("tc", "tc", 800, 600)

eCuts = [2., 4., 6., 8., 10.]
muCuts = [.2, .4, .6, .8]

#eCuts = [ 4., 6.]
#muCuts = [.2, .4]

results = {}
total = {}

for eCut in eCuts:
  results[eCut] = {}
  total[eCut] = {}
  for muCut in muCuts:
    results[eCut][muCut] = []
    total[eCut][muCut] = 0

for evt in tree:
  total[round(evt.eCut)][round(evt.muCut*10.)/10.] += 1
  if evt.covQual != 3:
    continue
  if evt.status_history_0 != 0:
    continue
  if evt.status_history_1 != 0:
    continue
  if evt.status != 0:
    continue
  if evt.limit_ac<0.01001e-6:
    #print "Hit lower limit limit: {0:.1f} {1:.1f} {2:d}".format(evt.eCut, evt.muCut, int(evt.seed))
    continue

  results[round(evt.eCut)][round(evt.muCut*10.)/10.].append(evt.limit_ac)


#for eCut in eCuts:
  #for muCut in muCuts:

    #tree.Draw("limit_ac>>limit_{0:.1f}_{1:.1f}(100,0,5e-7)".format(eCut, muCut),"abs(eCut-{0:f})<0.001 && abs(muCut-{1:f})<0.001 && limit_ac>0.01001e-6".format(eCut, muCut))

    #plot = gDirectory.Get("limit_{0:.1f}_{1:.1f}".format(eCut, muCut))
    #plot.GetXaxis().SetTitle("Limit")
    #plot.GetYaxis().SetTitle("Toys")
    #plot.GetYaxis().SetRangeUser(0., 120.)


    #tc.SaveAs("toy_plots/limit_ac_{0:.1f}_{1:.1f}.pdf".format(eCut, muCut))
    #tc.SaveAs("toy_plots/limit_ac_{0:.1f}_{1:.1f}.png".format(eCut, muCut))


from math import log, ceil, floor
def texround(v,e):
  error_power = floor(log(e,10))-1
  v /= 10**(error_power)
  e /= 10**(error_power)
  error_power = (round(error_power))
  v = (round(v))
  e = (round(e))
  value_power = ceil(log(v,10.))-1
  power  = error_power+value_power
  v /= 10**(value_power)
  e /= 10**(value_power)

  return "({0:f}\\pm{1:f})\\times{{}}10^{{{2:d}}}".format(v,e,int(round(power)))

from uncertainties import ufloat
for eCut in eCuts:
  for muCut in muCuts:
    r = results[eCut][muCut]
    n = len(r)
    t = total[eCut][muCut]

    eff = 100.*float(n)/float(t)

    avg = sum(r)/float(n)
    err = sqrt(sum([(x-avg)**2 for x in r]))/float(n)

    std = (sum([(x-ufloat(avg,err))**2 for x in r])/float(n-1))**.5

    #print "e cut: {0:<5.1f} mu cut: {1:<5.1f} avg: {2:>9.3e} \pm {3:<9.3e} {4:<5.2f}".format(eCut, muCut, avg, err, avg/err)

    print "${0:<5.1f}$ & ${1:<5.1f}$ & ${2:.2uL}$ & ${3:.2uL}$ \\\\".format(eCut, muCut, ufloat(avg, err), std)
