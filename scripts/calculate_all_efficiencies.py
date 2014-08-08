
import sys
from math import ceil, sqrt, log10

import ROOT
from ROOT import TFile, gROOT, TH1D, TCanvas, TChain

from wookie import config as wookie_config

config = {



  "emu2011" : {
      "cuts" : wookie_config.emu_cuts.get_list(),
      "datasets" : [wookie_config.datasets["mcemu2011"]],
    },
  "emu2012" : {
      "cuts" : wookie_config.emu_cuts.get_list(),
      "datasets" : [wookie_config.datasets["mcemu2012"]],
    },
  "pipi2011" : {
      "cuts" : wookie_config.pipi_cuts.get_list(),
      "datasets" : [wookie_config.datasets["mcpipi2011"]],
    },
  "pipi2012" : {
      "cuts" : wookie_config.pipi_cuts.get_list(),
      "datasets" : [wookie_config.datasets["mcpipi2012"]],
    },
  "pipiasemu2011" : {
      "cuts" : wookie_config.pipiasemu_cuts.get_list(),
      "datasets" : [wookie_config.datasets["mcpipiasemu2011"]],
    },
  "pipiasemu2012" : {
      "cuts" : wookie_config.pipiasemu_cuts.get_list(),
      "datasets" : [wookie_config.datasets["mcpipiasemu2012"]],
    },
  "kpi2011" : {
      "cuts" : wookie_config.kpi_cuts.get_list(),
      "datasets" : [wookie_config.datasets["mckpi2011"]],
    },
  "kpi2012" : {
      "cuts" : wookie_config.kpi_cuts.get_list(),
      "datasets" : [wookie_config.datasets["mckpi2012"]],
    },












  #"pipiasemu" : {
      #"cuts" : [
        #"abs(x1_TRUEID)==211 && abs(x2_TRUEID)==211 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60",
        #"x1_ID*x2_ID<0",
        #"x2_L0MuonDecision_TOS == 1",
        #"x2_Hlt1TrackMuonDecision_TOS == 1",
        #"D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1815 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1915 )",
        #"abs(Dst_DTF_CHI2)<100",
        #"Dst_DTF_D0_MM > 1815 && Dst_DTF_D0_MM < 1915",
        #"x1_ProbNNe>0.32 && x2_ProbNNmu>0.2 && pi_ProbNNpi>0.9",

      #],
      #"events" : {"magup":  502999+1000998, "magdown": 516999+1022495},
      #"file" : "/afs/cern.ch/work/t/tbird/demu/ntuples/mcpipi/strip_emu.root",
    #},
  #"emu2011" : {
      #"cuts" : [
        #"abs(x1_TRUEID)==11 && abs(x2_TRUEID)==13 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT",
        #"x1_ID*x2_ID<0",
        #"x2_L0MuonDecision_TOS == 1",
        #"x2_Hlt1TrackMuonDecision_TOS == 1",
        #"D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1815 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1915 )",
        #"abs(Dst_DTF_CHI2)<100",
        #"Dst_DTF_D0_MM > 1815 && Dst_DTF_D0_MM < 1915",
        #"x1_ProbNNe>0.32 && x2_ProbNNmu>0.2 && pi_ProbNNpi>0.9",

      #],
      #"events" : {"magup":  1010498, "magdown": 1029498},
      #"file" : "/afs/cern.ch/work/t/tbird/demu/ntuples/mcemu/strip_emu_2011.root",
    #},
  #"emu2012" : {
      #"cuts" : [
        #"abs(x1_TRUEID)==11 && abs(x2_TRUEID)==13 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT",
        ##"Dst_BKGCAT == 0",
        #"x1_ID*x2_ID<0",
        #"x2_L0MuonDecision_TOS == 1",
        #"x2_Hlt1TrackMuonDecision_TOS == 1",
        #"D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1815 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1915 )",
        #"abs(Dst_DTF_CHI2)<100",
        #"Dst_DTF_D0_MM > 1815 && Dst_DTF_D0_MM < 1915",
        #"x1_ProbNNe>0.32 && x2_ProbNNmu>0.2 && pi_ProbNNpi>0.9",

      #],
      #"events" : {"magup":  2030990, "magdown": 2017492},
      #"file" : "/afs/cern.ch/work/t/tbird/demu/ntuples/mcemu/strip_emu_2012.root",
    #},
  #"pipi2011" : {
      #"cuts" : [
        #"abs(x1_TRUEID)==211 && abs(x2_TRUEID)==211 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT",
        #"x1_ID*x2_ID<0",
        #"x1_L0HadronDecision_TOS == 1 || x2_L0HadronDecision_TOS == 1",
        #"( x1_L0HadronDecision_TOS == 1 && x1_Hlt1TrackAllL0Decision_TOS == 1 ) || ( x2_L0HadronDecision_TOS == 1 && x2_Hlt1TrackAllL0Decision_TOS  == 1 )",
        #"Dst_Hlt2Dst2PiD02PiPiDecision_TOS == 1",
        ##"D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1",
        #"abs(Dst_DTF_CHI2)<100",
        #"x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNpi*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNk < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7",
      #],
      #"events" : {"magup": 502999, "magdown":516999 },
      #"file" : "/afs/cern.ch/work/t/tbird/demu/ntuples/mcpipi/strip_pipi_2011.root",
    #},
  #"pipi2012" : {
      #"cuts" : [
        #"abs(x1_TRUEID)==211 && abs(x2_TRUEID)==211 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT",
        #"x1_ID*x2_ID<0",
        #"x1_L0HadronDecision_TOS == 1 || x2_L0HadronDecision_TOS == 1",
        #"( x1_L0HadronDecision_TOS == 1 && x1_Hlt1TrackAllL0Decision_TOS == 1 ) || ( x2_L0HadronDecision_TOS == 1 && x2_Hlt1TrackAllL0Decision_TOS  == 1 )",
        #"Dst_Hlt2Dst2PiD02PiPiDecision_TOS == 1",
        ##"D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1",
        #"abs(Dst_DTF_CHI2)<100",
        #"x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNpi*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNk < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7",
      #],
      #"events" : {"magup": 1000998, "magdown":1022495},
      #"file" : "/afs/cern.ch/work/t/tbird/demu/ntuples/mcpipi/strip_pipi_2012.root",
    #},
  #"kpi2011" : {
      #"cuts" : [
        #"abs(x1_TRUEID)==321 && abs(x2_TRUEID)==211 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT",
        #"x1_ID*x2_ID<0",
        #"x1_L0HadronDecision_TOS == 1 || x2_L0HadronDecision_TOS == 1",
        #"( x1_L0HadronDecision_TOS == 1 && x1_Hlt1TrackAllL0Decision_TOS == 1 ) || ( x2_L0HadronDecision_TOS == 1 && x2_Hlt1TrackAllL0Decision_TOS  == 1 )",
        #"Dst_Hlt2Dst2PiD02KPiDecision_TOS == 1",
        ##"D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1",
        #"abs(Dst_DTF_CHI2)<100",
        #"x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNpi*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNk < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7",
      #],
      #"events" : {"magup": 502999, "magdown":516999 },
      #"file" : "/afs/cern.ch/work/t/tbird/demu/ntuples/mcpipi/strip_pipi_2011.root",
    #},
  #"kpi2012" : {
      #"cuts" : [
        #"abs(x1_TRUEID)==321 && abs(x2_TRUEID)==211 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT",
        #"x1_ID*x2_ID<0",
        #"x1_L0HadronDecision_TOS == 1 || x2_L0HadronDecision_TOS == 1",
        #"( x1_L0HadronDecision_TOS == 1 && x1_Hlt1TrackAllL0Decision_TOS == 1 ) || ( x2_L0HadronDecision_TOS == 1 && x2_Hlt1TrackAllL0Decision_TOS  == 1 )",
        #"Dst_Hlt2Dst2PiD02KPiDecision_TOS == 1",
        ##"D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1",
        #"abs(Dst_DTF_CHI2)<100",
        #"x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNpi*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNk < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7",
      #],
      #"events" : {"magup": 1000998, "magdown":1022495},
      #"file" : "/afs/cern.ch/work/t/tbird/demu/ntuples/mcpipi/strip_pipi_2012.root",
    #},
  #"pipi2012test" : {
      #"cuts" : [
        #"abs(x1_TRUEID)==211 && abs(x2_TRUEID)==211 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT",
        #"x1_ID*x2_ID<0",
        #"x1_L0HadronDecision_TOS == 1 || x2_L0HadronDecision_TOS == 1",
        #"( x1_L0HadronDecision_TOS == 1 && x1_Hlt1TrackAllL0Decision_TOS == 1 ) || ( x2_L0HadronDecision_TOS == 1 && x2_Hlt1TrackAllL0Decision_TOS  == 1 )",
        #"Dst_Hlt2Dst2PiD02PiPiDecision_TOS == 1",
        ##"D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1",
        #"abs(Dst_DTF_CHI2)<100",
        #"x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNpi*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNk < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7",
      #],
      #"events" : {"magup": 36500, "magdown":0},
      #"file" : "/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/1457/2/output/Demu_NTuple.root",
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
        errarr.append(float(passed)/t * sqrt(1./passed + 1./t))
      else:
        errarr.append(1.)
  else:
    effarr = [float(passed)/total]
    errarr = [1.]
    if passed != 0:
      errarr = [ effarr[0] * sqrt(1./passed + 1./total) ]

  res_arr = []
  for eff,err in zip(effarr,errarr):
    dp = (int(ceil(-log10(err)))-1)
    if dp < 1:
      dp = 1
    res_str = "$(%.{dp}f \\pm %.{dp}f)\\%%$".format(dp=dp)
    res_arr.append(res_str%(100.*eff,100.*err))
  results = "   ".join(res_arr)

  print append+results+prepend


for ds in [dataset]:
  ttree = TChain("Demu_NTuple/Demu_NTuple")

  grand_total = 0
  for ds_dict in config[ds]["datasets"]:
    ttree.Add(ds_dict["file"])
    grand_total += ds_dict["events"]["magup"] + ds_dict["events"]["magdown"]

  cut_str = ""

  passed = 0
  total = grand_total

  for cut in [""]+config[ds]["cuts"]:
    if cut != "":
      if cut_str != "":
        cut_str += " && (%s)" % (cut)
      else:
        cut_str = "(%s)" % (cut)

    print "Applying cut:", cut
    passed = ttree.GetEntries(cut_str)
    print_eff(passed,[total,grand_total])

    if passed == 0:
      print "Break! Break! Break! No events passed."
      break

    total = passed

  print "Total efficiency:"
  print_eff(passed,grand_total)



