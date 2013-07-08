


try:
  stripRun
except NameError:

  #stripRun = True
  #stripConf = "min"
  #stripLine = "emu"
  #dataType = "MC10"
  #blinded = False
  #hltReport = True
  #tupleDecay = "emu"
  #evtMax = -1
  #mag = "down"

  stripRun = False
  stripConf = "default"
  stripLine = "emu"
  dataType = "data"
  blinded = True
  hltReport = False
  tupleDecay = "emu" #"pipi"
  evtMax = -1
  mag = "up"





#0 "pi" "pi"
#1 "mu" "mu"
#2 "K"  "pi"
#3 "e"  "mu"
#4 "K"  "mu"
stripLines = {
  "pipi":0,
  "mumu":1,
  "kpi":2,
  "emu":3,
  "kmu":4
  }

lineNumber = stripLines[stripLine]







from Gaudi.Configuration import *
from LHCbKernel.Configuration import *
from Configurables import FilterDesktop, CombineParticles
from PhysSelPython.Wrappers import Selection, DataOnDemand
from StrippingConf.StrippingLine import StrippingLine
from StrippingUtils.Utils import LineBuilder, checkConfig
from Configurables import DaVinci
from StrippingConf.Configuration import StrippingConf

# Tighten Trk Chi2 to <3
from CommonParticles.Utils import DefaultTrackingCuts
DefaultTrackingCuts().Cuts  = { "Chi2Cut" : [ 0, 3 ],
                                "CloneDistCut" : [5000, 9e+99 ]}
                                #"GhostProbCut" : [-2.0, 0.5 ] }





strConfig ={'PrescalepipiBox'     : 0.5
                 , 'PrescalemumuBox'     : 1.
                 , 'PrescaleKpiBox'    : 0.3
                 , 'PrescaleemuBox'    : 1.
                 , 'PrescaleeKBox'    : 1.
                 , 'PrescaleepiBox'    : 1.
                 , 'PrescalepimuBox'    : 1.
                 , 'PrescaleKmuBox'    : 1.
                 , 'Prescalepipi_untagged_Box'     : 0.2
                 , 'Prescalemumu_untagged_Box'     : 1.
                 , 'PrescaleKpi_untagged_Box'    : 0.2
                 , 'Prescalepimu_untagged_Box'    : 1.
                 , 'PrescaleKmu_untagged_Box'    : 0.2
                 , 'PrescaleKpi_untagged_BoxMB' : 1
                 , 'Prescalepipi_untagged_BoxMB':1
                 , 'PrescaleKpi_untagged_BoxMBTrEff' : 1
                 ,'DMassWin'           : 70.       # MeV
                 ,'DMassWinMuMuLow'    : -150.       #MeV
                 ,'DMassWinMuMuHigh'   : 300       #MeV
                 ,'DMassWinEMu'        : 2000
                 ,'doca'               : 0.4#0.1        # mm
                 ,'XminPT'             : 75.       # MeV
                 ,'XmaxPT'             : 300#1100.      # MeV
                 ,'XminP'              : 2000.      # MeV
                 ,'XTrackChi2'         : 5.        # adimensional
                 ,'XTrackChi2Pi'         : 7.        # adimensional
                 ,'XminIPChi2'         : 1.5#3      # adimensional
                 ,'XmaxIPChi2'         : 8        # adimensional
                 ,'ghostProbCut'       : 0.5      #added for Stripping20 by A Contu
                 ,'DMinFlightChi2'    :  20.
                 ,'DDira'              : 0.9997     # adimensional
                 ,'D0MinPT'            : 800.#1800.      # MeV
                 ,'DMaxIPChi2'        :15.
                 ,'DVChi2'            :10. 
                 ,'PiMinPT'            : 110.       # MeV
                 ,'PiMaxIPCHI2'        : 10.         # adimensional
                 ,'DstMassWin'         : 300.       # MeV
                 ,'DstD0DMWin'         : 10.        # MeV
                 ,'DstD0DMWinMuMu'      : 30.        # MeV  
                 ,'RequireHlt'         : 1          # 
                 ,'prefix'         : '' 
                 }









            
def monHist(name,binMin=0.,binMax=5000.,prefix=""):
  safe = name
  for i in [",","(",")","'","\""," ","<",">","/","\\"]:
    safe = safe.replace(i,"_")
  if not prefix == "":
    safe = prefix + "_" + safe
  if True:
    return "monitor( %s , Gaudi.Histo1DDef( '%s histo', %f , %f) , 'histo_%s' )" %(name,safe,binMin,binMax,safe)
    #return "monitor( %s , 'histo_%s/myDir', 'histo_%s' , Gaudi.Histo1DDef( '%s histo', 0 , 5000) )"%(name,safe,safe,safe)
  else:
    return name



config ={
      'XTrackChi2'         : 5.        # adimensional
      ,'XminIPChi2'         : 0.#3        # adimensional
      ,'ghostProbCut'       : 1.#.5      #added for Stripping20 by A Contu
      ,'doca'               : 3.#0.1        # mm
      ,'DMassWinEMu'        : 1000
      ,'DDira'              : 0.998#0.9997     # adimensional
      ,'DMinFlightChi2'    :  0.#20.
      ,'DMaxIPChi2'        :20.
      ,'DVChi2'            :20. 
      
      ,'PiMinPT'            : 0.#110.       # MeV
      ,'PiMaxIPCHI2'        : 20.         # adimensional
      #,'XTrackChi2Pi'         : 7.        # adimensional
      ,'DstD0DMWin'         : 100.        # MeV
      ,'DstMassWin'         : 1000.       # MeV
      ,'prefix'         : 'Toms' 
    }

xplus = "e"
xminus = "mu"
combname = xplus+xminus

def local_line():

  from StrippingConf.StrippingLine import StrippingLine
  from Configurables import CombineParticles

  d0_comb_daughtercut = "("+monHist("MIPCHI2DV(PRIMARY)",0,50,"X")+"> %(XminIPChi2)s) & ( "+monHist("TRGHOSTPROB",0,1.1,"X")+" < %(ghostProbCut)s )" 
  d0_comb_combcut =  "("+monHist("AMAXDOCA('')",0.,5,"Comb")+"< %(doca)s *mm) & ("+monHist("ADAMASS('D0')",0,2500,"Comb")+"< %(DMassWinEMu)s *MeV) "
  d0_comb_mothercut =    "("+monHist("BPVDIRA",0.99,1,"D")+"> %(DDira)s) & ("+monHist("BPVVDCHI2",0,1000,"D")+"> %(DMinFlightChi2)s) & ("+monHist("MIPCHI2DV(PRIMARY)",0,20,"D")+"< %(DMaxIPChi2)s) & ("+monHist("VFASPF(VCHI2/VDOF)",0,50,"D")+"< %(DVChi2)s)"

  xx_name = "D02"+combname
  d0_comb = CombineParticles( config['prefix']+xx_name )

  inputLoc = {
      "mu" : "Phys/StdAllLooseMuons/Particles",
      "e" : "Phys/StdAllLooseElectrons/Particles"
      }

  req_sel = []
  req_sel.append(DataOnDemand(Location = inputLoc[xplus]))
  req_sel.append(DataOnDemand(Location = inputLoc[xminus]))

  #d0_comb.DecayDescriptors =  ["D0 -> e+ mu- ", "D~0 -> e- mu+ ", "D0 -> e+ mu+ ", "D~0 -> e- mu- " ]
  d0_comb.DecayDescriptors =  ["[D0 -> e+ mu-]cc", "[D0 -> e- mu-]cc"]
  d0_comb.DaughtersCuts = { xplus+"+"  : (d0_comb_daughtercut % config).replace("X_",xplus.upper()+"_"),
                            xminus+"-" : (d0_comb_daughtercut % config).replace("X_",xminus.upper()+"_") }
      
  d0_comb.MotherCut = d0_comb_mothercut  % config
  d0_comb.CombinationCut = d0_comb_combcut % config

  d0_comb_sel = Selection (config['prefix']+xx_name+"Sel", Algorithm = d0_comb, RequiredSelections = req_sel)
  #d0_comb_sel = self.combinetwobody(name, config,xplus, xminus,"forTag")

  dstar_comb_d0cut   = "("+monHist("PT",0,10000,"D0")+">0)"
  dstar_comb_picut   = "("+monHist("PT",0,10000,"Pi")+"> %(PiMinPT)s * MeV) &  ( "+monHist("MIPCHI2DV(PRIMARY)",0,50,"Pi")+"< %(PiMaxIPCHI2)s) "
  dstar_comb_dstcut  = "("+monHist("abs(M-MAXTREE('D0'==ABSID,M)-145.42)",0,500,"Dst")+" < %(DstD0DMWin)s ) & ("+monHist("VFASPF(VCHI2/VDOF)",0,50,"Dst")+"< %(DVChi2)s)"
  dstar_comb_combcut = "("+monHist("ADAMASS('D*(2010)+')",0,3000,"DstComb")+"<%(DstMassWin)s * MeV)"

  dstar_comb = CombineParticles( config['prefix']+"Dst2Pi"+xx_name )
  dstar_comb.DecayDescriptors = ['D*(2010)+ -> D0 pi+', 'D*(2010)+ -> D~0 pi+', 
                                 'D*(2010)- -> D0 pi-', 'D*(2010)- -> D~0 pi-']
  #dstar_comb.DecayDescriptors = ['[D*(2010)+ -> [D0]cc pi+]cc']
  dstar_comb.DaughtersCuts = { "pi+" : dstar_comb_picut % config,
                               "D0"  : dstar_comb_d0cut % config
                              }
  dstar_comb.CombinationCut = dstar_comb_combcut % config
  dstar_comb.MotherCut      = dstar_comb_dstcut % config

  #dstar_comb = self.combineDstar(name, config)
  #dstar_box = dstar_comb.clone(config['prefix']+"Dst2PiD02"+combname+"D0PiComb" )
  dst_req_sel = [DataOnDemand("Phys/StdAllNoPIDsPions/Particles"),
                 DataOnDemand("Phys/StdNoPIDsUpPions/Particles"),
                 d0_comb_sel]

  tag_sel = Selection (config['prefix']+"Dst2PiD02"+combname+"Sel",
                       Algorithm = dstar_comb,
                       RequiredSelections = dst_req_sel)

  # Capitalize particle names to match Hlt2 D*->pi D0-> xx lines
  Xplus  = xplus[0].upper() + xplus[1:]    
  Xminus = xminus[0].upper() + xminus[1:]

  line_box = StrippingLine(config['prefix']+"Dst2PiD02"+combname+"Line",
                            algos = [ tag_sel ], prescale = 1.)

  return line_box








# Now build the stream
from StrippingConf.StrippingStream import StrippingStream
ss = StrippingStream("ByTom")


### CharmFromBSemi module

from StrippingSelections import StrippingDstarD02xx
line = False
if stripConf == "default" or stripConf == "def":
  line = StrippingDstarD02xx.StrippingDstarD02xxConf("DstarD02xx", StrippingDstarD02xx.config_default)
  ss.appendLines( [line.lines()[lineNumber]] )
  stripOutputLoc = line.outputLocations()[lineNumber]
elif stripConf == "min":
  line = local_line()
  ss.appendLines( [line] )
  #stripOutputLoc = "Phys/"+config['prefix']+"Dst2PiD02"+combname+"Line"+"/Particles"
  stripOutputLoc = line.outputLocation()
else:
  line = StrippingDstarD02xx.StrippingDstarD02xxConf("DstarD02xx", strConfig)
  ss.appendLines( [line.lines()[lineNumber]] )
  stripOutputLoc = line.outputLocations()[lineNumber]



from Configurables import  ProcStatusCheck
filterBadEvents =  ProcStatusCheck()

# Configure the stripping using the same options as in Reco06-Stripping10
conf = StrippingConf( HDRLocation = "SomeNonExistingLocation", Streams = [ ss ] )
#conf = StrippingConf( Streams = [ ss ],
                    #AcceptBadEvents = False,
                    #BadEventSelection = filterBadEvents )

#from StrippingArchive import Utils
#line,conf=Utils.lineBuilderAndConf("stripping20r1","DstarD02xx")

#ss.appendLines( [ line ] )










from Configurables import StrippingReport
sr = StrippingReport(Selections = conf.selections())






# get classes to build the SelectionSequence
from PhysSelPython.Wrappers import AutomaticData, Selection, SelectionSequence

# Get the Candidates from the DST. AutomaticData is for data on the DST
if stripRun:
  blind_Sel = AutomaticData(Location = stripOutputLoc)
else:
  blind_Sel = AutomaticData(Location = "/Event/CharmCompleteEvent/" + stripOutputLoc)
  
# Filter the Candidate.  Let's throw away everything above 4 GeV
from Configurables import FilterDesktop
blind_Filter = FilterDesktop('blind_Filter', 
    Code = """( CHILDCUT ( 'D0' == ABSID , 1 ) & (( CHILD(M,1)<1700*MeV) | (CHILD(M,1)>1900*MeV)) ) | ( CHILDCUT ( 'D0' == ABSID , 2 ) & (( CHILD(M,2)<1700*MeV) | (CHILD(M,2)>1900*MeV)) )""")

# make a Selection
blind_FilterSel = Selection(name = 'blind_FilterSel',
                          Algorithm = blind_Filter,
                          RequiredSelections = [ blind_Sel ])

# build the SelectionSequence
blind_Seq = SelectionSequence('blind_Seq',
                             TopSelection = blind_FilterSel,
                            )










## Remove the microbias and beam gas etc events before doing the tagging step
#regexp = "HLT_PASS_RE('Hlt1(?!ODIN)(?!L0)(?!Lumi)(?!Tell1)(?!MB)(?!NZS)(?!Velo)(?!BeamGas)(?!Incident).*Decision')"
#from Configurables import LoKi__HDRFilter
#filterHLT = LoKi__HDRFilter("FilterHLT",Code = regexp )

MessageSvc().Format = "% F%60W%S%7W%R%T %0W%M"

from Configurables import ReadHltReport
from Configurables import FilterDesktop

StdParticles = []
StdParticles.append("Phys/StdAllNoPIDsPions")
StdParticles.append("Phys/StdAllLooseMuons")
StdParticles.append("Phys/StdAllLooseKaons")
StdParticles.append("Phys/StdAllLooseElectrons")
StdParticles.append("Phys/StdAllNoPIDsPions")
StdParticles.append("Phys/StdNoPIDsUpPions")

MakeParticles = FilterDesktop('MakeParticles')
MakeParticles.Inputs=StdParticles
MakeParticles.Code="ALL"

DaVinci().PrintFreq = 500
DaVinci().HistogramFile = 'DV_stripping_histos.root'
DaVinci().TupleFile = "Demu_NTuple.root"
DaVinci().EvtMax = evtMax
#DaVinci().EvtMax = -1
#DaVinci().EventPreFilters = [ filterHLT ]
DaVinci().appendToMainSequence( [ MakeParticles ] )
if stripRun:
  DaVinci().appendToMainSequence( [ conf.sequence() ] )
  DaVinci().appendToMainSequence( [ sr ] )
if hltReport:
  DaVinci().appendToMainSequence( [ ReadHltReport() ] )
if blinded:
  DaVinci().appendToMainSequence( [ blind_Seq.sequence() ] )
DaVinci().InputType = 'DST'

if dataType == "MC10":
  DaVinci().DataType = "2010"
  DaVinci().Simulation = True
  DaVinci().DDDBtag = "head-20101206"
  if mag == "up":
    DaVinci().CondDBtag = "sim-20101210-vc-mu100"
  elif mag == "down":
    DaVinci().CondDBtag = "sim-20101210-vc-md100"
  DaVinci().Lumi = False
elif dataType == "MC11":
  DaVinci().DataType = "2011"
  DaVinci().Simulation = True
  DaVinci().DDDBtag = "MC11-20111102"
  if mag == "up":
    DaVinci().CondDBtag = "sim-20111111-vc-mu100"
  elif mag == "down":
    DaVinci().CondDBtag = "sim-20111111-vc-md100"
  DaVinci().Lumi = False
elif dataType == "data":
  DaVinci().DataType = "2012"
  DaVinci().Simulation = False
  DaVinci().DDDBtag = "dddb-20130111"
  if mag == "up":
    DaVinci().CondDBtag = "cond-20130114"
  elif mag == "down":
    DaVinci().CondDBtag = "cond-20130114"
  DaVinci().Lumi = True

from Configurables import DecayTreeTuple, TupleToolDecay, TupleToolMCTruth, TupleToolMCBackgroundInfo, MCTupleToolHierarchy, TupleToolTrigger, TupleToolTISTOS, TupleToolPropertime, PropertimeFitter, TupleToolKinematic, TupleToolGeometry, TupleToolEventInfo, TupleToolPrimaries, TupleToolPid, TupleToolTrackInfo, TupleToolRecoStats

from PhysSelPython.Wrappers import Selection, SelectionSequence, DataOnDemand, AutomaticData 
from Configurables import LoKi__Hybrid__TupleTool, FitDecayTrees
import GaudiKernel.SystemOfUnits as Units


dttuple = DecayTreeTuple( "Demu_NTuple" )

dttuple.ToolList = [ "TupleToolPropertime"
                  , "TupleToolTrigger"
                  , "TupleToolKinematic"
                  , "TupleToolGeometry"
                  , "TupleToolEventInfo"
                  , "TupleToolPrimaries"
                  , "TupleToolTISTOS"
                  , "TupleToolPid"
                  , "TupleToolTrackInfo"
                  , "TupleToolRecoStats"
                    ]
if blinded:
  dttuple.Inputs = blind_Seq.outputLocations()#[ "Phys/DstarD02xxDst2PiD02pipiBox/Particles" ]
elif stripRun:
  dttuple.Inputs = [ stripOutputLoc ]
else:
  dttuple.Inputs = ["/Event/CharmCompleteEvent/" + stripOutputLoc ]
  #dttuple.Inputs = ["/Event/CharmCompleteEvent/Phys/DstarD02xxDst2PiD02emuBox/Particles" ]
  
print "tuple input :",dttuple.Inputs
print "number of events:", DaVinci().EvtMax
 
#dttuple.Inputs = [ "Phys/DstarD02xxDst2PiD02emuBox/Particles" ]
#dttuple.Decay = "[[D*(2010)+]cc -> (^[D0]cc -> ^e+ ^mu-) ^[pi+]cc]cc"
#dttuple.Decay = "D*(2010)+ -> (^D0 -> ^e+ ^mu-) ^pi+"
#dttuple.Decay = "D*(2010)- -> (^D0 -> ^e+ ^mu-) ^pi-"
#dttuple.Decay = "[[D*(2010)-] -> (^[D0] -> ^e- ^mu+) ^[pi-]]"

if tupleDecay == "ls":
  dttuple.Decay = "[D*(2010)+ -> ([^D0]cc -> [^e+ ^mu+]cc) ^pi+]cc"
  dttuple.Branches = {
    "Dst": "[D*(2010)+]cc: [D*(2010)+ -> ([D0]cc -> [e+ mu+]cc) pi+]cc",
    "D0":  "[D*(2010)+ -> ([^D0]cc -> [e+ mu+]cc) pi+]cc",
    "x1":  "[D*(2010)+ -> ([D0]cc -> [^e+ mu+]cc) pi+]cc",
    "x2":  "[D*(2010)+ -> ([D0]cc -> [e+ ^mu+]cc) pi+]cc",
    "pi":  "[D*(2010)+ -> ([D0]cc -> [e+ mu+]cc) ^pi+]cc"
    }
elif tupleDecay == "emu":
  dttuple.Decay = "[D*(2010)+ -> ([^D0]cc -> [^e-]cc [^mu+]cc) ^pi+]cc"
  dttuple.Branches = {
    "Dst": "[D*(2010)+]cc: [D*(2010)+ -> ([D0]cc -> [e-]cc [mu+]cc) pi+]cc",
    "D0":  "[D*(2010)+ -> ([^D0]cc -> [e-]cc [mu+]cc) pi+]cc",
    "x1":  "[D*(2010)+ -> ([D0]cc -> [^e-]cc [mu+]cc) pi+]cc",
    "x2":  "[D*(2010)+ -> ([D0]cc -> [e-]cc [^mu+]cc) pi+]cc",
    "pi":  "[D*(2010)+ -> ([D0]cc -> [e-]cc [mu+]cc) ^pi+]cc"
    }
  
elif tupleDecay == "pipi":
  dttuple.Decay = "[D*(2010)+ -> ([^D0]cc -> [^pi-]cc [^pi+]cc) ^pi+]cc"
  dttuple.Branches = {
    "Dst": "[D*(2010)+]cc: [D*(2010)+ -> ([D0]cc -> [pi-]cc [pi+]cc) pi+]cc",
    "D0":  "[D*(2010)+ -> ([^D0]cc -> [pi-]cc [pi+]cc) pi+]cc",
    "x1":  "[D*(2010)+ -> ([D0]cc -> [^pi-]cc [pi+]cc) pi+]cc",
    "x2":  "[D*(2010)+ -> ([D0]cc -> [pi-]cc [^pi+]cc) pi+]cc",
    "pi":  "[D*(2010)+ -> ([D0]cc -> [pi-]cc [pi+]cc) ^pi+]cc"
    }
  
elif tupleDecay == "mumu":
  dttuple.Decay = "[D*(2010)+ -> ([^D0]cc -> [^mu-]cc [^mu+]cc) ^pi+]cc"
  dttuple.Branches = {
    "Dst": "[D*(2010)+]cc: [D*(2010)+ -> ([D0]cc -> [mu-]cc [mu+]cc) pi+]cc",
    "D0":  "[D*(2010)+ -> ([^D0]cc -> [mu-]cc [mu+]cc) pi+]cc",
    "x1":  "[D*(2010)+ -> ([D0]cc -> [^mu-]cc [mu+]cc) pi+]cc",
    "x2":  "[D*(2010)+ -> ([D0]cc -> [mu-]cc [^mu+]cc) pi+]cc",
    "pi":  "[D*(2010)+ -> ([D0]cc -> [mu-]cc [mu+]cc) ^pi+]cc"
    }


dttuple.TupleName = "Demu_NTuple"

dttuple.addTool( TupleToolPropertime() )

dttuple.addTool( TupleToolTISTOS() )
dttuple.TupleToolTISTOS.VerboseL0 = True
dttuple.TupleToolTISTOS.VerboseHlt1 = True
dttuple.TupleToolTISTOS.VerboseHlt2 = True
dttuple.TupleToolTISTOS.Verbose = True
dttuple.TupleToolTISTOS.TriggerList = [
  "L0Global",
  "L0DiMuonDecision",
  "L0ElectronDecision",
  "L0HadronDecision",
  "L0MuonDecision",
  "L0MuonHighDecision",
  "L0PhotonDecision",
  "Hlt1Global",
  "Hlt1SingleMuonNoIPL0Decision",
  "Hlt1TrackAllL0Decision",
  "Hlt1TrackMuonDecision",
  "Hlt1SingleMuonNoIPL0HighPTDecision",
  "Hlt2Global",
  "Hlt2Dst2PiD02EMuDecision",
  "Hlt2Dst2PiD02KMuDecision",
  "Hlt2Dst2PiD02KPiDecision",
  "Hlt2Dst2PiD02MuMuDecision",
  "Hlt2Dst2PiD02PiMuDecision",
  "Hlt2Dst2PiD02PiPiDecision",
  "Hlt2BiasedDiMuonIPDecision",
  "Hlt2CharmOSTF2BodyDecision",
  "Hlt2CharmOSTF3BodyDecision",
  "Hlt2IncPhiRobustDecision",
  "Hlt2IncPhiSidebandsDecision",
  "Hlt2IncPhiTrackFitDecision",
  "Hlt2MuTrackDecision",
  "Hlt2PromptJPsiDecision",
  "Hlt2TopoOSTF2BodyDecision",
  "Hlt2TopoOSTF3BodyDecision",
  "Hlt2TopoOSTF4BodyDecision",
  "Hlt2diphotonDiMuonDecision",
  "Hlt2UnbiasedDiMuonLowMassDecision"
  ]

D_variables = {"DIRA": "BPVDIRA",
               "IP": "IPMIN",
               "IPChi2": "BPVVDCHI2",
               # Min IP wrt all primary verticies
               "MinIP_PRIMARY": "MIPDV(PRIMARY)",
               "MinIPChi2_PRIMARY": "MIPCHI2DV(PRIMARY)",
               "VChi2_per_NDOF": "VFASPF(VCHI2/VDOF)",
               #"AMAXDOCA": "AMAXDOCA('')",
             }
# XXX How to calculate the DOCA of the two leptons?
lepton_variables = {"TOMPT": "PT",
                    "TOMP": "P",
                    "TRCHI2DOF": "TRCHI2DOF",
                    "TRGHOSTPROB": "TRGHOSTPROB",
                    "IP": "IPMIN",
                    # XXX should this be BPVIPCHI2()?
                    "IPChi2": "BPVVDCHI2",
                    # Min IP wrt all primary verticies
                    "MinIP_PRIMARY": "MIPDV(PRIMARY)",
                    "MinIPChi2_PRIMARY": "MIPCHI2DV(PRIMARY)",
                    "VChi2_per_NDOF": "VFASPF(VCHI2/VDOF)",
}
dttuple.addTool(TupleToolDecay, name = "x2")
LoKi_x2=LoKi__Hybrid__TupleTool("LoKi_x2")
LoKi_x2.Variables = lepton_variables
dttuple.x2.addTool(LoKi_x2)
dttuple.x2.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_x2"]

dttuple.addTool(TupleToolDecay, name = "x1")
LoKi_x1=LoKi__Hybrid__TupleTool("LoKi_x1")
LoKi_x1.Variables = lepton_variables
dttuple.x1.addTool(LoKi_x1)
dttuple.x1.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_x1"]

dttuple.addTool(TupleToolDecay, name="D0")
LoKi_D0=LoKi__Hybrid__TupleTool("LoKi_D0")
LoKi_D0.Variables = D_variables
dttuple.D0.addTool(LoKi_D0)
dttuple.D0.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_D0"]

dttuple.addTool(TupleToolDecay, name="Dst")
LoKi_Dst=LoKi__Hybrid__TupleTool("LoKi_Dst")
LoKi_Dst.Variables = D_variables
dttuple.Dst.addTool(LoKi_Dst)
dttuple.Dst.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_Dst"]


if "MC" in dataType:
  dttuple.addTool(TupleToolMCBackgroundInfo, name="TupleToolMCBackgroundInfo")
  dttuple.TupleToolMCBackgroundInfo.Verbose=True
  dttuple.addTool(TupleToolMCTruth, name="truth")
  dttuple.truth.ToolList+=["MCTupleToolHierarchy"]
  dttuple.ToolList+=["TupleToolMCBackgroundInfo/TupleToolMCBackgroundInfo"]
  dttuple.ToolList+=["TupleToolMCTruth/truth"]



#from Configurables import DaVinci, PrintDecayTree, GaudiSequencer
#from Configurables import LoKi__HDRFilter
#TupleSeq = GaudiSequencer('TupleSeq')
##pt = PrintDecayTree(Inputs = [ location ])
#sf = LoKi__HDRFilter( 'StripPassFilter', Code="HLT_PASS('StrippingDstarD02xxDst2PiD02emuBoxDecision')", Location="/Event/Strip/Phys/DecReports" )
#TupleSeq.Members = [ sf, dttuple ]
#DaVinci().appendToMainSequence( [ TupleSeq ] )



DaVinci().appendToMainSequence( [ dttuple ] )
