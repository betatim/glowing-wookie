
import sys
from math import ceil, sqrt, log10

import ROOT
from ROOT import TFile, gROOT, TH1D, TCanvas, TChain

from wookie import config as wookie_config

config = {

  "emu" : {
      "cuts" : wookie_config.emu_cuts.get_list(["mcmatch", "ls", "l0", "hlt1", "hlt2", "hlt2_1815_1915", "dtf", "mass", "ghost"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcemu2011"]],
      "dataset2012" : [wookie_config.datasets["mcemu2012"]],
    },

  "emu_nopid" : {
      "cuts" : wookie_config.emu_cuts.get_list(["mcmatch", "ls", "l0", "hlt1", "hlt2", "hlt2_1815_1915", "dtf", "mass", "ghost"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcnopidemu2011"]],
      "dataset2012" : [wookie_config.datasets["mcnopidemu2012"]],
    },

  "emu_1740_1950" : {
      #"cuts" : wookie_config.emu_cuts.get_list(["mcmatch","ls","l0","hlt1","hlt2_1790_1930","dtf","mass","ghost","pid"]),
      "cuts" : wookie_config.emu_cuts.get_list(["mcmatch","ls","l0","hlt1","hlt2","hlt2_1740_1950","hlt2_1815_1915"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcemu2011"]],
      "dataset2012" : [wookie_config.datasets["mcemu2012"]],
    },
  "emu_1790_1950" : {
      #"cuts" : wookie_config.emu_cuts.get_list(["mcmatch","ls","l0","hlt1","hlt2_1790_1930","dtf","mass","ghost","pid"]),
      "cuts" : wookie_config.emu_cuts.get_list(["mcmatch","ls","l0","hlt1","hlt2","hlt2_1790_1950","hlt2_1815_1915"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcemu2011"]],
      "dataset2012" : [wookie_config.datasets["mcemu2012"]],
    },
  "emu_1790_1930" : {
      #"cuts" : wookie_config.emu_cuts.get_list(["mcmatch","ls","l0","hlt1","hlt2_1790_1930","dtf","mass","ghost","pid"]),
      "cuts" : wookie_config.emu_cuts.get_list(["mcmatch","ls","l0","hlt1","hlt2","hlt2_1790_1930","hlt2_1815_1915"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcemu2011"]],
      "dataset2012" : [wookie_config.datasets["mcemu2012"]],
    },
  "emu_1815_1915" : {
      #"cuts" : wookie_config.emu_cuts.get_list(["mcmatch","ls","l0","hlt1","hlt2_1790_1930","dtf","mass","ghost","pid"]),
      "cuts" : wookie_config.emu_cuts.get_list(["mcmatch","ls","l0","hlt1","hlt2","hlt2_1815_1915"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcemu2011"]],
      "dataset2012" : [wookie_config.datasets["mcemu2012"]],
    },
  
  "emu_l0_1" : {
      "cuts" : wookie_config.pipi_cuts.get_list(to_cut="ls") + wookie_config.emu_cuts.get_list(["ls","l0","hlt1","hlt2_1815_1915","dtf","mass","ghost","pid"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcpipi2011"]],
      "dataset2012" : [wookie_config.datasets["mcpipi2012"]],
    },
  "emu_l0_2" : {
      "cuts" : wookie_config.pipi_cuts.get_list(to_cut="ls") + wookie_config.emu_cuts.get_list(["ls","hlt2_1815_1915","l0","hlt1","dtf","mass","ghost","pid"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcpipi2011"]],
      "dataset2012" : [wookie_config.datasets["mcpipi2012"]],
    },
  "emu_l0_3" : {
      "cuts" : wookie_config.pipi_cuts.get_list(to_cut="ls") + wookie_config.emu_cuts.get_list(["ls","hlt2_1815_1915","dtf","mass","ghost","l0","hlt1","pid"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcpipi2011"]],
      "dataset2012" : [wookie_config.datasets["mcpipi2012"]],
    },
  "emu_l0_4" : {
      "cuts" : wookie_config.pipi_cuts.get_list(to_cut="ls") + wookie_config.emu_cuts.get_list(["ls","hlt2_1815_1915","dtf","mass","ghost","pid","l0","hlt1"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcpipi2011"]],
      "dataset2012" : [wookie_config.datasets["mcpipi2012"]],
    },
  "emu_l0_5" : {
      "cuts" : wookie_config.pipi_cuts.get_list(to_cut="ls") + wookie_config.emu_cuts.get_list(["ls","hlt1","l0","hlt2_1815_1915","dtf","mass","ghost","pid"]),
      "cutnames" : wookie_config.emu_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcpipi2011"]],
      "dataset2012" : [wookie_config.datasets["mcpipi2012"]],
    },


  "pipi" : {
      "cuts" : wookie_config.pipi_cuts.get_list(),
      "cutnames" : wookie_config.pipi_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mcpipi2011"]],
      "dataset2012" : [wookie_config.datasets["mcpipi2012"]],
    },
  "kpi" : {
      "cuts" : wookie_config.kpi_cuts.get_list(),
      "cutnames" : wookie_config.kpi_cuts.get_name_list(),
      "dataset2011" : [wookie_config.datasets["mckpi2011"]],
      "dataset2012" : [wookie_config.datasets["mckpi2012"]],
    },
  "pipiasemu" : {
      "cuts" : wookie_config.pipiasemu_cuts.get_list(["mcmatch", "ls", "hlt2", "hlt2_1815_1915", "dtf", "mass", "ghost"]),
        #wookie_config.pipi_cuts.get_list(to_cut="ls") + wookie_config.emu_cuts.get_list(from_cut="ls",to_cut="pid"),
      "cutnames" : wookie_config.pipiasemu_cuts.get_name_list(),
        #wookie_config.pipi_cuts.get_name_list(to_cut="ls") + wookie_config.emu_cuts.get_name_list(from_cut="ls",to_cut="pid"),
      "dataset2011" : [wookie_config.datasets["mcpipiasemu2011"]],
      "dataset2012" : [wookie_config.datasets["mcpipiasemu2012"]],
    },
  #"pipiasemu" : {
      #"cuts" : wookie_config.pipi_cuts.get_list(to_cut="ls") + wookie_config.emu_cuts.get_list(from_cut="ls"),
      #"datasets" : [wookie_config.datasets["mcpipiasemu"]],
    #},


  }

if len(sys.argv) < 2:
  print "Script takes an argument, which is the dataset to calculate efficiency on."
  print "Try one of:", [key for key, val in config.iteritems()]
  sys.exit(1)

dataset = sys.argv[1]

try:
  config[dataset]
except KeyError:
  print dataset, "is not a dataset this script knows about try one of:", [key for key, val in config.iteritems()]





def print_eff(passed,total,append="",prepend=""):
  effarr = []
  errarr = []
  if isinstance(total, list):
    effarr = [float(passed)/t for t in total]
    for t in total:
      if passed != 0.:
        #errarr.append(float(passed)/t * sqrt(1./passed + 1./t)) #poisson
        errarr.append((1./t) * sqrt(float(passed) * ( 1. - float(passed)/t)))
      else:
        errarr.append(1.)
  else:
    effarr = [float(passed)/total]
    errarr = [1.]
    if passed != 0:
      #errarr = [ effarr[0] * sqrt(1./passed + 1./total) ] #poisson
      errarr = [ (1./total) * sqrt(float(passed) *( 1. - effarr[0])) ] #binomial

  res_arr = []
  for eff,err in zip(effarr,errarr):
    dp = (int(ceil(-log10(err)))-1) if err != 0. else 1
    if dp < 1:
      dp = 1
    res_str = "$(%.{dp}f \\pm %.{dp}f)\\%%$".format(dp=dp)
    res_arr.append(res_str%(100.*eff,100.*err))
  results = " & ".join(res_arr)

  return append+results+prepend

subsamps = ["2011","2012"]

results = []
for y in subsamps:
  results.append("MC%s"%y)
  results.append("MC%s Total"%y)
print " & "," & ".join(results),"\\\\"


for ds in [dataset]:
  ttree = {}
  grand_total = {}
  for y in subsamps:
    ttree[y] = TChain("Demu_NTuple/Demu_NTuple")

    grand_total[y] = 0
    for ds_dict in config[ds]["dataset%s"%y]:
      ttree[y].Add(ds_dict["file"])
      grand_total[y] += ds_dict["events"]["magup"] + ds_dict["events"]["magdown"]

  cut_str = ""

  passed = {}
  total = {}
  for y in subsamps:
    passed[y] = 0
    total[y] = grand_total[y]

  for cut,name in zip(config[ds]["cuts"],config[ds]["cutnames"]):
    results = []
    if cut != "":
      if cut_str != "":
        cut_str += " && (%s)" % (cut)
      else:
        cut_str = "(%s)" % (cut)
    print "%Applying cut:", cut

    for y in subsamps:
      passed[y] = ttree[y].GetEntries(cut_str)
      #results.append(print_eff(passed[y],[total[y],grand_total[y]]))
      results.append(print_eff(passed[y],[total[y]]))

      if passed[y] == 0:
        print "%Break! Break! Break! No events passed."
        continue

      total[y] = passed[y]
    print wookie_config.cut_titles[name],"& "," & ".join(results),"\\\\"

  print "%Total efficiency:"
  print "\\midrule"
  results = []
  for y in subsamps:
    #results.append(print_eff(passed[y],grand_total[y]))
    results.append(print_eff(passed[y],grand_total[y]))
  print "Total & "," & ".join(results),"\\\\"



