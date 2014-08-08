

#doGof = True

from wookie import config as wookie_config



def substituteExpForCheby(w):

  old_pdf = w.obj('Norm_D0M_Bkg')

  new_pdf = w.factory("RooChebychev::Norm_D0M_Bkg_Cheby(D0_Mass,{Norm_D0M_Bkg_Cheby_1,Norm_D0M_Bkg_Cheby_2[-0.1,-0.7,1]})")

  w.obj('Norm_Comb').replaceServer(old_pdf,new_pdf,True,False)
  w.obj('Norm_Comb').pdfList().replace(old_pdf,new_pdf)

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
    'postHook': substituteExpForCheby,
  }
