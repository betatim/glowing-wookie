
import re
import operator

import ROOT
from ROOT import TFile, gROOT, TH1D, TCanvas

tf = TFile("/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/142/0/output/Demu_NTuple.root")
ttree = tf.Get("Demu_NTuple/Demu_NTuple")

l0_tc = TCanvas("l0_tc","l0_tc",800,600)

l0_re = re.compile("Dst_L0.*_Dec")
hlt1_re = re.compile("Dst_Hlt1.*_Dec")
hlt2_re = re.compile("Dst_Hlt2.*_Dec")

l0 = []
hlt1 = []
hlt2 = []

l0_eff = {}
hlt1_eff = {}
hlt2_eff = {}

l0_best = []
hlt1_best = []
hlt2_best = []

for br in ttree.GetListOfBranches():
  br_name = br.GetName()
  print br_name
  if hlt1_re.match(br_name):
    hlt1.append(br_name)
  elif hlt2_re.match(br_name):
    hlt2.append(br_name)
  elif l0_re.match(br_name):
    l0.append(br_name)
    


l0_tot = float(ttree.GetEntries())

for br_name in l0:
  l0_eff[br_name] = ttree.Draw(br_name,br_name+"==1")/l0_tot
  
l0_eff = sorted(l0_eff.iteritems(), key=operator.itemgetter(1))
l0_eff.reverse()
  
l0_hist = TH1D("l0_hist","l0_hist",10,0,10)
l0_hist.SetBit(TH1D.kCanRebin)
for line,eff in l0_eff:
  l0_hist.Fill(line.replace("Dst_","").replace("_Dec",""), eff)
  if (not ("Global" in line)) and (not ("Phys" in line)):
    l0_best.append((line,eff))

l0_hist.LabelsDeflate()
l0_hist.Draw()

print "two most efficient lines are:",l0_best[0],l0_best[1]

    
    
hlt1_tc = TCanvas("hlt1_tc","hlt1_tc",800,600)

hlt1_tot = float(ttree.GetEntries())

for br_name in hlt1:
  hlt1_eff[br_name] = ttree.Draw(br_name,br_name+"==1")/hlt1_tot
  
hlt1_eff = sorted(hlt1_eff.iteritems(), key=operator.itemgetter(1))
hlt1_eff.reverse()
  
hlt1_hist = TH1D("hlt1_hist","hlt1_hist",10,0,10)
hlt1_hist.SetBit(TH1D.kCanRebin)
for line,eff in hlt1_eff:
  hlt1_hist.Fill(line.replace("Dst_","").replace("_Dec",""), eff)
  if (not ("Global" in line)) and (not ("Phys" in line)):
    hlt1_best.append((line,eff))

hlt1_hist.LabelsDeflate()
hlt1_hist.Draw()

print "two most efficient lines are:",hlt1_best[0],hlt1_best[1]

hlt1_cut = hlt1_best[0][0]+"==1||"+hlt1_best[0][0]+"==1"
#hlt1_cut = "1"

hlt2_tc = TCanvas("hlt2_tc","hlt2_tc",800,600)

hlt2_tot = float(ttree.Draw(hlt1_best[0][0],hlt1_cut))

for br_name in hlt2:
  hlt2_eff[br_name] = ttree.Draw(br_name,br_name+"==1"+"&&("+hlt1_cut+")")/hlt2_tot
  
hlt2_eff = sorted(hlt2_eff.iteritems(), key=operator.itemgetter(1))
hlt2_eff.reverse()
  
hlt2_hist = TH1D("hlt2_hist","hlt2_hist",10,0,10)
hlt2_hist.SetBit(TH1D.kCanRebin)
for line,eff in hlt2_eff:
  hlt2_hist.Fill(line.replace("Dst_","").replace("_Dec",""), eff)
  if (not ("Global" in line)) and (not ("Phys" in line)):
    hlt2_best.append((line,eff))

hlt2_hist.LabelsDeflate()
hlt2_hist.Draw()

