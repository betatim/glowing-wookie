# -*- coding: utf-8 -*-

import sys, os, argparse

parser = argparse.ArgumentParser(description='Fitter to determine Dms and Dmd from semi-leptonic B decays')
parser.add_argument("systematic", help='Name of the systematic to run')
parser.add_argument("nCPUs", type=int, help='Number of CPU cores to use')
parser.add_argument("PIDeCut", nargs='?', type=float, default=6.0, help='Cut on PIDe')
parser.add_argument("PIDmuCut", nargs='?', type=float, default=0.4, help='Cut on ProbNNmu')
parser.add_argument("-s", "--seed", type=int, default=1, help='Seed to use for toy')

args = parser.parse_args()

#print args
#sys.exit(0)

#if len(sys.argv) != 2+1:
  #print "To use this script run it like so:"
  #print sys.argv[0], "<systematic name> <number of CPUs>"
  #print ""
  #sys.exit(0)

sys.path.append("../..")

systName   = args.systematic
nCPUs   = args.nCPUs

print "script args:", systName, nCPUs, args.seed, args.PIDeCut, args.PIDmuCut
print ""

import subprocess, ROOT, datetime, array
try:
  from wookie import config as wookie_config
except ImportError:
  import config as wookie_config


def defaultPostHook(w):
  pass

config = {
  'outFileName': "fitResult.%s_%s.%s.root"%(systName,str(args.PIDeCut),str(args.PIDmuCut)),
  'loadFileName': "fitResult.blank.root",

  'kpiFile': wookie_config.datasets["fitterkpi2011"]["file"],
  'pipiFile': wookie_config.datasets["fitterpipi2011"]["file"],
  'mvaFile': wookie_config.datasets["fitterlooseemu2011unblind"]["file"],
  #root://castorlhcb.cern.ch//castor/cern.ch/grid/lhcb/LHCb/Collision11/CHARM.MDST/00012718/0000/00012718_00000012_1.charm.mdst?svcClass=lhcbdisk
  #'kpiFile': "root://castorlhcb.cern.ch//castor/cern.ch/user/t/tbird/demu/ntuples/kpi/strip_kpi_fitter.root?svcClass=default",
  #'pipiFile': "root://castorlhcb.cern.ch//castor/cern.ch/user/t/tbird/demu/ntuples/pipi/strip_pipi_fitter.root?svcClass=default",
  #'mvaFile': "root://castorlhcb.cern.ch//castor/cern.ch/user/t/tbird/demu/ntuples/emu/mva_emu_fitter.root?svcClass=default",
  #'kpiFile': "root://castor/cern.ch/user/t/tbird/demu/ntuples/kpi/strip_kpi_fitter.root",
  #'pipiFile': "root://castor/cern.ch/user/t/tbird/demu/ntuples/pipi/strip_pipi_fitter.root",
  #'mvaFile': "root://castor/cern.ch/user/t/tbird/demu/ntuples/emu/mva_emu_fitter.root",

  'mode': "datapretoy",

  'pipiBR': [1.401e-3,0.026e-3],
  'kpiBR': [3.88e-2,0.05e-2],

  'emuEff': (6.94e-2 * 10.537e-2 * 1. * 60.93e-2 * 53.29e-2 * 25.12e-2 * 99.852e-2 * 1. * 87.52e-2 * 79.97e-2),
  #           str pre|strip e|  tr e            |  off e
  #'pipiEff': (0.5 * 1.6e-2 * 0.398*0.558*0.887 * 0.5733),
  'kpiEff':  (21.415e-2 * 3.721e-2 * 1. * 18.82e-2 * 42.49e-2 * 99.714e-2 * 1. * 99.503e-2 * 81.65e-2 * 0.01),

  'pipiAsEmuEff': (20.205e-2 * 1.090e-2 * 0.4719e-2 * 60.01e-2 * 9.9990e-2),

  'emuMuPidCut': args.PIDmuCut,
  'emuEPidCut': args.PIDeCut,

  'norm':'kpi',
  'normScale': wookie_config.datasets["fitteremu2011unblind"]["lumi"]/wookie_config.datasets["fitterkpi2011"]["lumi"],
  #'normScale': 1.0,
  'normEvents': [30800.,210.],
  #'normEvents': [(wookie_config.datasets["fitterkpi2011"]["lumi"]+wookie_config.datasets["fitterkpi2012"]["lumi"])/wookie_config.datasets["fitteremu2011unblind"]["lumi"]*30800.,1.2*sqrt((wookie_config.datasets["fitterkpi2011"]["lumi"]+wookie_config.datasets["fitterkpi2012"]["lumi"])/wookie_config.datasets["fitteremu2011unblind"]["lumi"])],
  'normConstrained': False,
  'removeNorm': False,

  'toyScale': (wookie_config.datasets["fitterkpi2011"]["lumi"]+wookie_config.datasets["fitterkpi2012"]["lumi"])/wookie_config.datasets["fitteremu2011unblind"]["lumi"],

  'doFit': True,
  'loadFit': False,
  #'loadFit': not doFit,
  'doNlls': True,
  'doSPlot': False,
  'doBinned': False,
  'doBinnedNll': False,
  'doProfile': False,
  'doPlots': True,
  'doLimits': False,
  'visError': False,
  'doGof': False,
  'doPlotsAsymLong': False,
  'partialNlls': False,

  #'cutStr': "RAND<0.1",
  #'cutStr': "",

  'binScale': 1.,

  'niceness': 3,

  'splot_vars': ['Norm_N_Sig'],
  #'splot_out_file': wookie_config.datasets["splotkpi2011"]["file"],

  "doTree": False,
  "treeFile": "fitResultsTree.%s.%s_%s_%s.root"%(systName,str(args.PIDeCut),str(args.PIDmuCut),str(args.seed)),
  'kinitCheck': True,
  'postHook': defaultPostHook


}


sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT
from ROOT import RooStats

from ROOT import TStopwatch, TFile, RooFit, RooAbsData, RooDataSet, RooDataHist
from ROOT import RooCategory, RooArgSet, RooMsgService, RooCmdArg, RooLinkedList
from ROOT import RooRandom, RooArgList, TCanvas, TTree


timers = {
  "startup":TStopwatch(),
  "fitting":TStopwatch(),
  "plotting":TStopwatch(),
  "limits":TStopwatch(),
  "splot":TStopwatch(),
  "nlls":TStopwatch(),
  "profile":TStopwatch(),
  "gof":TStopwatch(),
  "tree":TStopwatch(),
  "total":TStopwatch()
  }
timers["total"].Start()
timers["startup"].Start()

pipi_eff = {2:{}, 4:{}, 6:{}, 8:{} ,10:{}}
emu_eff  = {2:{}, 4:{}, 6:{}, 8:{}, 10:{}}

pipi_eff[2][0.2]  = [13.16, 0.73]
pipi_eff[4][0.2]  = [4.47, 0.25]
pipi_eff[6][0.2]  = [1.097, 0.064]
pipi_eff[8][0.2]  = [0.1305, 0.0077]
pipi_eff[10][0.2] = [0.0090, 0.0010]
pipi_eff[2][0.4]  = [11.41, 0.73]
pipi_eff[4][0.4]  = [3.88, 0.25]
pipi_eff[6][0.4]  = [0.952, 0.064]
pipi_eff[8][0.4]  = [0.1140, 0.0077]
pipi_eff[10][0.4] = [0.00805, 0.00100]
pipi_eff[2][0.6]  = [9.25, 0.73]
pipi_eff[4][0.6]  = [3.15, 0.25]
pipi_eff[6][0.6]  = [0.774, 0.064]
pipi_eff[8][0.6]  = [0.0930, 0.0077]
pipi_eff[10][0.6] = [0.00656, 0.00094]
pipi_eff[2][0.8]  = [6.0389, 0.0081]
pipi_eff[4][0.8]  = [2.0623, 0.0033]
pipi_eff[6][0.8]  = [0.5095, 0.0013]
pipi_eff[8][0.8]  = [0.06170, 0.00061]
pipi_eff[10][0.8] = [0.00436, 0.00037]

emu_eff[2][0.2]  = [sum(i)/2. for i in zip([93.035, 0.032],[92.797, 0.039])]
emu_eff[4][0.2]  = [sum(i)/2. for i in zip([81.400, 0.051],[80.259, 0.061])]
emu_eff[6][0.2]  = [sum(i)/2. for i in zip([58.407, 0.064],[57.661, 0.075])]
emu_eff[8][0.2]  = [sum(i)/2. for i in zip([31.795, 0.059],[31.126, 0.066])]
emu_eff[10][0.2] = [sum(i)/2. for i in zip([12.998, 0.040],[13.216, 0.047])]
emu_eff[2][0.4]  = [sum(i)/2. for i in zip([89.761, 0.031],[89.551, 0.038])]
emu_eff[4][0.4]  = [sum(i)/2. for i in zip([78.547, 0.050],[77.474, 0.059])]
emu_eff[6][0.4]  = [sum(i)/2. for i in zip([56.383, 0.062],[55.677, 0.072])]
emu_eff[8][0.4]  = [sum(i)/2. for i in zip([30.711, 0.057],[30.077, 0.064])]
emu_eff[10][0.4] = [sum(i)/2. for i in zip([12.570, 0.039],[12.780, 0.045])]
emu_eff[2][0.6]  = [sum(i)/2. for i in zip([81.663, 0.029],[81.505, 0.035])]
emu_eff[4][0.6]  = [sum(i)/2. for i in zip([71.487, 0.045],[70.564, 0.054])]
emu_eff[6][0.6]  = [sum(i)/2. for i in zip([51.366, 0.056],[50.750, 0.066])]
emu_eff[8][0.6]  = [sum(i)/2. for i in zip([28.021, 0.052],[27.465, 0.058])]
emu_eff[10][0.6] = [sum(i)/2. for i in zip([11.500, 0.036],[11.692, 0.042])]
emu_eff[2][0.8]  = [sum(i)/2. for i in zip([61.334, 0.023],[61.149, 0.027])]
emu_eff[4][0.8]  = [sum(i)/2. for i in zip([53.744, 0.036],[53.047, 0.042])]
emu_eff[6][0.8]  = [sum(i)/2. for i in zip([38.719, 0.044],[38.228, 0.051])]
emu_eff[8][0.8]  = [sum(i)/2. for i in zip([21.201, 0.041],[20.781, 0.046])]
emu_eff[10][0.8] = [sum(i)/2. for i in zip([8.760,  0.028],[8.888, 0.033])]

config["emuEff"] *= emu_eff[config["emuEPidCut"]][config["emuMuPidCut"]][0]/100.
config["pipiAsEmuEff"] *= pipi_eff[config["emuEPidCut"]][config["emuMuPidCut"]][0]/100.


print "emuMuPidCut:", config["emuMuPidCut"], "emuEPidCut:", config["emuEPidCut"]
print "emuEff:", config['emuEff'], "pipiAsEmuEff:", config['pipiAsEmuEff']
print "ratio:", config['pipiAsEmuEff']*config['pipiBR'][0]/config['kpiBR'][0]/config['kpiEff']

exec("import syst_"+systName+" as syst")

for k,v in syst.config.iteritems():
  config[k] = v


doKinitCheck = config["kinitCheck"]
hostProc = subprocess.Popen(["hostname"],stdout=subprocess.PIPE)
hostOut = hostProc.stdout.readlines()
for line in hostOut:
  if "blackbook" in line:
    doKinitCheck = False
  elif "rigel" in line:
    doKinitCheck = False
hostProc.poll()

timeStr = False
if doKinitCheck:
  tocProc = subprocess.Popen(["tokens"],stdout=subprocess.PIPE)
  tocOut = tocProc.stdout.readlines()
  for line in tocOut:
    if "afs@cern.ch" in line and "[Expires " in line:
      timeStr = line.strip()[9+line.find("[Expires "):-1]

  if timeStr:
    now = datetime.datetime.today()
    tleft = datetime.datetime.strptime(timeStr+" "+str(now.year),"%b %d %H:%M %Y") - now
    if tleft < datetime.timedelta(0,1*3600):
      sys.exit("need longer afs token, run kinit")
    elif tleft < datetime.timedelta(0,12*3600):
      print ""
      print "----------------------------------------------------"
      print "WARNING: Will soon need longer afs token, run kinit!"
      print "----------------------------------------------------"
      print ""
  else:
    sys.exit("need longer afs token, run kinit")

  tocProc.poll()

try:
  from wookie.fitter.variableUtils import *
  import wookie.fitter.integral as pdfIntegrator
  import wookie.fitter.fullPdf as pdf
except ImportError:
  from variableUtils import *
  import integral as pdfIntegrator
  import fullPdf as pdf



w = pdf.setup_workspace(config)

D0_Mass = w.obj("D0_Mass")
Del_Mass = w.obj("Del_Mass")
Final_PDF = w.obj("Final_PDF")
if config["normConstrained"]:
  Final_PDF = Final_PDF = w.obj("Final_PDF_Constrained")
  

if config["normConstrained"]:
  w.obj("Norm_N_Sig").setVal(config["normEvents"][0])
  w.obj("Norm_N_Sig").setError(config["normEvents"][1])

#for component, lineColour, lineStyle, fillColour, fillStyle, lineWidth in componantColours:
componantColours = [
    #["BDT1_Sig,BDT2_Sig,BDT3_Sig,Norm_Sig", 16, ROOT.kSolid,16,1001],
    ["BDT1_Sig,BDT2_Sig,BDT3_Sig,Norm_Sig", 16, ROOT.kSolid, 16],
    #["BDT1_D0M_Sig_CB1,BDT2_D0M_Sig_CB1,BDT3_D0M_Sig_CB1", ROOT.kBlue+2],
    #["BDT1_D0M_Sig_CB2,BDT2_D0M_Sig_CB2,BDT3_D0M_Sig_CB2", ROOT.kBlue+4],
    ["BDT1_Comb,BDT2_Comb,BDT3_Comb_Blind,Norm_Comb", 14, 7],
    ["Norm_Prompt", ROOT.kRed+4, 4],
    ["BDT1_PiPi,BDT2_PiPi,BDT3_PiPi", ROOT.kMagenta+2, ROOT.kSolid,0,0,1],
    #["Norm_MisId", ROOT.kMagenta+2, ROOT.kSolid,0,0,1],
    ["Norm_MisRecod", ROOT.kGreen+4],
    #["Norm_MisId_Prompt", ROOT.kGreen+4],
    #["D0M_Bkg_Poly", ROOT.kGreen+2],
    ["*", ROOT.kBlue]
  ]





checkVarRanges(w)
printVarLimits(w)
printSetVarLimits(w)
#printSetVarConst(w)
checkVarLimits(w)

print '{:<12}'.format('doFit:')+'{:<12}'.format(str(config['doFit']))+'{:<18}'.format('loadFit:')+'{:<12}'.format((loadFileName if config['loadFit'] else "False"))
print '{:<12}'.format('doPlots:')+'{:<12}'.format(str(config['doPlots']))+'{:<18}'.format('visError:')+'{:<12}'.format(str(config['visError']))
print '{:<12}'.format('doNlls:')+'{:<12}'.format(str(config['doNlls']))+'{:<18}'.format('partialNlls:')+'{:<12}'.format(str(config['partialNlls']))
print '{:<12}'.format('doBinned:')+'{:<12}'.format(str(config['doBinned']))+'{:<18}'.format('doBinnedNll:')+'{:<12}'.format(str(config['doBinnedNll']))
print '{:<12}'.format('doGof:')+'{:<12}'.format(str(config['doGof']))+'{:<18}'.format('doPlotsAsymLong:')+'{:<12}'.format(str(config['doPlotsAsymLong']))
print '{:<12}'.format('doLimits:')+'{:<12}'.format(str(config['doLimits']))+'{:<18}'.format('doSPlot:')+'{:<12}'.format(str(config['doSPlot']))
print '{:<12}'.format('doProfile:')+'{:<12}'.format(str(config['doProfile']))
print ''


print "Norm Scale  {:<10.5f}".format(config["normScale"])
print "Norm events",config["normEvents"]
print "N PiPi      1: {:<10.5f}2: {:<10.5f}3: {:<10.5f}".format(w.obj("BDT1_N_PiPi").getVal(), w.obj("BDT2_N_PiPi").getVal(), w.obj("BDT3_N_PiPi").getVal())
print ""


toyRatio = 1.
#if config['mode'] is "toy":
  #side = pdfIntegrator.calculate(w.obj("BDT_D0M_Bkg"),RooArgSet(w.obj("D0_Mass")))
  #sideBlind = pdfIntegrator.calculate(w.obj("BDT_D0M_Bkg"),RooArgSet(w.obj("D0_Mass")),"blinded")
  #toyRatio = side/sideBlind
  #print "emu background integrals:",(toyRatio,side,sideBlind)

if "norm" not in config["mode"]:
  mvaFile = TFile(config['mvaFile'],"OPEN")
  mvaTree = mvaFile.Get("subTree")
  # old bdt region - 0.455 - 0.613 -
  bdt1UnbDataSet = RooDataSet("bdt1UnbDataSet", "bdt1UnbDataSet", mvaTree, w.set("argsPreCut"), "BDT_ada<0.07 && Del_Mass>139.4 && D0_Mass > 1815 && D0_Mass < 1915 && x1_PIDe>%f && x2_ProbNNmu>%f"%(config["emuEPidCut"],config["emuMuPidCut"]))
  bdt1UnbDataSet.Print()
  bdt2UnbDataSet = RooDataSet("bdt2UnbDataSet", "bdt2UnbDataSet", mvaTree, w.set("argsPreCut"), "BDT_ada>0.07 && BDT_ada<0.49 && Del_Mass>139.4 && D0_Mass > 1815 && D0_Mass < 1915 && x1_PIDe>%f && x2_ProbNNmu>%f"%(config["emuEPidCut"],config["emuMuPidCut"]))
  bdt2UnbDataSet.Print()
  bdt3UnbDataSet = RooDataSet("bdt3UnbDataSet", "bdt3UnbDataSet", mvaTree, w.set("argsPreCut"), "BDT_ada>0.49 && Del_Mass>139.4 && D0_Mass > 1815 && D0_Mass < 1915 && x1_PIDe>%f && x2_ProbNNmu>%f"%(config["emuEPidCut"],config["emuMuPidCut"]))
  bdt3UnbDataSet.Print()

  bdt1UnbPruneDataSet = RooDataSet("bdt1UnbPruneDataSet", "bdt1UnbPruneDataSet", bdt1UnbDataSet, w.set("argsBasic"), "")
  bdt1UnbPruneDataSet.Print()
  bdt2UnbPruneDataSet = RooDataSet("bdt2UnbPruneDataSet", "bdt2UnbPruneDataSet", bdt2UnbDataSet, w.set("argsBasic"), "")
  bdt2UnbPruneDataSet.Print()
  bdt3UnbPruneDataSet = RooDataSet("bdt3UnbPruneDataSet", "bdt3UnbPruneDataSet", bdt3UnbDataSet, w.set("argsBasic"), "")
  bdt3UnbPruneDataSet.Print()

if config['mode'] in ["mcnorm", "norm", "data"]:
  if config['norm'] is 'pipi':
    pipiFile = TFile(config['pipiFile'],"OPEN")
    normTree = pipiFile.Get("subTree")

    pipiUnbDataSet = RooDataSet("pipiUnbDataSet", "pipiUnbDataSet", normTree, w.set("argsPreCutNorm"), "Del_Mass>139.4 && RAND < %f" % (config["normScale"]))
    pipiUnbDataSet.Print()

    pipiUnbPruneDataSet = RooDataSet("pipiUnbPruneDataSet", "pipiUnbPruneDataSet", pipiUnbDataSet, w.set("argsBasic"), "D0_Mass>1826 && D0_Mass<1920")
    pipiUnbPruneDataSet.Print()
  elif config['norm'] is 'kpi':
    pipiFile = TFile(config['kpiFile'],"OPEN")
    normTree = pipiFile.Get("subTree")

    pipiUnbDataSet = RooDataSet("pipiUnbDataSet", "pipiUnbDataSet", normTree, w.set("argsPreCutKPi"), "Del_Mass>139.4 && RAND < %f" % (config["normScale"]))
    pipiUnbDataSet.Print()

    #pipiUnbPruneDataSet = RooDataSet("pipiUnbPruneDataSet", "pipiUnbPruneDataSet", pipiUnbDataSet, w.set("argsBasic"), "D0_Mass>1800 && D0_Mass<1920")
    pipiUnbPruneDataSet = RooDataSet("pipiUnbPruneDataSet", "pipiUnbPruneDataSet", pipiUnbDataSet, w.set("argsBasic"))
    pipiUnbPruneDataSet.Print()


if config['mode'] is "toy":
  print "Setting random seed to", args.seed
  RooRandom.randomGenerator().SetSeed(args.seed)
  print "Generating dataset 1 ..."
  bdt1UnbToyDataSet = w.obj("BDT1_Comb").generate(
      w.set("argsBasic"),
      RooFit.NumEvents( RooRandom.randomGenerator().Poisson(config['toyScale']*(bdt1UnbPruneDataSet.numEntries())-w.obj("BDT1_N_PiPi").getVal()) )
    )
  bdt1UnbToyDataSet.Print()
  bdt1UnbToyDataSet.append( w.obj("BDT1_PiPi").generate(  w.set("argsBasic"),
                                                          RooFit.NumEvents(RooRandom.randomGenerator().Poisson(w.obj("BDT1_N_PiPi").getVal()))
                                                          ) )
  bdt1UnbToyDataSet.Print()
  print "Generating dataset 2 ..."
  bdt2UnbToyDataSet = w.obj("BDT2_Comb").generate(
      w.set("argsBasic"),
      RooFit.NumEvents( RooRandom.randomGenerator().Poisson(config['toyScale']*(bdt2UnbPruneDataSet.numEntries())-w.obj("BDT2_N_PiPi").getVal()) )
    )
  bdt2UnbToyDataSet.Print()
  bdt2UnbToyDataSet.append( w.obj("BDT2_PiPi").generate(  w.set("argsBasic"),
                                                          RooFit.NumEvents(RooRandom.randomGenerator().Poisson(w.obj("BDT2_N_PiPi").getVal()))
                                                          ) )
  bdt2UnbToyDataSet.Print()
  print "Generating dataset 3 ..."
  bdt3UnbToyDataSet = w.obj("BDT3_Comb").generate(
      w.set("argsBasic"),
      RooFit.NumEvents( RooRandom.randomGenerator().Poisson(config['toyScale']*(bdt3UnbPruneDataSet.numEntries())-w.obj("BDT3_N_PiPi").getVal()) )
    )
  bdt3UnbToyDataSet.Print()
  bdt3UnbToyDataSet.append( w.obj("BDT3_PiPi").generate(  w.set("argsBasic"),
                                                          RooFit.NumEvents( RooRandom.randomGenerator().Poisson(w.obj("BDT3_N_PiPi").getVal()) )
                                                          ) )
  bdt3UnbToyDataSet.Print()

  fullUnbDataSet = RooDataSet("fullUnbDataSet",
                              "fullUnbDataSet",
                              w.set("argsBasic"),
                              RooFit.Index(w.cat("DataSet")),
                              RooFit.Import("BDT1",bdt1UnbToyDataSet),
                              RooFit.Import("BDT2",bdt2UnbToyDataSet),
                              RooFit.Import("BDT3",bdt3UnbToyDataSet)
                              #,RooFit.Import("Norm",pipiUnbPruneDataSet)
                              )
  fullUnbDataSet.Print()



if config['mode'] is "data":
  if config["normConstrained"]:
    fullUnbDataSet = RooDataSet("fullUnbDataSet",
                                "fullUnbDataSet",
                                w.set("argsBasic"),
                                RooFit.Index(w.cat("DataSet")),
                                RooFit.Import("BDT1",bdt1UnbPruneDataSet),
                                RooFit.Import("BDT2",bdt2UnbPruneDataSet),
                                RooFit.Import("BDT3",bdt3UnbPruneDataSet)
                                )
  else:
    fullUnbDataSet = RooDataSet("fullUnbDataSet",
                                "fullUnbDataSet",
                                w.set("argsBasic"),
                                RooFit.Index(w.cat("DataSet")),
                                RooFit.Import("BDT1",bdt1UnbPruneDataSet),
                                RooFit.Import("BDT2",bdt2UnbPruneDataSet),
                                RooFit.Import("BDT3",bdt3UnbPruneDataSet),
                                RooFit.Import("Norm",pipiUnbPruneDataSet)
                                )

if "norm" in config['mode']:
  fullUnbDataSet = RooDataSet("fullUnbDataSet",
                              "fullUnbDataSet",
                              w.set("argsBasic"),
                              RooFit.Index(w.cat("DataSet")),
                              RooFit.Import("Norm",pipiUnbPruneDataSet))





if config['mode'] in ["mc", "mcpipi", "datapretoy"]:
  bdtEvents = []
  for ds in [bdt1UnbPruneDataSet,bdt2UnbPruneDataSet,bdt3UnbPruneDataSet]:
    bdtEvents.append(float(ds.numEntries()))
  for var,value in [("BDT1_Sig_Eff",bdtEvents[0]/sum(bdtEvents)),("BDT2_Sig_Eff",bdtEvents[1]/sum(bdtEvents))]:
    print "w.obj('"+var+"').setVal("+str(value)+") ; w.obj('"+var+"').setConstant(True)"

  fullUnbDataSet = RooDataSet("fullUnbDataSet",
                              "fullUnbDataSet",
                              w.set("argsBasic"),
                              RooFit.Index(w.cat("DataSet")),
                              RooFit.Import("BDT1",bdt1UnbPruneDataSet),
                              RooFit.Import("BDT2",bdt2UnbPruneDataSet),
                              RooFit.Import("BDT3",bdt3UnbPruneDataSet))



fullUnbDataSet.Print()


if "norm" not in config['mode']:
  bdt1UnbDataSet.Delete()
  bdt2UnbDataSet.Delete()
  bdt3UnbDataSet.Delete()
  bdt1UnbPruneDataSet.Delete()
  bdt2UnbPruneDataSet.Delete()
  bdt3UnbPruneDataSet.Delete()
  mvaFile.Close()

if config['mode'] == "data":
  pipiUnbDataSet.Delete()
  pipiUnbPruneDataSet.Delete()
  pipiFile.Close()

if config['mode'] == "toy":
  bdt1UnbToyDataSet.Delete()
  bdt2UnbToyDataSet.Delete()
  bdt3UnbToyDataSet.Delete()

binnedDataSet = False
fullDataSet = False
highResDataSet = False

fullDataSet = RooDataHist("fullDataSet","fullDataSet",w.set("args"),fullUnbDataSet)
fullDataSet.Print()










print "Dataset imported to workspace"

ds = fullDataSet

timers["startup"].Stop()
timers["startup"].Print()

timers["fitting"].Start()

Final_PDF.Print()
print "Simultaneous PDF?", (Final_PDF.ClassName() == "RooSimultaneous")

print "To MINUIT! Fitting to %s::%s in mode %s at %s, saving result in %s" % (Final_PDF.ClassName(), Final_PDF.GetName(), config['mode'],datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"), config['outFileName'])

r=False
if config['doFit']:
  constrainedArg = RooCmdArg.none()
  if config["normConstrained"]:
    constrainedArg = RooFit.Constrain(RooArgSet(w.obj("Norm_N_Sig")))
  if config['doBinned']:
    #r=Final_PDF.fitTo(fullDataSet,RooFit.Save(),RooFit.NumCPU(nCPUs,True),RooFit.Timer(True),RooFit.PrintEvalErrors(1),RooFit.Minimizer("Minuit2", "Migrad"))
    #r=Final_PDF.fitTo(fullDataSet,RooFit.Save(),RooFit.NumCPU(nCPUs,1),RooFit.Timer(True),RooFit.PrintEvalErrors(1),RooFit.Optimize(0))
    r=Final_PDF.fitTo(fullDataSet,RooFit.Save(),RooFit.NumCPU(nCPUs,1),RooFit.Timer(True),RooFit.PrintEvalErrors(1),RooFit.Strategy(0),RooFit.Optimize(0),RooFit.Minimizer("Minuit2", "migrad"),constrainedArg)
    #r=Final_PDF.fitTo(fullDataSet,RooFit.Save(),RooFit.NumCPU(nCPUs,1),RooFit.Timer(True),RooFit.PrintEvalErrors(1),RooFit.Strategy(2),RooFit.Optimize(0))
  else:
    #r=Final_PDF.fitTo(fullUnbDataSet,RooFit.Save(),RooFit.NumCPU(nCPUs,True),RooFit.Timer(True),RooFit.PrintEvalErrors(1),RooFit.Minimizer("Minuit2", "Migrad"))
    r=Final_PDF.fitTo(fullUnbDataSet,RooFit.Save(),RooFit.NumCPU(nCPUs,1),RooFit.Timer(True),RooFit.PrintEvalErrors(1),RooFit.Strategy(0),RooFit.Optimize(0),RooFit.Minimizer("Minuit2", "migrad"),constrainedArg)
    #r=Final_PDF.fitTo(fullUnbDataSet,RooFit.Save(),RooFit.NumCPU(nCPUs,1),RooFit.Timer(True),RooFit.PrintEvalErrors(1),RooFit.Strategy(2),RooFit.Optimize(0))
  r.SetName("RooFitResults")
  getattr(w, 'import')(r)
elif config['loadFit']:
  fitResultsFile = TFile.Open(loadFileName,"OPEN")
  r = fitResultsFile.Get("RooFitResults")
  fitResultsFile.Close()

RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)


if r:
  finalPars = r.floatParsFinal()
  it=finalPars.createIterator()
  while True:
    var = it.Next()
    if not var:
      print "End of variables"
      break
    else:
      w.obj(var.GetName()).setVal(var.getVal())
      w.obj(var.GetName()).setError(var.getError())

  printTexRes(r)
  #print "Minimum value of NLL:", r.minNll()

  initPars = r.floatParsInit()
  iterI=initPars.createIterator()
  iterF=finalPars.createIterator()
  ret = []
  while True:
    varI = iterI.Next()
    varF = iterF.Next()
    if not varI or not varF:
      print "End of variables"
      break
    else:
      if varI.getVal() == varF.getVal():
        ret.append(varI.GetName() + "'s final value of "+str(varF.getVal())+" is the same as it's initial value!")
  
  checkVarChange(r)

printSetVarLimits(w)
checkTitles(w)
checkVarLimits(w)
if r:
  r.Print()
sys.stdout.flush()

timers["fitting"].Stop()
timers["fitting"].Print()

timers["plotting"].Start()

#w.obj("D_DMASS_Ds").setBins(100)
#w.obj("B_CORTAU").setBins(int(round(100*maxtau/5.)))
#lowResDataSet = RooDataHist("lowResDataSet","lowResDataSet",w.set("args"),fullUnbDataSet)
#lowResDataSet.Print()


colours = [ROOT.kBlack, ROOT.kBlue]
coloursAsym = [ROOT.kBlack, ROOT.kBlue]

for index, default in [[2, ROOT.kSolid],[3,0],[4,0],[5,3]]:
  for componentItem in componantColours:
    try:
      componentItem[index]
    except IndexError:
      if len(componentItem) == index:
        componentItem.append(default)

simultaneousFit = (Final_PDF.ClassName() == "RooSimultaneous")

def largePlotOn(pdf,frame,*args):
  l = RooLinkedList()
  for arg in args:
    l.Add(arg)
  pdf.plotOn(frame,l)

def ueberPlot(w,plotName,plotVar,cpus,mixState,massCat,cut,dataArr,varMax=-1,asym=False,numBins=False):
  frame = False
  if numBins!=False:
    frame = plotVar.frame(plotVar.getMin(),varMax if varMax != -1 else plotVar.getMax(),numBins)
  else:
    frame = plotVar.frame(plotVar.getMin(),varMax if varMax != -1 else plotVar.getMax())
  dsName = "dsBinnedMassCat-"+cut
  dataRedArr = []
  i=0
  for data in dataArr:
    dataRedArr.append((getattr(data,"reduce")(RooFit.CutRange(cut)),i))
    i += 1

  visRooCmdArg = RooCmdArg.none()
  if config['visError'] and (config['doFit'] or config['loadFit']):
    if r.covQual() == 3:
      visRooCmdArg = RooFit.VisualizeError(r)

  if massCat != "":
    massCat = massCat + "_"

  asymVar = asym
  if mixState == "":
    oscSlice = RooCmdArg.none()
  elif mixState == "Mixed":
    oscSlice = RooFit.Slice(B0_OSCIL,"Oscil")
  elif mixState == "Unmixed":
    oscSlice = RooFit.Slice(B0_OSCIL,"NonOscil")
  #elif mixState == "Pos":
    #oscSlice = RooFit.Slice(w.obj("Mu_CHARGE_CAT"),"positive")
  #elif mixState == "Neg":
    #oscSlice = RooFit.Slice(w.obj("Mu_CHARGE_CAT"),"negitive")

  if config["mode"] == "mc":
    pdfName = "Sig"
  elif config["mode"] == "mcnorm":
    pdfName = "Sig_NotExtend"
  elif config["mode"] == "mcpipi":
    pdfName = "PiPi"
  elif config["mode"] == "datapretoy":
    pdfName = "Comb_Blind"
  else:
    pdfName = "Final_PDF"

  if config["normConstrained"]:
    pdfName += "_Constrained"
  
  cpus = 1

  #dataB.Print()
  if not asym:
    print "Plotting:" ,plotName
    sys.stdout.flush()
    for data,icolour in dataRedArr:
      binning = ROOT.RooCmdArg.none()
      if bins != False:
        binning = RooFit.Binning(bins, frame.GetMinimum(), frame.GetMaximum())
      data.plotOn(frame, RooFit.MarkerColor(colours[icolour]), RooFit.MarkerSize(0.8))
    #for component, lineColour in [ ["*TM_Side1", ROOT.kRed], ["*TM_Side2", ROOT.kGreen], ["*TM_Peak_*", ROOT.kOrange], ["*TM_Sig_Bs", ROOT.kMagenta], ["*TM_Sig_Bd,*TM_Sig_Bd_in_Bs", ROOT.kMagenta+2], ["*TM_Bplus*",ROOT.kGray+1], ["*TM_Sig_BdDStar", ROOT.kCyan], ["*", ROOT.kBlue] ]:
    for component, lineColour, lineStyle, fillColour, fillStyle, lineWidth in componantColours:
      arguments = RooLinkedList()
      for arg in [RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.LineWidth(lineWidth), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.Precision(1e-4)]:
        arguments.Add(arg)
      if fillStyle != 0:
        arguments.Add(RooFit.DrawOption("F"))
      if mixState == "Mixed":
        arguments.Add(RooFit.Slice(B0_OSCIL,"Oscil"))
      elif mixState == "Unmixed":
        arguments.Add(RooFit.Slice(B0_OSCIL,"NonOscil"))
      if config['visError'] and (config['doFit'] or config['loadFit']):
        if r.covQual() == 3:
          arguments.Add(RooFit.VisualizeError(r))
      #print("+")
      if massCat == "":
        dataB = RooDataHist(dsName, dsName, RooArgSet(w.obj("DataSet")), dataRedArr[-1][0], 1.0)
        arguments.Add(RooFit.ProjWData(dataB))
        #arguments.Add(RooFit.NumCPU(nCPUs,kTRUE))
        if cut != "":
          arguments.Add(RooFit.ProjectionRange(cut))
          arguments.Add(RooFit.NormRange(cut))
          #largePlotOn(TM_Total, frame, RooFit.ProjectionRange(cut), RooFit.NormRange(cut), RooFit.ProjWData(dataB), RooFit.NumCPU(nCPUs,kTRUE), RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.Precision(1e-4), visRooCmdArg, oscSlice)
          #TM_Total.plotOn(frame, RooFit.ProjectionRange(cut), RooFit.NormRange(cut), RooFit.ProjWData(dataB), RooFit.NumCPU(nCPUs,kTRUE), RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.DrawOption("F"), RooFit.Precision(1e-4), visRooCmdArg, oscSlice) #12 args
          Final_PDF.plotOn(frame, arguments)
        else:
          #TM_Total.plotOn(frame, RooFit.ProjWData(dataB), RooFit.NumCPU(nCPUs,kTRUE), RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.Precision(1e-4), visRooCmdArg, oscSlice) #10 args
          Final_PDF.plotOn(frame, arguments)
        dataB.Delete()
      else:
        if config['visError'] and (config['doFit'] or config['loadFit']):
          if r.covQual() == 3:
            arguments.Add(RooFit.VisualizeError(r))
        if cut != "":
          arguments.Add(RooFit.ProjectionRange(cut))
          arguments.Add(RooFit.NormRange(cut))
          #w.obj(massCat+"Final_PDF").plotOn(frame, RooFit.ProjectionRange(cut), RooFit.NormRange(cut), RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.Precision(1e-4), visRooCmdArg, oscSlice) #10 args
          w.obj(massCat+pdfName).plotOn(frame, arguments)
        else:
          #w.obj(massCat+"Final_PDF").plotOn(frame, RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.Precision(1e-4), visRooCmdArg, oscSlice) #8 args
          w.obj(massCat+pdfName).plotOn(frame, arguments)
    for data,icolour in dataRedArr:
      data.plotOn(frame, RooFit.MarkerColor(colours[icolour]), RooFit.MarkerSize(0.8))
  else: # its an asym plot
    print "Plotting:" ,plotName
    sys.stdout.flush()
    timeThisBit = TStopwatch()
    timeThisBit.Start()
    for data,icolour in dataRedArr:
      data.plotOn(frame, RooFit.Asymmetry(asymVar), RooFit.MarkerColor(coloursAsym[icolour]),RooFit.Binning(numBins))
    arguments = RooLinkedList()
    for arg in [RooFit.Asymmetry(asymVar), RooFit.LineColor(ROOT.kRed), RooFit.Precision(1e-4)]:
      arguments.Add(arg)
    if massCat == "":
      dataB = RooDataHist(dsName, dsName, RooArgSet(w.obj("DataSet")), dataRedArr[-1][0], 1.0)
      dataB.Print()
      print "nCPUs:",nCPUs
      if visRooCmdArg != RooCmdArg.none():
        print "Ignoring the visualise errors command when creating asymmetry plots over multiple categories"
      if cut != "":
        arguments.Add(RooFit.ProjectionRange(cut))
        arguments.Add(RooFit.NormRange(cut))
        arguments.Add(RooFit.ProjWData(dataB))
        #TM_Total.plotOn(frame, RooFit.Asymmetry(asymVar), RooFit.ProjectionRange(cut), RooFit.NormRange(cut), RooFit.ProjWData(dataB), RooFit.NumCPU(nCPUs,kTRUE), RooFit.LineColor(ROOT.kRed), RooFit.Precision(1e-4))
        Final_PDF.plotOn(frame, arguments)
      else:
        #TM_Total.plotOn(frame, RooFit.Asymmetry(asymVar), RooFit.ProjWData(dataB), RooFit.NumCPU(nCPUs,kTRUE), RooFit.LineColor(ROOT.kRed), RooFit.Precision(1e-4))
        Final_PDF.plotOn(frame, arguments)
      dataB.Delete()
    else:
      if cut != "":
        arguments.Add(RooFit.ProjectionRange(cut))
        arguments.Add(RooFit.NormRange(cut))
        #w.obj(massCat+"Final_PDF").plotOn(frame, RooFit.Asymmetry(asymVar), RooFit.ProjectionRange(cut), RooFit.NormRange(cut), RooFit.NumCPU(1), RooFit.LineColor(ROOT.kRed), RooFit.Precision(1e-4), visRooCmdArg)
        w.obj(massCat+pdfName).plotOn(frame, arguments)
      else:
        #w.obj(massCat+"Final_PDF").plotOn(frame, RooFit.Asymmetry(asymVar), RooFit.NumCPU(1), RooFit.LineColor(ROOT.kRed), RooFit.Precision(1e-4), visRooCmdArg)
        w.obj(massCat+pdfName).plotOn(frame, arguments)
    frame.SetAxisRange(-.4,.4,"y")
    timeThisBit.Stop()
    timeThisBit.Print()
  for data,icolour in dataRedArr:
    data.Delete()
  sys.stdout.flush()
  return frame

def plotData(var,data):
  print "Plotting: Data_"+var+"_"+data.GetName()
  frame = w.obj(var).frame()
  data.plotOn(frame)
  return ["Data_"+var+"_"+data.GetName(),frame]

from multiprocessing import Process, Queue

def makePlotArray(q,w,plotName,plotVar,cpus,mixState,massCat,cut,dataArr,varMax=-1,asym=False,numBins=False):
  os.nice(config['niceness'])
  plot = [plotName,ueberPlot(w,plotName,plotVar,cpus,mixState,massCat,cut,dataArr,varMax,asym,numBins)]
  histNameSuffix = "" if asym == False else "_Asym["+asym.GetName()+"]"
  #plot[1].Print("v")
  q.put([plot,
         [plotName+"_Pull",plot[1].pullHist("h_"+dataArr[-1].GetName()+histNameSuffix)]])


timePlots = []

queueList = []
processList = []

if config['doPlots']:

  #w.obj("D_DMASS_Ds").setBins(massBinning.numBins())
  #w.obj("B_CORTAU").setBins(tauBinning.numBins())
  binnedDataSet = RooDataHist("binnedDataSet","binnedDataSet",w.set("args"),fullUnbDataSet)
  binnedDataSet.Print()
  ##getattr(w,"import")(binnedDataSet)
  #w.obj("D_DMASS_Ds").setBins(100)
  #w.obj("B_CORTAU").setBins(int(round(maxtau*50./.12)))
  ##w.obj("B_CORTAU").setBinning(tauBinningHigZoom)
  ##w.obj("B_CORTAU").setMax(0.12)
  ##w.obj("B_CORTAU").setBins(int(round(2200*maxtau/5.)))
  ##w.obj("B_CORTAU").setBins(50)
  ##w.obj("B_CORTAU").setBinning(tauBinningHigZoom)
  ##highResDataSet = RooDataHist("highResDataSet","highResDataSet",w.set("args"),getattr(fullUnbDataSet,'reduce')('B_CORTAU<0.12'))
  #highResDataSet = RooDataHist("highResDataSet","highResDataSet",w.set("args"),fullUnbDataSet)
  #highResDataSet.Print()
  #w.obj("D_DMASS_Ds").setBins(100)
  #w.obj("B_CORTAU").setBins(int(round(maxtau*50./.5)))
  ##w.obj("B_CORTAU").setBinning(tauBinningMidZoom)
  ##w.obj("B_CORTAU").setMax(0.5)
  ##w.obj("B_CORTAU").setBins(int(round(400*maxtau/5.)))
  ##w.obj("B_CORTAU").setBins(50)
  ##midResDataSet = RooDataHist("midResDataSet","midResDataSet",w.set("args"),getattr(fullUnbDataSet,'reduce')('B_CORTAU<0.5'))
  #midResDataSet = RooDataHist("midResDataSet","midResDataSet",w.set("args"),fullUnbDataSet)
  #midResDataSet.Print()
  #w.obj("B_CORTAU").setMax(maxtau)

  timePlots = [plotData("D0_Mass",binnedDataSet),plotData("Del_Mass",binnedDataSet)]

  mixState = ""

  datacats = ['']
  if config['mode'] in ["data", "toy"]:
    datacats = ["BDT1","BDT2","BDT3"]
    if not config["normConstrained"]:
      datacat += ["Norm"]
  if config['mode'] == "norm":
    datacats = ["Norm"]
  if config['mode'] in ["mc", "mcpipi", "datapretoy"]:
    datacats = ["BDT1","BDT2","BDT3"]

  for datacat in (datacats if simultaneousFit else ['']):
    for dsN,data in [("FullData",[binnedDataSet])]:
      for dst_side in ["", "delhigh", "delsig", "dellow"]:
      #for dst_side in [""]:
        for d_side in [""]:
          cutName = datacat+dst_side+d_side
          bins = False if datacat == "Norm" else 25
          plotName = dsN + "_" + datacat + "_D0M_" + (dst_side if dst_side != "" else "delall") + "_" + (d_side if d_side != "" else "d0all")
          queueList.append(Queue())
          processList.append(Process(target=makePlotArray, args=(queueList[-1],w,plotName,w.obj("D0_Mass"),nCPUs,mixState,datacat,cutName,data,-1,False,bins)))

    for dsN,data in [("FullData",[binnedDataSet])]:
      for dst_side in [""]:
        for d_side in ["", "dhigh2", "dhigh1", "dhigh", "dsig", "dlow", "dlow1", "dlow2"]:
        #for d_side in [""]:
          cutName = datacat+dst_side+d_side
          bins = False if datacat == "Norm" else 25
          plotName = dsN + "_" + datacat + "_DelM_" + (dst_side if dst_side != "" else "delall") + "_" + (d_side if d_side != "" else "d0all")
          queueList.append(Queue())
          processList.append(Process(target=makePlotArray, args=(queueList[-1],w,plotName,w.obj("Del_Mass"),nCPUs,mixState,datacat,cutName,data,-1,False,bins)))

  startAt = 0
  if config['doPlotsAsymLong']:
    startAt = 2
    for i in range(startAt):
      #print "starting", i
      processList[i].start()

  minPlotNumber = startAt
  while len(processList) > minPlotNumber:
    threads = spareThreads = (nCPUs - startAt - 1) if (nCPUs - startAt - 1) > 0 else 1
    if len(processList) - minPlotNumber < spareThreads:
      threads = len(processList) - minPlotNumber
    for i in range(threads):
      #print "starting", i+minPlotNumber
      sys.stdout.flush()
      processList[i+minPlotNumber].start()
    for i in range(threads):
      #print "getting", i+minPlotNumber
      sys.stdout.flush()
      timePlots += queueList[i+minPlotNumber].get()
      #print "joining", i+minPlotNumber
      processList[i+minPlotNumber].join()
    minPlotNumber += threads

  #timePlots.sort()

  binnedDataSet.Delete()
  #highResDataSet.Delete()
  #midResDataSet.Delete()
  #lowResDataSet.Delete()

def nllPlot(var,dpll):
  nframe = var.frame(RooFit.Title("nll plot of " + var.GetName()))
  #arguments = RooLinkedList()
  #for arg in [RooFit.Precision(1e-4),RooFit.ShiftToZero(),RooFit.PrintEvalErrors(-1),RooFit.EvalErrorValue(nll.getVal()+10),RooFit.LineStyle(ROOT.kDashed)]:
    #arguments.Add(arg)
  #nll.plotOn(nframe,arguments)
  nll.plotOn(nframe,RooFit.Precision(1e-4),RooFit.ShiftToZero(),RooFit.PrintEvalErrors(-1),RooFit.EvalErrorValue(nll.getVal()+10),RooFit.LineStyle(ROOT.kDashed))
  #nll.plotOn(nframe,RooFit.Precision(1e-4),RooFit.ShiftToZero(),RooFit.PrintEvalErrors(-1),RooFit.EvalErrorValue(nll.getVal()+10),RooFit.LineStyle(ROOT.kDashed))
  #nll.plotOn(nframe,RooFit.Precision(1e-4),RooFit.ShiftToZero(),RooFit.PrintEvalErrors(-1),RooFit.EvalErrorValue(nll.getVal()+10),RooFit.LineStyle(ROOT.kSolid))
  #nframe.GetYaxis().SetRangeUser(0,2000)
  if dpll:
    pll = nll.createProfile(RooArgSet(var))
    pll.plotOn(nframe,RooFit.NumCPU(nCPUs,True),RooFit.PrintEvalErrors(-1))
    #nframe.SetTitle( "nll plot of " + var.GetName()) ;
    #ncanv=TCanvas("ncanv" + var.GetName() ,nframe.GetTitle(),800,600)
    #nframe.Draw()
  return nframe

def allNlls(cpus=10,mixedSignals=False):
  doPll = False
  varList = Final_PDF.getParameters(fullDataSet)

  it=varList.createIterator()
  out=[]
  while True:
    var = it.Next()
    if not var:
      print "End of variables"
      sys.stdout.flush()
      break
    if var.Class().GetName() == "RooCategory":
      print var.GetName(), "is a RooCategory, skipping"
      sys.stdout.flush()
      continue
    if var.isConstant():
      print var.GetName(), "is constant, skipping"
      sys.stdout.flush()
      continue
    if config['partialNlls'] != False:
      if not config['partialNlls'] in var.GetName():
        print var.GetName(), "doesn't have", config['partialNlls'], "in its name"
        continue
    print var.GetName(), "looks good calculating nll plot"
    sys.stdout.flush()
    np = nllPlot(var,doPll)
    out.append([var.GetName(),np])
    #nll_file = TFile.Open("nllPlots.root","UPDATE")
    #np.Write("NllOf_"+var.GetName())
    #nll_file.Close()

  return out



hcorr = False
if config['doFit'] or config['loadFit']:
  if r:
    hcorr = r.correlationHist()

print "Saving plots to file..."
sys.stdout.flush()
save_file = TFile.Open(config['outFileName'],"RECREATE")
save_file.cd()
for i in timePlots:
  if not i[1]:
    print "Plot ERROR!:", i
  else:
    i[1].Write(i[0])
if config['doFit'] or config['loadFit']:
  if r:
    hcorr.Write("CorrelationHist")
    r.Write("RooFitResults")
save_file.Close()
print "Plots saved"
sys.stdout.flush()

save_file = False

timers["plotting"].Stop()
timers["plotting"].Print()

timers["limits"].Start()

allVars = Final_PDF.getParameters(getattr(w,"set")("args"))
i = allVars.createIterator()
nuisPars = RooArgSet()
while True:
  var = i.Next()
  if not var:
    break
  if var.isConstant():
    continue
  if var.ClassName() == "RooCategory":
    continue
  nuisPars.add(var)

br_val = w.var("EMu_BR").getVal()
print "EMu_BR is", br_val

poiArgSet = RooArgSet(w.var("EMu_BR"))
globPars = RooArgSet(w.var("Norm_N_Sig"))

sbModel = RooStats.ModelConfig("ModelConfig", w)
sbModel.SetPdf(Final_PDF)
sbModel.SetParametersOfInterest(poiArgSet)
sbModel.SetObservables(getattr(w,"set")("args"))
sbModel.SetNuisanceParameters(nuisPars)
sbModel.SetGlobalObservables(globPars)
sbModel.SetSnapshot( poiArgSet )

bModel = sbModel.Clone("ModelConfig_BOnly")
w.var("EMu_BR").setVal(0.)
nullArgSet = RooArgSet(w.var("EMu_BR"))
bModel.SetSnapshot( nullArgSet )
w.var("EMu_BR").setVal(br_val)

limit_ac = -1
limit_pc = -1

if config['doLimits']:

  if config['doBinned']:
    data = fullDataSet
  else:
    data = fullUnbDataSet

  from ROOT import RooStats


  plh = RooStats.ProfileLikelihoodCalculator(data, Final_PDF, RooArgSet(w.var("EMu_BR")))

  #plh.SetConfidenceLevel(0.683)
  plh.SetConfidenceLevel(0.90)
  interval = plh.GetInterval()
  print "90% CL interval for EMu_BR:"
  print (interval.LowerLimit(w.var("EMu_BR")), interval.UpperLimit(w.var("EMu_BR")))
  print "#limits %.2f, %.2f, %.15f, %i, %i, %i" %(args.PIDeCut,args.PIDmuCut,interval.UpperLimit(w.var("EMu_BR")),r.statusCodeHistory(0),r.statusCodeHistory(1),r.covQual())

  limit_pc = interval.UpperLimit(w.var("EMu_BR"))

  ## Now for some significance testing
  ## background only model
  #asym_calc = ROOT.RooStats.AsymptoticCalculator(data, Final_PDF, w.obj("Final_PDF_Background"))
  #asym_calc.SetOneSidedDiscovery(True)
  #result = asym_calc.GetHypoTest()
  #result.Print()


  RooMsgService.instance().setGlobalKillBelow(RooFit.DEBUG)
  #RooMsgService.instance().addStream(RooFit.INFO,RooFit.Topic(32767))
  RooMsgService.instance().addStream(RooFit.INFO,RooFit.Topic(RooFit.Minimization + RooFit.Plotting + RooFit.Fitting + RooFit.LinkStateMgmt + RooFit.Eval + RooFit.Caching + RooFit.Optimization + RooFit.ObjectHandling + RooFit.InputArguments + RooFit.Tracing + RooFit.Contents + RooFit.DataHandling))
  RooMsgService.instance().Print()

  fc = RooStats.FrequentistCalculator(data, bModel, sbModel)
  fc.SetToys(500,500)

  #hc = RooStats.HybridCalculator(data, bModel, sbModel)
  #hc.SetToys(100,50)    # 1000 for null (S+B) , 50 for alt (B)
  #nuisPdf = RooStats.MakeNuisancePdf(sbModel,"nuisancePdf_sbmodel")
  #hc.ForcePriorNuisanceAlt(nuisPdf)
  #hc.ForcePriorNuisanceNull(nuisPdf)

  #ac = RooStats.AsymptoticCalculator(data, bModel, sbModel)
  #ac.SetOneSided(True)  # for one-side tests (limits)
  #RooStats.AsymptoticCalculator.SetPrintLevel(-1)

  calc = RooStats.HypoTestInverter(fc)
  calc.SetConfidenceLevel(0.90)
  calc.UseCLs(True)
  calc.SetVerbose(2)

  toymcs = calc.GetHypoTestCalculator().GetTestStatSampler()

  slrts = RooStats.SimpleLikelihoodRatioTestStat(bModel.GetPdf(),sbModel.GetPdf())
  slrts.SetNullParameters(bModel.GetSnapshot())
  slrts.SetAltParameters(sbModel.GetSnapshot())

  profll = RooStats.ProfileLikelihoodTestStat(sbModel.GetPdf())
  profll.SetOneSided(True)
  profll.SetStrategy(0)

  # ratio of profile likelihood - need to pass snapshot for the alt
  #ropl = RooStats.RatioOfProfiledLikelihoodsTestStat(sbModel.GetPdf(), bModel.GetPdf(), bModel.GetSnapshot())

  # set the test statistic to use
  #toymcs.SetTestStatistic(slrts)
  toymcs.SetTestStatistic(profll)
  #toymcs.SetTestStatistic(ropl)

  from ROOT import TProof
  #TProof.AddEnvVar("PROOF_INITCMD", "cat /afs/cern.ch/user/t/tbird/emu/glowing-wookie/scripts/fitters/proof-env.sh") ;
  #pc = RooStats.ProofConfig(w, nCPUs, "", False)
  #pc = RooStats.ProofConfig(w, 1)
  #toymcs.SetProofConfig(pc)

  ## if the pdf is not extended (e.g. in the Poisson model)
  ## we need to set the number of events
  #print sbModel.GetPdf().canBeExtended() # prints true
  #if not sbModel.GetPdf().canBeExtended(): # doesnt run
     #toymcs.SetNEventsPerToy(1)

  #int npoints = 10  # number of points to scan
  # min and max (better to choose smaller intervals)
  #poimin = 0.1e-8
  #poimax = 3e-8
  poimin = 1e-7
  poimax = 5e-7

  calc.SetFixedScan(15,poimin,poimax)

  print "Getting inteval from hypo test inverter"
  inteval = calc.GetInterval()

  upperLimit = inteval.UpperLimit()
  ulError = inteval.UpperLimitEstimatedError()

  limit_ac = upperLimit

  # double lowerLimit = inteval.LowerLimit()
  # double llError = inteval.LowerLimitEstimatedError()
  # if (lowerLimit < upperLimit(1.- 1.E-4))
  #    print "The computed lower limit is: " , lowerLimit , " +/- " , llError
  print "The computed upper limit is: " , upperLimit , " +/- " , ulError

  # compute expected limit
  print "Expected upper limits, using the B (alternate) model : "
  print " expected limit (-1 sig) " , inteval.GetExpectedUpperLimit(-1)
  print " expected limit (median) " , inteval.GetExpectedUpperLimit(0)
  print " expected limit (+1 sig) " , inteval.GetExpectedUpperLimit(1)

  # plot now the result of the scan
  htiplot = RooStats.HypoTestInverterPlot("HTI_Result_Plot","Feldman-Cousins Interval",inteval)

  # plot in a new canvas with style
  brazilCanv = TCanvas("HypoTestInverter Scan")
  htiplot.Draw("CLb 2CL")  # plot also CLb and CLs+b
  #htiplot.Draw("")  # plot also CLb and CLs+b
  brazilCanv.SaveAs("brazil-test.pdf")
  timePlots.append( ["Brazil_Canv",brazilCanv] )
  timePlots.append( ["Brazil_Plot",htiplot] )

  save_file = TFile.Open(config['outFileName'],"RECREATE")
  save_file.cd()
  for i in timePlots:
    if not i[1]:
      print "Plot ERROR!:", i
    else:
      i[1].Write(i[0])
  if config['doFit'] or config['loadFit']:
    if r:
      hcorr.Write("CorrelationHist")
      r.Write("RooFitResults")
  save_file.Close()

  if r:
    finalPars = r.floatParsFinal()
    it=finalPars.createIterator()
    while True:
      var = it.Next()
      if not var:
        print "End of variables"
        break
      else:
        w.obj(var.GetName()).setVal(var.getVal())
        w.obj(var.GetName()).setError(var.getError())

  RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)
  RooMsgService.instance().deleteStream(2)

timers["limits"].Stop()
timers["limits"].Print()


timers["splot"].Start()

if config['doSPlot']:
  print "Starting splots"
  sys.stdout.flush()

  fullUnbDataSet.Print("v")

  varList = r.floatParsFinal()
  it = varList.createIterator()
  setconst=[]
  while True:
    var = it.Next()
    if not var:
      break
    if var.isConstant():
      continue
    setconst.append(var.GetName())
    var.setConstant(True)

  splot_vars = RooArgList()
  for v in config["splot_vars"]:
    splot_vars.add(w.obj(v))

  #normTree

  sData = RooStats.SPlot("sData","An SPlot", fullUnbDataSet, Final_PDF, splot_vars )
  sData.Print()

  for v in config["splot_vars"]:
    print v,"Fitted value: %.2f sPlot value: %.2f"%(w.obj(v).getVal(), sData.GetYieldFromSWeight(v))

  for v in setconst:
    w.obj(v).setConstant(False)

  fullUnbDataSet.Print("v")

  save_file = TFile.Open(config['outFileName'],"RECREATE")
  save_file.cd()
  for i in timePlots:
    if not i[1]:
      print "Plot ERROR!:", i
    else:
      i[1].Write(i[0])
  if config['doFit'] or config['loadFit']:
    if r:
      hcorr.Write("CorrelationHist")
      r.Write("RooFitResults")
  if config['doSPlot']:
    fullUnbDataSet.Write("sPlotData")
  save_file.Close()

timers["splot"].Stop()
timers["splot"].Print()


timers["nlls"].Start()
print "Starting nll plots"
sys.stdout.flush()

RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

if config['doNlls']:
  nll = False
  if config['doBinnedNll']:
    nll = Final_PDF.createNLL(fullDataSet, RooFit.NumCPU(nCPUs,True))
  else:
    nll = Final_PDF.createNLL(fullUnbDataSet, RooFit.NumCPU(nCPUs,True))

  if "norm" in config['mode']:
    w.obj('Norm_N_Sig').setConstant(False)

  nlllist = allNlls()

  for i in nlllist:
    timePlots.append(["NllOf_"+i[0],i[1]])

print "Getting high CPU asym Plots..."#, startAt, doPlots, config['doPlotsAsymLong']
#print "Getting Long asym Plots", startAt, doPlots, config['doPlotsAsymLong']
if config['doPlots']:
  if config['doPlotsAsymLong']:
    for i in range(startAt):
      #print "getting", i
      sys.stdout.flush()
      timePlots += queueList[i].get()
      #print "joining", i
      sys.stdout.flush()
      processList[i].join()



save_file = TFile.Open(config['outFileName'],"RECREATE")
save_file.cd()
for i in timePlots:
  if not i[1]:
    print "Plot ERROR!:", i
  else:
    i[1].Write(i[0])
if config['doFit'] or config['loadFit']:
  if r:
    hcorr.Write("CorrelationHist")
    r.Write("RooFitResults")
if config['doSPlot']:
  fullUnbDataSet.Write("sPlotData")
save_file.Close()

if r:
  finalPars = r.floatParsFinal()
  it=finalPars.createIterator()
  while True:
    var = it.Next()
    if not var:
      print "End of variables"
      break
    else:
      w.obj(var.GetName()).setVal(var.getVal())
      w.obj(var.GetName()).setError(var.getError())

timers["nlls"].Stop()
timers["nlls"].Print()

timers["profile"].Start()
sys.stdout.flush()

if config['doProfile']:

  if config['doBinned']:
    data = fullDataSet
  else:
    data = fullUnbDataSet

  profIns = RooStats.ProfileInspector()
  l = profIns.GetListOfProfilePlots(data, sbModel)

  for i in range(l.GetSize()):
    timePlots.append( ["ProfileInspector_"+l.At(i).GetName(),l.At(i)] )

  save_file = TFile.Open(config['outFileName'],"RECREATE")
  save_file.cd()
  for i in timePlots:
    if not i[1]:
      print "Plot ERROR!:", i
    else:
      i[1].Write(i[0])
  if config['doFit'] or config['loadFit']:
    if r:
      hcorr.Write("CorrelationHist")
      r.Write("RooFitResults")
  if config['doSPlot']:
    fullUnbDataSet.Write("sPlotData")
  save_file.Close()

  if r:
    finalPars = r.floatParsFinal()
    it=finalPars.createIterator()
    while True:
      var = it.Next()
      if not var:
        print "End of variables"
        break
      else:
        w.obj(var.GetName()).setVal(var.getVal())
        w.obj(var.GetName()).setError(var.getError())

timers["profile"].Stop()
timers["profile"].Print()

timers["gof"].Start()
sys.stdout.flush()


def gofCalcL(queue,gof,radius):
  os.nice(config['niceness'])
  queue.put(gof.calculateL(radius))

gofPlot = False
if config['doGof']:
  print "Starting gof calculation"


  cuts = [["UnmixedLowBMass","B0_MASS_CAT == 0 && "+B0_OSCIL.GetName()+" == -1"],["MixedLowBMass","B0_MASS_CAT == 0 && "+B0_OSCIL.GetName()+" == 1"],["UnmixedHighBMass","B0_MASS_CAT == 1 && "+B0_OSCIL.GetName()+" == -1"],["MixedHighBMass","B0_MASS_CAT == 1 && "+B0_OSCIL.GetName()+" == 1"]]

  globalPulls = []
  from math import sqrt
  from ROOT import TH1D

  for name,cut in cuts:
    data = getattr(fullDataSet,"reduce")(cut)
    nEntries = data.numEntries()

    observables = Final_PDF.getObservables(data)
    #normVars = observables
    normVars = RooArgSet(w.obj("D_DMASS_Ds"),w.obj("B_CORTAU"))

    globalPulls.append(["GlobalBinVol_"+name,TH1D("GlobalBinVol_"+name,"GlobalBinVol_"+name,400,0,.2)])
    globalPulls.append(["GlobalPull_"+name,TH1D("GlobalPull_"+name,"GlobalPull_"+name,400,-50,50)])
    globalPulls.append(["GlobalPdf_"+name,TH1D("GlobalPdf_"+name,"GlobalPdf_"+name,400,0,.2)])
    globalPulls.append(["GlobalEntries_"+name,TH1D("GlobalEntries_"+name,"GlobalEntries_"+name,200,0,200)])

    print "Calculating global pull for",name

    emptyBins = 0
    pdfSum = 0.

    timeThisBit = TStopwatch()
    timeThisBit.Start()
    for i in xrange(nEntries):
      if i%(nEntries/10) == 0:
        print 100*i/nEntries, "% complete"
      if i%10==0:
        argSet = data.get(i)
        entries = data.weight(argSet)
        volume = data.binVolume(argSet)
        if entries == 0.:
          emptyBins += 1
          continue
        obsIter = argSet.createIterator()
        while True:
          obj = obsIter.Next()
          if not obj:
            break
          if "RooCategory" == obj.ClassName():
            value = argSet.find(obj.GetName()).getBin()
            observables.find(obj.GetName()).setBin(value)
          elif "RooRealVar" == obj.ClassName():
            value = argSet.find(obj.GetName()).getVal()
            observables.find(obj.GetName()).setVal(value)
        pdf = Final_PDF.getVal(normVars)
        pdfSum += pdf*nEntries*volume
        globalPulls[-4][1].Fill(volume)
        globalPulls[-3][1].Fill((entries-pdf*nEntries*volume)/sqrt(entries))
        globalPulls[-2][1].Fill(pdf)
        globalPulls[-1][1].Fill(entries)

    print "There are",emptyBins," empty bins of",nEntries,"total bins,",emptyBins*100/nEntries,"% in",name,"pdfSum",pdfSum
    timeThisBit.Stop()
    timeThisBit.Print()

  globalPulls.sort()
  timePlots += globalPulls


  print "Calculating gof with density method"

  from ROOT import TGraph

  processList = []
  queueList = []
  resultList = []
  gof = {}

  nPoints = 40
  maxR = 0.2

  print "Radius going from", maxR*float(1)/nPoints, "to", maxR*float(nPoints)/nPoints, "in", nPoints, "steps"

  datasets = {}
  for name,cut in cuts:
    datasets[name] = getattr(fullUnbDataSet,"reduce")(cut)
    gof[name] = RooGofSquareDensity(Final_PDF, datasets[name], w.obj("B_CORTAU"), w.obj("D_DMASS_Ds"))
    gof[name].readData(1./10.)
    for i in range(nPoints):
      radius = maxR*float(i+1)/nPoints
      queueList.append(Queue())
      processList.append(Process(target=gofCalcL, args=(queueList[-1],gof[name],radius)))

  startAt = 0
  minPlotNumber = startAt
  while len(processList) > minPlotNumber:
    threads = spareThreads = (nCPUs - startAt - 1) if (nCPUs - startAt - 1) > 0 else 1
    if len(processList) - minPlotNumber < spareThreads:
      threads = len(processList) - minPlotNumber
    for i in range(threads):
      #print "starting", i+minPlotNumber
      sys.stdout.flush()
      processList[i+minPlotNumber].start()
    for i in range(threads):
      #print "getting", i+minPlotNumber
      sys.stdout.flush()
      resultList.append(queueList[i+minPlotNumber].get())
      #print "joining", i+minPlotNumber
      processList[i+minPlotNumber].join()
    minPlotNumber += threads

  offset = 0
  for name,cut in cuts:
    tg = TGraph(nPoints)
    for i in range(nPoints):
      tg.SetPoint(i,maxR*float(i+1)/nPoints,resultList[i+offset])
    offset += nPoints
    timePlots.append(["Gof_"+name,tg])

  save_file = TFile.Open(config['outFileName'],"RECREATE")
  save_file.cd()
  for i in timePlots:
    if not i[1]:
      print "Plot ERROR!:", i
    else:
      i[1].Write(i[0])
  #if doGof:
    #gofPlot.Write("Gof_LDist")
  if config['doFit'] or config['loadFit']:
    if r:
      hcorr.Write("CorrelationHist")
      r.Write("RooFitResults")
  if config['doSPlot']:
    fullUnbDataSet.Write("sPlotData")
  save_file.Close()

timers["gof"].Stop()
timers["gof"].Print()

timers["tree"].Start()

gROOT.ProcessLine(\
"struct TreeHelperStruct{\
float float_value;\
int int_value;\
};")

from ROOT import TreeHelperStruct, AddressOf, TTreeFormula

class BranchInfo:
  def __init__(self, name, float_type=True):
    self.name = name
    self.float_type = float_type
    self.struct = TreeHelperStruct()

  def __init__(self, tree, name, value, float_type=True):
    self.name = name
    self.float_type = float_type
    self.struct = TreeHelperStruct()
    self.struct.float_value = float(value)
    self.struct.int_value = int(value)
    self.setupFormula(tree)
    self.value = value

  def setupFormula(self, tree):
    type_letter = "F" if self.float_type else "I"
    type_struct_name = "float_value" if self.float_type else "int_value"
    self.branch = tree.Branch(self.name,AddressOf(self.struct,type_struct_name),self.name+"/"+type_letter)

  def fill(self):
    if self.float_type:
      self.struct.float_value = self.value
    else:
      self.struct.int_value = self.value
    self.branch.Fill()


class FitResultsTree:
  def __init__(self, roofitresults, args, limit_pc = -1., limit_ac = -1.):
    self.tree = TTree("RooFitResultsTree", "RooFitResultsTree")
    self.extraBranchInfos = []
    self.tmpFile = None
    self.result = roofitresults
    self.setupVariables()
    self.addBranch("limit_pc",limit_pc)
    self.addBranch("limit_ac",limit_ac)
    self.addBranch("covQual",self.result.covQual(), False)
    self.addBranch("status",self.result.status(), False)
    for i in xrange(self.result.numStatusHistory()):
      self.addBranch("status_history_%i"%i,self.result.statusCodeHistory(i), False)
    self.addBranch("muCut",args.PIDmuCut)
    self.addBranch("eCut",args.PIDeCut)
    self.addBranch("seed",args.seed)
    self.tree.Fill()

  #def doFill(self):
    #for branch in self.extraBranchInfos:
      #branch.fill()

  def addBranch(self, name, value, float_type=True):
    self.extraBranchInfos.append(BranchInfo(self.tree, name, value, float_type))

  def setupVariable(self, name):
    init_var = self.result.floatParsInit().find(name)
    final_var = self.result.floatParsFinal().find(name)

    self.addBranch(name+"_init_val", init_var.getVal())
    self.addBranch(name+"_init_err", init_var.getError())
    self.addBranch(name+"_final_val", final_var.getVal())
    self.addBranch(name+"_final_err", final_var.getError())
    self.addBranch(name+"_pull", (final_var.getVal()-init_var.getVal())/final_var.getError())

  def setupVariables(self):
    it = self.result.floatParsInit().createIterator()
    while True:
      var = it.Next()
      if not var:
        break
      print "Filling", var.GetName()
      self.setupVariable(var.GetName())

if config["doTree"]:
  if config['doBinned']:
    data = fullDataSet
  else:
    data = fullUnbDataSet

  tree_save_file = TFile.Open(config['treeFile'],"RECREATE")
  tree_save_file.cd()

  frt = FitResultsTree(r,args,limit_pc,limit_ac)
  frt.tree.Write("RooFitResultsTree")

  tree_save_file.Close()

timers["tree"].Stop()
timers["tree"].Print()

timers["total"].Stop()

#sshProc = subprocess.call("ssh -f thomas@`who | grep tbird | grep -v \":pts\" | cut -d'(' -f 2 | sed \"s/)//\"` \"DISPLAY=:0 kdialog --msgbox \\\"Fitter finished on `hostname`\\\"\"", shell=True)


if r:
  finalPars = r.floatParsFinal()
  it=finalPars.createIterator()
  while True:
    var = it.Next()
    if not var:
      print "End of variables"
      break
    else:
      w.obj(var.GetName()).setVal(var.getVal())
      w.obj(var.GetName()).setError(var.getError())

if config['doFit'] or config['loadFit']:
  if r:
    printSetVarLimits(w)
    printTexRes(r)
    checkVarLimits(w)
    print "Minimum value of NLL:", r.minNll()
    r.Print()
    sys.stdout.flush()
else:
  printSetVarLimits(w)
  checkVarLimits(w)
  sys.stdout.flush()


for key in ['startup', 'fitting', 'plotting', 'limits', 'splot', 'nlls', 'profile', 'gof', 'tree', 'total']:
  sys.stdout.write('{:<13}'.format(key+":"))
  timers[key].Print()

print "Done at %s, saved in" % datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"), config['outFileName']

