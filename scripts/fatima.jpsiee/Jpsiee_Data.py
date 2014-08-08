########################################################################
#
# $Id: DaVinci.py,v 1.36 2009/05/20 14:18:09 pkoppenb Exp $
#
# Options for a typical DaVinci job
#
# @date 2008-08-06
#
########################################################################
################ First define all things to run ########################
########################################################################
from DaVinci.Configuration import *
from Gaudi.Configuration import *
from Configurables import GaudiSequencer, DecayTreeTuple, TupleToolDecay, TupleToolTrigger, TupleToolTISTOS, FilterDesktop
from PhysSelPython.Wrappers import AutomaticData, DataOnDemand, Selection, SelectionSequence

mumu = False
Usegrid = True

myEvents = 1000

cutBDTS = False
weightFile= ""
flatteningFile= ""

if cutBDTS:
    weightFile =  "TMVA_7Dec.weights.xml" #"/home/fsoomro/cmtuser/DaVinci_v29r2/Phys/DecayTreeTuple/cmt/TMVA_7Dec.weights.xml"
    flatteningFile =  "HflatBDTS_7Dec.root" #"/home/fsoomro/cmtuser/DaVinci_v29r2/Phys/DecayTreeTuple/cmt/HflatBDTS_7Dec.root"

from Configurables import EventCountHisto,  LoKi__Hybrid__EvtTupleTool,  LoKi__Hybrid__TupleTool
DaVinci().MoniSequence += [EventCountHisto("DaVinciMonitor") ] 

if Usegrid:
    myEvents = -1
    
from Configurables import HltDecReportsDecoder, HltSelReportsDecoder, HltVertexReportsDecoder
DataOnDemandSvc().AlgMap["Hlt/DecReports"] = HltDecReportsDecoder(OutputLevel = WARNING)
DataOnDemandSvc().AlgMap["Hlt/SelReports"] = HltSelReportsDecoder(OutputLevel = WARNING)
DataOnDemandSvc().AlgMap["Hlt/VertexReports"] = HltVertexReportsDecoder( OutputLevel = WARNING)

## --- Input locations for  official blind DSTs in the bkk 
B2JpsiKInput = ""
myDecay = ""

if mumu == True:
    B2JpsiKInput =   "/Event/BsmumuUnblind/Phys/SelBu2JPsiK"
    myDecay = "[B+ -> (^J/psi(1S) -> ^mu+ ^mu-) ^K+ ]cc"
    print "===>  input was ", B2JpsiKInput, "for decay ", myDecay
    
## Jpsi ee inputs on calibration dsts
if mumu == False:
    B2JpsiKInput = "/Event/Calibration/Phys/Jpsi2eeForElectronIDBu2JpsiKLine/Particles"
    myDecay = "[B+ -> (^J/psi(1S) -> ^e+ ^e-) ^K+ ]cc"
    ##print "===>  input was ", B2JpsiKInput, "for decay ", myDecay

## ----  IT clusters decoding  --- ##
from Configurables import RawBankToSTClusterAlg
createITClusters = RawBankToSTClusterAlg("CreateITClusters")
createITClusters.DetType     = "IT"
mySequencer = GaudiSequencer('mySequencer')
mySequencer.Members += [ createITClusters ]

############################
### Configure the ntuple ###
############################

myNTUPLE = DecayTreeTuple('myNTUPLE')   
myNTUPLE.ReFitPVs = True # re-fit the PVs
myNTUPLE.ToolList +=  [  "TupleToolGeometry"
                          , "TupleToolKinematic"
                          , "TupleToolEventInfo"
                          , "TupleToolPid"
                          , "TupleToolPropertime"
                          , "TupleToolRecoStats"
                          , "TupleToolTrigger"
                          , "TupleToolTISTOS"
                          , "TupleToolTrackInfo"
                          , "TupleToolMuonVariables"
                          ,"LoKi::Hybrid::EvtTupleTool/LoKiEvent"
                          #,"LoKi::Hybrid::TupleTool/LoKiTool"
                          ]

## ----------  Store Triggers  ---------##

L0Triggers = ["L0MuonDecision" , "L0DiMuonDecision", "L0HadronDecision", "L0ElectronDecision", "L0ElectronHiDecision", "L0PhotonDecision", "L0PhotonHiDecision" ]
##            ['Muon',               'DiMuon',               '  Hadron',     'Electron',  'Photon','PhotonHi','ElectronHi']

Hlt1Triggers = [  "Hlt1SingleMuonNoIPDecision"  ,"Hlt1SingleMuonHighPTDecision"
                  ,"Hlt1SingleElectronNoIPDecision"
                  ,'Hlt1TrackAllL0Decision'   ,'Hlt1TrackMuonDecision'  ,'Hlt1TrackPhotonDecision'
                  ,"Hlt1DiMuonLowMassDecision" ,"Hlt1DiMuonHighMassDecision"
                  ,'Hlt1MB.*Decision']

Hlt2Triggers = [
    ## muon lines
    "Hlt2SingleMuonDecision", "Hlt2SingleMuonLowPTDecision", "Hlt2SingleMuonHighPTDecision",
    "Hlt2DiMuonDecision",  "Hlt2DiMuonLowMassDecision",
    "Hlt2DiMuonJPsiDecision",  "Hlt2DiMuonJPsiHighPTDecision",  "Hlt2DiMuonPsi2SDecision",
    "Hlt2DiMuonDetachedDecision",  "Hlt2DiMuonDetachedJPsiDecision", "Hlt2DiMuonDetachedHeavyDecision", "Hlt2TriMuonTauDecision",
    ## hadron/Topo lines
    "Hlt2B2HHDecision",
    "Hlt2DiMuonBDecision",  'Hlt2DiMuonZDecision',
    "Hlt2TopoMu2BodyBBDTDecision", "Hlt2TopoMu3BodyBBDTDecision", "Hlt2TopoMu4BodyBBDTDecision",
    "Hlt2Topo2BodyBBDTDecision",   "Hlt2Topo3BodyBBDTDecision",   "Hlt2Topo4BodyBBDTDecision",
    "Hlt2Topo2BodySimpleDecision", "Hlt2Topo3BodySimpleDecision", "Hlt2Topo4BodySimpleDecision",
    "Hlt2TopoE2BodyBBDTDecision","Hlt2TopoE3BodyBBDTDecision","Hlt2TopoE4BodyBBDTDecision",
    ## others for electron
    "Hlt2SingleElectronTFLowPtDecision","Hlt2SingleElectronTFHighPtDecision",
    "Hlt2DiElectronHighMassDecision","Hlt2DiElectronBDecision",
    "Hlt2DiMuonZDecision","Hlt2DiMuonDY1Decision","Hlt2DiMuonDY2Decision"
    "Hlt2DiMuonDY3Decision","Hlt2DiMuonDY4Decision"
    "Hlt2ExpressJPsiDecision","Hlt2ExpressJPsiTagProbeDecision",
    "Hlt2Bs2PhiGammaDecision","Hlt2Bs2PhiGammaWideBMassDecision",
    "Hlt2Bd2KstGammaDecision","Hlt2Bd2KstGammaWideKMassDecision","Hlt2Bd2KstGammaWideBMassDecision"
    ##others
    "Hlt2PassThroughDecision",
    "Hlt2TransparentDecision",
    "Hlt2IncPhiDecision",
    ## inclusive decisions
    ##"Hlt2DiMuonDY.*Decision","Hlt2TopoE.*Decision", "Hlt2Topo.*Decision",  "Hlt2Charm.*Decision", 'Hlt2DiElectron.*Decision', 'Hlt2.*GammaDecision'
    ]

triggerListF = L0Triggers + Hlt1Triggers + Hlt2Triggers

myNTUPLE.addTool(TupleToolTISTOS)
myNTUPLE.TupleToolTISTOS.VerboseL0 = True
myNTUPLE.TupleToolTISTOS.VerboseHlt1 = True
myNTUPLE.TupleToolTISTOS.VerboseHlt2 = True
myNTUPLE.TupleToolTISTOS.OutputLevel = WARNING
myNTUPLE.TupleToolTISTOS.FillL0 = True
myNTUPLE.TupleToolTISTOS.FillHlt1 = True
myNTUPLE.TupleToolTISTOS.FillHlt2 = True
myNTUPLE.TupleToolTISTOS.TriggerList = triggerListF
myNTUPLE.TupleToolTISTOS.PIDList = [511, 521, 531, 443, 13, 11, 321]

############################
###     Make    ntuples  ###
############################
B2JpsiKTuple = myNTUPLE.clone("B2JpsiKTuple")
B2JpsiKTuple.Inputs = [B2JpsiKInput]
B2JpsiKTuple.Decay = myDecay

############################
###   DV configuration ####
############################

from Configurables import DaVinci
DaVinci().EvtMax = myEvents  
DaVinci().SkipEvents = 0
DaVinci().DataType = "2011"
DaVinci().Simulation   = False
DaVinci().Lumi   = True
DaVinci().UserAlgorithms = [ mySequencer ]
DaVinci().MoniSequence += [B2JpsiKTuple]
DaVinci().TupleFile = 'myNtuple.root'
DaVinci().DDDBtag   = 'head-20110914'
DaVinci().CondDBtag = 'head-20111111'
DaVinci().InputType = "DST"

if not(Usegrid):
    ##DaVinci().Input  = [  "DATAFILE='PFN:/home/fsoomro/Test.Unblind.dst' TYP='POOL_ROOTTREE' OPT='READ'"] ##Strip15/16
    DaVinci().Input  = [  "DATAFILE='PFN:/home/fsoomro/BlindDST.dst' TYP='POOL_ROOTTREE' OPT='READ'"] ##Strip17
    ## DaVinci().Input = ["DATAFILE= 'PFN:/castor/cern.ch/grid/lhcb/user/m/mbettler/2011_07/22986/22986612/Test.Unblind.dst' TYP='POOL_ROOTTREE' OPT='READ'",


########################################################################
# HLT
#DaVinci().ReplaceL0BanksWithEmulated = True ## enable if you want to rerun L0
#DaVinci().Hlt2Requires = 'L0+Hlt1'          ## change if you want Hlt2 irrespective of Hlt1
#DaVinci().HltType = 'Hlt1'             ## pick one of 'Hlt1', 'Hlt2', or 'Hlt1+Hlt2'
########################################################################
MessageSvc().Format = "% F%60W%S%7W%R%T %0W%M"
########################################################################
#
# To run : gaudirun.py options/DaVinci.py options/DaVinciTestData.py
#
########################################################################


