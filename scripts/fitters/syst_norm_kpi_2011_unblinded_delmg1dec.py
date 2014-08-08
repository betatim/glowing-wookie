

#doGof = True


def changeConstants(w):

    w.obj('Norm_D0M_Sig_Gaus1_Frac').setVal(0.7)
    w.obj('Norm_DelM_Sig_Gaus1_Frac').setVal(0.15)
    w.obj('Norm_DelM_Sig_Gaus3_Frac').setVal(0.15)

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
    'postHook': changeConstants,
  }
