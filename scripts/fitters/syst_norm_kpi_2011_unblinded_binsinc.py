

#doGof = True




def doChanges(w):

  w.obj("Del_Mass").setBins(int(w.obj("Del_Mass").getBins()*1.5))
  w.obj("D0_Mass").setBins(int(w.obj("D0_Mass").getBins()*1.5))

config = {  
    #'doFit':False,
    'doLimits':False,
    'doNlls':True,
    'doProfile':False,
    'doSPlot':False,
    #'doSPlot':True,
    'mode':'norm',
    #'normScale': 1.0,
    'norm':'kpi',
    'normConstrained': False,
    'doBinned': True,
    'doBinnedNll': True,
    'postHook': doChanges,
  }
