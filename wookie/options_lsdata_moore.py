

from Gaudi.Configuration import *
from LHCbKernel.Configuration import *


def execute(evtMax, dataType, mag, **leftovers):
    
  from Configurables import Moore
  from Configurables import L0MuonAlg, LoKiSvc
  from Configurables import L0Conf, CondDB, MessageSvc

  LoKiSvc().Welcome = False
  MessageSvc().Format = "% F%280W%S%7W%R%T %60W%M"

  #Configure L0 emulation
  #L0MuonAlg( "L0Muon" ).L0DUConfigProviderType = "L0DUConfigProvider"
  #Moore().L0=True
  #Moore().RunL0Emulator=True
  #Moore().ForceSingleL0Configuration = False
  Moore().CheckOdin  = False
  #CondDB().IgnoreHeartBeat = True 
  
  Moore().EnableDataOnDemand = True
  #Moore().EnableRunChangeHandler = False
  Moore().EnableMonitoring = False

  # How are we configuring the trigger? TCK or settings? 
  #Moore().ThresholdSettings = 'TomsCharmHadronLines' 
  #Moore().ThresholdSettings = 'Physics_September2012' 
  Moore().UseTCK = True
  Moore().InitialTCK = '0x99990000'
  #Moore().InitialTCK = '0x00a10045'                        #Change me to the TCK you want to use
  #Moore().WriterRequires=['HltDecsionSequence']            #What sequence must pass for the events to be written out? 
  Moore().WriterRequires=[] 
  Moore().UseDBSnapshot   = False
  #Moore().EnableRunChangeHandler = False
  #Moore().Verbose = True
  Moore().EvtMax = evtMax
  Moore().outputFile  = 'Demu.lsdata.dst'
  #Moore().Split  = 'Hlt1Hlt2'

  #Moore().RootInTES = '/Event/lsdata/Phys/dst_FilterSel'
  
  
  from Configurables import ConfigTarFileAccessSvc
  ConfigTarFileAccessSvc().File='config.tar'
  Moore().TCKData='./'
  #Moore().TCKData='/afs/cern.ch/user/t/tbird/cmtuser/Moore_v20r4/TCKData'
  
  #Moore().generateConfig = True
  #Moore().configLabel = 'D2emu like-sign enabled TCK'
  #Moore().TCKData = '/afs/cern.ch/user/t/tbird/cmtuser/Moore_v20r4/TCKData'

  if dataType == "data2012":
    Moore().DataType = "2012"
    Moore().Simulation = False
    #Moore().DDDBtag = "dddb-20130111"
    #if mag == "up":
      #Moore().CondDBtag = "cond-20130114"
    #elif mag == "down":
      #Moore().CondDBtag = "cond-20130114"
  elif dataType == "data2011":
    Moore().DataType = "2011"
    Moore().Simulation = False
    #Moore().DDDBtag = "dddb-20130111"
    #if mag == "up":
      #Moore().CondDBtag = "cond-20130114"
    #elif mag == "down":
      #Moore().CondDBtag = "cond-20130114"

  from Configurables import bankKiller
  ### Since Moore was already run in production for MC10, kill the resulting
  ### rawbanks.
  ##bk = bankKiller( "KillHltBanks", BankTypes = [ "HltRoutingBits", "HltSelReports", "HltVertexReports", "HltDecReports", "HltLumiSummary" ] )
  ##bk.RawEventLocations = ["Trigger/RawEvent","Other/RawEvent","Calo/RawEvent","Muon/RawEvent","Rich/RawEvent"]
  ##from Gaudi.Configuration import appendPostConfigAction
  ##from Configurables import ApplicationMgr
  ##appendPostConfigAction( lambda : ApplicationMgr().TopAlg.insert( 0, bk ) )
  
  
  #storeExp = StoreExplorerAlg("StoreExplorer1")
  #storeExp.Load = 1
  #storeExp.PrintFreq = 5.0
  
  #ApplicationMgr().TopAlg.insert( 0, storeExp )
  
  from Configurables import RawEventMapCombiner, RawEventSimpleCombiner, DataOnDemandSvc
  myCombiner=RawEventSimpleCombiner("resurectRawEvent")
  myCombiner.InputRawEventLocations=[
      "Trigger/RawEvent",
      "Other/RawEvent",
      "Rich/RawEvent",
      "Muon/RawEvent",
      "Calo/RawEvent"#,
      ]
  ApplicationMgr().TopAlg.insert( 0, myCombiner )
  
  bk = bankKiller( "KillHltBanks", BankTypes = [ "HltRoutingBits", "HltSelReports", "HltVertexReports", "HltDecReports", "HltLumiSummary" ] )
  bk.RawEventLocations = ['DAQ/RawEvent']
  #appendPostConfigAction( lambda : ApplicationMgr().TopAlg.insert( 0, bk ) )
  ApplicationMgr().TopAlg.insert( 1, bk )

  #from Configurables import RecombineRawEvent
  #RecombineRawEvent()
  
  #storeExp2 = StoreExplorerAlg("StoreExplorer2")
  #storeExp2.Load = 1
  #storeExp2.PrintFreq = 5.0
  
  #ApplicationMgr().TopAlg.insert( 3, storeExp2 )
  
  enk = EventNodeKiller()
  enk.Nodes=[
      "Trigger/RawEvent",
      "Other/RawEvent",
      "Rich/RawEvent",
      "Muon/RawEvent",
      "Calo/RawEvent"]
  ApplicationMgr().TopAlg.insert( 2, enk )
  
  #storeExp3 = StoreExplorerAlg("StoreExplorer3")
  #storeExp3.Load = 1
  #storeExp3.PrintFreq = 5.0
  
  #ApplicationMgr().TopAlg.insert( 5, storeExp3 )
  
  
  
  
  #ApplicationMgr().ExtSvc=["DataOnDemandSvc"]+[svc for svc in ApplicationMgr().ExtSvc if svc is not "DataOnDemandSvc"]
  #DataOnDemandSvc().AlgMap["DAQ/RawEvent"] = myCombiner
  #DataOnDemandSvc().NodeMap[ "DAQ" ] = "DataObject"
  
  
  #ApplicationMgr().TopAlg+=GaudiSequencer("Spam") 
  
  #Writer=InputCopyStream("MyStream") 
  #IOHelper().outStream("Demu.lsdata.dst",writer=Writer) 
    
  #RawEventJuggler().Input="Pit" 
  #RawEventJuggler().Output="Stripping20"
  #RawEventJuggler().Sequencer=GaudiSequencer("Spam") 
  #RawEventJuggler().KillExtraBanks=True 
  #RawEventJuggler().KillExtraNodes=True 
  #RawEventJuggler().WriterOptItemList=Writer 
  
  #from Configurables import ReadHltReport  
  #Moore().appendToMainSequence( [ ReadHltReport() ] )

  InputCopyStream("Writer").ItemList.append("/Event/DAQ/RawEvent#1")

  from Configurables import TimingAuditor, SequencerTimerTool
  TimingAuditor('TIMER').addTool(SequencerTimerTool, name="TIMER")
  TimingAuditor('TIMER').TIMER.NameSize=80
  
  

  
