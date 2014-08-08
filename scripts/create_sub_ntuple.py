#!/usr/bin/env python

from ROOT import gROOT
gROOT.SetBatch(True)

import random
import subprocess
import ROOT

from math import fabs, pi

from ROOT import TFile, TStopwatch, gROOT, gDirectory
from ROOT import gROOT, TFile, TTreeFormula, TChain

#from wookie import config as wookie_config


def combine_cuts(cuts):
  ret = ""
  last_cut = len(cuts) - 1
  if isinstance(cuts, list):
    for cut_number,(cut) in enumerate(cuts):
      ret += "(%s)" % cut
      #if cut_number is not 0:
      if cut_number is not last_cut:
        ret += "&&"

  elif isinstance(cuts, tuple):
    for cut_number,(cut,positive) in enumerate(cuts):
      if positive:
        ret += "(%s)" % cut
      else:
        ret += "!(%s)" % cut

      #if cut_number is not 0:
      if cut_number is not last_cut:
        ret += "&&"
  elif isinstance(cuts, str):
    return cuts

  else:
    raise TypeError("cuts is not a list, tuple or string")

  return ret

#directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/"

#inPath = "Demu_NTuple/Demu_NTuple"
#outName = "Demu_NTuple"

from wookie import config as wookie_config

import sys

dsArr = [k for k,v in wookie_config.datasets.iteritems()]
def usage():
  print "This program takes exactly one argument, the data set which is to be reduced."
  dsArr.sort()
  print "Availble datasets:", dsArr

if len(sys.argv) != 1+1:
  usage()
  sys.exit(1)

ds = str(sys.argv[1])
if ds not in dsArr:
  usage()
  sys.exit(1)


def change_branch_status(tree,branch_names):
  tree.SetBranchStatus("*",0)

  for branch_name in branch_names:
    tree.SetBranchStatus(branch_name,1)


def create_tree(config):
  sw = TStopwatch()
  sw.Start()

  print "Using dataset %s with cuts: %s"% (ds,config['cuts'])

  random.seed(112)


  tmpFile = TFile("/media/data/tmp-erwtertretert-omgapony.root","RECREATE")
  tmpFile.cd() # needed for big ntuples

  inTree = TChain(config['intree'])

  if isinstance(config['infile'],str):
    inTree.Add(config['infile'])
  else:
    for filename in config['infile']:
      inTree.Add(filename)

  inTree.Write()

  n_before = inTree.GetEntries()

  change_branch_status(inTree, ['Dst_LoKi_BPVVDCHI2','Dst_DTF_CHI2','D0_FDCHI2_OWNPV','D0_IPCHI2_OWNPV','Dst_IPCHI2_OWNPV','*_TRACK_PCHI2','Dst_DTF_*', '*_TRUEID', '*_BKGCAT', '*_MOTHER_KEY', '*_MOTHER_ID', '*ProbNN*', "x*_ID", "*_TOS", 'D0_CosTheta', 'D0_DOCA', 'D0_VChi2_per_NDOF', 'D0_MinIPChi2_PRIMARY', 'D0_IPChi2', 'Dst_MinIPChi2_PRIMARY', 'D0_DIRA', 'x1_CosTheta', 'x2_CosTheta', 'x1_IPCHI2_OWNPV', 'x2_IPCHI2_OWNPV', 'D0_PT', 'x1_PT', 'x2_PT', 'Dst_cpt_1.00','D0_TAU','*_P*','*_TRACK_Eta*','nTracks*','x*_M','pi_P*','pi_M','x1_BremP*','nSPDHits',"x*_PIDe","x*_PIDK"])

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
  float Del_M_BREM;\
  float Del_M_NOBREM;\
  float D0_M_BREM;\
  float D0_M_NOBREM;\
  float Dst_M_BREM;\
  float Dst_M_NOBREM;\
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
  float D0_DelPhi;\
  float D0_DelEta;\
  float BDT_ada;\
  int nTracks_Scaled;\
  int nTracks_Scaled_Inc;\
  int nTracks_Scaled_Dec;\
  };")
  from ROOT import TreeHelperStruct, AddressOf, TMVA
  s=TreeHelperStruct()
  from array import array

  br_Dst_M = tree.Branch('Dst_Mass',AddressOf(s,"Dst_M"),'Dst_Mass/F')
  br_D0_M = tree.Branch('D0_Mass',AddressOf(s,"D0_M"),'D0_Mass/F')
  br_Del_M = tree.Branch('Del_Mass',AddressOf(s,"Del_M"),'Del_Mass/F')
  #br_Del_M_BREM = tree.Branch('Del_M_BREM',AddressOf(s,"Del_M_BREM"),'Del_M_BREM/F')
  #br_Del_M_NOBREM = tree.Branch('Del_M_NOBREM',AddressOf(s,"Del_M_NOBREM"),'Del_M_NOBREM/F')
  #br_D0_M_BREM = tree.Branch('D0_M_BREM',AddressOf(s,"D0_M_BREM"),'D0_M_BREM/F')
  #br_D0_M_NOBREM = tree.Branch('D0_M_NOBREM',AddressOf(s,"D0_M_NOBREM"),'D0_M_NOBREM/F')
  #br_Dst_M_BREM = tree.Branch('Dst_M_BREM',AddressOf(s,"Dst_M_BREM"),'Dst_M_BREM/F')
  #br_Dst_M_NOBREM = tree.Branch('Dst_M_NOBREM',AddressOf(s,"Dst_M_NOBREM"),'Dst_M_NOBREM/F')
  br_RAND = tree.Branch('RAND',AddressOf(s,"RAND"),'RAND/F')
  br_nTracks_Scaled = tree.Branch('nTracks_Scaled',AddressOf(s,"nTracks_Scaled"),'nTracks_Scaled/I')
  br_nTracks_Scaled_Inc = tree.Branch('nTracks_Scaled_Inc',AddressOf(s,"nTracks_Scaled_Inc"),'nTracks_Scaled_Inc/I')
  br_nTracks_Scaled_Dec = tree.Branch('nTracks_Scaled_Dec',AddressOf(s,"nTracks_Scaled_Dec"),'nTracks_Scaled_Dec/I')

  fo_Dst_M = TTreeFormula('fo_Dst_M','Dst_DTF_Dst_MM',tree)
  fo_D0_M = TTreeFormula('fo_D0_M','Dst_DTF_D0_MM',tree)

  fo_Del_M = TTreeFormula('fo_Del_M','Dst_DTF_Dst_MM-Dst_DTF_D0_MM',tree)
  #fo_D0_M_BREM = TTreeFormula('fo_D0_M_BREM','sqrt(Dst_DTF_e_MM*Dst_DTF_e_MM + Dst_DTF_mu_MM*Dst_DTF_mu_MM + 2.*( sqrt(Dst_DTF_e_MM*Dst_DTF_e_MM+Dst_DTF_e_P*Dst_DTF_e_P) * sqrt(Dst_DTF_mu_MM*Dst_DTF_mu_MM+Dst_DTF_mu_P*Dst_DTF_mu_P) - (Dst_DTF_e_PX*Dst_DTF_mu_PX+Dst_DTF_e_PY*Dst_DTF_mu_PY+Dst_DTF_e_PZ*Dst_DTF_mu_PZ) ))',tree)

  #fo_D0_M_NOBREM = TTreeFormula('fo_D0_M_NOBREM','sqrt( Dst_DTF_e_MM*Dst_DTF_e_MM + Dst_DTF_mu_MM*Dst_DTF_mu_MM + 2.*( sqrt( Dst_DTF_e_MM*Dst_DTF_e_MM + ( (Dst_DTF_e_PX-x1_BremPX)*(Dst_DTF_e_PX-x1_BremPX) + (Dst_DTF_e_PY-x1_BremPY)*(Dst_DTF_e_PY-x1_BremPY) + (Dst_DTF_e_PZ-x1_BremPZ)*(Dst_DTF_e_PZ-x1_BremPZ) ) ) * sqrt(Dst_DTF_mu_MM*Dst_DTF_mu_MM+Dst_DTF_mu_P*Dst_DTF_mu_P) - ( (Dst_DTF_e_PX-x1_BremPX)*Dst_DTF_mu_PX + (Dst_DTF_e_PY-x1_BremPY)*Dst_DTF_mu_PY + (Dst_DTF_e_PZ-x1_BremPZ)*Dst_DTF_mu_PZ ) ) ) ',tree)

  #fo_Dst_M_BREM = TTreeFormula('fo_Dst_M_BREM','sqrt( pi_M*pi_M + ( Dst_DTF_e_MM*Dst_DTF_e_MM + Dst_DTF_mu_MM*Dst_DTF_mu_MM + 2.*( sqrt(Dst_DTF_e_MM*Dst_DTF_e_MM+Dst_DTF_e_P*Dst_DTF_e_P) * sqrt(Dst_DTF_mu_MM*Dst_DTF_mu_MM+Dst_DTF_mu_P*Dst_DTF_mu_P) - (Dst_DTF_e_PX*Dst_DTF_mu_PX+Dst_DTF_e_PY*Dst_DTF_mu_PY+Dst_DTF_e_PZ*Dst_DTF_mu_PZ) ) ) + 2.*(  sqrt( pi_M*pi_M+pi_P*pi_P ) * sqrt( ( Dst_DTF_e_MM*Dst_DTF_e_MM + Dst_DTF_mu_MM*Dst_DTF_mu_MM + 2.*( sqrt(Dst_DTF_e_MM*Dst_DTF_e_MM+Dst_DTF_e_P*Dst_DTF_e_P) * sqrt(Dst_DTF_mu_MM*Dst_DTF_mu_MM+Dst_DTF_mu_P*Dst_DTF_mu_P) - (Dst_DTF_e_PX*Dst_DTF_mu_PX+Dst_DTF_e_PY*Dst_DTF_mu_PY+Dst_DTF_e_PZ*Dst_DTF_mu_PZ) ) ) +  (Dst_DTF_e_PX+Dst_DTF_mu_PX)*(Dst_DTF_e_PX+Dst_DTF_mu_PX) + (Dst_DTF_e_PY+Dst_DTF_mu_PY)*(Dst_DTF_e_PY+Dst_DTF_mu_PY) + (Dst_DTF_e_PZ+Dst_DTF_mu_PZ)*(Dst_DTF_e_PZ+Dst_DTF_mu_PZ) ) - (pi_PX*(Dst_DTF_e_PX+Dst_DTF_mu_PX)+pi_PY*(Dst_DTF_e_PY+Dst_DTF_mu_PY)+pi_PZ*(Dst_DTF_e_PZ+Dst_DTF_mu_PZ)) ) )',tree)

  #fo_Dst_M_NOBREM = TTreeFormula('fo_Dst_M_NOBREM','sqrt( pi_M*pi_M + ( Dst_DTF_e_MM*Dst_DTF_e_MM + Dst_DTF_mu_MM*Dst_DTF_mu_MM + 2.*( sqrt(Dst_DTF_e_MM*Dst_DTF_e_MM+((Dst_DTF_e_PX-x1_BremPX)*(Dst_DTF_e_PX-x1_BremPX)+(Dst_DTF_e_PY-x1_BremPY)*(Dst_DTF_e_PY-x1_BremPY)+(Dst_DTF_e_PZ-x1_BremPZ)*(Dst_DTF_e_PZ-x1_BremPZ))) * sqrt(Dst_DTF_mu_MM*Dst_DTF_mu_MM+Dst_DTF_mu_P*Dst_DTF_mu_P) - ((Dst_DTF_e_PX-x1_BremPX)*Dst_DTF_mu_PX+(Dst_DTF_e_PY-x1_BremPY)*Dst_DTF_mu_PY+(Dst_DTF_e_PZ-x1_BremPZ)*Dst_DTF_mu_PZ) ) ) + 2.*(  sqrt( pi_M*pi_M+pi_P*pi_P ) * sqrt( ( Dst_DTF_e_MM*Dst_DTF_e_MM + Dst_DTF_mu_MM*Dst_DTF_mu_MM + 2.*( sqrt(Dst_DTF_e_MM*Dst_DTF_e_MM+((Dst_DTF_e_PX-x1_BremPX)*(Dst_DTF_e_PX-x1_BremPX)+(Dst_DTF_e_PY-x1_BremPY)*(Dst_DTF_e_PY-x1_BremPY)+(Dst_DTF_e_PZ-x1_BremPZ)*(Dst_DTF_e_PZ-x1_BremPZ))) * sqrt(Dst_DTF_mu_MM*Dst_DTF_mu_MM+Dst_DTF_mu_P*Dst_DTF_mu_P) - ((Dst_DTF_e_PX-x1_BremPX)*Dst_DTF_mu_PX+(Dst_DTF_e_PY-x1_BremPY)*Dst_DTF_mu_PY+(Dst_DTF_e_PZ-x1_BremPZ)*Dst_DTF_mu_PZ) ) ) +  ((Dst_DTF_e_PX-x1_BremPX)+Dst_DTF_mu_PX)*((Dst_DTF_e_PX-x1_BremPX)+Dst_DTF_mu_PX) + ((Dst_DTF_e_PY-x1_BremPY)+Dst_DTF_mu_PY)*((Dst_DTF_e_PY-x1_BremPY)+Dst_DTF_mu_PY) + ((Dst_DTF_e_PZ-x1_BremPZ)+Dst_DTF_mu_PZ)*((Dst_DTF_e_PZ-x1_BremPZ)+Dst_DTF_mu_PZ) ) - (pi_PX*((Dst_DTF_e_PX-x1_BremPX)+Dst_DTF_mu_PX)+pi_PY*((Dst_DTF_e_PY-x1_BremPY)+Dst_DTF_mu_PY)+pi_PZ*((Dst_DTF_e_PZ-x1_BremPZ)+Dst_DTF_mu_PZ)) ) )',tree)
  fo_nTracks = TTreeFormula('fo_nTracks','nTracks',tree)

  br_D0_pointing = tree.Branch('D0_pointing',AddressOf(s,"D0_pointing"),'D0_pointing/F')
  br_LepCosTheta = tree.Branch('LepCosTheta',AddressOf(s,"LepCosTheta"),'LepCosTheta/F')
  br_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV = tree.Branch('log_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV',AddressOf(s,"minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV"),'minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV/F')
  br_minx1_PT_x2_PT = tree.Branch('minx1_PT_x2_PT',AddressOf(s,"minx1_PT_x2_PT"),'minx1_PT_x2_PT/F')
  br_D0_PtScaledIso = tree.Branch('D0_PtScaledIso',AddressOf(s,"D0_PtScaledIso"),'D0_PtScaledIso/F')
  br_D0_DelPhi = tree.Branch('D0_DelPhi',AddressOf(s,"D0_DelPhi"),'D0_DelPhi/F')
  br_D0_DelEta = tree.Branch('D0_DelEta',AddressOf(s,"D0_DelEta"),'D0_DelEta/F')
  br_D0_VChi2_per_NDOF = tree.Branch('log_D0_VChi2_per_NDOF',AddressOf(s,"D0_VChi2_per_NDOF"),'log_D0_VChi2_per_NDOF/F')
  br_BDT_ada = tree.Branch('BDT_ada',AddressOf(s,"BDT_ada"),'BDT_ada/F')

  fo_D0_CosTheta = TTreeFormula('fo_D0_CosTheta','D0_CosTheta',tree)
  fo_D0_DOCA = TTreeFormula('fo_D0_DOCA','D0_DOCA',tree)
  fo_D0_pointing = TTreeFormula('fo_D0_pointing','-log(1-(D0_DIRA))',tree)
  fo_D0_VChi2_per_NDOF = TTreeFormula('fo_D0_VChi2_per_NDOF','-log(D0_VChi2_per_NDOF)',tree)
  fo_D0_MinIPChi2_PRIMARY = TTreeFormula('fo_D0_MinIPChi2_PRIMARY','D0_MinIPChi2_PRIMARY',tree)
  fo_D0_IPChi2 = TTreeFormula('fo_D0_IPChi2','D0_IPChi2',tree)
  fo_Dst_MinIPChi2_PRIMARY = TTreeFormula('fo_Dst_MinIPChi2_PRIMARY','Dst_MinIPChi2_PRIMARY',tree)
  fo_LepCosTheta = TTreeFormula('fo_LepCosTheta','(abs(x1_ID)==15||abs(x1_ID)==13||abs(x1_ID)==11)*((x1_ID<0)*x1_CosTheta+(x1_ID>0)*x2_CosTheta)+(abs(x1_ID)!=15&&abs(x1_ID)!=13&&abs(x1_ID)!=11)*((x1_ID>0)*x1_CosTheta+(x1_ID<0)*x2_CosTheta)',tree) # returns costheta of positive particle
  fo_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV = TTreeFormula('fo_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV','-log((x1_IPCHI2_OWNPV<x2_IPCHI2_OWNPV)*x1_IPCHI2_OWNPV+(x2_IPCHI2_OWNPV<x1_IPCHI2_OWNPV)*x2_IPCHI2_OWNPV)',tree)
  fo_minx1_PT_x2_PT = TTreeFormula('fo_minx1_PT_x2_PT','(x1_PT<x2_PT)*x1_PT+(x2_PT<x1_PT)*x2_PT',tree)
  fo_D0_DelPhi = TTreeFormula('fo_D0_DelPhi','cos(x1_TRACK_Phi-x2_TRACK_Phi)',tree)
  #fo_D0_DelPhi = TTreeFormula('fo_D0_DelPhi','fmod(abs(x1_TRACK_Phi-x2_TRACK_Phi),3.14159)',tree)
  fo_D0_DelEta = TTreeFormula('fo_D0_DelEta','(abs(x1_ID)==15||abs(x1_ID)==13||abs(x1_ID)==11)*((x1_ID<0)*(x1_TRACK_Eta-x2_TRACK_Eta)+(x1_ID>0)*(x2_TRACK_Eta-x1_TRACK_Eta))+(abs(x1_ID)!=15&&abs(x1_ID)!=13&&abs(x1_ID)!=11)*((x1_ID>0)*(x1_TRACK_Eta-x2_TRACK_Eta)+(x1_ID<0)*(x2_TRACK_Eta-x1_TRACK_Eta))',tree)
  fo_D0_PtScaledIso = TTreeFormula('fo_D0_PtScaledIso','Dst_PT/(Dst_PT+Dst_cpt_1.00)',tree)
  fo_Dst_DTF_CHI2 = TTreeFormula('fo_Dst_DTF_CHI2','Dst_DTF_CHI2',tree)
  fo_pi_TRACK_PCHI2 = TTreeFormula('fo_pi_TRACK_PCHI2','pi_TRACK_PCHI2',tree)

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
  ar_D0_DelPhi = array('f',[0])
  ar_D0_DelEta = array('f',[0])
  ar_Dst_DTF_CHI2 = array('f',[0])
  ar_pi_TRACK_PCHI2 = array('f',[0])

  if config["mva"]:
    reader = TMVA.Reader()
    reader.AddVariable("D0_CosTheta",ar_D0_CosTheta)
    reader.AddVariable("D0_DOCA",ar_D0_DOCA)
    #reader.AddVariable("D0_pointing",ar_D0_pointing)
    reader.AddVariable("log_D0_VChi2_per_NDOF",ar_D0_VChi2_per_NDOF)
    reader.AddVariable("D0_MinIPChi2_PRIMARY",ar_D0_MinIPChi2_PRIMARY)
    #reader.AddVariable("D0_IPChi2",ar_D0_IPChi2)
    #reader.AddVariable("Dst_MinIPChi2_PRIMARY",ar_Dst_MinIPChi2_PRIMARY)
    reader.AddVariable("LepCosTheta",ar_LepCosTheta)
    reader.AddVariable("log_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV",ar_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV)
    reader.AddVariable("D0_PtScaledIso",ar_D0_PtScaledIso)
    #reader.AddVariable("minx1_PT_x2_PT",ar_minx1_PT_x2_PT)
    reader.AddVariable("D0_DelEta",ar_D0_DelEta)
    reader.AddVariable("D0_DelPhi",ar_D0_DelPhi)
    reader.AddVariable("Dst_DTF_CHI2",ar_Dst_DTF_CHI2)
    reader.AddVariable("pi_TRACK_PCHI2",ar_pi_TRACK_PCHI2)

    #reader.BookMVA("BDT","d2emu_BDT_grad_30_120_7_1_5.weights.xml")
    #reader.BookMVA("BDT","d2emu_BDT_Grad_30_172_4_0_10.weights.xml")
    reader.BookMVA("BDTG","mva/weights_final/TMVAClassification_BDTG.weights.Jun2012.xml")

  s.BDT_ada = -999.

  print "Looping over all events"
  for i in range(total):
    if i%(total/10) == 0:
      print "Now read entry",i+1,"of",total
    tree.GetEntry(i)

    #for i in D0_CosTheta D0_DOCA D0_pointing D0_VChi2_per_NDOF D0_MinIPChi2_PRIMARY D0_IPChi2 Dst_MinIPChi2_PRIMARY LepCosTheta minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV minx1_PT_x2_PT D0_PtScaledIso ; do echo "s.${i} = ar_${i} = fo_${i}.EvalInstance(0)" ; done
    s.D0_CosTheta = ar_D0_CosTheta[0] = fo_D0_CosTheta.EvalInstance(0)
    s.D0_DOCA = ar_D0_DOCA[0] = fo_D0_DOCA.EvalInstance(0)
    s.D0_pointing = ar_D0_pointing[0] = fo_D0_pointing.EvalInstance(0) ; br_D0_pointing.Fill()
    s.D0_VChi2_per_NDOF = ar_D0_VChi2_per_NDOF[0] = fo_D0_VChi2_per_NDOF.EvalInstance(0) ; br_D0_VChi2_per_NDOF.Fill()
    s.D0_MinIPChi2_PRIMARY = ar_D0_MinIPChi2_PRIMARY[0] = fo_D0_MinIPChi2_PRIMARY.EvalInstance(0)
    s.D0_IPChi2 = ar_D0_IPChi2[0] = fo_D0_IPChi2.EvalInstance(0)
    s.Dst_MinIPChi2_PRIMARY = ar_Dst_MinIPChi2_PRIMARY[0] = fo_Dst_MinIPChi2_PRIMARY.EvalInstance(0)
    s.LepCosTheta = ar_LepCosTheta[0] = fo_LepCosTheta.EvalInstance(0) ; br_LepCosTheta.Fill()
    s.minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV = ar_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV[0] = fo_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV.EvalInstance(0) ; br_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV.Fill()
    s.minx1_PT_x2_PT = ar_minx1_PT_x2_PT[0] = fo_minx1_PT_x2_PT.EvalInstance(0) ; br_minx1_PT_x2_PT.Fill()
    s.D0_DelPhi = ar_D0_DelPhi[0] = fo_D0_DelPhi.EvalInstance(0) ; br_D0_DelPhi.Fill()
    s.D0_DelEta = ar_D0_DelEta[0] = fo_D0_DelEta.EvalInstance(0) ; br_D0_DelEta.Fill()
    s.D0_PtScaledIso = ar_D0_PtScaledIso[0] = fo_D0_PtScaledIso.EvalInstance(0) ; br_D0_PtScaledIso.Fill()

    ar_Dst_DTF_CHI2[0] = fo_Dst_DTF_CHI2.EvalInstance(0)
    ar_pi_TRACK_PCHI2[0] = fo_pi_TRACK_PCHI2.EvalInstance(0)

    if config["mva"]:
      s.BDT_ada = reader.EvaluateMVA("BDTG") ; br_BDT_ada.Fill()

    #if config['inPath'] == "TestTree":
      #s.D0_M = fo_D0_M.EvalInstance(0) ; br_D0_M.Fill()
      #s.Dst_M = fo_Dst_M.EvalInstance(0) ; br_Dst_M.Fill()

    #for i in Del_M RAND ; do echo "s.$i = fo_${i}.EvalInstance(0) ; br_$i.Fill()" ; done
    s.Dst_M = fo_Dst_M.EvalInstance(0) ; br_Dst_M.Fill()
    s.D0_M = fo_D0_M.EvalInstance(0) ; br_D0_M.Fill()
    s.Del_M = fo_Del_M.EvalInstance(0) ; br_Del_M.Fill()
    #s.D0_M_BREM = fo_D0_M_BREM.EvalInstance(0) ; br_D0_M_BREM.Fill()
    #s.D0_M_NOBREM = fo_D0_M_NOBREM.EvalInstance(0) ; br_D0_M_NOBREM.Fill()
    #s.Dst_M_BREM = fo_Dst_M_BREM.EvalInstance(0) ; br_Dst_M_BREM.Fill()
    #s.Dst_M_NOBREM = fo_Dst_M_NOBREM.EvalInstance(0) ; br_Dst_M_NOBREM.Fill()
    #s.Del_M_BREM =  s.Dst_M_BREM-s.D0_M_BREM; br_Del_M_BREM.Fill()
    #s.Del_M_NOBREM =  s.Dst_M_NOBREM-s.D0_M_NOBREM; br_Del_M_NOBREM.Fill()
    s.RAND = random.random() ; br_RAND.Fill()
    s.nTracks_Scaled = int(round(1.28*(random.random()-.5+float(fo_nTracks.EvalInstance(0))))) ; br_nTracks_Scaled.Fill()
    s.nTracks_Scaled_Inc = int(round(1.28*1.1*(random.random()-.5+float(fo_nTracks.EvalInstance(0))))) ; br_nTracks_Scaled_Inc.Fill()
    s.nTracks_Scaled_Dec = int(round(1.28*0.9*(random.random()-.5+float(fo_nTracks.EvalInstance(0))))) ; br_nTracks_Scaled_Dec.Fill()

  #final_branches = ['D0_Mass','D0_M_BREM','D0_M_NOBREM','Dst_M_BREM','Dst_M_NOBREM', 'Dst_Mass', 'Del_Mass', 'Del_M_BREM', 'Del_M_NOBREM', "BDT_ada",'RAND','*ProbNN*','*_TRACK_Eta','nTracks*','*_P','*_PT','nSPDHits']
  final_branches = ['D0_Mass', 'Dst_Mass', 'Del_Mass', 'RAND', "x1_PIDe", "x2_ProbNNmu"]
  if "pid" in ds:
    final_branches += ['x*_ProbNN*','x*_PIDe','x*_PIDK', 'pi_ProbNN*', '*_TRACK_Eta', 'nTracks*', '*_P', '*_PT', 'nSPDHits']
  elif "mva" in ds:
    final_branches += ['D0_TAU','Dst_LoKi_BPVVDCHI2','Dst_DTF_CHI2','D0_FDCHI2_OWNPV','*_TRACK_PCHI2',"D0_DelEta", "D0_DelPhi", "D0_CosTheta", "D0_DOCA", "D0_pointing", "*D0_VChi2_per_NDOF", "D0_MinIPChi2_PRIMARY", "D0_IPChi2", "Dst_MinIPChi2_PRIMARY", "LepCosTheta", "*minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV", "minx1_PT_x2_PT", "D0_PtScaledIso",'D0_IPCHI2_OWNPV','Dst_IPCHI2_OWNPV' ]

  if config['mva']:
    final_branches += ["BDT_ada"]

  change_branch_status(tree, final_branches)

  tree.SetName('subTree')
  tree.Write()

  print "Removing extra leaves"
  outFile = TFile(config['file'],"RECREATE")
  outFile.cd()
  outTree = tree.CloneTree(-1)

  n_after = outTree.GetEntries()

  print "Writing to", config['file']
  outTree.Write()
  outFile.Close()

  tmpFile.Close()
  subprocess.call(["bash", "-c", "rm /media/data/tmp-erwtertretert-omgapony.root"])

  #for f in inFile:
    #f.Close()

  #print "Done! Offline selection is %.2f%% efficient." %(100.*float(n_after)/float(n_before)) # this isnt offline sel any more
  print "Done!"
  sw.Stop()
  sw.Print()


create_tree(wookie_config.datasets[ds])














  #x1_M*x1_M +
  #x2_M*x2_M +
  #2.*(
    #sqrt(x1_M*x1_M+x1_PE*x1_PE) * sqrt(x2_M*x2_M+x2_PE*x2_PE) -
    #(x1_PX*x2_PX+x1_PY*x2_PY+x1_PZ*x2_PZ)
  #)



#sqrt(
  #pi_M*pi_M +
  #(
    #x1_M*x1_M +
    #x2_M*x2_M +
    #2.*(
      #sqrt(x1_M*x1_M+x1_PE*x1_PE) * sqrt(x2_M*x2_M+x2_PE*x2_PE) -
      #(x1_PX*x2_PX+x1_PY*x2_PY+x1_PZ*x2_PZ)
    #)
  #) +
  #2.*(
    #sqrt(
      #pi_M*pi_M+pi_PE*pi_PE
    #) *
    #sqrt(
      #(
        #x1_M*x1_M +
        #x2_M*x2_M +
        #2.*(
          #sqrt(x1_M*x1_M+x1_PE*x1_PE) * sqrt(x2_M*x2_M+x2_PE*x2_PE) -
          #(x1_PX*x2_PX+x1_PY*x2_PY+x1_PZ*x2_PZ)
        #)
      #) +
      #(x1_PX+x2_PX)*(x1_PX+x2_PX) +
      #(x1_PY+x2_PY)*(x1_PY+x2_PY) +
      #(x1_PZ+x2_PZ)*(x1_PZ+x2_PZ)
    #) -
    #(pi_PX*(x1_PX+x2_PX)+pi_PY*(x1_PY+x2_PY)+pi_PZ*(x1_PZ+x2_PZ))
  #)
#)


#sqrt( pi_M*pi_M + ( x1_M*x1_M + x2_M*x2_M + 2.*( sqrt(x1_M*x1_M+x1_PE*x1_PE) * sqrt(x2_M*x2_M+x2_PE*x2_PE) - (x1_PX*x2_PX+x1_PY*x2_PY+x1_PZ*x2_PZ) ) ) + 2.*(  sqrt( pi_M*pi_M+pi_PE*pi_PE ) * sqrt( ( x1_M*x1_M + x2_M*x2_M + 2.*( sqrt(x1_M*x1_M+x1_PE*x1_PE) * sqrt(x2_M*x2_M+x2_PE*x2_PE) - (x1_PX*x2_PX+x1_PY*x2_PY+x1_PZ*x2_PZ) ) ) +  (x1_PX+x2_PX)*(x1_PX+x2_PX) + (x1_PY+x2_PY)*(x1_PY+x2_PY) + (x1_PZ+x2_PZ)*(x1_PZ+x2_PZ) ) - (pi_PX*(x1_PX+x2_PX)+pi_PY*(x1_PY+x2_PY)+pi_PZ*(x1_PZ+x2_PZ)) ) )


#sqrt(
  #pi_M*pi_M +
  #(
    #x1_M*x1_M +
    #x2_M*x2_M +
    #2.*(
      #sqrt(x1_M*x1_M+(x1_PE-x1_BremPE)*(x1_PE-x1_BremPE)) * sqrt(x2_M*x2_M+x2_PE*x2_PE) -
      #((x1_PX-x1_BremPX)*x2_PX+(x1_PY-x1_BremPY)*x2_PY+(x1_PZ-x1_BremPZ)*x2_PZ)
    #)
  #) +
  #2.*(
    #sqrt(
      #pi_M*pi_M+pi_PE*pi_PE
    #) *
    #sqrt(
      #(
        #x1_M*x1_M +
        #x2_M*x2_M +
        #2.*(
          #sqrt(x1_M*x1_M+(x1_PE-x1_BremPE)*(x1_PE-x1_BremPE)) * sqrt(x2_M*x2_M+x2_PE*x2_PE) -
          #((x1_PX-x1_BremPX)*x2_PX+(x1_PY-x1_BremPY)*x2_PY+(x1_PZ-x1_BremPZ)*x2_PZ)
        #)
      #) +
      #((x1_PX-x1_BremPX)+x2_PX)*((x1_PX-x1_BremPX)+x2_PX) +
      #((x1_PY-x1_BremPY)+x2_PY)*((x1_PY-x1_BremPY)+x2_PY) +
      #((x1_PZ-x1_BremPZ)+x2_PZ)*((x1_PZ-x1_BremPZ)+x2_PZ)
    #) -
    #(pi_PX*(x1_PX+x2_PX)+pi_PY*(x1_PY+x2_PY)+pi_PZ*(x1_PZ+x2_PZ))
  #)
#)


#sqrt(pi_M*pi_M +(x1_M*x1_M +x2_M*x2_M +2.*(sqrt(x1_M*x1_M+(x1_PE-x1_BremPE)*(x1_PE-x1_BremPE)) * sqrt(x2_M*x2_M+x2_PE*x2_PE) -((x1_PX-x1_BremPX)*x2_PX+(x1_PY-x1_BremPY)*x2_PY+(x1_PZ-x1_BremPZ)*x2_PZ))) +2.*( sqrt(pi_M*pi_M+pi_PE*pi_PE) *sqrt((x1_M*x1_M +x2_M*x2_M +2.*(sqrt(x1_M*x1_M+(x1_PE-x1_BremPE)*(x1_PE-x1_BremPE)) * sqrt(x2_M*x2_M+x2_PE*x2_PE) -((x1_PX-x1_BremPX)*x2_PX+(x1_PY-x1_BremPY)*x2_PY+(x1_PZ-x1_BremPZ)*x2_PZ))) +((x1_PX-x1_BremPX)+x2_PX)*((x1_PX-x1_BremPX)+x2_PX) +((x1_PY-x1_BremPY)+x2_PY)*((x1_PY-x1_BremPY)+x2_PY) +((x1_PZ-x1_BremPZ)+x2_PZ)*((x1_PZ-x1_BremPZ)+x2_PZ)) -(pi_PX*(x1_PX+x2_PX)+pi_PY*(x1_PY+x2_PY)+pi_PZ*(x1_PZ+x2_PZ))))


#sqrt(x1_M*x1_M + x2_M*x2_M + 2.*( sqrt((x1_M+x1_PE-x1_BremPE)*(x1_M+x1_PE-x1_BremPE)) * sqrt((x2_M+x2_PE)*(x2_M+x2_PE)) - ((x1_PX-x1_BremPX)*x2_PX+(x1_PY-x1_BremPY)*x2_PY+(x1_PZ-x1_BremPZ)*x2_PZ) ))






