
import sys

if len(sys.argv) < 2:
  print "The dataset must also be specified, either emu or pipi."
  sys.exit(1)

ds = sys.argv[1]

import re
import operator

from ROOT import gROOT
gROOT.SetBatch(True)
gROOT.ProcessLine(".x lhcbstyle.C")

import ROOT
from ROOT import TFile, gROOT, TH1D, TCanvas, TChain

from wookie import config as wookie_config

#tf = TFile("/afs/cern.ch/work/t/tbird/demu/ntuples/mc%s/strip_%s.root"%(ds,ds))
#ttree = tf.Get("Demu_NTuple/Demu_NTuple")
print "Opeining file..."
ttree_orig = TChain("Demu_NTuple/Demu_NTuple")

#    1598 |        DaVinci | completed |   emu-MC2012-stripped-magdown |     0 |    44 |    44 |   1.89G |     Dirac |                     |                       all trigger lines 
#    1599 |        DaVinci | completed |     emu-MC2011-stripped-magup |     0 |    56 |    56 |   1.09G |     Dirac |                     |                       all trigger lines 
#    1602 |        DaVinci | completed |   emu-MC2011-stripped-magdown |     0 |    57 |    57 |   1.11G |     Dirac |                     |                       all trigger lines 
#    1603 |        DaVinci | completed |     emu-MC2012-stripped-magup |     0 |    37 |    37 |   1.88G |     Dirac |                     |                       all trigger lines 

#MC2012
#ttree_orig.Add("/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/1598/output/Demu_NTuple.root")
#ttree_orig.Add("/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/1603/output/Demu_NTuple.root")
#MC2011
ttree_orig.Add("/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/1602/output/Demu_NTuple.root")
#ttree_orig.Add("/afs/cern.ch/work/t/tbird/gangadir6/workspace/tbird/LocalXML/1599/output/Demu_NTuple.root")

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

tmp_file = TFile("/tmp/tbird/this_is_a_flaming_awesome_tempfile.root","RECREATE")
ttree = None
if ds == "emu":
  print "Reducing TTree..."
  #ttree = ttree_orig
  ttree = ttree_orig.CopyTree(combine_cuts(wookie_config.emu_cuts.get_list(["mcmatch", "ls", "dtf", "mass", "ghost", "pid"])))
  print "Reduced."
else: 
  ttree = ttree_orig

cuts = {
  "pipi" : "x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNpi*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNk < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7",
  #"emu"   : "x1_BremMultiplicity == 0 && x1_ProbNNe>0.45 && pi_ProbNNghost<0.05 && x2_ProbNNghost<0.05 && x2_ProbNNmu>0.3 && x2_ProbNNk<0.55 && pi_ProbNNpi>0.45 && x1_ProbNNk<0.8",
  "emu"  : "1",
  #"emu"  : combine_cuts(wookie_config.emu_cuts.get_list(["mcmatch", "ls", "dtf", "mass", "ghost", "pid"])),
  "kpi"  : "x1_ProbNNk > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNk*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNpi < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7",
  }

offline_cuts = cuts[ds]

lines_per_level = 1

def makeCanvas(name):
  tc = TCanvas(name,name,800,1200)
  tc.SetBottomMargin(0.5)
  #tc.SetRightMargin(0.3)
  tc.SetLeftMargin(0.15)
  return tc

tc = makeCanvas("tc")

l0_re = re.compile("Dst_L0.*_TOS")
hlt1_re = re.compile("Dst_Hlt1.*_TOS")
hlt2_re = re.compile("Dst_Hlt2.*_TOS")

l0 = []
hlt1 = []
hlt2 = []

for br in ttree.GetListOfBranches():
  br_name = br.GetName()
  #print br_name
  if (not ("Global_TOS" in br_name)) and (not ("Phys_TOS" in br_name)) and not ">>>" in br_name:
    if hlt1_re.match(br_name):
      #print "HLT1:",br_name
      if float(ttree.GetEntries(br_name+"==1")) > 0:
        hlt1.append(br_name)
    elif hlt2_re.match(br_name):
      #print "HLT2:",br_name
      if float(ttree.GetEntries(br_name+"==1")) > 0:
        hlt2.append(br_name)
    elif l0_re.match(br_name):
      #print "L0:  ",br_name
      if float(ttree.GetEntries(br_name+"==1")) > 0:
        l0.append(br_name)
    
#print l0
#print hlt1
#print hlt2

#for arr,name,typ in [(l0,"L0","Global"), (hlt1,"Hlt1","Phys"), (hlt2,"Hlt2","Phys")]:
  #arr.append("Dst_%s_TIS"%(name+typ))

def combine_line_names(names,use_prescale=True):
  last_name = len(names) - 1
  cut = ""
  for i, name in enumerate(names):
    prescale, scales = get_prescale(name)
    
    if "Dst_Hlt2CharmHadD02HH_D02PiPiDecision_TOS" in name:
      name = "(%s==1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1815 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1915 ))"%name
    #if "Dst_Hlt2CharmHadD02HH_D02KPiDecision_TOS" in name:
      #name = "(%s==1 && (SelReport_Hlt2CharmHadD02HH_D02KPiDecision_Particle_measuredMass > 1815 && SelReport_Hlt2CharmHadD02HH_D02KPiDecision_Particle_measuredMass < 1915 ))"%name
    if prescale == 1. or not use_prescale:
      if i is not last_name:
        cut += "(" + name + " == 1) || "
      else:
        cut += "(" + name + " == 1)"
    else:
      if i is not last_name:
        cut += "(" + name + " == 1 && rndm() < " + str(prescale) + ") || "
      else:
        cut += "(" + name + " == 1 && rndm() < " + str(prescale) + ")"
  return cut

def create_cut(levels):
  last_level = len(levels) - 1
  cut_prescaled = ""
  cut_no_prescale = ""
  for i, level in enumerate(levels):
    if i is not last_level:
      if isinstance(level,list):
        cut_prescaled += "(" + combine_line_names(level) + ") && "
        cut_no_prescale += "(" + combine_line_names(level,False) + ") && "
      else:
        cut_prescaled += "(" + level + ") && "
        cut_no_prescale += "(" + level + ") && "
    else:
      if isinstance(level,list):
        cut_prescaled += "(" + combine_line_names(level) + ")"
        cut_no_prescale += "(" + combine_line_names(level,False) + ")"
      else:
        cut_prescaled += "(" + level + ")"
        cut_no_prescale += "(" + level + ")"
  #print "       >>> ", cut, levels
  #print cut
  return cut_prescaled, cut_no_prescale


def calc_eff(triggers):
  cut_prescaled, cut_no_prescale = create_cut(triggers)
  
  total_prescaled = float(ttree.GetEntries(cut_prescaled))
  total_noprescale = float(ttree.GetEntries(cut_no_prescale))
  
  return total_prescaled, total_noprescale

prescales = {

  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDWideMassPreScaler':0.05000000,
  'Hlt2CharmHadLambdaC2PiPKPostScaler':1.00000000,
  'Hlt2TopoE4BodyBBDTPostScaler':1.00000000,
  'Hlt1MBNoBiasPreScaler':0.10000000,
  'Hlt2DiMuonDetachedPsi2SPostScaler':1.00000000,
  'Hlt2B2HHPostScaler':1.00000000,
  'Hlt2DiMuonBPostScaler':1.00000000,
  'Hlt2DisplVerticesSingleLoosePSPostScaler':1.00000000,
  'Hlt2SingleTFElectronPreScaler':1.00000000,
  'Hlt2Bd2KstGammaPreScaler':1.00000000,
  'Hlt2DisplVerticesSinglePSPreScaler':0.01000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLPreScaler':1.00000000,
  'Hlt2DiMuonAndMuonPostScaler':1.00000000,
  'Hlt2DisplVerticesSingleVeryHighFDPostScaler':1.00000000,
  'Hlt2Dst2PiD02MuMuPostScaler':1.00000000,
  'Hlt2DisplVerticesSinglePostScaler':1.00000000,
  'Hlt1Tell1ErrorPreScaler':0.00000000,
  'Hlt2CharmHadD02HHHHDst_K3piWideMassPostScaler':1.00000000,
  'Hlt2DoubleDiMuonPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_KKpipiWideMassPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDPostScaler':1.00000000,
  'Hlt2CharmSemilep3bodyD2PiMuMuSSPreScaler':1.00000000,
  'Hlt2CharmSemilepD02HMuNu_D02PiMuNuWSPostScaler':1.00000000,
  'Hlt2Dst2PiD02PiPiPostScaler':1.00000000,
  'Hlt2IncPhiSidebandsPostScaler':0.05000000,
  'Hlt2CharmSemilepD02HMuNu_D02KMuNuWSPreScaler':0.01000000,
  'Hlt2CharmHadD2HHHPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_hhXWideMassPostScaler':1.00000000,
  'Hlt2CharmSemilepD02HMuNu_D02PiMuNuWSPreScaler':0.01000000,
  'Hlt2CharmHadD2HHHWideMassPostScaler':1.00000000,
  'Hlt2LowMultChiC2HHPostScaler':1.00000000,
  'Hlt2TriMuonTauPostScaler':1.00000000,
  'Hlt1L0AnyNoSPDPostScaler':1.00000000,
  'Hlt2B2HHPi0_MergedPreScaler':1.00000000,
  'Hlt2TopoE3BodyBBDTPostScaler':1.00000000,
  'Hlt2TFBc2JpsiMuXSignalPreScaler':1.00000000,
  'Hlt2LowMultDDIncCPPreScaler':1.00000000,
  'Hlt2CharmHadMinBiasLambdaC2LambdaPiPostScaler':1.00000000,
  'Hlt1TrackForwardPassThroughPreScaler':0.00000000,
  'Hlt2LowMultD2K3PiWSPostScaler':1.00000000,
  'Hlt2GlobalPostScaler':1.00000000,
  'Hlt2LowMultPhotonPreScaler':0.01000000,
  'Hlt2DiElectronBPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_K3piWideMassPostScaler':1.00000000,
  'Hlt2LowMultHadronPostScaler':1.00000000,
  'Hlt2CharmSemilepD02HMuNu_D02PiMuNuPreScaler':0.05000000,
  'Hlt2ChargedHyperon_Xi2Lambda0DDPiPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_4piPostScaler':1.00000000,
  'Hlt2DiProtonLowMultPostScaler':1.00000000,
  'Hlt1NoPVPassThroughPostScaler':1.00000000,
  'Hlt2CharmSemilepD02KPiMuMuPreScaler':1.00000000,
  'Hlt2DisplVerticesSingleHighFDPostScaler':1.00000000,
  'Hlt2LowMultD2KPiPiPreScaler':1.00000000,
  'Hlt1TrackAllL0PostScaler':1.00000000,
  'Hlt2CharmSemilep3bodyLambdac2PMuMuPreScaler':1.00000000,
  'Hlt2DiMuonAndDsPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_3KpiPreScaler':0.10000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDPreScaler':1.00000000,
  'Hlt2DiMuonJPsiPreScaler':0.20000000,
  'Hlt2DiMuonDetachedHeavyPostScaler':1.00000000,
  'Hlt2TriMuonDetachedPostScaler':1.00000000,
  'Hlt1DiProtonLowMultPostScaler':1.00000000,
  'Hlt2HighPtJetsPostScaler':1.00000000,
  'Hlt2DiMuonAndLcPreScaler':1.00000000,
  'Hlt2LowMultHadron_nofilterPreScaler':0.01000000,
  'Hlt2LambdaC_LambdaC2Lambda0DDKPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLPreScaler':1.00000000,
  'Hlt2Bd2KstGammaWideBMassPreScaler':0.05000000,
  'Hlt2CharmRareDecayD02MuMuPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_4piWideMassPostScaler':1.00000000,
  'Hlt2DiMuonDY2PostScaler':1.00000000,
  'Hlt2CharmHadMinBiasD02KKPreScaler':1.00000000,
  'Hlt2LowMultD2K3PiPostScaler':1.00000000,
  'Hlt1SingleMuonHighPTPostScaler':1.00000000,
  'Hlt1MBMicroBiasVeloPreScaler':0.00000000,
  'Hlt2B2HHLTUnbiasedPreScaler':0.00000000,
  'Hlt2diPhotonDiMuonPostScaler':1.00000000,
  'Hlt2CharmHadD2KS0KS0WideMassPostScaler':1.00000000,
  'Hlt2TopoE4BodyBBDTPreScaler':1.00000000,
  'Hlt2CharmSemilep3bodyD2PiMuMuPostScaler':1.00000000,
  'Hlt2KshortToMuMuPiPiPreScaler':1.00000000,
  'Hlt1BeamGasNoBeamBeam1PreScaler':0.0,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWideMassPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDPreScaler':1.00000000,
  'Hlt2DebugEventPostScaler':1.00000000,
  'Hlt2DisplVerticesSingleHighMassPreScaler':1.00000000,
  'Hlt1DiProtonLowMultPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLPostScaler':1.00000000,
  'Hlt1TrackForwardPassThroughPostScaler':1.00000000,
  'Hlt2LowMultElectronPostScaler':1.00000000,
  'Hlt2CharmHadMinBiasLambdaC2LambdaPiPreScaler':1.00000000,
  'Hlt2DiMuonAndD0PreScaler':1.00000000,
  'Hlt2Bs2PhiGammaWideBMassPreScaler':0.10000000,
  'Hlt2ChargedHyperon_Omega2Lambda0LLKPreScaler':1.00000000,
  'Hlt2LumiPreScaler':1.00000000,
  'Hlt2LowMultPhotonPostScaler':1.00000000,
  'Hlt2DiMuonDetachedJPsiPreScaler':1.00000000,
  'Hlt2CharmSemilepD02KKMuMuPreScaler':1.00000000,
  'Hlt2TopoMu3BodyBBDTPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_3KpiWideMassPreScaler':0.10000000,
  'Hlt2DiProtonLowMultPreScaler':1.00000000,
  'Hlt2DoubleDiMuonPostScaler':1.00000000,
  'Hlt2Topo2BodySimplePostScaler':1.00000000,
  'Hlt1TrackPhotonPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_4piWideMassPreScaler':0.10000000,
  'Hlt2GlobalPreScaler':1.00000000,
  'Hlt2DiPhiPreScaler':1.00000000,
  'Hlt2TriMuonTauPreScaler':1.00000000,
  'Hlt2IncPhiPostScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02PiPiPreScaler':1.00000000,
  'Hlt2DiMuonPsi2SPostScaler':1.00000000,
  'Hlt2LowMultD2KPiPostScaler':1.00000000,
  'Hlt2ChargedHyperon_Omega2Lambda0DDKPostScaler':1.00000000,
  'Hlt2CharmHadD2KS0KS0PreScaler':1.00000000,
  'Hlt2DiMuonDY2PreScaler':0.03000000,
  'Hlt2CharmHadD02HH_D02KPiPreScaler':1.00000000,
  'Hlt2Topo4BodySimplePreScaler':0.00000000,
  'Hlt1L0AnyPostScaler':1.00000000,
  'Hlt2ExpressJPsiTagProbePreScaler':0.00000000,
  'Hlt2LowMultElectron_nofilterPostScaler':1.00000000,
  'Hlt1L0AnyNoSPDPreScaler':0.01000000,
  'Hlt2DisplVerticesDoublePreScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_4piPostScaler':1.00000000,
  'Hlt1BeamGasNoBeamBeam2PreScaler':0.0,
  'Hlt1VeloClosingMicroBiasPreScaler':1.00000000,
  'Hlt2DiMuonAndGammaPreScaler':0.00000000,
  'Hlt2SingleMuonVHighPTPreScaler':1.00000000,
  'Hlt2Dst2PiD02KMuPostScaler':1.00000000,
  'Hlt2Topo3BodyBBDTPreScaler':1.00000000,
  'Hlt1CharmCalibrationNoBiasPreScaler':1.00000000,
  'Hlt2CharmHadLambdaC2KPKWideMassPostScaler':0.10000000,
  'Hlt2ExpressKSPreScaler':0.00100000,
  'Hlt1TrackForwardPassThroughLoosePreScaler':0.00000000,
  'Hlt2LowMultMuonPostScaler':1.00000000,
  'Hlt1BeamGasCrossingEnhancedBeam1PreScaler':0.0,
  'Hlt1DiMuonLowMassPostScaler':1.00000000,
  'Hlt2DisplVerticesSingleHighMassPostScaler':1.00000000,
  'Hlt2CharmHadD2KS0H_D2KS0DDKPostScaler':1.00000000,
  'Hlt2ChargedHyperon_Omega2Lambda0LLKPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDWideMassPostScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02PiPiWideMassPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_3KpiPreScaler':1.00000000,
  'Hlt1DiMuonLowMassPreScaler':1.00000000,
  'Hlt2SingleTFVHighPtElectronPostScaler':1.00000000,
  'Hlt2ExpressJPsiPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_hhXPostScaler':1.00000000,
  'Hlt2LowMultMuonPreScaler':0.10000000,
  'Hlt2CharmHadD2HHHPostScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02KKWideMassPreScaler':1.00000000,
  'Hlt2Topo3BodyBBDTPostScaler':1.00000000,
  'Hlt2SingleMuonLowPTPostScaler':1.00000000,
  'Hlt1MBMicroBiasTStationPostScaler':1.00000000,
  'Hlt1BeamGasCrossingParasiticPreScaler':0.0,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDWideMassPreScaler':0.05000000,
  'Hlt2CharmHadD02HHHHDst_KKpipiPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDWideMassPostScaler':1.00000000,
  'Hlt2DiElectronHighMassPostScaler':1.00000000,
  'Hlt2TopoMu3BodyBBDTPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_K3piWideMassPreScaler':0.10000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLWideMassPostScaler':1.00000000,
  'Hlt2DiMuonDY3PreScaler':1.00000000,
  'Hlt2DiMuonAndMuonPreScaler':1.00000000,
  'Hlt2Topo3BodySimplePreScaler':0.00000000,
  'Hlt2Topo2BodyBBDTPostScaler':1.00000000,
  'Hlt2Bs2PhiGammaPostScaler':1.00000000,
  'Hlt2ChargedHyperon_Xi2Lambda0DDMuPostScaler':1.00000000,
  'Hlt2RadiativeTopoTrackPostScaler':1.00000000,
  'Hlt2DiMuonBPreScaler':1.00000000,
  'Hlt2CharmSemilep3bodyD2KMuMuPostScaler':1.00000000,
  'Hlt2CharmSemilep3bodyLambdac2PMuMuSSPreScaler':1.00000000,
  'Hlt2LowMultElectronPreScaler':1.00000000,
  'Hlt2LowMultChiC2HHWSPostScaler':1.00000000,
  'Hlt2ExpressDStar2D0PiPreScaler':0.10000000,
  'Hlt2LowMultDDIncVFPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLPreScaler':1.00000000,
  'Hlt2Bs2PhiGammaPreScaler':1.00000000,
  'Hlt2CharmHadLambdaC2PiPPiWideMassPreScaler':1.00000000,
  'Hlt1HighPtJetsSinglePVPreScaler':1.00000000,
  'Hlt2KshortToMuMuPiPiPostScaler':1.00000000,
  'Hlt2CharmHadMinBiasD02KPiPreScaler':1.00000000,
  'Hlt2CharmSemilepD02PiPiMuMuPostScaler':1.00000000,
  'Hlt1TrackMuonPostScaler':1.00000000,
  'Hlt2CharmSemilepD02KPiMuMuPostScaler':1.00000000,
  'Hlt2CharmSemilepD02HMuNu_D02PiMuNuPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_KKpipiPostScaler':1.00000000,
  'Hlt2ChargedHyperon_Xi2Lambda0LLMuPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWideMassPreScaler':0.05000000,
  'Hlt2LowMultChiC2HHHHWSPostScaler':1.00000000,
  'Hlt2SingleElectronTFHighPtPostScaler':1.00000000,
  'Hlt2CharmHadLambdaC2PiPPiWideMassPostScaler':0.10000000,
  'Hlt2CharmHadMinBiasLambdaC2KPPiPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_hhXPreScaler':1.00000000,
  'Hlt2TopoRad2plus1BodyBBDTPreScaler':0.00000000,
  'Hlt2DisplVerticesSingleHighFDPreScaler':1.00000000,
  'Hlt2CharmHadD02HHKsLLPreScaler':1.00000000,
  'Hlt2LowMultChiC2HHWSPreScaler':0.10000000,
  'Hlt2CharmHadLambdaC2PiPPiPostScaler':1.00000000,
  'Hlt2Topo2BodyBBDTPreScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02KKPostScaler':1.00000000,
  'Hlt2TransparentPostScaler':1.00000000,
  'Hlt2CharmSemilep3bodyD2KMuMuPreScaler':1.00000000,
  'Hlt2TopoE2BodyBBDTPreScaler':1.00000000,
  'Hlt2Bs2PhiGammaWideBMassPostScaler':1.00000000,
  'Hlt2CharmHadD2HHHKsLLPreScaler':1.00000000,
  'Hlt2ExpressBeamHaloPreScaler':0.00100000,
  'Hlt2CharmRareDecayD02MuMuPostScaler':1.00000000,
  'Hlt2LowMultD2K3PiWSPreScaler':0.10000000,
  'Hlt2SingleTFElectronPostScaler':1.00000000,
  'Hlt1BeamGasBeam2PreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLWideMassPreScaler':0.05000000,
  'Hlt2ExpressDs2PhiPiPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_2K2piWideMassPostScaler':1.00000000,
  'Hlt1NoPVPassThroughPreScaler':1.00000000,
  'Hlt2ForwardPreScaler':0.00001000,
  'Hlt2LowMultChiC2PPPreScaler':1.00000000,
  'Hlt1SingleMuonNoIPPostScaler':1.00000000,
  'Hlt2DiMuonJPsiPostScaler':1.00000000,
  'Hlt2LambdaC_LambdaC2Lambda0LLKPostScaler':1.00000000,
  'Hlt2LowMultDDIncCPPostScaler':1.00000000,
  'Hlt2CharmSemilepD02HMuNu_D02KMuNuPreScaler':0.05000000,
  'Hlt2SingleMuonPostScaler':1.00000000,
  'Hlt2DiMuonAndDpPreScaler':1.00000000,
  'Hlt2CharmHadD2HHHKsLLPostScaler':1.00000000,
  'Hlt2SingleMuonLowPTPreScaler':0.00200000,
  'Hlt1DiMuonHighMassPreScaler':1.00000000,
  'Hlt1LumiPreScaler':1.00000000,
  'Hlt2DiMuonDY1PreScaler':0.00500000,
  'Hlt2CharmHadD02HHHH_2K2piPreScaler':0.10000000,
  'Hlt2DiMuonDetachedHeavyPreScaler':1.00000000,
  'Hlt2PassThroughPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_3KpiPostScaler':1.00000000,
  'Hlt2CharmHadD2KS0H_D2KS0DDPiPreScaler':1.00000000,
  'Hlt1DiProtonPreScaler':1.00000000,
  'Hlt1TrackPhotonPostScaler':1.00000000,
  'Hlt2DiMuonDetachedPostScaler':1.00000000,
  'Hlt2DiPhiPostScaler':1.00000000,
  'Hlt2LowMultD2K3PiPreScaler':1.00000000,
  'Hlt1LumiMidBeamCrossingPostScaler':1.00000000,
  'Hlt2CharmHadD02HHKsDDPostScaler':1.00000000,
  'Hlt2LowMultD2KPiPiPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLWideMassPostScaler':1.00000000,
  'Hlt2TopoMu4BodyBBDTPreScaler':1.00000000,
  'Hlt2CharmSemilepD02HMuNu_D02KMuNuTightPreScaler':1.00000000,
  'Hlt2TopoRad2BodyBBDTPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXPostScaler':1.00000000,
  'Hlt2DiMuonDY4PostScaler':1.00000000,
  'Hlt2TopoRad2BodyBBDTPreScaler':0.00000000,
  'Hlt2DiMuonDY1PostScaler':1.00000000,
  'Hlt2Dst2PiD02MuMuPreScaler':1.00000000,
  'Hlt2TopoE2BodyBBDTPostScaler':1.00000000,
  'Hlt2LowMultD2KPiWSPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_KKpipiPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDPreScaler':1.00000000,
  'Hlt2CharmHadD02HHKsLLPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_KKpipiWideMassPreScaler':0.05000000,
  'Hlt2CharmHadD02HHHH_K3piPostScaler':1.00000000,
  'Hlt1BeamGasCrossingForcedRecoPreScaler':0.0,
  'Hlt2TopoMu2BodyBBDTPreScaler':1.00000000,
  'Hlt2CharmHadD2KS0H_D2KS0PiPreScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02KPiWideMassPostScaler':0.10000000,
  'Hlt2DiElectronHighMassPreScaler':1.00000000,
  'Hlt1GlobalPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_3KpiWideMassPreScaler':0.05000000,
  'Hlt1SingleMuonHighPTPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLWideMassPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDPreScaler':1.00000000,
  'Hlt2LowMultLMR2HHPostScaler':1.00000000,
  'Hlt2LowMultD2KPiPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWideMassPreScaler':0.05000000,
  'Hlt2CharmSemilepD02PiPiMuMuPreScaler':1.00000000,
  'Hlt2LumiPostScaler':1.00000000,
  'Hlt2Topo4BodySimplePostScaler':1.00000000,
  'Hlt2DiMuonAndD0PostScaler':1.00000000,
  'Hlt2LowMultD2KPiPiWSPostScaler':1.00000000,
  'Hlt2LowMultChiC2HHHHWSPreScaler':0.10000000,
  'Hlt2ExpressLambdaPreScaler':0.01000000,
  'Hlt2LowMultDDIncVFPostScaler':1.00000000,
  'Hlt2DiProtonPostScaler':1.00000000,
  'Hlt2CharmHadD2KS0H_D2KS0PiPostScaler':1.00000000,
  'Hlt2CharmHadMinBiasD02KKPostScaler':1.00000000,
  'Hlt1TrackForwardPassThroughLoosePostScaler':1.00000000,
  'Hlt1LumiPostScaler':1.00000000,
  'Hlt2ExpressD02KPiPreScaler':0.10000000,
  'Hlt2DiMuonAndDpPostScaler':1.00000000,
  'Hlt2LambdaC_LambdaC2Lambda0DDPiPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXPreScaler':1.00000000,
  'Hlt2CharmSemilepD02HMuNu_D02KMuNuPostScaler':1.00000000,
  'Hlt2HighPtJetsPreScaler':1.00000000,
  'Hlt2DisplVerticesSingleLoosePSPreScaler':0.00100000,
  'Hlt2IncPhiSidebandsPreScaler':1.00000000,
  'Hlt1SingleMuonNoIPPreScaler':0.01000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLWideMassPreScaler':0.05000000,
  'Hlt2DiMuonDY3PostScaler':1.00000000,
  'Hlt2DiMuonPsi2SHighPTPreScaler':1.00000000,
  'Hlt2DiMuonPsi2SHighPTPostScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02PiPiPostScaler':1.00000000,
  'Hlt1TrackAllL0TightPostScaler':1.00000000,
  'Hlt2CharmSemilep3bodyLambdac2PMuMuPostScaler':1.00000000,
  'Hlt2DiMuonDetachedPsi2SPreScaler':1.00000000,
  'Hlt2CharmHadD02HHKsDDPreScaler':1.00000000,
  'Hlt2RadiativeTopoPhotonPreScaler':1.00000000,
  'Hlt2CharmHadMinBiasDplus2hhhPreScaler':1.00000000,
  'Hlt2LowMultD2KPiPiWSPreScaler':0.10000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDPostScaler':1.00000000,
  'Hlt1TrackAllL0PreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLWideMassPreScaler':0.05000000,
  'Hlt2TopoE3BodyBBDTPreScaler':1.00000000,
  'Hlt1TrackMuonPreScaler':1.00000000,
  'Hlt2CharmHadD2HHHKsDDPostScaler':1.00000000,
  'Hlt2DisplVerticesSingleVeryHighFDPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXPostScaler':1.00000000,
  'Hlt2diPhotonDiMuonPreScaler':1.00000000,
  'Hlt2CharmHadLambdaC2KPKPostScaler':1.00000000,
  'Hlt2B2HHLTUnbiasedDetachedPreScaler':1.00000000,
  'Hlt2DiElectronBPreScaler':1.00000000,
  'Hlt2ErrorEventPreScaler':1.00000000,
  'Hlt2CharmHadLambdaC2KPPiPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_4piPreScaler':1.00000000,
  'Hlt2Topo4BodyBBDTPostScaler':1.00000000,
  'Hlt2DiMuonAndDsPostScaler':1.00000000,
  'Hlt1BeamGasCrossingEnhancedBeam2PreScaler':0.0,
  'Hlt2CharmHadD02HHHHDst_3KpiPostScaler':1.00000000,
  'Hlt2CharmSemilep3bodyLambdac2PMuMuSSPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWideMassPostScaler':1.00000000,
  'Hlt2SingleElectronTFLowPtPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_KKpipiPreScaler':0.10000000,
  'Hlt2LowMultHadron_nofilterPostScaler':1.00000000,
  'Hlt2DisplVerticesSingleDownPostScaler':1.00000000,
  'Hlt2TopoRad2plus1BodyBBDTPostScaler':1.00000000,
  'Hlt1ErrorEventPreScaler':1.00000000,
  'Hlt2CharmSemilep3bodyD2KMuMuSSPostScaler':1.00000000,
  'Hlt2LambdaC_LambdaC2Lambda0LLPiPostScaler':1.00000000,
  'Hlt1GlobalPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDWideMassPostScaler':1.00000000,
  'Hlt2CharmSemilep3bodyD2KMuMuSSPreScaler':1.00000000,
  'Hlt2SingleElectronTFHighPtPreScaler':0.01000000,
  'Hlt2DisplVerticesDoublePSPreScaler':0.01000000,
  'Hlt2B2HHPreScaler':1.00000000,
  'Hlt2TFBc2JpsiMuXPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_KKpipiWideMassPreScaler':0.10000000,
  'Hlt2CharmHadD2HHHKsDDPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_2K2piWideMassPreScaler':0.10000000,
  'Hlt2DisplVerticesDoublePSPostScaler':1.00000000,
  'Hlt2CharmHadLambdaC2PiPPiPreScaler':1.00000000,
  'Hlt1BeamGasHighRhoVerticesPreScaler':0.0,
  'Hlt1L0AnyPreScaler':0.00000100,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDPostScaler':1.00000000,
  'Hlt1SingleElectronNoIPPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_4piPreScaler':0.10000000,
  'Hlt2CharmHadD02HHHHDst_K3piPostScaler':1.00000000,
  'Hlt2IncPhiPreScaler':1.00000000,
  'Hlt2CharmHadLambdaC2PiPKWideMassPostScaler':0.10000000,
  'Hlt1MBMicroBiasTStationPreScaler':0.00000000,
  'Hlt2CharmHadMinBiasD02KPiPostScaler':1.00000000,
  'Hlt2TransparentPreScaler':1.00000000,
  'Hlt2CharmHadMinBiasDplus2hhhPostScaler':1.00000000,
  'Hlt2Dst2PiD02KPiPostScaler':1.00000000,
  'Hlt2DisplVerticesDoublePostScaler':1.00000000,
  'Hlt2Dst2PiD02PiPiPreScaler':0.03000000,
  'Hlt2DiMuonAndGammaPostScaler':1.00000000,
  'Hlt2ChargedHyperon_Xi2Lambda0LLPiPostScaler':1.00000000,
  'Hlt2DiMuonZPostScaler':1.00000000,
  'Hlt2Bd2KstGammaWideBMassPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDWideMassPreScaler':0.05000000,
  'Hlt2LambdaC_LambdaC2Lambda0DDKPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_2K2piPostScaler':1.00000000,
  'Hlt2CharmHadD2KS0KS0PostScaler':1.00000000,
  'Hlt2SingleElectronTFLowPtPreScaler':0.00100000,
  'Hlt2Bd2KstGammaPostScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02KPiWideMassPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLPostScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02KKWideMassPostScaler':0.10000000,
  'Hlt1VertexDisplVertexPreScaler':1.00000000,
  'Hlt2DisplVerticesSinglePreScaler':1.00000000,
  'Hlt2DisplVerticesSinglePSPostScaler':1.00000000,
  'Hlt2CharmSemilepD02KKMuMuPostScaler':1.00000000,
  'Hlt2DiProtonPreScaler':1.00000000,
  'Hlt2LowMultChiC2PPPostScaler':1.00000000,
  'Hlt2CharmHadD2HHHWideMassPreScaler':0.10000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDWideMassPreScaler':0.05000000,
  'Hlt2SingleTFVHighPtElectronPreScaler':1.00000000,
  'Hlt2RadiativeTopoPhotonPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLWideMassPreScaler':0.05000000,
  'Hlt1ODINTechnicalPostScaler':1.00000000,
  'Hlt2ChargedHyperon_Xi2Lambda0LLPiPreScaler':1.00000000,
  'Hlt1LumiMidBeamCrossingPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_2K2piWideMassPostScaler':1.00000000,
  'Hlt1MBMicroBiasVeloPostScaler':1.00000000,
  'Hlt2CharmHadD2KS0H_D2KS0DDKPreScaler':1.00000000,
  'Hlt2DisplVerticesSingleDownPreScaler':1.00000000,
  'Hlt2LowMultChiC2HHHHPostScaler':1.00000000,
  'Hlt2DiMuonJPsiHighPTPostScaler':1.00000000,
  'Hlt2LowMultHadronPreScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02PiPiWideMassPostScaler':0.10000000,
  'Hlt2LowMultD2KPiWSPreScaler':0.10000000,
  'Hlt2CharmHadD02HHXDst_hhXWideMassPreScaler':0.05000000,
  'Hlt1Tell1ErrorPostScaler':1.00000000,
  'Hlt1BeamGasCrossingForcedRecoFullZPreScaler':0.0,
  'Hlt2LowMultElectron_nofilterPreScaler':0.05000000,
  'Hlt2SingleMuonHighPTPreScaler':1.00000000,
  'Hlt2ChargedHyperon_Xi2Lambda0DDMuPreScaler':1.00000000,
  'Hlt2ChargedHyperon_Xi2Lambda0DDPiPreScaler':1.00000000,
  'Hlt2Topo2BodySimplePreScaler':0.00000000,
  'Hlt1HighPtJetsSinglePVPostScaler':1.00000000,
  'Hlt2PassThroughPreScaler':0.00010000,
  'Hlt2CharmHadD02HHHH_KKpipiWideMassPostScaler':1.00000000,
  #'Hlt1ODINTechnicalPreScaler':@OnlineEnv.AcceptRate@0,
  'Hlt2DiMuonDetachedJPsiPostScaler':1.00000000,
  'Hlt2CharmHadD2KS0H_D2KS0DDPiPostScaler':1.00000000,
  'Hlt1BeamGasBeam1PreScaler':1.00000000,
  'Hlt2CharmHadD2KS0H_D2KS0KPreScaler':1.00000000,
  'Hlt2ChargedHyperon_Xi2Lambda0LLMuPreScaler':1.00000000,
  'Hlt2RadiativeTopoTrackPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_K3piWideMassPreScaler':0.05000000,
  'Hlt2Topo3BodySimplePostScaler':1.00000000,
  'Hlt2B2HHPi0_MergedPostScaler':1.00000000,
  'Hlt2CharmHadLambdaC2KPKWideMassPreScaler':1.00000000,
  'Hlt2CharmHadLambdaC2KPPiPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXPreScaler':1.00000000,
  'Hlt2ChargedHyperon_Omega2Lambda0DDKPreScaler':1.00000000,
  'Hlt2DebugEventPreScaler':0.00000100,
  'Hlt2Dst2PiD02KPiPreScaler':0.01000000,
  'Hlt2CharmHadD02HHHH_K3piPreScaler':0.10000000,
  'Hlt2CharmHadD2KS0H_D2KS0KPostScaler':1.00000000,
  'Hlt2DiMuonAndLcPostScaler':1.00000000,
  'Hlt2CharmHadD2KS0KS0WideMassPreScaler':0.10000000,
  'Hlt2TopoMu4BodyBBDTPostScaler':1.00000000,
  'Hlt2TriMuonDetachedPreScaler':1.00000000,
  'Hlt2LambdaC_LambdaC2Lambda0LLPiPreScaler':1.00000000,
  'Hlt2B2HHLTUnbiasedPostScaler':1.00000000,
  'Hlt2DiMuonDY4PreScaler':1.00000000,
  'Hlt1TrackAllL0TightPreScaler':1.00000000,
  'Hlt2Bd2KstGammaWideKMassPreScaler':0.05000000,
  'Hlt2B2HHLTUnbiasedDetachedPostScaler':1.00000000,
  'Hlt2DiMuonDetachedPreScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02KPiPostScaler':1.00000000,
  'Hlt2CharmSemilepD02HMuNu_D02KMuNuTightPostScaler':1.00000000,
  'Hlt2Dst2PiD02KMuPreScaler':0.15000000,
  'Hlt2LambdaC_LambdaC2Lambda0DDPiPreScaler':1.00000000,
  'Hlt2DiMuonPsi2SPreScaler':0.10000000,
  'Hlt1SingleElectronNoIPPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLPostScaler':1.00000000,
  'Hlt2Topo4BodyBBDTPreScaler':1.00000000,
  'Hlt2CharmHadLambdaC2KPPiWideMassPreScaler':1.00000000,
  'Hlt2LowMultLMR2HHPreScaler':0.05000000,
  'Hlt2CharmHadD02HHHH_3KpiWideMassPostScaler':1.00000000,
  'Hlt2CharmHadLambdaC2PiPKPreScaler':1.00000000,
  'Hlt2DiMuonJPsiHighPTPreScaler':1.00000000,
  'Hlt2CharmHadLambdaC2KPPiWideMassPostScaler':0.10000000,
  'Hlt2SingleMuonVHighPTPostScaler':1.00000000,
  'Hlt2LambdaC_LambdaC2Lambda0LLKPreScaler':1.00000000,
  'Hlt1DiMuonHighMassPostScaler':1.00000000,
  'Hlt1DiProtonPostScaler':1.00000000,
  'Hlt1VertexDisplVertexPostScaler':1.00000000,
  'Hlt2CharmHadD02HH_D02KKPreScaler':1.00000000,
  'Hlt2LowMultChiC2HHPreScaler':1.00000000,
  'Hlt1L0HighSumETJetPostScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLWideMassPostScaler':1.00000000,
  'Hlt2SingleMuonHighPTPostScaler':1.00000000,
  'Hlt2CharmSemilepD02HMuNu_D02KMuNuWSPostScaler':1.00000000,
  'Hlt2TopoMu2BodyBBDTPostScaler':1.00000000,
  'Hlt2SingleMuonPreScaler':0.50000000,
  'Hlt2CharmHadD02HHHH_2K2piPostScaler':1.00000000,
  'Hlt2LowMultChiC2HHHHPreScaler':1.00000000,
  'Hlt2CharmSemilep3bodyD2PiMuMuPreScaler':1.00000000,
  'Hlt1MBNoBiasPostScaler':1.00000000,
  'Hlt2ForwardPostScaler':1.00000000,
  'Hlt2Bd2KstGammaWideKMassPostScaler':1.00000000,
  'Hlt2CharmSemilep3bodyD2PiMuMuSSPostScaler':1.00000000,
  'Hlt2DiMuonZPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_3KpiWideMassPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_K3piPreScaler':1.00000000,
  'Hlt2CharmHadMinBiasLambdaC2KPPiPostScaler':1.00000000,
  'Hlt2CharmHadLambdaC2PiPKWideMassPreScaler':1.00000000,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDWideMassPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_4piWideMassPreScaler':0.05000000,
  'Hlt2TFBc2JpsiMuXPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_4piWideMassPostScaler':1.00000000,
  'Hlt2CharmHadD02HHHH_2K2piWideMassPreScaler':0.05000000,
  'Hlt2CharmHadLambdaC2KPKPreScaler':1.00000000,
  'Hlt1L0HighSumETJetPreScaler':1.00000000,
  'Hlt2CharmHadD02HHHHDst_2K2piPreScaler':1.00000000,
  'Hlt2TFBc2JpsiMuXSignalPostScaler':1.00000000,

  'Hlt1DiMuonHighMassRunFrac':0.999988,
  'Hlt1DiMuonLowMassRunFrac':0.999988,
  'Hlt1SingleMuonNoIPRunFrac':0.999988,
  'Hlt1SingleMuonHighPTRunFrac':0.999988,
  'Hlt1SingleElectronNoIPRunFrac':0.998258,
  'Hlt1TrackAllL0RunFrac':0.999988,
  'Hlt1TrackMuonRunFrac':0.999988,
  'Hlt1TrackPhotonRunFrac':0.999988,
  'Hlt1TrackForwardPassThroughRunFrac':0.998258,
  'Hlt1TrackForwardPassThroughLooseRunFrac':0.998258,
  'Hlt1LumiRunFrac':0.999988,
  'Hlt1LumiMidBeamCrossingRunFrac':0.999988,
  'Hlt1MBNoBiasRunFrac':0.999988,
  'Hlt1MBMicroBiasVeloRunFrac':0.999998,
  'Hlt1MBMicroBiasVeloRateLimitedRunFrac':0.370184,
  'Hlt1MBMicroBiasTStationRunFrac':0.999988,
  'Hlt1MBMicroBiasTStationRateLimitedRunFrac':0.370184,
  'Hlt1L0AnyRunFrac':0.999988,
  'Hlt1L0AnyRateLimitedRunFrac':0.370184,
  'Hlt1L0AnyNoSPDRunFrac':0.999988,
  'Hlt1L0AnyNoSPDRateLimitedRunFrac':0.370184,
  'Hlt1NoPVPassThroughRunFrac':0.999988,
  'Hlt1DiProtonRunFrac':0.999988,
  'Hlt1DiProtonLowMultRunFrac':0.999988,
  'Hlt1BeamGasNoBeamBeam1RunFrac':0.999988,
  'Hlt1BeamGasNoBeamBeam2RunFrac':0.999988,
  'Hlt1BeamGasBeam1RunFrac':0.999988,
  'Hlt1BeamGasBeam2RunFrac':0.999988,
  'Hlt1BeamGasCrossingEnhancedBeam1RunFrac':0.999988,
  'Hlt1BeamGasCrossingEnhancedBeam2RunFrac':0.999988,
  'Hlt1BeamGasCrossingForcedRecoRunFrac':0.999988,
  'Hlt1ODINTechnicalRunFrac':0.999988,
  'Hlt1Tell1ErrorRunFrac':0.999988,
  'Hlt1VeloClosingMicroBiasRunFrac':0.999988,
  'Hlt1BeamGasCrossingParasiticRunFrac':0.999988,
  'Hlt1ErrorEventRunFrac':0.999988,
  'Hlt1GlobalRunFrac':0.999999,
  'Hlt1L0PURunFrac':0.000000,
  'Hlt1L0CALORunFrac':0.000000,
  'Hlt1CharmCalibrationNoBiasRunFrac':0.899604,
  'Hlt1L0HighSumETJetRunFrac':0.899604,
  'Hlt1BeamGasCrossingForcedRecoFullZRunFrac':0.669045,
  'Hlt1BeamGasHighRhoVerticesRunFrac':0.669045,
  'Hlt1VertexDisplVertexRunFrac':0.669045,
  'Hlt1TrackAllL0TightRunFrac':0.457761,
  'Hlt1HighPtJetsSinglePVRunFrac':0.218467,


  'Hlt2SingleElectronTFLowPtRunFrac':0.999988,
  'Hlt2SingleElectronTFHighPtRunFrac':0.999988,
  'Hlt2DiElectronHighMassRunFrac':0.999988,
  'Hlt2DiElectronBRunFrac':0.999988,
  'Hlt2B2HHLTUnbiasedRunFrac':0.999988,
  'Hlt2Topo2BodySimpleRunFrac':0.999988,
  'Hlt2Topo3BodySimpleRunFrac':0.999988,
  'Hlt2Topo4BodySimpleRunFrac':0.999988,
  'Hlt2Topo2BodyBBDTRunFrac':0.999988,
  'Hlt2Topo3BodyBBDTRunFrac':0.999988,
  'Hlt2Topo4BodyBBDTRunFrac':0.999988,
  'Hlt2TopoMu2BodyBBDTRunFrac':0.999988,
  'Hlt2TopoMu3BodyBBDTRunFrac':0.999988,
  'Hlt2TopoMu4BodyBBDTRunFrac':0.999988,
  'Hlt2TopoE2BodyBBDTRunFrac':0.999988,
  'Hlt2TopoE3BodyBBDTRunFrac':0.999988,
  'Hlt2TopoE4BodyBBDTRunFrac':0.999988,
  'Hlt2IncPhiRunFrac':0.999988,
  'Hlt2IncPhiSidebandsRunFrac':0.999988,
  'Hlt2CharmHadD02HHKsLLRunFrac':0.999988,
  'Hlt2Dst2PiD02PiPiRunFrac':0.999988,
  'Hlt2Dst2PiD02MuMuRunFrac':0.999988,
  'Hlt2Dst2PiD02KMuRunFrac':0.999988,
  'Hlt2Dst2PiD02KPiRunFrac':0.999988,
  'Hlt2PassThroughRunFrac':0.999988,
  'Hlt2TransparentRunFrac':0.999988,
  'Hlt2ForwardRunFrac':0.999988,
  'Hlt2DebugEventRunFrac':0.999988,
  'Hlt2CharmHadD02HH_D02PiPiRunFrac':0.999988,
  'Hlt2CharmHadD02HH_D02PiPiWideMassRunFrac':0.999988,
  'Hlt2CharmHadD02HH_D02KKRunFrac':0.999988,
  'Hlt2CharmHadD02HH_D02KKWideMassRunFrac':0.999988,
  'Hlt2CharmHadD02HH_D02KPiRunFrac':0.999988,
  'Hlt2CharmHadD02HH_D02KPiWideMassRunFrac':0.999988,
  'Hlt2ExpressJPsiRunFrac':0.999988,
  'Hlt2ExpressJPsiTagProbeRunFrac':0.999988,
  'Hlt2ExpressLambdaRunFrac':0.999988,
  'Hlt2ExpressKSRunFrac':0.999988,
  'Hlt2ExpressDs2PhiPiRunFrac':0.999988,
  'Hlt2ExpressBeamHaloRunFrac':0.999988,
  'Hlt2ExpressDStar2D0PiRunFrac':0.999988,
  'Hlt2ExpressHLT1PhysicsRunFrac':0.197317,
  'Hlt2Bs2PhiGammaRunFrac':0.999988,
  'Hlt2Bs2PhiGammaWideBMassRunFrac':0.999988,
  'Hlt2Bd2KstGammaRunFrac':0.999988,
  'Hlt2Bd2KstGammaWideKMassRunFrac':0.999988,
  'Hlt2Bd2KstGammaWideBMassRunFrac':0.999988,
  'Hlt2CharmHadD2KS0H_D2KS0PiRunFrac':0.999988,
  'Hlt2CharmHadD2KS0H_D2KS0KRunFrac':0.999988,
  'Hlt2CharmRareDecayD02MuMuRunFrac':0.999988,
  'Hlt2B2HHRunFrac':0.999988,
  'Hlt2MuonFromHLT1RunFrac':0.330943,
  'Hlt2SingleMuonRunFrac':0.999988,
  'Hlt2SingleMuonHighPTRunFrac':0.999988,
  'Hlt2SingleMuonLowPTRunFrac':0.999988,
  'Hlt2DiProtonRunFrac':0.999988,
  'Hlt2DiProtonTFRunFrac':0.197317,
  'Hlt2DiProtonLowMultRunFrac':0.999988,
  'Hlt2DiProtonLowMultTFRunFrac':0.197317,
  'Hlt2CharmSemilepD02HMuNu_D02KMuNuWSRunFrac':0.999988,
  'Hlt2CharmSemilepD02HMuNu_D02PiMuNuWSRunFrac':0.999988,
  'Hlt2CharmSemilepD02HMuNu_D02KMuNuRunFrac':0.999988,
  'Hlt2CharmSemilepD02HMuNu_D02PiMuNuRunFrac':0.999988,
  'Hlt2TFBc2JpsiMuXRunFrac':0.999988,
  'Hlt2TFBc2JpsiMuXSignalRunFrac':0.999988,
  'Hlt2diPhotonDiMuonRunFrac':0.998258,
  'Hlt2LowMultMuonRunFrac':0.998258,
  'Hlt2LowMultHadronRunFrac':0.998258,
  'Hlt2LowMultPhotonRunFrac':0.998258,
  'Hlt2LowMultElectronRunFrac':0.998258,
  'Hlt2DisplVerticesLowMassSingleRunFrac':0.100384,
  'Hlt2DisplVerticesHighMassSingleRunFrac':0.542227,
  'Hlt2DisplVerticesDoubleRunFrac':0.999988,
  'Hlt2DisplVerticesSinglePostScaledRunFrac':0.542227,
  'Hlt2DisplVerticesHighFDSingleRunFrac':0.542227,
  'Hlt2DisplVerticesSingleDownRunFrac':0.999988,
  'Hlt2CharmSemilepD2HMuMuRunFrac':0.330943,
  'Hlt2CharmSemilepD2HMuMuWideMassRunFrac':0.330943,
  'Hlt2B2HHPi0_MergedRunFrac':0.999988,
  'Hlt2CharmHadD2HHHRunFrac':0.999988,
  'Hlt2CharmHadD2HHHWideMassRunFrac':0.999988,
  'Hlt2DiMuonRunFrac':0.330943,
  'Hlt2DiMuonLowMassRunFrac':0.330943,
  'Hlt2DiMuonJPsiRunFrac':0.999988,
  'Hlt2DiMuonJPsiHighPTRunFrac':0.999988,
  'Hlt2DiMuonPsi2SRunFrac':0.999988,
  'Hlt2DiMuonBRunFrac':0.999988,
  'Hlt2DiMuonZRunFrac':0.999988,
  'Hlt2DiMuonDY1RunFrac':0.999988,
  'Hlt2DiMuonDY2RunFrac':0.999988,
  'Hlt2DiMuonDY3RunFrac':0.999988,
  'Hlt2DiMuonDY4RunFrac':0.999988,
  'Hlt2DiMuonDetachedRunFrac':0.999988,
  'Hlt2DiMuonDetachedHeavyRunFrac':0.999988,
  'Hlt2DiMuonDetachedJPsiRunFrac':0.999988,
  'Hlt2TriMuonDetachedRunFrac':0.999988,
  'Hlt2TriMuonTauRunFrac':0.999988,
  'Hlt2CharmSemilepD02HHMuMuRunFrac':0.330943,
  'Hlt2CharmSemilepD02HHMuMuWideMassRunFrac':0.330943,
  'Hlt2CharmHadD02HHHHRunFrac':0.330943,
  'Hlt2CharmHadD02HHHHWideMassRunFrac':0.330943,
  'Hlt2ErrorEventRunFrac':0.999988,
  'Hlt2GlobalRunFrac':0.999988,
  'Hlt2DiMuonNoPVRunFrac':0.001730,
  'Hlt2SingleTFElectronRunFrac':0.899604,
  'Hlt2SingleTFVHighPtElectronRunFrac':0.899604,
  'Hlt2B2HHLTUnbiasedDetachedRunFrac':0.899604,
  'Hlt2TopoRad2BodyBBDTRunFrac':0.802671,
  'Hlt2TopoRad2plus1BodyBBDTRunFrac':0.802671,
  'Hlt2LumiRunFrac':0.802671,
  'Hlt2CharmHadLambdaC2KPPiRunFrac':0.899604,
  'Hlt2SingleMuonVHighPTRunFrac':0.899604,
  'Hlt2CharmSemilepD02HMuNu_D02KMuNuTightRunFrac':0.899604,
  'Hlt2CharmHadMinBiasLambdaC2KPPiRunFrac':0.899604,
  'Hlt2CharmHadMinBiasD02KPiRunFrac':0.899604,
  'Hlt2CharmHadMinBiasD02KKRunFrac':0.899604,
  'Hlt2CharmHadMinBiasDplus2hhhRunFrac':0.899604,
  'Hlt2CharmHadMinBiasLambdaC2LambdaPiRunFrac':0.899604,
  'Hlt2LowMultHadron_nofilterRunFrac':0.802671,
  'Hlt2LowMultElectron_nofilterRunFrac':0.802671,
  'Hlt2DisplVerticesSingleRunFrac':0.899604,
  'Hlt2DisplVerticesDoublePostScaledRunFrac':0.441843,
  'Hlt2DisplVerticesSingleHighMassPostScaledRunFrac':0.441843,
  'Hlt2DisplVerticesSingleHighFDPostScaledRunFrac':0.441843,
  'Hlt2DisplVerticesSingleMVPostScaledRunFrac':0.441843,
  'Hlt2RadiativeTopoTrackTOSRunFrac':0.230559,
  'Hlt2RadiativeTopoPhotonL0RunFrac':0.230559,
  'Hlt2DiMuonPsi2SHighPTRunFrac':0.899604,
  'Hlt2DoubleDiMuonRunFrac':0.899604,
  'Hlt2DiMuonAndMuonRunFrac':0.899604,
  'Hlt2DiMuonAndGammaRunFrac':0.899604,
  'Hlt2DiMuonAndD0RunFrac':0.899604,
  'Hlt2DiMuonAndDpRunFrac':0.899604,
  'Hlt2DiMuonAndDsRunFrac':0.899604,
  'Hlt2DiMuonAndLcRunFrac':0.899604,
  'Hlt2CharmSemilepD02HHMuMuHardHadronsSoftMuonsRunFrac':0.230559,
  'Hlt2CharmSemilepD02HHMuMuHardHadronsSoftMuonsWideMassRunFrac':0.230559,
  'Hlt2CharmSemilepD02HHMuMuHardHadronsAndMuonsRunFrac':0.230559,
  'Hlt2CharmSemilepD02HHMuMuHardHadronsAndMuonsWideMassRunFrac':0.230559,
  'Hlt2CharmHadD02HHKsDDRunFrac':0.669045,
  'Hlt2CharmHadD2KS0KS0RunFrac':0.669045,
  'Hlt2CharmHadD2KS0KS0WideMassRunFrac':0.669045,
  'Hlt2ExpressD02KPiRunFrac':0.669045,
  'Hlt2CharmHadLambdaC2KPPiWideMassRunFrac':0.669045,
  'Hlt2CharmHadLambdaC2KPKRunFrac':0.669045,
  'Hlt2CharmHadLambdaC2KPKWideMassRunFrac':0.669045,
  'Hlt2CharmHadLambdaC2PiPPiRunFrac':0.669045,
  'Hlt2CharmHadLambdaC2PiPPiWideMassRunFrac':0.669045,
  'Hlt2CharmHadLambdaC2PiPKRunFrac':0.669045,
  'Hlt2CharmHadLambdaC2PiPKWideMassRunFrac':0.669045,
  'Hlt2CharmHadD2KS0H_D2KS0DDPiRunFrac':0.669045,
  'Hlt2CharmHadD2KS0H_D2KS0DDKRunFrac':0.669045,
  'Hlt2DiPhiRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDstNoHltOne_4piRunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_4piWideMassRunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_K3piRunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_K3piWideMassRunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_KKpipiRunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_KKpipiWideMassRunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_2K2piRunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_2K2piWideMassRunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_3KpiRunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_3KpiWideMassRunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_Ch2RunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDstNoHltOne_Ch2WideMassRunFrac':0.039241,
  'Hlt2CharmSemilep3bodyD2PiMuMuRunFrac':0.669045,
  'Hlt2CharmSemilep3bodyD2PiMuMuSSRunFrac':0.669045,
  'Hlt2CharmSemilep3bodyD2KMuMuRunFrac':0.669045,
  'Hlt2CharmSemilep3bodyD2KMuMuSSRunFrac':0.669045,
  'Hlt2CharmSemilep3bodyLambdac2PMuMuRunFrac':0.669045,
  'Hlt2CharmSemilep3bodyLambdac2PMuMuSSRunFrac':0.669045,
  'Hlt2LambdaC_LambdaC2Lambda0LLPiRunFrac':0.669045,
  'Hlt2LambdaC_LambdaC2Lambda0LLKRunFrac':0.669045,
  'Hlt2LambdaC_LambdaC2Lambda0DDPiRunFrac':0.669045,
  'Hlt2LambdaC_LambdaC2Lambda0DDKRunFrac':0.669045,
  'Hlt2RadiativeTopoTrackRunFrac':0.669045,
  'Hlt2RadiativeTopoPhotonRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_4piRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_4piWideMassRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_K3piRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_K3piWideMassRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_KKpipiRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_KKpipiWideMassRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_2K2piRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_2K2piWideMassRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_3KpiRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_3KpiWideMassRunFrac':0.669045,
  'Hlt2CharmHadD02HHHHDst_Ch2RunFrac':0.039241,
  'Hlt2CharmHadD02HHHHDst_Ch2WideMassRunFrac':0.039241,
  'Hlt2CharmSemilepD02PiPiMuMuRunFrac':0.669045,
  'Hlt2CharmSemilepD02KKMuMuRunFrac':0.669045,
  'Hlt2CharmSemilepD02KPiMuMuRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_4piRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_4piWideMassRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_K3piRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_K3piWideMassRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_KKpipiRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_KKpipiWideMassRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_2K2piRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_2K2piWideMassRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_3KpiRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_3KpiWideMassRunFrac':0.669045,
  'Hlt2CharmHadD02HHHH_Ch2RunFrac':0.039241,
  'Hlt2CharmHadD02HHHH_Ch2WideMassRunFrac':0.039241,
  'Hlt2DiMuonDetachedPsi2SRunFrac':0.629804,
  'Hlt2LowMultD2KPiRunFrac':0.457761,
  'Hlt2LowMultD2KPiPiRunFrac':0.457761,
  'Hlt2LowMultD2K3PiRunFrac':0.457761,
  'Hlt2LowMultChiC2HHRunFrac':0.457761,
  'Hlt2LowMultChiC2HHHHRunFrac':0.457761,
  'Hlt2LowMultD2KPiWSRunFrac':0.457761,
  'Hlt2LowMultD2KPiPiWSRunFrac':0.457761,
  'Hlt2LowMultD2K3PiWSRunFrac':0.457761,
  'Hlt2LowMultChiC2HHWSRunFrac':0.457761,
  'Hlt2LowMultChiC2HHHHWSRunFrac':0.457761,
  'Hlt2LowMultDDIncRunFrac':0.239294,
  'Hlt2CharmHadD02HHXDst_hhXRunFrac':0.629804,
  'Hlt2CharmHadD02HHXDst_hhXWideMassRunFrac':0.629804,
  'Hlt2DisplVerticesSingleLoosePSRunFrac':0.457761,
  'Hlt2DisplVerticesSingleHighFDRunFrac':0.457761,
  'Hlt2DisplVerticesSingleVeryHighFDRunFrac':0.457761,
  'Hlt2DisplVerticesSingleHighMassRunFrac':0.457761,
  'Hlt2DisplVerticesSinglePSRunFrac':0.457761,
  'Hlt2DisplVerticesDoublePSRunFrac':0.457761,
  'Hlt2CharmHadD2HHHKsLLRunFrac':0.218467,
  'Hlt2CharmHadD2HHHKsDDRunFrac':0.218467,
  'Hlt2KshortToMuMuPiPiRunFrac':0.218467,
  'Hlt2LowMultChiC2PPRunFrac':0.218467,
  'Hlt2LowMultDDIncCPRunFrac':0.218467,
  'Hlt2LowMultDDIncVFRunFrac':0.218467,
  'Hlt2LowMultLMR2HHRunFrac':0.218467,
  'Hlt2HighPtJetsRunFrac':0.218467,
  'Hlt2ChargedHyperon_Xi2Lambda0LLPiRunFrac':0.218467,
  'Hlt2ChargedHyperon_Xi2Lambda0LLMuRunFrac':0.218467,
  'Hlt2ChargedHyperon_Omega2Lambda0LLKRunFrac':0.218467,
  'Hlt2ChargedHyperon_Xi2Lambda0DDPiRunFrac':0.218467,
  'Hlt2ChargedHyperon_Xi2Lambda0DDMuRunFrac':0.218467,
  'Hlt2ChargedHyperon_Omega2Lambda0DDKRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_BaryonhhXRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWideMassRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLWideMassRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLWideMassRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDWideMassRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDWideMassRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_LeptonhhXRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWideMassRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLWideMassRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLWideMassRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDWideMassRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDRunFrac':0.218467,
  'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDWideMassRunFrac':0.218467,


  #"Hlt2CharmHadD02HH_D02PiPiWideMass":0.1,
  #"Hlt2CharmHadD02HH_D02KPiWideMass":0.1,
  #"Hlt2CharmHadD02HH_D02KKWideMass":0.1,
  #"Hlt2Dst2PiD02KPi":0.01,
  #"Hlt2Dst2PiD02PiPi":0.03,
  #"Hlt2Dst2PiD02EMu":0.0,
  #"Hlt2Dst2PiD02KMu":0.15,
}

def get_prescale(line):
  prescale = 1.
  basename = line[4:-12] # remove Dst_ and Decision_TOS
  #try:
    #prescale = prescales[basename]
  #except KeyError:
  ret = {}
  try:
    ret["prescale"] = prescales[basename+"PreScaler"]
    prescale *= prescales[basename+"PreScaler"]
  except KeyError:
    ret["prescale"] = 1.
  try:
    ret["postscale"] = prescales[basename+"PostScaler"]
    prescale *= prescales[basename+"PostScaler"]
  except KeyError:
    ret["postscale"] = 1.
  try:
    ret["active"] = prescales[basename+"RunFrac"]
    prescale *= prescales[basename+"RunFrac"]
  except KeyError:
    ret["active"] = 1.
  return prescale, ret


def find_most_useful(all_lines,best_lines,given_lines = None):
  best_line = ""
  best_line_value = 0.
  best_line_value_no_prescale = 0.
  for line in all_lines:
    if line in best_lines:
      continue
    tmp_lines = [line]
    #if not best_lines == []: tmp_lines += best_lines
    if given_lines == None:
      tmp_lines = [tmp_lines] + [offline_cuts]
    else:
      tmp_lines = [tmp_lines] + given_lines + [offline_cuts]
    #print tmp_lines
    passed, passed_no_prescale = calc_eff(tmp_lines)
    if passed > best_line_value:
      best_line = line
      best_line_value = passed
      best_line_value_no_prescale = passed_no_prescale
  return (best_line, best_line_value, best_line_value_no_prescale)


plots = ["efficiency", "total", "prescale", "postscale", "active"]

def trigger_plots(name,max_lines,lines,given_lines=[]):
  tot, tot_no_prescale = calc_eff([offline_cuts]+given_lines)
  print name, tot, tot_no_prescale
  hists = {}
  for plot in plots:
    hists[plot] = TH1D(name+"_"+plot+"_hist",name+"_"+plot+"_hist;;"+plot.capitalize(),10,0,10)
    hists[plot].SetBit(TH1D.kCanRebin)

  eff = []
  used_lines = []
  while len(used_lines) < max_lines and len(used_lines) < len(lines):
    print len(used_lines) < max_lines, max_lines, len(used_lines), len(used_lines) < len(lines), len(lines)
    next_best_line, value, value_no_prescale = find_most_useful(lines,used_lines,given_lines)
    tot_prescale, scales = get_prescale(next_best_line)
    next_best_line_nice_name = next_best_line.replace("Decision","").replace(name.capitalize(),"").replace("_TOS","")[4:]
    #eff.append(value/tot)
    hists["total"].Fill(next_best_line_nice_name, value/tot)
    hists["efficiency"].Fill(next_best_line_nice_name, value_no_prescale/tot_no_prescale)
    hists["active"].Fill(next_best_line_nice_name, scales["active"])
    hists["prescale"].Fill(next_best_line_nice_name, scales["prescale"])
    hists["postscale"].Fill(next_best_line_nice_name, scales["postscale"])
    print next_best_line, value/tot, value_no_prescale/tot_no_prescale, scales
    used_lines.append(next_best_line)
    eff.append(value/tot)

  for hist_name,hist in hists.iteritems():
    hist.LabelsDeflate()
    hist.Draw()
    hist.SetStats(False)
    hist.GetYaxis().SetDecimals(True)
    hist.GetYaxis().SetRangeUser(0.,1.07)
    hist.GetXaxis().LabelsOption("v")
    
    tc.SaveAs(ds+"_"+name+"_"+hist_name+"_trig.pdf")
    tc.SaveAs(ds+"_"+name+"_"+hist_name+"_trig.png")

  best_lines = used_lines[:lines_per_level]

  #print "two most efficient lines at %.2f%% are:" % (100.*eff[lines_per_level-1]), best_lines
  
  return best_lines, zip(used_lines,eff)


l0_best_lines, l0_good_lines = trigger_plots("l0",10,l0)
hlt1_best_lines, hlt1_good_lines = trigger_plots("hlt1",10,hlt1,[l0_best_lines])
hlt2_best_lines, hlt2_good_lines = trigger_plots("hlt2",15,hlt2,[l0_best_lines,hlt1_best_lines])


#l0_tot = calc_eff([offline_cuts])

#l0_hist = TH1D("l0_hist","l0_hist;;Efficiency",10,0,10)
#l0_hist.SetBit(TH1D.kCanRebin)

#l0_eff = []
#l0_used_lines = []
#while len(l0_used_lines) < 7 and len(l0_used_lines) < len(l0):
  #next_best_line, value = find_most_useful(l0,l0_used_lines)
  #l0_eff.append(value/l0_tot)
  #l0_hist.Fill(next_best_line.replace("Decision","").replace("L0","").replace("_TOS","")[4:], value/l0_tot)
  #l0_used_lines.append(next_best_line)

#l0_hist.LabelsDeflate()
#l0_hist.Draw()
#l0_hist.SetStats(False)
#l0_hist.GetYaxis().SetDecimals(True)
#l0_hist.GetYaxis().SetRangeUser(0.,1.05)
#l0_hist.GetXaxis().LabelsOption("v")

#l0_lines_for_hlt1 = l0_used_lines[:lines_per_level]

#print "two most efficient lines at %.2f%% are:" % (100.*l0_eff[lines_per_level-1]), l0_lines_for_hlt1
#l0_tc.SaveAs(ds+"_l0_trig.pdf")
#l0_tc.SaveAs(ds+"_l0_trig.png")


#hlt1_tc = makeCanvas("hlt1_tc")

#hlt1_tot = calc_eff([offline_cuts,l0_lines_for_hlt1])

#hlt1_hist = TH1D("hlt1_hist","hlt1_hist;;Efficiency",10,0,10)
#hlt1_hist.SetBit(TH1D.kCanRebin)

#hlt1_eff = []
#hlt1_used_lines = []
#while len(hlt1_used_lines) < 7 and len(hlt1_used_lines) < len(hlt1):
  #next_best_line, value = find_most_useful(hlt1,hlt1_used_lines,[l0_lines_for_hlt1])
  #hlt1_eff.append(value/hlt1_tot)
  #hlt1_hist.Fill(next_best_line.replace("Decision","").replace("Hlt1","").replace("_TOS","")[4:], value/hlt1_tot)
  #hlt1_used_lines.append(next_best_line)

#hlt1_hist.LabelsDeflate()
#hlt1_hist.Draw()
#hlt1_hist.SetStats(False)
#hlt1_hist.GetYaxis().SetDecimals(True)
#hlt1_hist.GetYaxis().SetRangeUser(0.,1.05)
#hlt1_hist.GetXaxis().LabelsOption("v")

#hlt1_lines_for_hlt2 = hlt1_used_lines[:lines_per_level]

#print "two most efficient lines at %.2f%% are:" % (100.*hlt1_eff[lines_per_level-1]), hlt1_lines_for_hlt2
#hlt1_tc.SaveAs(ds+"_hlt1_trig.pdf")
#hlt1_tc.SaveAs(ds+"_hlt1_trig.png")


#hlt2_tc = makeCanvas("hlt2_tc")

#hlt2_tot = calc_eff([offline_cuts,hlt1_lines_for_hlt2,l0_lines_for_hlt1])

#hlt2_hist = TH1D("hlt2_hist","hlt2_hist;;Efficiency",10,0,10)
#hlt2_hist.SetBit(TH1D.kCanRebin)

#hlt2_eff = []
#hlt2_used_lines = []
#while len(hlt2_used_lines) < 15 and len(hlt2_used_lines) < len(hlt2):
  #next_best_line, value = find_most_useful(hlt2,hlt2_used_lines,[hlt1_lines_for_hlt2,l0_lines_for_hlt1])
  #hlt2_eff.append(value/hlt2_tot)
  #hlt2_hist.Fill(next_best_line.replace("Decision","").replace("Hlt2","").replace("_TOS","")[4:], value/hlt2_tot)
  #hlt2_used_lines.append(next_best_line)

#hlt2_hist.LabelsDeflate()
#hlt2_hist.Draw()
#hlt2_hist.SetStats(False)
#hlt2_hist.GetYaxis().SetDecimals(True)
#hlt2_hist.GetYaxis().SetRangeUser(0.,1.05)
#hlt2_hist.GetXaxis().LabelsOption("v")

#print "two most efficient lines at %.2f%% are:" % (100.*hlt2_eff[lines_per_level-1]), hlt2_used_lines[:lines_per_level]
#hlt2_tc.SaveAs(ds+"_hlt2_trig.pdf")
#hlt2_tc.SaveAs(ds+"_hlt2_trig.png")

#print "overall eff is %.2f%%"%(100.*hlt2_eff[lines_per_level-1]*hlt1_eff[lines_per_level-1]*l0_eff[lines_per_level-1])

for i in [l0_good_lines,hlt1_good_lines,hlt2_good_lines]:
  for line,eff in i:
    print line.replace("Dst_","").replace("_Dec",""), "& %.1f \\\\"%(100.*eff)
