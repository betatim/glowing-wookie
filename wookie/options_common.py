


#try:
  #stripRun
#except NameError:

  ##stripRun = True
  ##stripConf = "min"
  ##stripLine = "emu"
  ##dataType = "MC10"
  ##blinded = False
  ##hltReport = True
  ##tupleDecay = "emu"
  ##evtMax = -1
  ##mag = "down"

  #stripRun = True
  #stripConf = "default"
  #stripLine = "emu"
  #dataType = "MC10" #"data"
  #blinded = False
  #hltReport = False
  #tupleDecay = "emu" #"pipi"
  #evtMax = -1
  #mag = "up"












import sys

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






def local_line(config, xplus = "e", xminus = "mu"):

  combname = xplus+xminus

  from StrippingConf.StrippingLine import StrippingLine
  from Configurables import CombineParticles
  from PhysSelPython.Wrappers import Selection, DataOnDemand

  xx_name = "D02"+combname
  d0_comb = CombineParticles( config['prefix']+xx_name )
  d0_comb.Preambulo = ["from LoKiPhysMC.decorators import *" , "from LoKiPhysMC.functions import mcMatch"]


  inputLoc = {
      #"mu" : "Phys/StdAllLooseMuons/Particles",
      #"e" : "Phys/StdAllLooseElectrons/Particles",
      "mu" : "Phys/StdNoPIDsMuons/Particles",
      "e" : "Phys/StdNoPIDsElectrons/Particles",
      }

  req_sel = []
  req_sel.append(DataOnDemand(Location = inputLoc[xplus]))
  req_sel.append(DataOnDemand(Location = inputLoc[xminus]))

  #d0_comb.DecayDescriptors =  ["D0 -> e+ mu- ", "D~0 -> e- mu+ ", "D0 -> e+ mu+ ", "D~0 -> e- mu- " ]
  d0_comb.DecayDescriptors =  ["[D0 -> %s+ %s-]cc" % (xplus, xminus)]
  d0_comb.DaughtersCuts = { xplus+"+"  : "mcMatch('[D0 => ^%s+ %s-]CC') | mcMatch('[D0 => ^%s- %s+]CC') | mcMatch('[D0 => ^%s- %s-]CC')" % ((xplus, xminus)*3),
                            xminus+"-" : "mcMatch('[D0 => %s+ ^%s-]CC') | mcMatch('[D0 => %s- ^%s+]CC') | mcMatch('[D0 => %s- ^%s-]CC')" % ((xplus, xminus)*3) }

  d0_comb.CombinationCut = "AMAXCHILD(PT)>0*MeV"
  d0_comb.MotherCut = "PT>0*MeV"

  d0_comb_sel = Selection (config['prefix']+xx_name+"Sel", Algorithm = d0_comb, RequiredSelections = req_sel)
  #d0_comb_sel = self.combinetwobody(name, config,xplus, xminus,"forTag")

  dstar_comb_d0cut   = "("+monHist("PT",0,10000,"D0")+">0)"
  dstar_comb_picut   = "("+monHist("PT",0,10000,"Pi")+"> %(PiMinPT)s * MeV) &  ( "+monHist("MIPCHI2DV(PRIMARY)",0,50,"Pi")+"< %(PiMaxIPCHI2)s) "
  dstar_comb_dstcut  = "("+monHist("abs(M-MAXTREE('D0'==ABSID,M)-145.42)",0,500,"Dst")+" < %(DstD0DMWin)s ) & ("+monHist("VFASPF(VCHI2/VDOF)",0,50,"Dst")+"< %(DVChi2)s)"
  dstar_comb_combcut = "("+monHist("ADAMASS('D*(2010)+')",0,3000,"DstComb")+"<%(DstMassWin)s * MeV)"

  dstar_comb = CombineParticles( config['prefix']+"Dst2Pi"+xx_name )
  dstar_comb.DecayDescriptors = ['D*(2010)+ -> D0 pi+', 'D*(2010)- -> D~0 pi-']
  #dstar_comb.DecayDescriptors = ['[D*(2010)+ -> [D0]cc pi+]cc']
  dstar_comb.DaughtersCuts = { "pi+" : "mcMatch('D*(2010)+ -> D0 ^pi+') | mcMatch('D*(2010)+ -> D~0 ^pi+') | mcMatch('D*(2010)- -> D0 ^pi-') | mcMatch('D*(2010)- -> D~0 ^pi-')",
                               "D0"  : "mcMatch('D*(2010)+ -> ^D0 pi+') | mcMatch('D*(2010)+ -> ^D~0 pi+') | mcMatch('D*(2010)- -> ^D0 pi-') | mcMatch('D*(2010)- -> ^D~0 pi-')"
                              }
  dstar_comb.CombinationCut = "AMAXCHILD(PT)>0*MeV"
  dstar_comb.MotherCut      = "PT>0*MeV"

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

  return line_box, tag_sel



def likesign_line(config, xplus = "e", xminus = "mu"):
  from StrippingConf.StrippingLine import StrippingLine
  from Configurables import CombineParticles
  from PhysSelPython.Wrappers import DataOnDemand, Selection

  name = "DstarD02xxLs"

  if(xplus == "mu") and (xminus == "mu") :
      d0comb_combcut =       "(AMAXDOCA('')< %(doca)s *mm) & (DAMASS('D0')< %(DMassWinMuMuHigh)s *MeV) & (DAMASS('D0')> %(DMassWinMuMuLow)s *MeV) & (AMAXCHILD(PT)>%(XmaxPT)s *MeV) & (APT> %(D0MinPT)s)"
  elif (((xplus == "mu") and (xminus == "e")) or ((xplus == "e") and (xminus == "mu"))) :
      d0comb_combcut =       "(AMAXDOCA('')< %(doca)s *mm) & (ADAMASS('D0')< %(DMassWinEMu)s *MeV) & (AMAXCHILD(PT)>%(XmaxPT)s *MeV) & (APT> %(D0MinPT)s)"
  else :
      d0comb_combcut =       "(AMAXDOCA('')< %(doca)s *mm) & (ADAMASS('D0')< %(DMassWin)s *MeV) & (AMAXCHILD(PT)>%(XmaxPT)s *MeV) & (APT> %(D0MinPT)s)"

  d0comb_childcut = "(PT> %(XminPT)s *MeV) & (P>%(XminP)s *MeV) & (TRCHI2DOF<%(XTrackChi2)s) & (MIPCHI2DV(PRIMARY)> %(XminIPChi2)s) & ( TRGHOSTPROB < %(ghostProbCut)s )"
  d0comb_d0cut = "(BPVDIRA> %(DDira)s) & (INGENERATION( (MIPCHI2DV(PRIMARY)>%(XmaxIPChi2)s),1 ) ) & (BPVVDCHI2> %(DMinFlightChi2)s) & (MIPCHI2DV(PRIMARY)< %(DMaxIPChi2)s) & (VFASPF(VCHI2/VDOF)< %(DVChi2)s)"
  xx_name = "D02"+xplus+xminus+"forTag"
  xx_comb = CombineParticles( config['prefix']+xx_name )

  inputLoc = {
       "pi" : "Phys/StdAllNoPIDsPions/Particles"
      ,"mu" : "Phys/StdAllLooseMuons/Particles"
      ,"K" : "Phys/StdAllLooseKaons/Particles"
      ,"e" : "Phys/StdAllLooseElectrons/Particles"
      }
  req_sel = []
  if xplus != xminus :
      decays = ["D0 -> "+ xplus + "+ " + xminus + "+ ", "D0 -> "+ xplus + "- " + xminus + "- " ]
      xx_comb.DecayDescriptors =  decays
      xx_comb.DaughtersCuts = { xplus+"+" : d0comb_childcut % config
                                , xminus+"+" : d0comb_childcut % config }
      req_sel.append(DataOnDemand(Location = inputLoc[xplus]))
      req_sel.append(DataOnDemand(Location = inputLoc[xminus]))
  else:
      decay = "D0 -> "+ xplus + "+ " + xminus + "+ "
      xx_comb.DecayDescriptor =  decay
      xx_comb.DaughtersCuts = { xplus+"+" : d0comb_childcut % config }
      req_sel.append(DataOnDemand(Location = inputLoc[xplus]))
  xx_comb.MotherCut = d0comb_d0cut  % config
  xx_comb.CombinationCut = d0comb_combcut % config

  xxCombSel = Selection (name+"seq_"+xx_name+"_selection", Algorithm = xx_comb, RequiredSelections = req_sel)


  from Configurables import CombineParticles
  dstcomb_dstcut       =  "(abs(M-MAXTREE('D0'==ABSID,M)-145.42) < %(DstD0DMWin)s ) & (VFASPF(VCHI2/VDOF)< %(DVChi2)s)"
  dstcomb_combcut =  "(ADAMASS('D*(2010)+')<%(DstMassWin)s * MeV)"
  dstcomb_picut = "(PT> %(PiMinPT)s * MeV) &  ( MIPCHI2DV(PRIMARY)< %(PiMaxIPCHI2)s) & (TRCHI2DOF<%(XTrackChi2Pi)s) "
  dstcomb_d0cut = "PT>0"

  dstar = CombineParticles( config['prefix']+"combine" )
  #dstar.DecayDescriptors = ['[D*(2010)+ -> D0 pi+]cc']
  dstar.DecayDescriptors = ['D*(2010)+ -> D0 pi+', 'D*(2010)- -> D0 pi-']
  dstar.DaughtersCuts = {    "pi+" : dstcomb_picut % config ,
                              "D0"    : dstcomb_d0cut % config
                              }
  dstar.CombinationCut = dstcomb_combcut % config
  dstar.MotherCut =  dstcomb_dstcut % config


  combname = xplus+xminus
  dstar_box = dstar.clone(name+config['prefix']+"Dst2PiD02"+combname+"D0PiComb" )
  dst_req_sel = [DataOnDemand( "Phys/StdAllNoPIDsPions/Particles" ) ,
                  DataOnDemand( "Phys/StdNoPIDsUpPions/Particles"),
                  xxCombSel]

  pres = "Prescale"+combname+"Box"
  _tag_sel = Selection (name+"_seq_"+combname+"_box",
                        Algorithm = dstar_box,
                        RequiredSelections = dst_req_sel)####

  # Capitalize particle names to match Hlt2 D*->pi D0-> xx lines
  Xplus  = xplus[0].upper() + xplus[1:]
  Xminus = xminus[0].upper() + xminus[1:]

  if (xplus == "e" and xminus =="mu") or (xplus == "mu" and xminus == "e"):
      line_box = StrippingLine(name+config['prefix']+"Dst2PiD02"+combname+"Box",
                                algos = [ _tag_sel ],
                                prescale = 1.)

  else:
      hltname = "Hlt2Dst2PiD02"+Xplus+Xminus+"*Decision"  # * matches Signal, Sidebands and Box lines
      line_box = StrippingLine(name+config['prefix']+"Dst2PiD02"+combname+"Box",
                                HLT = "HLT_PASS_RE('"+hltname+"')",
                                algos = [ _tag_sel ], prescale = 1.)
  return line_box, _tag_sel







from Gaudi.Configuration import *
from LHCbKernel.Configuration import *


def execute(stripRun, stripConf, stripLine, dataType, blinded, hltReport, tupleDecay, evtMax, mag, outputType="ntuple", strippingStream = "CharmCompleteEvent"):

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

  #strippingStream = "CharmCompleteEvent"

  #MessageSvc().Format = "% F%280W%S%7W%R%T %60W%M"


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
                  , 'PrescaleeKBox'     : 1.
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



  # Now build the stream
  from StrippingConf.StrippingStream import StrippingStream
  ss = StrippingStream("ByTom")


  ### CharmFromBSemi module

  selection = False

  from StrippingSelections import StrippingDstarD02xx
  line = False
  if stripConf == "default" or stripConf == "def":
    def_str_no_pre = StrippingDstarD02xx.config_default
    for key, val in def_str_no_pre.iteritems():
      if "Prescale" in key:
        def_str_no_pre[key] = 1.0
    line = StrippingDstarD02xx.StrippingDstarD02xxConf("DstarD02xx", def_str_no_pre)
    ss.appendLines( [line.lines()[lineNumber]] )
    stripOutputLoc = line.outputLocations()[lineNumber]
  elif stripConf == "nopid":
    def_str_no_pre = StrippingDstarD02xx.config_default
    for key, val in def_str_no_pre.iteritems():
      if "Prescale" in key:
        def_str_no_pre[key] = 1.0
    def_str_no_pre["NoPID"] = True
    line = StrippingDstarD02xx.StrippingDstarD02xxConf("DstarD02xx", def_str_no_pre)
    ss.appendLines( [line.lines()[lineNumber]] )
    stripOutputLoc = line.outputLocations()[lineNumber]
  elif stripConf == "min" or stripConf == "minimal" :
    if stripLine == "emu":
      line, selection = local_line(config, "mu","e")
    elif stripLine == "pipi":
      line, selection = local_line(config, "pi","pi")
    else:
      sys.exit("not implemented")
    ss.appendLines( [line] )
    #stripOutputLoc = "Phys/"+config['prefix']+"Dst2PiD02"+combname+"Line"+"/Particles"
    stripOutputLoc = line.outputLocation()
  elif stripConf == "ls" or stripConf == "likesign" :
    if stripLine == "emu":
      line, selection = likesign_line(StrippingDstarD02xx.config_default, "e","mu")
    elif stripLine == "pipi":
      line, selection = likesign_line(StrippingDstarD02xx.config_default, "pi","pi")
    else:
      sys.exit("not implemented")
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
    blind_Sel = AutomaticData(Location = "/Event/"+strippingStream+"/" + stripOutputLoc)

  # Filter the Candidate.  Let's throw away everything above 4 GeV
  from Configurables import FilterDesktop
  blind_Filter = FilterDesktop('blind_Filter',
      Code = """( CHILDCUT ( 'D0' == ABSID , 1 ) & (( CHILD(M,1)<1800*MeV) | (CHILD(M,1)>1900*MeV)) ) | ( CHILDCUT ( 'D0' == ABSID , 2 ) & (( CHILD(M,2)<1800*MeV) | (CHILD(M,2)>1900*MeV)) )""")

  blind_FilterSel = Selection(name = 'blind_FilterSel',
                            Algorithm = blind_Filter,
                            RequiredSelections = [ blind_Sel ])

  blind_Seq = SelectionSequence('blind_Seq',
                              TopSelection = blind_FilterSel,
                              )






  ## Remove the microbias and beam gas etc events before doing the tagging step
  #regexp = "HLT_PASS_RE('Hlt1(?!ODIN)(?!L0)(?!Lumi)(?!Tell1)(?!MB)(?!NZS)(?!Velo)(?!BeamGas)(?!Incident).*Decision')"
  #from Configurables import LoKi__HDRFilter
  #filterHLT = LoKi__HDRFilter("FilterHLT",Code = regexp )

  MessageSvc().Format = "% F%60W%S%7W%R%T %0W%M"

  from Configurables import ReadHltReport, RawEventDump
  from Configurables import FilterDesktop

  #from Configurables import DataOnDemandSvc, L0SelReportsMaker, L0DecReportsMaker
  #DataOnDemandSvc().AlgMap["HltLikeL0/DecReports"] = L0DecReportsMaker()
  #DataOnDemandSvc().AlgMap["HltLikeL0/SelReports"] = L0SelReportsMaker()
  #from Configurables import L0Conf
  #L0Conf().FullL0MuonDecoding = True
  #L0Conf().EnableL0DecodingOnDemand = True

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
  storeExp = StoreExplorerAlg()
  storeExp.Load = 1
  storeExp.PrintFreq = 5.0

  #DaVinci().appendToMainSequence( [ storeExp ] )
  #DaVinci().appendToMainSequence( [ MakeParticles ] )
  if stripRun:
    DaVinci().appendToMainSequence( [ conf.sequence() ] )
    DaVinci().appendToMainSequence( [ sr ] )
  if hltReport:
    DaVinci().appendToMainSequence( [ ReadHltReport() ] )
  if blinded:
    DaVinci().appendToMainSequence( [ blind_Seq.sequence() ] )
  DaVinci().InputType = 'DST'

  a = "->"

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
  elif dataType == "MC11a":
    DaVinci().DataType = "2011"
    DaVinci().Simulation = True
    DaVinci().DDDBtag = "MC11-20111102"
    if mag == "up":
      DaVinci().CondDBtag = "sim-20111111-vc-mu100"
    elif mag == "down":
      DaVinci().CondDBtag = "sim-20111111-vc-md100"
    DaVinci().Lumi = False
  elif dataType == "MC2012":
    DaVinci().DataType = "2012"
    DaVinci().Simulation = True
    DaVinci().DDDBtag = "Sim08-20130503-1"
    if mag == "up":
      DaVinci().CondDBtag = "Sim08-20130503-1-vc-mu100"
    elif mag == "down":
      DaVinci().CondDBtag = "Sim08-20130503-1-vc-md100"
    DaVinci().Lumi = False
  elif dataType == "MC2011":
    DaVinci().DataType = "2011"
    DaVinci().Simulation = True
    DaVinci().DDDBtag = "Sim08-20130503"
    if mag == "up":
      DaVinci().CondDBtag = "Sim08-20130503-vc-mu100"
    elif mag == "down":
      DaVinci().CondDBtag = "Sim08-20130503-vc-md100"
    DaVinci().Lumi = False
  elif dataType == "data2012":
    a = "->"
    DaVinci().DataType = "2012"
    DaVinci().Simulation = False
    DaVinci().DDDBtag = "dddb-20130111"
    if mag == "up":
      DaVinci().CondDBtag = "cond-20130114"
    elif mag == "down":
      DaVinci().CondDBtag = "cond-20130114"
    DaVinci().Lumi = True
  elif dataType == "data2011":
    a = "->"
    DaVinci().DataType = "2011"
    DaVinci().Simulation = False
    DaVinci().DDDBtag = "dddb-20130111"
    if mag == "up":
      DaVinci().CondDBtag = "cond-20130114"
    elif mag == "down":
      DaVinci().CondDBtag = "cond-20130114"
    DaVinci().Lumi = True
  elif dataType == "data":
    sys.exit("correct the dataType to include the year")


  if not stripRun and (stripConf == "ls" or stripConf == "likesign"):
    DaVinci().RootInTES = '/Event/lsdata/Phys/dst_FilterSel'


  from Configurables import DecayTreeTuple, TupleToolDecay, TupleToolMCTruth
  from Configurables import TupleToolMCBackgroundInfo, MCTupleToolHierarchy
  from Configurables import TupleToolTrigger, TupleToolTISTOS, TupleToolPropertime
  from Configurables import PropertimeFitter, TupleToolKinematic, TupleToolGeometry
  from Configurables import TupleToolEventInfo, TupleToolPrimaries, TupleToolPid
  from Configurables import TupleToolTrackInfo, TupleToolRecoStats, TupleToolSelReport

  from PhysSelPython.Wrappers import Selection, SelectionSequence, DataOnDemand, AutomaticData
  from Configurables import LoKi__Hybrid__TupleTool, FitDecayTrees, TupleToolDecayTreeFitter
  import GaudiKernel.SystemOfUnits as Units

  if outputType in ["ntuple", "nt", "tuple", "root"]:
    from DecayTreeTuple.Configuration import *

    dttuple = DecayTreeTuple( "Demu_NTuple" )

    dttuple.ToolList = ["TupleToolGeometry",
                        "TupleToolEventInfo",
                        "TupleToolGeometry",
                        "TupleToolKinematic",
                        "TupleToolPrimaries",
                        "TupleToolPropertime",
                        "TupleToolTrackInfo",
                        "TupleToolAngles",
                        "TupleToolPid",
                        "TupleToolRICHPid",
                        "TupleToolDecay",
                        #"TupleToolGeneration",
                        "TupleToolTrigger",
                        "TupleToolTrackIsolation",
                        "TupleToolTrackInfo",
                        "TupleToolTrackPosition",
                        "TupleToolBremInfo",
                        "TupleToolTrigger",
                        "TupleToolTISTOS",
                        "TupleToolSelReport",
                        "TupleToolTrackInfo",
                        "TupleToolRecoStats",
                        "TupleToolDira",
                        ]
    if blinded:
      dttuple.Inputs = blind_Seq.outputLocations()
    elif stripRun:
      dttuple.Inputs = [ stripOutputLoc ]
    elif not stripRun and (stripConf == "ls" or stripConf == "likesign"):
      appendPostConfigAction(pleaseWorkNow)
      dttuple.Inputs = [ "lsdata/"+stripOutputLoc, "lsdata/Phys/dst_FilterSel/Particles" ]
      #dttuple.Inputs = [ stripOutputLoc ]
      #dttuple.Inputs = [ "/Event/"+strippingStream+"/" + stripOutputLoc ]
      #dttuple.Inputs = [ "lsdata/Phys/dst_FilterSel/Particles" ]
      #dttuple.Inputs = [ "/Event/lsdata/Phys/DstarD02xxLsseq_D02emuforTag_selection/Particles" ]
      #/DstarD02xxLsseq_D02emuforTag_selection
    else:
      dttuple.Inputs = [ "/Event/"+strippingStream+"/" + stripOutputLoc ]
      #dttuple.Inputs = ["/Event/"+strippingStream+"/Phys/DstarD02xxDst2PiD02emuBox/Particles" ]

    print "tuple input :",dttuple.Inputs
    print "number of events:", DaVinci().EvtMax

    if tupleDecay == "lsemu":
      dttuple.Decay = "[D*(2010)+ "+a+" ^([([D0]cc "+a+" ^e+ ^mu+),([D0]cc "+a+" ^e- ^mu-)]) ^pi+]CC"
      dttuple.addBranches ({
        "Dst": "[D*(2010)+ "+a+" ([([D0]cc "+a+" e+ mu+),([D0]cc "+a+" e- mu-)]) pi+]CC",
        "D0":  "[D*(2010)+ "+a+" ^([([D0]cc "+a+" e+ mu+),([D0]cc "+a+" e- mu-)]) pi+]CC",
        "x1":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" ^e+ mu+),([D0]cc "+a+" ^e- mu-)]) pi+]CC",
        "x2":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" e+ ^mu+),([D0]cc "+a+" e- ^mu-)]) pi+]CC",
        "pi":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" e+ mu+),([D0]cc "+a+" e- mu-)]) ^pi+]CC"
        })
    elif tupleDecay == "emu":
      dttuple.Decay = "[D*(2010)+ "+a+" ^([D0]cc "+a+" ^[e+]cc ^[mu-]cc) ^pi+]CC"
      dttuple.addBranches ({
        "Dst": "[D*(2010)+ "+a+" ([([D0]cc "+a+" e- mu+),([D0]cc "+a+" e+ mu-)]) pi+]CC",
        "D0":  "[D*(2010)+ "+a+" ^([([D0]cc "+a+" e- mu+),([D0]cc "+a+" e+ mu-)]) pi+]CC",
        "x1":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" ^e- mu+),([D0]cc "+a+" ^e+ mu-)]) pi+]CC",
        "x2":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" e- ^mu+),([D0]cc "+a+" e+ ^mu-)]) pi+]CC",
        "pi":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" e- mu+),([D0]cc "+a+" e+ mu-)]) ^pi+]CC"
        })
      #dttuple.Decay = "[D*(2010)+ -> ([^D0]CC -> [^e-]CC [^mu+]CC) ^pi+]CC"
      #dttuple.addBranches ({
        #"Dst": "^[D*(2010)+ -> ([D0]CC -> [e-]CC [mu+]CC) pi+]CC",
        #"D0":  "[D*(2010)+ -> ([^D0]CC -> [e-]CC [mu+]CC) pi+]CC",
        #"x1":  "[D*(2010)+ -> ([D0]CC -> [^e-]CC [mu+]CC) pi+]CC",
        #"x2":  "[D*(2010)+ -> ([D0]CC -> [e-]CC [^mu+]CC) pi+]CC",
        #"pi":  "[D*(2010)+ -> ([D0]CC -> [e-]CC [mu+]CC) ^pi+]CC"
        #})
    elif tupleDecay == "kpi":
      dttuple.Decay = "[D*(2010)+ "+a+" ^([D0]cc "+a+" ^[K+]cc ^[pi-]cc) ^pi+]CC"
      dttuple.addBranches ({
        "Dst": "[D*(2010)+ "+a+" ([([D0]cc "+a+" K- pi+),([D0]cc "+a+" K+ pi-)]) pi+]CC",
        "D0":  "[D*(2010)+ "+a+" ^([([D0]cc "+a+" K- pi+),([D0]cc "+a+" K+ pi-)]) pi+]CC",
        "x1":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" ^K- pi+),([D0]cc "+a+" ^K+ pi-)]) pi+]CC",
        "x2":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" K- ^pi+),([D0]cc "+a+" K+ ^pi-)]) pi+]CC",
        "pi":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" K- pi+),([D0]cc "+a+" K+ pi-)]) ^pi+]CC"
        })

    elif tupleDecay == "pipi":
      dttuple.Decay = "[D*(2010)+ "+a+" ^([D0]cc "+a+" ^[pi+]cc ^[pi-]cc) ^pi+]CC"
      dttuple.addBranches ({
        "Dst": "[D*(2010)+ "+a+" ([([D0]cc "+a+" pi- pi+),([D0]cc "+a+" pi+ pi-)]) pi+]CC",
        "D0":  "[D*(2010)+ "+a+" ^([([D0]cc "+a+" pi- pi+),([D0]cc "+a+" pi+ pi-)]) pi+]CC",
        "x1":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" ^pi- pi+),([D0]cc "+a+" ^pi+ pi-)]) pi+]CC",
        "x2":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" pi- ^pi+),([D0]cc "+a+" pi+ ^pi-)]) pi+]CC",
        "pi":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" pi- pi+),([D0]cc "+a+" pi+ pi-)]) ^pi+]CC"
        })


      #dttuple.Decay = "[D*(2010)+ -> ([^D0]CC -> [^pi-]CC [^pi+]CC) ^pi+]CC"
      #dttuple.addBranches ({
        #"Dst": "^[D*(2010)+ -> ([D0]CC -> [pi-]CC [pi+]CC) pi+]CC",
        #"D0":  "[D*(2010)+ -> ([^D0]CC -> [pi-]CC [pi+]CC) pi+]CC",
        #"x1":  "[D*(2010)+ -> ([D0]CC -> [^pi-]CC [pi+]CC) pi+]CC",
        #"x2":  "[D*(2010)+ -> ([D0]CC -> [pi-]CC [^pi+]CC) pi+]CC",
        #"pi":  "[D*(2010)+ -> ([D0]CC -> [pi-]CC [pi+]CC) ^pi+]CC"
        #})

    elif tupleDecay == "mumu":
      dttuple.Decay = "[D*(2010)+ "+a+" ^([D0]cc "+a+" ^[mu+]cc ^[mu-]cc) ^pi+]CC"
      dttuple.addBranches ({
        "Dst": "[D*(2010)+ "+a+" ([([D0]cc "+a+" mu- mu+),([D0]cc "+a+" mu+ mu-)]) pi+]CC",
        "D0":  "[D*(2010)+ "+a+" ^([([D0]cc "+a+" mu- mu+),([D0]cc "+a+" mu+ mu-)]) pi+]CC",
        "x1":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" ^mu- mu+),([D0]cc "+a+" ^mu+ mu-)]) pi+]CC",
        "x2":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" mu- ^mu+),([D0]cc "+a+" mu+ ^mu-)]) pi+]CC",
        "pi":  "[D*(2010)+ "+a+" ([([D0]cc "+a+" mu- mu+),([D0]cc "+a+" mu+ mu-)]) ^pi+]CC"
        })
      #dttuple.Decay = "[D*(2010)+ -> ([^D0]CC -> [^mu-]CC [^mu+]CC) ^pi+]CC"
      #dttuple.addBranches ({
        #"Dst": "^[D*(2010)+ -> ([D0]CC -> [mu-]CC [mu+]CC) pi+]CC",
        #"D0":  "[D*(2010)+ -> ([^D0]CC -> [mu-]CC [mu+]CC) pi+]CC",
        #"x1":  "[D*(2010)+ -> ([D0]CC -> [^mu-]CC [mu+]CC) pi+]CC",
        #"x2":  "[D*(2010)+ -> ([D0]CC -> [mu-]CC [^mu+]CC) pi+]CC",
        #"pi":  "[D*(2010)+ -> ([D0]CC -> [mu-]CC [mu+]CC) ^pi+]CC"
        #})


    dttuple.TupleName = "Demu_NTuple"

    dttuple.addTool(TupleToolPropertime())
    dttuple.addTool(TupleToolTISTOS())
    dttuple.TupleToolTISTOS.VerboseL0 = True
    dttuple.TupleToolTISTOS.VerboseHlt1 = True
    dttuple.TupleToolTISTOS.VerboseHlt2 = True
    dttuple.TupleToolTISTOS.Verbose = True

    dttuple.addTool(TupleToolSelReport())
    #dttuple.TupleToolSelReport.OutputLevel=VERBOSE
    dttuple.TupleToolSelReport.Verbose = True
    dttuple.TupleToolSelReport.OnlyMass = False
    dttuple.TupleToolSelReport.TriggerList = ["Hlt2CharmHadD02HH_D02PiPiDecision"]

    if "ls" not in tupleDecay:
      dttuple.TupleToolTISTOS.TriggerList = [
        ##"L0Global",
        #"L0DiMuonDecision",
        "L0MuonDecision",
        "L0ElectronDecision",
        "L0HadronDecision",
        #"L0MuonHighDecision",
        #"L0PhotonDecision",
        ##"Hlt1Global",
        "Hlt1TrackMuonDecision",
        "Hlt1TrackAllL0Decision",
        #"Hlt1SingleMuonNoIPL0Decision",
        #"Hlt1SingleMuonNoIPL0HighPTDecision",
        ###"Hlt2Global",
        "Hlt2Dst2PiD02EMuDecision",
        "Hlt2Dst2PiD02KKDecision",
        ##"Hlt2Dst2PiD02KMuDecision",
        "Hlt2Dst2PiD02KPiDecision",
        ##"Hlt2Dst2PiD02MuMuDecision",
        ##"Hlt2Dst2PiD02PiMuDecision",
        "Hlt2Dst2PiD02PiPiDecision",
        ##"Hlt2BiasedDiMuonIPDecision",
        ##"Hlt2CharmOSTF2BodyDecision",
        ##"Hlt2CharmOSTF3BodyDecision",
        ##"Hlt2IncPhiRobustDecision",
        ##"Hlt2IncPhiSidebandsDecision",
        ##"Hlt2IncPhiTrackFitDecision",
        ##"Hlt2MuTrackDecision",
        ##"Hlt2PromptJPsiDecision",
        ##"Hlt2TopoOSTF2BodyDecision",
        ##"Hlt2TopoOSTF3BodyDecision",
        ##"Hlt2TopoOSTF4BodyDecision",
        ##"Hlt2diphotonDiMuonDecision",
        ##"Hlt2UnbiasedDiMuonLowMassDecision",
        "Hlt2CharmHadD02HH2BodyIncDecision",
        "Hlt2CharmHadD02HH_D02PiPiDecision",
        #"Hlt2CharmHadD02HH_D02PiPiWideMassDecision",
        "Hlt2CharmHadD02HH_D02KPiDecision",
        #"Hlt2CharmHadD02HH_D02KPiWideMassDecision",
        "Hlt2CharmHadD02HH_D02KKDecision",
        #"Hlt2CharmHadD02HH_D02KKWideMassDecision",

        "Hlt2TopoMu2BodyDecision",
        "Hlt2TopoE2BodyDecision",

        'Hlt2CharmHadD02HHXDst_hhXDecision',
        ##'Hlt2CharmHadD02HHXDst_hhXWideMassDecision',
        ##'Hlt2CharmHadD02HHXDst_BaryonhhXDecision',
        ##'Hlt2CharmHadD02HHXDst_BaryonhhXWideMassDecision',
        ##'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLDecision',
        ##'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLWideMassDecision',
        ##'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLDecision',
        ##'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLWideMassDecision',
        ##'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDDecision',
        ##'Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDWideMassDecision',
        ##'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDDecision',
        ##'Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDWideMassDecision',
        'Hlt2CharmHadD02HHXDst_LeptonhhXDecision',
        ##'Hlt2CharmHadD02HHXDst_LeptonhhXWideMassDecision',
        ##'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLDecision',
        ##'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLWideMassDecision',
        ##'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLDecision',
        ##'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLWideMassDecision',
        ##'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDDecision',
        ##'Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDWideMassDecision',
        ##'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDDecision',
        ##'Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDWideMassDecision',
        ] #+ [ trigger_name+"Decision" for trigger_name in
          #      ["L0CALO","L0ElectronNoSPD","L0PhotonNoSPD","L0HadronNoSPD","L0MuonNoSPD","L0DiMuonNoSPD","L0Electron","L0ElectronHi","L0Photon","L0PhotonHi","L0Hadron","L0Muon","L0DiMuon","L0HighSumETJet","L0B1gas","L0B2gas",]\
          #    + ["Hlt1MBMicroBiasVelo","Hlt1Global","Hlt1DiMuonHighMass","Hlt1DiMuonLowMass","Hlt1SingleMuonNoIP","Hlt1SingleMuonHighPT","Hlt1TrackAllL0","Hlt1TrackMuon","Hlt1TrackPhoton","Hlt1Lumi","Hlt1LumiMidBeamCrossing","Hlt1MBNoBias","Hlt1MBMicroBiasVeloRateLimited","Hlt1MBMicroBiasTStation","Hlt1MBMicroBiasTStationRateLimited","Hlt1L0Any","Hlt1L0AnyRateLimited","Hlt1L0AnyNoSPD","Hlt1L0AnyNoSPDRateLimited","Hlt1NoPVPassThrough","Hlt1DiProton","Hlt1DiProtonLowMult","Hlt1BeamGasNoBeamBeam1","Hlt1BeamGasNoBeamBeam2","Hlt1BeamGasBeam1","Hlt1BeamGasBeam2","Hlt1BeamGasCrossingEnhancedBeam1","Hlt1BeamGasCrossingEnhancedBeam2","Hlt1BeamGasCrossingForcedReco","Hlt1ODINTechnical","Hlt1Tell1Error","Hlt1VeloClosingMicroBias","Hlt1BeamGasCrossingParasitic","Hlt1ErrorEvent","Hlt1SingleElectronNoIP","Hlt1TrackForwardPassThrough","Hlt1TrackForwardPassThroughLoose","Hlt1CharmCalibrationNoBias","Hlt1L0HighSumETJet","Hlt1BeamGasCrossingForcedRecoFullZ","Hlt1BeamGasHighRhoVertices","Hlt1VertexDisplVertex","Hlt1TrackAllL0Tight","Hlt1HighPtJetsSinglePV","Hlt1L0PU","Hlt1L0CALO",]\
          #    + ["Hlt2SingleElectronTFLowPt","Hlt2SingleElectronTFHighPt","Hlt2DiElectronHighMass","Hlt2DiElectronB","Hlt2B2HHLTUnbiased","Hlt2Topo2BodySimple","Hlt2Topo3BodySimple","Hlt2Topo4BodySimple","Hlt2Topo2BodyBBDT","Hlt2Topo3BodyBBDT","Hlt2Topo4BodyBBDT","Hlt2TopoMu2BodyBBDT","Hlt2TopoMu3BodyBBDT","Hlt2TopoMu4BodyBBDT","Hlt2TopoE2BodyBBDT","Hlt2TopoE3BodyBBDT","Hlt2TopoE4BodyBBDT","Hlt2IncPhi","Hlt2IncPhiSidebands","Hlt2CharmHadD02HHKsLL","Hlt2Dst2PiD02PiPi","Hlt2Dst2PiD02MuMu","Hlt2Dst2PiD02KMu","Hlt2Dst2PiD02KPi","Hlt2PassThrough","Hlt2Transparent","Hlt2Forward","Hlt2DebugEvent","Hlt2CharmHadD02HH_D02PiPi","Hlt2CharmHadD02HH_D02PiPiWideMass","Hlt2CharmHadD02HH_D02KK","Hlt2CharmHadD02HH_D02KKWideMass","Hlt2CharmHadD02HH_D02KPi","Hlt2CharmHadD02HH_D02KPiWideMass","Hlt2ExpressJPsi","Hlt2ExpressJPsiTagProbe","Hlt2ExpressLambda","Hlt2ExpressKS","Hlt2ExpressDs2PhiPi","Hlt2ExpressBeamHalo","Hlt2ExpressDStar2D0Pi","Hlt2ExpressHLT1Physics","Hlt2Bs2PhiGamma","Hlt2Bs2PhiGammaWideBMass","Hlt2Bd2KstGamma","Hlt2Bd2KstGammaWideKMass","Hlt2Bd2KstGammaWideBMass","Hlt2CharmHadD2KS0H_D2KS0Pi","Hlt2CharmHadD2KS0H_D2KS0K","Hlt2CharmRareDecayD02MuMu","Hlt2B2HH","Hlt2MuonFromHLT1","Hlt2SingleMuon","Hlt2SingleMuonHighPT","Hlt2SingleMuonLowPT","Hlt2DiProton","Hlt2DiProtonTF","Hlt2DiProtonLowMult","Hlt2DiProtonLowMultTF","Hlt2CharmSemilepD02HMuNu_D02KMuNuWS","Hlt2CharmSemilepD02HMuNu_D02PiMuNuWS","Hlt2CharmSemilepD02HMuNu_D02KMuNu","Hlt2CharmSemilepD02HMuNu_D02PiMuNu","Hlt2TFBc2JpsiMuX","Hlt2TFBc2JpsiMuXSignal","Hlt2DisplVerticesLowMassSingle","Hlt2DisplVerticesHighMassSingle","Hlt2DisplVerticesDouble","Hlt2DisplVerticesSinglePostScaled","Hlt2DisplVerticesHighFDSingle","Hlt2DisplVerticesSingleDown","Hlt2CharmSemilepD2HMuMu","Hlt2CharmSemilepD2HMuMuWideMass","Hlt2B2HHPi0_Merged","Hlt2CharmHadD2HHH","Hlt2CharmHadD2HHHWideMass","Hlt2DiMuon","Hlt2DiMuonLowMass","Hlt2DiMuonJPsi","Hlt2DiMuonJPsiHighPT","Hlt2DiMuonPsi2S","Hlt2DiMuonB","Hlt2DiMuonZ","Hlt2DiMuonDY1","Hlt2DiMuonDY2","Hlt2DiMuonDY3","Hlt2DiMuonDY4","Hlt2DiMuonDetached","Hlt2DiMuonDetachedHeavy","Hlt2DiMuonDetachedJPsi","Hlt2DiMuonNoPV","Hlt2TriMuonDetached","Hlt2TriMuonTau","Hlt2CharmSemilepD02HHMuMu","Hlt2CharmSemilepD02HHMuMuWideMass","Hlt2CharmHadD02HHHH","Hlt2CharmHadD02HHHHWideMass","Hlt2ErrorEvent","Hlt2Global","Hlt2diPhotonDiMuon","Hlt2LowMultMuon","Hlt2LowMultHadron","Hlt2LowMultPhoton","Hlt2LowMultElectron","Hlt2SingleTFElectron","Hlt2SingleTFVHighPtElectron","Hlt2B2HHLTUnbiasedDetached","Hlt2CharmHadLambdaC2KPPi","Hlt2SingleMuonVHighPT","Hlt2CharmSemilepD02HMuNu_D02KMuNuTight","Hlt2CharmHadMinBiasLambdaC2KPPi","Hlt2CharmHadMinBiasD02KPi","Hlt2CharmHadMinBiasD02KK","Hlt2CharmHadMinBiasDplus2hhh","Hlt2CharmHadMinBiasLambdaC2LambdaPi","Hlt2DisplVerticesSingle","Hlt2DisplVerticesDoublePostScaled","Hlt2DisplVerticesSingleHighMassPostScaled","Hlt2DisplVerticesSingleHighFDPostScaled","Hlt2DisplVerticesSingleMVPostScaled","Hlt2RadiativeTopoTrackTOS","Hlt2RadiativeTopoPhotonL0","Hlt2DiMuonPsi2SHighPT","Hlt2DoubleDiMuon","Hlt2DiMuonAndMuon","Hlt2DiMuonAndGamma","Hlt2DiMuonAndD0","Hlt2DiMuonAndDp","Hlt2DiMuonAndDs","Hlt2DiMuonAndLc","Hlt2CharmSemilepD02HHMuMuHardHadronsSoftMuons","Hlt2CharmSemilepD02HHMuMuHardHadronsSoftMuonsWideMass","Hlt2CharmSemilepD02HHMuMuHardHadronsAndMuons","Hlt2CharmSemilepD02HHMuMuHardHadronsAndMuonsWideMass","Hlt2TopoRad2BodyBBDT","Hlt2TopoRad2plus1BodyBBDT","Hlt2Lumi","Hlt2LowMultHadron_nofilter","Hlt2LowMultElectron_nofilter","Hlt2CharmHadD02HHKsDD","Hlt2CharmHadD2KS0KS0","Hlt2CharmHadD2KS0KS0WideMass","Hlt2ExpressD02KPi","Hlt2CharmHadLambdaC2KPPiWideMass","Hlt2CharmHadLambdaC2KPK","Hlt2CharmHadLambdaC2KPKWideMass","Hlt2CharmHadLambdaC2PiPPi","Hlt2CharmHadLambdaC2PiPPiWideMass","Hlt2CharmHadLambdaC2PiPK","Hlt2CharmHadLambdaC2PiPKWideMass","Hlt2CharmHadD2KS0H_D2KS0DDPi","Hlt2CharmHadD2KS0H_D2KS0DDK","Hlt2DiPhi","Hlt2CharmHadD02HHHHDstNoHltOne_4pi","Hlt2CharmHadD02HHHHDstNoHltOne_4piWideMass","Hlt2CharmHadD02HHHHDstNoHltOne_K3pi","Hlt2CharmHadD02HHHHDstNoHltOne_K3piWideMass","Hlt2CharmHadD02HHHHDstNoHltOne_KKpipi","Hlt2CharmHadD02HHHHDstNoHltOne_KKpipiWideMass","Hlt2CharmHadD02HHHHDstNoHltOne_2K2pi","Hlt2CharmHadD02HHHHDstNoHltOne_2K2piWideMass","Hlt2CharmHadD02HHHHDstNoHltOne_3Kpi","Hlt2CharmHadD02HHHHDstNoHltOne_3KpiWideMass","Hlt2CharmHadD02HHHHDstNoHltOne_Ch2","Hlt2CharmHadD02HHHHDstNoHltOne_Ch2WideMass","Hlt2CharmSemilep3bodyD2PiMuMu","Hlt2CharmSemilep3bodyD2PiMuMuSS","Hlt2CharmSemilep3bodyD2KMuMu","Hlt2CharmSemilep3bodyD2KMuMuSS","Hlt2CharmSemilep3bodyLambdac2PMuMu","Hlt2CharmSemilep3bodyLambdac2PMuMuSS","Hlt2LambdaC_LambdaC2Lambda0LLPi","Hlt2LambdaC_LambdaC2Lambda0LLK","Hlt2LambdaC_LambdaC2Lambda0DDPi","Hlt2LambdaC_LambdaC2Lambda0DDK","Hlt2RadiativeTopoTrack","Hlt2RadiativeTopoPhoton","Hlt2CharmHadD02HHHHDst_4pi","Hlt2CharmHadD02HHHHDst_4piWideMass","Hlt2CharmHadD02HHHHDst_K3pi","Hlt2CharmHadD02HHHHDst_K3piWideMass","Hlt2CharmHadD02HHHHDst_KKpipi","Hlt2CharmHadD02HHHHDst_KKpipiWideMass","Hlt2CharmHadD02HHHHDst_2K2pi","Hlt2CharmHadD02HHHHDst_2K2piWideMass","Hlt2CharmHadD02HHHHDst_3Kpi","Hlt2CharmHadD02HHHHDst_3KpiWideMass","Hlt2CharmHadD02HHHHDst_Ch2","Hlt2CharmHadD02HHHHDst_Ch2WideMass","Hlt2CharmSemilepD02PiPiMuMu","Hlt2CharmSemilepD02KKMuMu","Hlt2CharmSemilepD02KPiMuMu","Hlt2CharmHadD02HHHH_4pi","Hlt2CharmHadD02HHHH_4piWideMass","Hlt2CharmHadD02HHHH_K3pi","Hlt2CharmHadD02HHHH_K3piWideMass","Hlt2CharmHadD02HHHH_KKpipi","Hlt2CharmHadD02HHHH_KKpipiWideMass","Hlt2CharmHadD02HHHH_2K2pi","Hlt2CharmHadD02HHHH_2K2piWideMass","Hlt2CharmHadD02HHHH_3Kpi","Hlt2CharmHadD02HHHH_3KpiWideMass","Hlt2CharmHadD02HHHH_Ch2","Hlt2CharmHadD02HHHH_Ch2WideMass","Hlt2DiMuonDetachedPsi2S","Hlt2CharmHadD02HHXDst_hhX","Hlt2CharmHadD02HHXDst_hhXWideMass","Hlt2LowMultD2KPi","Hlt2LowMultD2KPiPi","Hlt2LowMultD2K3Pi","Hlt2LowMultChiC2HH","Hlt2LowMultChiC2HHHH","Hlt2LowMultD2KPiWS","Hlt2LowMultD2KPiPiWS","Hlt2LowMultD2K3PiWS","Hlt2LowMultChiC2HHWS","Hlt2LowMultChiC2HHHHWS","Hlt2LowMultDDInc","Hlt2DisplVerticesSingleLoosePS","Hlt2DisplVerticesSingleHighFD","Hlt2DisplVerticesSingleVeryHighFD","Hlt2DisplVerticesSingleHighMass","Hlt2DisplVerticesSinglePS","Hlt2DisplVerticesDoublePS","Hlt2CharmHadD2HHHKsLL","Hlt2CharmHadD2HHHKsDD","Hlt2KshortToMuMuPiPi","Hlt2LowMultChiC2PP","Hlt2LowMultDDIncCP","Hlt2LowMultDDIncVF","Hlt2LowMultLMR2HH","Hlt2HighPtJets","Hlt2ChargedHyperon_Xi2Lambda0LLPi","Hlt2ChargedHyperon_Xi2Lambda0LLMu","Hlt2ChargedHyperon_Omega2Lambda0LLK","Hlt2ChargedHyperon_Xi2Lambda0DDPi","Hlt2ChargedHyperon_Xi2Lambda0DDMu","Hlt2ChargedHyperon_Omega2Lambda0DDK","Hlt2CharmHadD02HHXDst_BaryonhhX","Hlt2CharmHadD02HHXDst_BaryonhhXWideMass","Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLL","Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLWideMass","Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LL","Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLWideMass","Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDD","Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDWideMass","Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DD","Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDWideMass","Hlt2CharmHadD02HHXDst_LeptonhhX","Hlt2CharmHadD02HHXDst_LeptonhhXWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLL","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LL","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDD","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DD","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDWideMass"]
          #  ]

      
    else:
      dttuple.TupleToolTISTOS.TriggerList = [
        "L0MuonDecision",
        "L0ElectronDecision",
        "L0HadronDecision",
        "Hlt1TrackMuonDecision",
        "Hlt1TrackAllL0Decision",
        "Hlt2CharmHadD02HH2BodyIncDecision",
        "Hlt2CharmHadD02HH_D02PiPiDecision",
        "Hlt2CharmHadD02HH_D02PiPiLsDecision",
        "Hlt2CharmHadD02HH_D02KPiDecision",
        "Hlt2CharmHadD02HH_D02KPiLsDecision",
        "Hlt2CharmHadD02HH_D02KKDecision",
        "Hlt2CharmHadD02HH_D02KKLsDecision",
        "Hlt2VegetableTrigger",
        ]

    D_variables = {"DIRA": "BPVDIRA",
                  "IPChi2": "BPVVDCHI2",
                  # Min IP wrt all primary verticies
                  "MinIP_PRIMARY": "MIPDV(PRIMARY)",
                  "MinIPChi2_PRIMARY": "MIPCHI2DV(PRIMARY)",
                  "VChi2_per_NDOF": "VFASPF(VCHI2/VDOF)",
                  "DOCA": "DOCA(1, 2)",
                  "BPVVDCHI2":"BPVVDCHI2",
                  #"AMAXDOCA": "AMAXDOCA('')",
                }
    # XXX How to calculate the DOCA of the two leptons?
    lepton_variables = {"TOMPT": "PT",
                        "TOMP": "P",
                        "TRCHI2DOF": "TRCHI2DOF",
                        "TRGHOSTPROB": "TRGHOSTPROB",
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

    dttuple.addTool(TupleToolDecay, name="pi")
    LoKi_pi = LoKi__Hybrid__TupleTool("LoKi_pi")
    LoKi_pi.Variables = lepton_variables
    dttuple.pi.addTool(LoKi_pi)
    dttuple.pi.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_pi"]

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


    LoKi_DTFMASS = LoKi__Hybrid__TupleTool("LoKi_DTFMASS")
    LoKi_DTFMASS.Variables = {
        "DTF_CHI2"   : "DTF_CHI2( True )",
        "DTF_NDOF"   : "DTF_NDOF( True )",

        "DTF_Dst_M"  : "DTF_FUN ( M ,                     True )",
        "DTF_Dst_MM" : "DTF_FUN ( MM ,                    True )",
        "DTF_Dst_P"  : "DTF_FUN ( P ,                     True )",
        "DTF_Dst_PT" : "DTF_FUN ( PT ,                    True )",
        "DTF_Dst_PE" : "DTF_FUN ( E ,                     True )",
        "DTF_Dst_PX" : "DTF_FUN ( PX ,                    True )",
        "DTF_Dst_PY" : "DTF_FUN ( PY ,                    True )",
        "DTF_Dst_PZ" : "DTF_FUN ( PZ ,                    True )",

        "DTF_D0_M"   : "DTF_FUN ( CHILD(M,1) ,             True )",
        "DTF_D0_MM"  : "DTF_FUN ( CHILD(MM,1) ,            True )",
        "DTF_D0_P"   : "DTF_FUN ( CHILD(P,1) ,             True )",
        "DTF_D0_PT"  : "DTF_FUN ( CHILD(PT,1) ,            True )",
        "DTF_D0_PE"  : "DTF_FUN ( CHILD(E,1) ,             True )",
        "DTF_D0_PX"  : "DTF_FUN ( CHILD(PX,1) ,            True )",
        "DTF_D0_PY"  : "DTF_FUN ( CHILD(PY,1) ,            True )",
        "DTF_D0_PZ"  : "DTF_FUN ( CHILD(PZ,1) ,            True )",

        "DTF_x1_M"    : "DTF_FUN ( CHILD(CHILD(M,1),1) ,    True )",
        "DTF_x1_MM"   : "DTF_FUN ( CHILD(CHILD(MM,1),1) ,   True )",
        "DTF_x1_P"    : "DTF_FUN ( CHILD(CHILD(P,1),1) ,    True )",
        "DTF_x1_PT"   : "DTF_FUN ( CHILD(CHILD(PT,1),1) ,   True )",
        "DTF_x1_PE"   : "DTF_FUN ( CHILD(CHILD(E,1),1) ,    True )",
        "DTF_x1_PX"   : "DTF_FUN ( CHILD(CHILD(PX,1),1) ,   True )",
        "DTF_x1_PY"   : "DTF_FUN ( CHILD(CHILD(PY,1),1) ,   True )",
        "DTF_x1_PZ"   : "DTF_FUN ( CHILD(CHILD(PZ,1),1) ,   True )",

        "DTF_x2_M"   : "DTF_FUN ( CHILD(CHILD(M,2),1) ,    True )",
        "DTF_x2_MM"  : "DTF_FUN ( CHILD(CHILD(MM,2),1) ,   True )",
        "DTF_x2_P"   : "DTF_FUN ( CHILD(CHILD(P,2),1) ,    True )",
        "DTF_x2_PT"  : "DTF_FUN ( CHILD(CHILD(PT,2),1) ,   True )",
        "DTF_x2_PE"  : "DTF_FUN ( CHILD(CHILD(E,2),1) ,    True )",
        "DTF_x2_PX"  : "DTF_FUN ( CHILD(CHILD(PX,2),1) ,   True )",
        "DTF_x2_PY"  : "DTF_FUN ( CHILD(CHILD(PY,2),1) ,   True )",
        "DTF_x2_PZ"  : "DTF_FUN ( CHILD(CHILD(PZ,2),1) ,   True )",

        "DTF_pi_M"   : "DTF_FUN ( CHILD(M,2) ,             True )",
        "DTF_pi_MM"  : "DTF_FUN ( CHILD(MM,2) ,            True )",
        "DTF_pi_P"   : "DTF_FUN ( CHILD(P,2) ,             True )",
        "DTF_pi_PT"  : "DTF_FUN ( CHILD(PT,2) ,            True )",
        "DTF_pi_PE"  : "DTF_FUN ( CHILD(E,2) ,             True )",
        "DTF_pi_PX"  : "DTF_FUN ( CHILD(PX,2) ,            True )",
        "DTF_pi_PY"  : "DTF_FUN ( CHILD(PY,2) ,            True )",
        "DTF_pi_PZ"  : "DTF_FUN ( CHILD(PZ,2) ,            True )",


        "LoKi_BPVVDCHI2"  : "CHILD(BPVVDCHI2,1)",
        #"LoKi_M"  : "CHILD(M,1)",
        #"LoKi_MM" : "CHILD(MM,1)",
        #"LoKi_AM" : "CHILD(AM(1,2),1)",

        }
    dttuple.Dst.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_DTFMASS"]
    dttuple.Dst.addTool(LoKi_DTFMASS)

    #dttuple.D0.addTool(TupleToolDecayTreeFitter("SVFit"))
    #dttuple.D0.SVFit.Verbose = True
    #dttuple.D0.SVFit.constrainToOriginVertex = True
    #dttuple.D0.ToolList += ["TupleToolDecayTreeFitter/SVFit"]

    #dttuple.Dst.addTool(TupleToolDecayTreeFitter("PVFit"))
    #dttuple.Dst.PVFit.Verbose = True
    #dttuple.Dst.PVFit.constrainToOriginVertex = True
    #dttuple.Dst.ToolList += ["TupleToolDecayTreeFitter/PVFit"]

    #dttuple.Dst.ToolList +=  ["TupleToolDecayTreeFitter/SubPiPi", "TupleToolDecayTreeFitter/SubKPi", "TupleToolDecayTreeFitter/SubPiK" ]
    #dttuple.Dst.addTool(TupleToolDecayTreeFitter("SubPiPi", Verbose=True, constrainToOriginVertex=True, Substitutions={ 'Strange -> Meson (Strange -> ^e+ mu-)': 'pi+', 'Strange -> Meson (Strange -> e+ ^mu-)': 'pi-' }))
    #dttuple.Dst.addTool(TupleToolDecayTreeFitter("SubKPi",  Verbose=True, constrainToOriginVertex=True, Substitutions={ 'Strange -> Meson (Strange -> ^e+ mu-)': 'K+',  'Strange -> Meson (Strange -> e+ ^mu-)': 'pi-' }))
    #dttuple.Dst.addTool(TupleToolDecayTreeFitter("SubPiK",  Verbose=True, constrainToOriginVertex=True, Substitutions={ 'Strange -> Meson (Strange -> ^e+ mu-)': 'pi+', 'Strange -> Meson (Strange -> e+ ^mu-)': 'K-' }))


    if "MC" in dataType:
      dttuple.addTool(TupleToolMCBackgroundInfo, name="TupleToolMCBackgroundInfo")
      dttuple.TupleToolMCBackgroundInfo.Verbose=True
      dttuple.addTool(TupleToolMCTruth, name="truth")
      dttuple.truth.ToolList += ["MCTupleToolHierarchy",
                                "MCTupleToolKinematic"]
      dttuple.ToolList+=["TupleToolMCBackgroundInfo/TupleToolMCBackgroundInfo"]
      dttuple.ToolList+=["TupleToolMCTruth/truth"]

    DaVinci().appendToMainSequence( [ dttuple ] )

  elif outputType == "dst":

    from Configurables import SelDSTWriter
    if blinded:
      dst_Sel = AutomaticData(Location = blind_Seq.outputLocations() )
    elif stripRun:
      dst_Sel = AutomaticData(Location = stripOutputLoc)
    else:
      dst_Sel = AutomaticData(Location = "/Event/"+strippingStream+"/" + stripOutputLoc)

    dst_Filter = FilterDesktop('dst_Filter', Code = "ALL")

    dst_FilterSel = Selection(name = line.name().replace("Stripping",""),
                              Algorithm = dst_Filter,
                              RequiredSelections = [ dst_Sel ])

    dst_Seq = SelectionSequence('lsdata',
                                TopSelection = dst_FilterSel,
                                )

    dstw = SelDSTWriter("DSTWriter")
    dstw.OutputFileSuffix = "Demu"
    #dstw.CopyProtoParticles = False
    dstw.SelectionSequences = [dst_Seq]
    #dstw.CopyL0DUReport = False
    #dstw.CopyHltDecReports = False
    #dstw.CopyMCTruth = True
    #dstw.CopyBTags = True
    DaVinci().appendToMainSequence( [ dstw.sequence() ] )



def pleaseWorkNow():
  from Configurables import DecodeRawEvent, HltSelReportsDecoder, ApplicationMgr
  from Configurables import DaVinci, RawEventDump
  from DAQSys.Decoders import DecoderDB
  for key, val in DecoderDB.iteritems():
    if "Hlt" in key and "ReportsDecoder" in key:
      val.Inputs={"InputRawEventLocation":"/Event/DAQ/RawEvent"}
      val.Properties["OutputLevel"] = VERBOSE
  DecodeRawEvent().OverrideInputs="Pit"
  HltSelReportsDecoder().OutputLevel=VERBOSE
  HltSelReportsDecoder().InputRawEventLocation="/Event/DAQ/RawEvent"
  #enk = EventNodeKiller()
  #enk.Nodes=[
      #"Trigger/RawEvent",
      #"Other/RawEvent",
      #"Rich/RawEvent",
      #"Muon/RawEvent",
      #"Calo/RawEvent"]
  #ApplicationMgr().TopAlg.insert( 0, enk )
  #DaVinci().appendToMainSequence( [ storeExp ] )

  red = RawEventDump()
  DaVinci().appendToMainSequence( [ red ] )

  from Configurables import ConfigTarFileAccessSvc
  ConfigTarFileAccessSvc().File = './config.tar'





