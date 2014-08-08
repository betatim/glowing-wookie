#!/usr/bin/env python

import ROOT
import GaudiPython
from Gaudi.Configuration import *

importOptions('$DAVINCIROOT/options/DaVinci-Default.py')

from Configurables import DaVinci
DaVinci().DataType = "2011"
DaVinci().HistogramFile = "DaVinci-plots.root"
DaVinci().Lumi = True
DaVinci().TupleFile = "DaVinci-lumi.root"

# Configuration
appMgrConf = ApplicationMgr( OutputLevel = INFO, AppName = 'myAnalysis' )

EventSelector().PrintFreq = 10 
EventSelector().OutputLevel = 1
#EventSelector().Input = ["data.dst"]
#EventSelector().Input=["00024181_00036685_1.charmcompleteevent.dst"]

#DataOnDemandSvc().Algorithms += ["DATA='/Event/MC/Particles' TYPE='UnpackMCParticle'"]
#DataOnDemandSvc().Algorithms += ["DATA='/Event/MC/Vertices' TYPE='UnpackMCVertex'"]

# acces to the actual service (event, tools, etc)
appMgr = GaudiPython.AppMgr() #from module GaudiPython
sel = appMgr.evtsel()
evt = appMgr.evtsvc()
hist = appMgr.histsvc()
toolSvc = appMgr.toolsvc()

std = GaudiPython.gbl.std
LHCb= GaudiPython.gbl.LHCb

strippingLine = "StrippingDstarD02xxDst2PiD02emuBoxDecision"

bins = 300
hmin = 1715
hmax = 2015

relations = {
  "Hlt2CharmHadD02HH_D02PiPiDecision": { 
    "nstr": hist.book('pipi_nstr_trigger_mass','pipi_nstr_trigger_mass', bins, hmin, hmax),
    "str" : hist.book('pipi_str_trigger_mass','pipi_str_trigger_mass', bins, hmin, hmax),
    "all" : hist.book('pipi_trigger_mass','pipi_trigger_mass', bins, hmin, hmax),
    },
  "Hlt2CharmHadD02HH_D02KPiDecision" : { 
    "nstr": hist.book('kpi_nstr_trigger_mass','kpi_nstr_trigger_mass', bins, hmin, hmax),
    "str" : hist.book('kpi_str_trigger_mass','kpi_str_trigger_mass', bins, hmin, hmax),
    "all" : hist.book('kpi_trigger_mass','kpi_trigger_mass', bins, hmin, hmax),
    },
  "Hlt2CharmHadD02HH_D02KKDecision"  : { 
    "nstr": hist.book('kk_nstr_trigger_mass','kk_nstr_trigger_mass', bins, hmin, hmax),
    "str" : hist.book('kk_str_trigger_mass','kk_str_trigger_mass', bins, hmin, hmax),
    "all" : hist.book('kk_trigger_mass','kk_trigger_mass', bins, hmin, hmax),
    },
  }

class MyAlg(GaudiPython.PyAlgorithm):
  def execute(self):
    eventHeader = evt['/Event/Rec/Header']
    if not eventHeader:
      # containers are required to exist by convention (even if empty)
      print "eventHeader not found - end of file"
      return False
    else:
      runNr = eventHeader.runNumber()
      eventNr = eventHeader.evtNumber()
      
    selReport = evt["/Event/Hlt/SelReports"]
    if not selReport:
      return True
    #decReport = evt["/Event/Hlt/DecReports"]
    decReport = evt["/Event/Strip/Phys/DecReports"]
    if not decReport:
      return True
    
    for name,plots in relations.iteritems():
      if selReport.hasSelectionName(name): 
        sr = selReport.selReport(name)
        strippingDec = False
        if decReport.hasDecisionName(strippingLine):
          strippingDec = (decReport.decReport(strippingLine).decision() == 1)
        for i in sr.substructure():
          mass = i.numericalInfo()["1#Particle.measuredMass"]
          print "--> Triggered by %s, with mass: %.2f, Stripped: %s" %(name,mass,repr(strippingDec))
          for i in decReport.decisionNames():
            print " ",i
          if strippingDec:
            plots["str"].fill(mass)
          else:
            plots["nstr"].fill(mass)
          plots["all"].fill(mass)
    
    return True

appMgr.addAlgorithm(MyAlg())
appMgr.run(-1)
