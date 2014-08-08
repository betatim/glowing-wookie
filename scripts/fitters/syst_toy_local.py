

#doGof = True

try:
  from wookie import config as wookie_config
except ImportError:
  import config as wookie_config

from math import sqrt

config = {
  "mode":"toy",
  'doLimits':False,
  'doNlls':True,
  'doPlots':True,
  'doProfile':False,

  'normEvents': [(wookie_config.datasets["fitterkpi2011"]["lumi"]+wookie_config.datasets["fitterkpi2012"]["lumi"])/wookie_config.datasets["fitteremu2011unblind"]["lumi"]*30800.,1.2*sqrt(30800.*(wookie_config.datasets["fitterkpi2011"]["lumi"]+wookie_config.datasets["fitterkpi2012"]["lumi"])/wookie_config.datasets["fitteremu2011unblind"]["lumi"])],

  'normScale': (wookie_config.datasets["fitterkpi2011"]["lumi"]+wookie_config.datasets["fitterkpi2012"]["lumi"])/wookie_config.datasets["fitterkpi2011"]["lumi"],

  #'mvaFile': "fitter_loose_emu_2011_unblind.root",
  #'kinitCheck': False,
  }
