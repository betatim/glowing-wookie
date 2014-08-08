

#doGof = True

from wookie import config as wookie_config

config = {
  "mode":"mcpipi",
  'mvaFile': wookie_config.datasets["mcfitterpipiasemu2012"]["file"],
  #'doFit': False,
  'doLimits': False,
  'doProfile': False,
  'normConstrained': False,
  }
