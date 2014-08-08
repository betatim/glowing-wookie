

#doGof = True

from wookie import config as wookie_config

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
  }
