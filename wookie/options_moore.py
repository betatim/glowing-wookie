

from Gaudi.Configuration import *
from LHCbKernel.Configuration import *


def execute(evtMax, dataType, mag, **leftovers):
    
  from Configurables import Moore
  from Configurables import L0MuonAlg
  from Configurables import L0Conf

  #Configure L0 emulation
  L0MuonAlg( "L0Muon" ).L0DUConfigProviderType = "L0DUConfigProvider"
  Moore().L0=False
  Moore().RunL0Emulator=False
  Moore().ForceSingleL0Configuration = True
  Moore().CheckOdin  = False

  # How are we configuring the trigger? TCK or settings? 
  Moore().ThresholdSettings = 'TomsCharmHadronLines' 
  #Moore().ThresholdSettings = 'Physics_September2012' 
  Moore().UseTCK = False
  #Moore().InitialTCK = '0x00a10045'                        #Change me to the TCK you want to use
  #Moore().WriterRequires=['HltDecsionSequence']            #What sequence must pass for the events to be written out? 
  Moore().WriterRequires=[] 
  Moore().UseDBSnapshot   = False
  Moore().EnableRunChangeHandler = False
  Moore().Verbose = False
  Moore().EvtMax = evtMax
  Moore().outputFile  = 'Demu.lsdata.dst'
  Moore().Split  = 'Hlt2'

  if dataType == "data2012":
    Moore().DataType = "2012"
    Moore().Simulation = False
    Moore().DDDBtag = "dddb-20130111"
    if mag == "up":
      Moore().CondDBtag = "cond-20130114"
    elif mag == "down":
      Moore().CondDBtag = "cond-20130114"
  elif dataType == "data2011":
    Moore().DataType = "2011"
    Moore().Simulation = False
    Moore().DDDBtag = "dddb-20130111"
    if mag == "up":
      Moore().CondDBtag = "cond-20130114"
    elif mag == "down":
      Moore().CondDBtag = "cond-20130114"

  from Configurables import bankKiller
  ### Since Moore was already run in production for MC10, kill the resulting
  ### rawbanks.
  #bk = bankKiller( "KillHltBanks", BankTypes = [ "HltRoutingBits", "HltSelReports", "HltVertexReports", "HltDecReports", "HltLumiSummary" ] )
  #bk.RawEventLocations = ["Trigger/RawEvent","Other/RawEvent","Calo/RawEvent","Muon/RawEvent","Rich/RawEvent"]
  #from Gaudi.Configuration import appendPostConfigAction
  #from Configurables import ApplicationMgr
  #appendPostConfigAction( lambda : ApplicationMgr().TopAlg.insert( 0, bk ) )
  
  bk = bankKiller( "KillHltBanks", BankTypes = [ "HltRoutingBits", "HltSelReports", "HltVertexReports", "HltDecReports", "HltLumiSummary" ] )
  bk.RawEventLocations = ['DAQ/RawEvent']
  appendPostConfigAction( lambda : ApplicationMgr().TopAlg.insert( 0, bk ) )

  from Configurables import RecombineRawEvent
  RecombineRawEvent()
  