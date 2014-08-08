

#doGof = True

from wookie import config as wookie_config

config = {
    #'doFit':False,
    'doLimits':False,
    'doNlls':True,
    'doProfile':False,
    'doSPlot':False,
    #'doSPlot':True,
    'mode':'mcnorm',
    #'normScale': 1.0,
    'norm':'kpi',
    'normConstrained': False,
    'kpiFile': wookie_config.datasets["mcfitterkpi2012"]["file"],
  }
