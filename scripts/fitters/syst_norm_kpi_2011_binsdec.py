

#doGof = True

from wookie import config as wookie_config


def doChanges(w):

  w.obj("Del_Mass").setBins(int(w.obj("Del_Mass").getBins()*0.8))
  w.obj("D0_Mass").setBins(int(w.obj("D0_Mass").getBins()*0.8))

config = {  
    #'doFit':False,
    'doLimits':False,
    'doNlls':True,
    'doProfile':False,
    'doSPlot':False,
    #'doSPlot':True,
    'mode':'norm',
    'normScale': 1.0,
    'norm':'kpi',
    'normConstrained': False,
    'kpiFile': wookie_config.datasets["fitterkpi2011"]["file"],
    'doBinned': True,
    'doBinnedNll': True,
    'postHook': doChanges,
  }
