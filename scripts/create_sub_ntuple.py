#!/usr/bin/env python

import sys

def usage():
  print "This program takes exactly one argument, the data set which is to be reduced."
  print "Availble datasets: pipi"

if len(sys.argv) != 1+1:
  usage()
  sys.exit(1)

ds = str(sys.argv[1])

from ROOT import gROOT
gROOT.SetBatch(True)

import random
import subprocess
import ROOT

from math import fabs, pi

from ROOT import TFile, TStopwatch, gROOT, gDirectory
from ROOT import gROOT, TFile, TTreeFormula, TChain


def combine_cuts(cuts):
  ret = ""
  last_cut = len(cuts) - 1
  for cut_number,(cut,positive) in enumerate(cuts):
    if positive:
      ret += "(%s)" % cut
    else:
      ret += "!(%s)" % cut
      
    #if cut_number is not 0:
    if cut_number is not last_cut:
      ret += "&&"
        
  return ret


cuts = ""
likeSignCut = "x1_ID*x2_ID>0"

pipiPidCut = "x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNpi*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNk < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7"
pipiTrigCut = "( Dst_L0HadronDecision_TOS == 1 ) && ( Dst_Hlt1TrackAllL0Decision_TOS == 1) && ( Dst_Hlt2Dst2PiD02PiPiDecision_TOS == 1 )"

kpiTrigCut = "( Dst_L0HadronDecision_TOS == 1 ) && ( Dst_Hlt1TrackAllL0Decision_TOS == 1) && ( Dst_Hlt2Dst2PiD02KPiDecision_TOS == 1 )"

emuPidCut = "x1_ProbNNe>0.45 && pi_ProbNNghost<0.05 && x2_ProbNNghost<0.05 && x2_ProbNNmu>0.3 && x2_ProbNNk<0.55 && pi_ProbNNpi>0.45 && x1_ProbNNk<0.8"
emuTrigCut = "Dst_L0MuonDecision_TOS == 1 && Dst_Hlt1TrackMuonDecision_TOS== 1 && (Dst_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 || Dst_Hlt2CharmHadD02HH_D02KPiDecision_TOS == 1 || Dst_Hlt2CharmHadD02HH_D02KKDecision_TOS == 1 )"

directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/"

inPath = "Demu_NTuple/Demu_NTuple"
outName = "Demu_NTuple"

config = {
  'pipi': {
    'infile' : [directory+"pipi/strip_pipi2011.root",directory+"pipi/strip_pipi2012.root"],
    'outfile': directory+"pipi/strip_pipi_fitter.root",
    'cuts'   : combine_cuts([(pipiTrigCut,True),(pipiPidCut,True),(likeSignCut,False)]),
    'inPath' : "Demu_NTuple/Demu_NTuple",
    'mva'    : False
  },
  'kpi': {
    'infile' : [directory+"kpi/strip_kpi2012.root"],
    'outfile': directory+"kpi/strip_kpi_fitter.root",
    'cuts'   : combine_cuts([(kpiTrigCut,True),(likeSignCut,False)]),
    'inPath' : "Demu_NTuple/Demu_NTuple",
    'mva'    : False
  },
  'mcpipi': {
    'infile' : directory+"mcpipi/strip_pipi.root",
    'outfile': directory+"mcpipi/strip_pipi_fitter.root",
    'cuts'   : combine_cuts([(pipiTrigCut,True),(pipiPidCut,True),(likeSignCut,False)]),
    'inPath' : "Demu_NTuple/Demu_NTuple",
    'mva'    : False
  },
  'emu': {
    #'infile' : directory+"d2emu-tmva.root",
    'infile' : [directory+"emu/strip_emu2011.root",directory+"emu/strip_emu2012.root"],
    'outfile': directory+"emu/mva_emu_fitter.root",
    'cuts'   : combine_cuts([(emuPidCut,True),(emuTrigCut,True),(likeSignCut,False)]),
    'inPath' : "Demu_NTuple/Demu_NTuple",
    'mva'    : True
  },
  'mcemu': {
    #'infile' : directory+"d2emu-tmva.root",
    'infile' : directory+"mcemu/strip_emu.root",
    'outfile': directory+"mcemu/mva_emu_fitter.root",
    'cuts'   : combine_cuts([(emuPidCut,True),(emuTrigCut,True),(likeSignCut,False)]),
    'inPath' : "Demu_NTuple/Demu_NTuple",
    'mva'    : True
  },
}
  
  
  
def change_branch_status(tree,branch_names):
  tree.SetBranchStatus("*",0)
  
  for branch_name in branch_names:
    tree.SetBranchStatus(branch_name,1)
  
  
def create_tree(config):
  sw = TStopwatch()
  sw.Start()

  print "Using dataset %s with cuts: %s"% (ds,config['cuts'])

  random.seed(112)


  tmpFile = TFile("/tmp/tmp-asdasdasdq-omgapony.root","RECREATE")
  tmpFile.cd() # needed for big ntuples

  inTree = TChain(config['inPath'])
  
  if isinstance(config['infile'],str):
    inTree.Add(config['infile'])
  else:
    for filename in config['infile']:
      inTree.Add(filename)
  
  inTree.Write()
  
  n_before = inTree.GetEntries()

  change_branch_status(inTree, ['D0_M*', 'Dst_M*', '*ProbNN*', "x*_ID", "*_TOS", 'D0_CosTheta', 'D0_DOCA', 'D0_VChi2_per_NDOF', 'D0_MinIPChi2_PRIMARY', 'D0_IPChi2', 'Dst_MinIPChi2_PRIMARY', 'D0_DIRA', 'x1_CosTheta', 'x2_CosTheta', 'x1_IPCHI2_OWNPV', 'x2_IPCHI2_OWNPV', 'D0_PT', 'x1_PT', 'x2_PT', 'D0_cpt_1.00'])

  print "Applying initial cuts"
  tree = inTree.CopyTree(config['cuts'])
  tree.Write()

  total = tree.GetEntries()
  print total, " candidates after inital cuts"

  #for i in Del_M ; do echo "double $i;\\" ; done
  gROOT.ProcessLine(\
  "struct TreeHelperStruct{\
  float Dst_M;\
  float D0_M;\
  float Del_M;\
  float RAND;\
  float D0_CosTheta;\
  float D0_DOCA;\
  float D0_pointing;\
  float D0_VChi2_per_NDOF;\
  float D0_MinIPChi2_PRIMARY;\
  float D0_IPChi2;\
  float Dst_MinIPChi2_PRIMARY;\
  float LepCosTheta;\
  float minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV;\
  float minx1_PT_x2_PT;\
  float D0_PtScaledIso;\
  float BDT_ada;\
  };")
  from ROOT import TreeHelperStruct, AddressOf, TMVA
  s=TreeHelperStruct()
  from array import array

  br_Del_M = tree.Branch('Del_M',AddressOf(s,"Del_M"),'Del_M/F')
  br_RAND = tree.Branch('RAND',AddressOf(s,"RAND"),'RAND/F')

  fr_Del_M = TTreeFormula('fr_Del_M','Dst_M-D0_M',tree)
  
  br_D0_pointing = tree.Branch('D0_pointing',AddressOf(s,"D0_pointing"),'D0_pointing/F')
  br_LepCosTheta = tree.Branch('LepCosTheta',AddressOf(s,"LepCosTheta"),'LepCosTheta/F')
  br_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV = tree.Branch('minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV',AddressOf(s,"minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV"),'minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV/F')
  br_minx1_PT_x2_PT = tree.Branch('minx1_PT_x2_PT',AddressOf(s,"minx1_PT_x2_PT"),'minx1_PT_x2_PT/F')
  br_D0_PtScaledIso = tree.Branch('D0_PtScaledIso',AddressOf(s,"D0_PtScaledIso"),'D0_PtScaledIso/F')
  br_BDT_ada = tree.Branch('BDT_ada',AddressOf(s,"BDT_ada"),'BDT_ada/F')
    
  fr_D0_CosTheta = TTreeFormula('fr_D0_CosTheta','D0_CosTheta',tree)
  fr_D0_DOCA = TTreeFormula('fr_D0_DOCA','D0_DOCA',tree)
  fr_D0_pointing = TTreeFormula('fr_D0_pointing','-log(1-cos(D0_DIRA))',tree)
  fr_D0_VChi2_per_NDOF = TTreeFormula('fr_D0_VChi2_per_NDOF','D0_VChi2_per_NDOF',tree)
  fr_D0_MinIPChi2_PRIMARY = TTreeFormula('fr_D0_MinIPChi2_PRIMARY','D0_MinIPChi2_PRIMARY',tree)
  fr_D0_IPChi2 = TTreeFormula('fr_D0_IPChi2','D0_IPChi2',tree)
  fr_Dst_MinIPChi2_PRIMARY = TTreeFormula('fr_Dst_MinIPChi2_PRIMARY','Dst_MinIPChi2_PRIMARY',tree)
  fr_LepCosTheta = TTreeFormula('fr_LepCosTheta','(x1_ID>0)*x1_CosTheta + (x1_ID<0)*x2_CosTheta',tree)
  fr_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV = TTreeFormula('fr_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV','(x1_IPCHI2_OWNPV<x2_IPCHI2_OWNPV)*x1_IPCHI2_OWNPV+(x2_IPCHI2_OWNPV<x1_IPCHI2_OWNPV)*x2_IPCHI2_OWNPV',tree)
  fr_minx1_PT_x2_PT = TTreeFormula('fr_minx1_PT_x2_PT','(x1_PT<x2_PT)*x1_PT+(x2_PT<x1_PT)*x2_PT',tree)
  fr_D0_PtScaledIso = TTreeFormula('fr_D0_PtScaledIso','D0_PT/(D0_PT+D0_cpt_1.00)',tree)
  
  #for i in D0_CosTheta D0_DOCA D0_pointing D0_VChi2_per_NDOF D0_MinIPChi2_PRIMARY D0_IPChi2 Dst_MinIPChi2_PRIMARY LepCosTheta minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV minx1_PT_x2_PT D0_PtScaledIso ; do echo "ar_${i} = array('f',[0])" ; done
  ar_D0_CosTheta = array('f',[0])
  ar_D0_DOCA = array('f',[0])
  ar_D0_pointing = array('f',[0])
  ar_D0_VChi2_per_NDOF = array('f',[0])
  ar_D0_MinIPChi2_PRIMARY = array('f',[0])
  ar_D0_IPChi2 = array('f',[0])
  ar_Dst_MinIPChi2_PRIMARY = array('f',[0])
  ar_LepCosTheta = array('f',[0])
  ar_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV = array('f',[0])
  ar_minx1_PT_x2_PT = array('f',[0])
  ar_D0_PtScaledIso = array('f',[0])
    
  if config["mva"]:
    reader = TMVA.Reader()
    reader.AddVariable("D0_CosTheta",ar_D0_CosTheta)
    reader.AddVariable("D0_DOCA",ar_D0_DOCA)
    reader.AddVariable("D0_pointing",ar_D0_pointing)
    reader.AddVariable("D0_VChi2_per_NDOF",ar_D0_VChi2_per_NDOF)
    reader.AddVariable("D0_MinIPChi2_PRIMARY",ar_D0_MinIPChi2_PRIMARY)
    reader.AddVariable("D0_IPChi2",ar_D0_IPChi2)
    reader.AddVariable("Dst_MinIPChi2_PRIMARY",ar_Dst_MinIPChi2_PRIMARY)
    reader.AddVariable("LepCosTheta",ar_LepCosTheta)
    reader.AddVariable("minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV",ar_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV)
    reader.AddVariable("minx1_PT_x2_PT",ar_minx1_PT_x2_PT)
    reader.AddVariable("D0_PtScaledIso",ar_D0_PtScaledIso)

    reader.BookMVA("BDT","d2emu_BDT_grad_30_120_7_1_5.weights.xml")

  s.BDT_ada = -999.

  print "Looping over all events"
  for i in range(total):
    if i%(total/10) == 0:
      print "Now read entry",i+1,"of",total
    tree.GetEntry(i)
    
    #for i in D0_CosTheta D0_DOCA D0_pointing D0_VChi2_per_NDOF D0_MinIPChi2_PRIMARY D0_IPChi2 Dst_MinIPChi2_PRIMARY LepCosTheta minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV minx1_PT_x2_PT D0_PtScaledIso ; do echo "s.${i} = ar_${i} = fr_${i}.EvalInstance(0)" ; done
    s.D0_CosTheta = ar_D0_CosTheta[0] = fr_D0_CosTheta.EvalInstance(0)
    s.D0_DOCA = ar_D0_DOCA[0] = fr_D0_DOCA.EvalInstance(0)
    s.D0_pointing = ar_D0_pointing[0] = fr_D0_pointing.EvalInstance(0) ; br_D0_pointing.Fill()
    s.D0_VChi2_per_NDOF = ar_D0_VChi2_per_NDOF[0] = fr_D0_VChi2_per_NDOF.EvalInstance(0)
    s.D0_MinIPChi2_PRIMARY = ar_D0_MinIPChi2_PRIMARY[0] = fr_D0_MinIPChi2_PRIMARY.EvalInstance(0)
    s.D0_IPChi2 = ar_D0_IPChi2[0] = fr_D0_IPChi2.EvalInstance(0)
    s.Dst_MinIPChi2_PRIMARY = ar_Dst_MinIPChi2_PRIMARY[0] = fr_Dst_MinIPChi2_PRIMARY.EvalInstance(0)
    s.LepCosTheta = ar_LepCosTheta[0] = fr_LepCosTheta.EvalInstance(0) ; br_LepCosTheta.Fill()
    s.minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV = ar_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV[0] = fr_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV.EvalInstance(0) ; br_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV.Fill()
    s.minx1_PT_x2_PT = ar_minx1_PT_x2_PT[0] = fr_minx1_PT_x2_PT.EvalInstance(0) ; br_minx1_PT_x2_PT.Fill()
    s.D0_PtScaledIso = ar_D0_PtScaledIso[0] = fr_D0_PtScaledIso.EvalInstance(0) ; br_D0_PtScaledIso.Fill()

    if config["mva"]:
      s.BDT_ada = reader.EvaluateMVA("BDT") ; br_BDT_ada.Fill()
    
    #if config['inPath'] == "TestTree":
      #s.D0_M = fr_D0_M.EvalInstance(0) ; br_D0_M.Fill()
      #s.Dst_M = fr_Dst_M.EvalInstance(0) ; br_Dst_M.Fill()
    
    #for i in Del_M RAND ; do echo "s.$i = fr_${i}.EvalInstance(0) ; br_$i.Fill()" ; done
    s.Del_M = fr_Del_M.EvalInstance(0) ; br_Del_M.Fill()
    s.RAND = random.random() ; br_RAND.Fill()
    
  final_branches = ['D0_M', 'Dst_M', 'Del_M', "BDT_ada",'RAND']
  if not config['mva']:
    try:
      final_branches.pop(final_branches.index("BDT_ada"))
    except ValueError:
      pass
  
  change_branch_status(tree, final_branches)

  tree.SetName('subTree')
  tree.Write()

  print "Removing extra leaves"
  outFile = TFile(config['outfile'],"RECREATE")
  outFile.cd()
  outTree = tree.CloneTree(-1)
  
  n_after = outTree.GetEntries()

  print "Writing to", config['outfile']
  outTree.Write()
  outFile.Close()

  tmpFile.Close()
  subprocess.call(["bash", "-c", "rm /tmp/tmp-asdasdasdq-omgapony.root"])
  
  #for f in inFile:
    #f.Close()

  #print "Done! Offline selection is %.2f%% efficient." %(100.*float(n_after)/float(n_before)) # this isnt offline sel any more
  print "Done!"
  sw.Stop()
  sw.Print()


create_tree(config[ds])
