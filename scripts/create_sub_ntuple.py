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

from ROOT import TFile,TStopwatch,gROOT,gDirectory
from ROOT import gROOT,TFile,TTreeFormula


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
pipiPidCut = "x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && pi_ProbNNpi > 0.6"
likeSignCut = "x1_ID*x2_ID>0"

directory = "/afs/cern.ch/work/t/tbird/demu/ntuples/"

inPath = "Demu_NTuple/Demu_NTuple"
outName = "Demu_NTuple"

config = {
  'pipi': {
    'infile' : directory+"pipi/strip_pipi.root",
    'outfile': directory+"pipi/strip_pipi_fitter.root",
    'cuts'   : combine_cuts([(pipiPidCut,True),(likeSignCut,False)]),
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

  inFile = TFile(config['infile'],"READ")

  tmpFile = TFile("/tmp/tmp-asdasdasdq-omgapony.root","RECREATE")
  tmpFile.cd() # needed for big ntuples

  inTree = inFile.Get(inPath)
  inTree.Write()

  change_branch_status(inTree, ['D0_M', 'Dst_M', '*ProbNN*', "x*_ID"])

  print "Applying initial cuts"
  tree = inTree.CopyTree(config['cuts'])
  tree.Write()

  total = tree.GetEntries()
  print total, " candidates after inital cuts"

  #for i in Del_M ; do echo "double $i;\\" ; done
  gROOT.ProcessLine(\
  "struct TreeHelperStruct{\
  float Del_M;\
  float RAND;\
  };")
  from ROOT import TreeHelperStruct, AddressOf
  s=TreeHelperStruct()

  #for i in Del_M RAND; do echo "br_$i = tree.Branch('$i',AddressOf(s.$i),'$i/F')" ; done
  br_Del_M = tree.Branch('Del_M',AddressOf(s,"Del_M"),'Del_M/F')
  br_RAND = tree.Branch('RAND',AddressOf(s,"RAND"),'RAND/F')

  fr_Del_M = TTreeFormula('fr_Del_M','Dst_M-D0_M',tree)

  print "Looping over all events"
  for i in range(total):
    if i%(total/10) == 0:
      print "Now read entry",i+1,"of",total
    tree.GetEntry(i)
    #for i in Del_M RAND ; do echo "s.$i = fr_${i}.EvalInstance(0) ; br_$i.Fill()" ; done
    s.Del_M = fr_Del_M.EvalInstance(0) ; br_Del_M.Fill()
    s.RAND = random.random() ; br_RAND.Fill()
    
  change_branch_status(tree, ['D0_M', 'Dst_M', 'Del_M', 'RAND'])

  tree.SetName('subTree')
  tree.Write()

  print "Removing extra leaves"
  outFile = TFile(config['outfile'],"RECREATE")
  outFile.cd()
  outTree = tree.CloneTree(-1)

  print "Writing to", config['outfile']
  outTree.Write()
  outFile.Close()

  tmpFile.Close()
  subprocess.call(["bash", "-c", "rm /tmp/tmp-asdasdasdq-omgapony.root"])


  print "Done!"
  sw.Stop()
  sw.Print()


create_tree(config[ds])