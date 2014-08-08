

#doGof = True




def doChanges(w):

  old_pdf = w.obj('Norm_DelM_Sig_Gaus3')

  new_pdf = w.factory("RooGaussian::Norm_DelM_Sig_Gaus3_SharedMean(Del_Mass,Norm_DelM_Sig_Gaus_Mean_Shifted,Norm_DelM_Sig_Gaus3_Sigma)")

  w.obj('Norm_DelM_Sig').replaceServer(old_pdf,new_pdf,True,False)
  w.obj('Norm_DelM_Sig').pdfList().replace(old_pdf,new_pdf)

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
