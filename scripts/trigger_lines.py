
import re
import operator

import ROOT
from ROOT import TFile, gROOT, TH1D, TCanvas

gROOT.ProcessLine(".x lhcbstyle.C")

tf = TFile("/afs/cern.ch/work/t/tbird/demu/ntuples/mcemu/strip_emu_tim.root")
ttree = tf.Get("Demu_NTuple/Demu_NTuple")

lines_per_level = 2

l0_tc = TCanvas("l0_tc","l0_tc",800,600)
l0_tc.SetBottomMargin(0.2)
l0_tc.SetRightMargin(0.2)

l0_re = re.compile("Dst_L0.*_Dec")
hlt1_re = re.compile("Dst_Hlt1.*_Dec")
hlt2_re = re.compile("Dst_Hlt2.*_Dec")

l0 = []
hlt1 = []
hlt2 = []

for br in ttree.GetListOfBranches():
  br_name = br.GetName()
  #print br_name
  if (not ("Global" in br_name)) and (not ("Phys" in br_name)):
    if hlt1_re.match(br_name):
      hlt1.append(br_name)
    elif hlt2_re.match(br_name):
      hlt2.append(br_name)
    elif l0_re.match(br_name):
      l0.append(br_name)


def combine_line_names(names):
  last_name = len(names) - 1
  cut = ""
  for i, name in enumerate(names):
    if i is not last_name:
      cut += name + " == 1 || "
    else:
      cut += name + " == 1"
  return cut
      
def create_cut(levels):
  last_level = len(levels) - 1
  cut = ""
  for i, level in enumerate(levels):
    if i is not last_level:
      if isinstance(level,list):
        cut += "(" + combine_line_names(level) + ") && "
      else:
        cut += "(" + level + ") && "
    else:
      if isinstance(level,list):
        cut += "(" + combine_line_names(level) + ")"
      else:
        cut += "(" + level + ")"
  #print "       >>> ", cut, levels
  return cut
      

def calc_eff(triggers,total = 1.):
  return ttree.Draw(br_name,create_cut(triggers))/total

def find_most_useful(all_lines,best_lines,given_lines = None):
  best_line = ""
  best_line_value = 0.
  for line in all_lines:
    if line in best_lines:
      continue
    tmp_lines = [line]
    if not best_lines == []: tmp_lines += best_lines 
    if given_lines == None:
      tmp_lines = [tmp_lines]
    else:
      tmp_lines = [tmp_lines] + given_lines 
    #print tmp_lines
    passed = calc_eff(tmp_lines)
    if passed > best_line_value:
      best_line = line
      best_line_value = passed
  return (best_line, best_line_value)
    
      



l0_tot = float(ttree.GetEntries())

l0_hist = TH1D("l0_hist","l0_hist;;Efficency",10,0,10)
l0_hist.SetBit(TH1D.kCanRebin)

l0_eff = []
l0_used_lines = []
while len(l0_used_lines) < len(l0):
  next_best_line, value = find_most_useful(l0,l0_used_lines)
  l0_eff.append(value/l0_tot)
  l0_hist.Fill(next_best_line.replace("Dst_","").replace("_Dec",""), value/l0_tot)
  l0_used_lines.append(next_best_line)

l0_hist.LabelsDeflate()
l0_hist.Draw()
l0_hist.SetStats(False)
l0_hist.GetYaxis().SetTitleFont(62)
l0_hist.GetYaxis().SetDecimals(True)
l0_hist.GetYaxis().SetRangeUser(0.5,0.8)

l0_lines_for_hlt1 = l0_used_lines[:lines_per_level]

print "two most efficient lines at %.2f%% are:" % (100.*l0_eff[lines_per_level-1]), l0_lines_for_hlt1


    
hlt1_tc = TCanvas("hlt1_tc","hlt1_tc",800,600)
hlt1_tc.SetBottomMargin(0.2)
hlt1_tc.SetRightMargin(0.2)

hlt1_tot = calc_eff([l0_lines_for_hlt1])

hlt1_hist = TH1D("hlt1_hist","hlt1_hist;;Efficency",10,0,10)
hlt1_hist.SetBit(TH1D.kCanRebin)

hlt1_eff = []
hlt1_used_lines = []
while len(hlt1_used_lines) < len(hlt1):
  next_best_line, value = find_most_useful(hlt1,hlt1_used_lines,[l0_lines_for_hlt1])
  hlt1_eff.append(value/hlt1_tot)
  hlt1_hist.Fill(next_best_line.replace("Dst_","").replace("_Dec",""), value/hlt1_tot)
  hlt1_used_lines.append(next_best_line)

hlt1_hist.LabelsDeflate()
hlt1_hist.Draw()
hlt1_hist.SetStats(False)
hlt1_hist.GetYaxis().SetTitleFont(62)
hlt1_hist.GetYaxis().SetDecimals(True)
hlt1_hist.GetYaxis().SetRangeUser(0.5,0.8)

hlt1_lines_for_hlt2 = hlt1_used_lines[:lines_per_level]

print "two most efficient lines at %.2f%% are:" % (100.*hlt1_eff[lines_per_level-1]), hlt1_lines_for_hlt2


    
hlt2_tc = TCanvas("hlt2_tc","hlt2_tc",800,600)
hlt2_tc.SetBottomMargin(0.2)
hlt2_tc.SetRightMargin(0.2)

hlt2_tot = calc_eff([hlt1_lines_for_hlt2,l0_lines_for_hlt1])

hlt2_hist = TH1D("hlt2_hist","hlt2_hist;;Efficency",10,0,10)
hlt2_hist.SetBit(TH1D.kCanRebin)

hlt2_eff = []
hlt2_used_lines = []
while len(hlt2_used_lines) < len(hlt2):
  next_best_line, value = find_most_useful(hlt2,hlt2_used_lines,[hlt1_lines_for_hlt2,l0_lines_for_hlt1])
  hlt2_eff.append(value/hlt2_tot)
  hlt2_hist.Fill(next_best_line.replace("Dst_","").replace("_Dec",""), value/hlt2_tot)
  hlt2_used_lines.append(next_best_line)

hlt2_hist.LabelsDeflate()
hlt2_hist.Draw()
hlt2_hist.SetStats(False)
hlt2_hist.GetYaxis().SetTitleFont(62)
hlt2_hist.GetYaxis().SetDecimals(True)
hlt2_hist.GetYaxis().SetRangeUser(0.5,0.8)
hlt2_hist.GetYaxis().LabelsOption("v")

print "two most efficient lines at %.2f%% are:" % (100.*hlt2_eff[lines_per_level-1]), hlt2_used_lines[:lines_per_level]

print "overall eff is %.2f%%"%(100.*hlt2_eff[lines_per_level-1]*hlt1_eff[lines_per_level-1]*l0_eff[lines_per_level-1])

for i in [zip(l0_used_lines,l0_eff),zip(hlt1_used_lines,hlt1_eff),zip(hlt2_used_lines,hlt2_eff)]:
  for line,eff in i:
    print line.replace("Dst_","").replace("_Dec",""), "& %.1f \\\\"%(100.*eff)
