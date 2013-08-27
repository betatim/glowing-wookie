


def setup_workspace(config):

  import ROOT
  from ROOT import RooWorkspace, gROOT, gStyle, RooAbsReal, RooMsgService, RooFit
  #from ROOT import RooFit, gROOT, gDirectory, gStyle, gPad, TTree, RooCmdArg,RooBinning
  #from ROOT import RooRealVar, RooMappedCategory, RooCategory, RooFormulaVar, RooAbsData
  #from ROOT import RooBMixDecay, RooMCStudy, RooAddModel, RooEffProd, RooMsgService
  #from ROOT import RooWorkspace, TCanvas, TFile, kFALSE, kTRUE, RooDataSet, TStopwatch
  #from ROOT import RooArgSet, RooArgList, RooRandom, RooMinuit, RooAbsReal, RooDataHist
  #from ROOT import TBrowser, TH2F, TF1, TH1F, RooGenericPdf, RooLinkedList

  gROOT.SetStyle("Plain")
  gStyle.SetPalette(1)
  gStyle.SetOptStat(0)
  gStyle.SetOptFit(0)
  gStyle.SetOptStat(1111)
  gStyle.SetOptFit(10111)
  gStyle.SetOptTitle(1)
  
  gROOT.ProcessLine(".L RooGaussianTrunk.cxx+")
  from ROOT import RooGaussianTrunk

  #RooAbsReal.defaultIntegratorConfig().Print()
  RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-8)
  RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-8)
  #RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-6)
  #RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-6)
  RooAbsReal.defaultIntegratorConfig().Print()

  print "Numeric integration set up" #TODO: is the integration acceptable?

  ##This controls the logging output from RooFit
  #RooMsgService.instance().addStream(RooFit.DEBUG,RooFit.Topic(RooFit.Fitting))
  RooMsgService.instance().deleteStream(1)
  #RooMsgService.instance().addStream(RooFit.INFO,RooFit.Topic(RooFit.Generation + RooFit.Minization + RooFit.Plotting + RooFit.Fitting + RooFit.Integration + RooFit.LinkStateMgmt + RooFit.Eval + RooFit.Caching + RooFit.Optimization + RooFit.ObjectHandling + RooFit.InputArguments + RooFit.Tracing + RooFit.Contents + RooFit.DataHandling + RooFit.NumericIntegration))
  RooMsgService.instance().addStream(RooFit.INFO,RooFit.Topic(RooFit.LinkStateMgmt + RooFit.Caching + RooFit.ObjectHandling + RooFit.InputArguments + RooFit.Tracing))
  RooMsgService.instance().Print()


  print "Message service set up"

  w = RooWorkspace("w",False)

  w.factory("RAND[0,1]")
  D0_M = w.factory("D0_M[1600,2000]") #TODO: define mass ranges slightly better
  #D0_M = w.factory("D0_M[1825,1930]") #TODO: define mass ranges slightly better
  Del_M = w.factory("Del_M[139,155]")
  Del_M.setUnit("MeV")
  D0_M.setUnit("MeV")
  D0_M.setBins(200)

  Dataset = w.factory("DataSet[BDT1,BDT2,BDT3,PiPi]")
  
  w.factory("classID[Sig=0,Bkg=1]")
  w.factory("BDT_ada[-1,1]")
  
  D0_M.setRange("blinded",1700.,1900.)
  
  for data in ["", "BDT1", "BDT2", "BDT3", "PiPi"]:
    for dst_side in ["", "delsig", "delhigh", "dellow"]:
      for d_side in ["", "dsig", "dhigh", "dlow"]:
        name = data+dst_side+d_side
        
        if data == "BDT1":
          Dataset.setRange(name,"BDT1")
        elif data == "BDT2":
          Dataset.setRange(name,"BDT2")
        elif data == "BDT3":
          Dataset.setRange(name,"BDT3")
        elif data == "PiPi":
          Dataset.setRange(name,"PiPi")
        
        if dst_side == "delhigh":
          Del_M.setRange(name,148.,155.)
        elif dst_side == "delsig":
          Del_M.setRange(name,143.,148.)
        elif dst_side == "dellow":
          Del_M.setRange(name,139.,143.)
          
        if d_side == "dhigh":
          D0_M.setRange(name,1885.,2000.)
        elif d_side == "dsig":
          D0_M.setRange(name,1835.,1885.)
        elif d_side == "dlow":
          D0_M.setRange(name,1600.,1835.)

  w.defineSet("args","D0_M,Del_M,DataSet")
  w.defineSet("argsBasic","D0_M,Del_M")
  w.defineSet("argsPreCut","D0_M,Del_M,RAND,classID,BDT_ada")
  w.defineSet("argsPreCutPiPi","D0_M,Del_M,RAND")

  # --- PiPi ---
  w.factory("RooGenericPdf::PiPi_D0M_Range('(D0_M>PiPi_D0M_Min&&D0_M<PiPi_D0M_Max)',{D0_M,PiPi_D0M_Min[1800],PiPi_D0M_Max[1930]})")

  #  D0_M Signal
  w.factory("RooGaussianTrunk::PiPi_D0M_Sig_Gaus1(D0_M,PiPi_D0M_Sig_Gaus_Mean[1867,1850,1880],PiPi_D0M_Sig_Gaus_Sigma1[5,0,10],PiPi_D0M_Min,PiPi_D0M_Max)")
  w.factory("RooGaussianTrunk::PiPi_D0M_Sig_Gaus2(D0_M,PiPi_D0M_Sig_Gaus_Mean,PiPi_D0M_Sig_Gaus_Sigma2[11,5,15],PiPi_D0M_Min,PiPi_D0M_Max)")
  w.factory("SUM::PiPi_D0M_Sig(PiPi_D0M_Sig_Gaus1_Frac[0.5,0,1]*PiPi_D0M_Sig_Gaus1,PiPi_D0M_Sig_Gaus2)")
  #w.factory("PROD::PiPi_D0M_Sig(PiPi_D0M_Sig_Sum,PiPi_D0M_Range)")
  
  #  D0_M MisId
  w.factory("RooGaussianTrunk::PiPi_D0M_MisId_Gaus1(D0_M,PiPi_D0M_MisId_Gaus_Mean[1790,1720,1820],PiPi_D0M_Sig_Gaus_Sigma1,PiPi_D0M_Min,PiPi_D0M_Max)")
  w.factory("RooGaussianTrunk::PiPi_D0M_MisId_Gaus2(D0_M,PiPi_D0M_MisId_Gaus_Mean,PiPi_D0M_Sig_Gaus_Sigma2,PiPi_D0M_Min,PiPi_D0M_Max)")
  w.factory("SUM::PiPi_D0M_MisId(PiPi_D0M_Sig_Gaus1_Frac*PiPi_D0M_MisId_Gaus1,PiPi_D0M_MisId_Gaus2)")
  #w.factory("PROD::PiPi_D0M_MisId(PiPi_D0M_MisId_Sum,PiPi_D0M_Range)")
  #w.factory("RooExponential::PiPi_D0M_MisId_Exp(D0_M,PiPi_D0M_MisId_Exp_Const[-0.15,-.3,-.1])")
  #w.factory("PROD::PiPi_D0M_MisId(PiPi_D0M_MisId_Exp,PiPi_D0M_Range)")
  
  #  D0_M Combinatorical
  w.factory("RooChebychev::PiPi_D0M_Bkg_Poly(D0_M,{PiPi_D0M_Bkg_Poly_a1[-0.25,-1.5,1]})")
  w.factory("PROD::PiPi_D0M_Bkg(PiPi_D0M_Bkg_Poly,PiPi_D0M_Range)")
  
  #  Del_M signal
  w.factory("RooGaussian::PiPi_DelM_Sig_Gaus1(Del_M,PiPi_DelM_Sig_Gaus_Mean[145.5,145,146],PiPi_DelM_Sig_Gaus_Sigma1[.4,0,1] )")
  w.factory("RooGaussian::PiPi_DelM_Sig_Gaus2(Del_M,PiPi_DelM_Sig_Gaus_Mean,PiPi_DelM_Sig_Gaus_Sigma2[.7,.1,2] )")
  w.factory("SUM::PiPi_DelM_Sig(PiPi_DelM_Sig_Gaus1_Frac[0.05,0,.5]*PiPi_DelM_Sig_Gaus1,PiPi_DelM_Sig_Gaus2)")

  #  Del_M Combinatorical
  w.factory("RooDstD0BG::PiPi_DelM_Bkg(Del_M,PiPi_DelM_Bkg_m0[139.5,137.5,140.5],PiPi_DelM_Bkg_c[40,7,350],PiPi_DelM_Bkg_a[-20,-100,-1],PiPi_DelM_Bkg_b[0.4,-0.1,2])")

  #  Del_M signal
  w.factory("RooGaussian::PiPi_DelM_MisId(Del_M,PiPi_DelM_Sig_Gaus_Mean,PiPi_DelM_MisId_Gaus_Sigma1[1,0,3])")

  w.factory("PROD::PiPi_Sig(PiPi_DelM_Sig,PiPi_D0M_Sig)")
  w.factory("PROD::PiPi_Comb(PiPi_DelM_Bkg,PiPi_D0M_Bkg)")
  w.factory("PROD::PiPi_MisId(PiPi_DelM_MisId,PiPi_D0M_MisId)")
  #w.factory("PROD::PiPi_MisId(PiPi_DelM_Sig,PiPi_D0M_MisId)")
  w.factory("PROD::PiPi_MisId_Prompt(PiPi_DelM_Bkg,PiPi_D0M_MisId)")
  w.factory("PROD::PiPi_Prompt(PiPi_DelM_Bkg,PiPi_D0M_Sig)")
  
  w.factory("SUM::PiPi_Final_PDF(PiPi_N_Sig[65000,20000,110000]*PiPi_Sig,PiPi_N_Prompt[35000,20000,60000]*PiPi_Prompt,PiPi_N_Comb[67000,1000,90000]*PiPi_Comb,PiPi_N_MisId[1300,100,3000]*PiPi_MisId,PiPi_N_MisId_Prompt[500,10,1000]*PiPi_MisId_Prompt)")
  #w.factory("SUM::PiPi_Final_PDF(PiPi_N_Sig[65000,20000,110000]*PiPi_Sig,PiPi_N_Prompt[35000,20000,60000]*PiPi_Prompt,PiPi_N_Comb[67000,1000,90000]*PiPi_Comb,PiPi_N_MisId[1300,100,3000]*PiPi_MisId)")
  #w.factory("SUM::PiPi_Final_PDF(PiPi_N_Sig[65000,20000,110000]*PiPi_Sig,PiPi_N_Prompt[35000,20000,60000]*PiPi_Prompt,PiPi_N_Comb[67000,1000,90000]*PiPi_Comb,PiPi_N_MisId_Prompt[500,10,1000]*PiPi_MisId_Prompt)")
  #w.factory("SUM::PiPi_Final_PDF(PiPi_N_Sig[65000,20000,110000]*PiPi_Sig,PiPi_N_Prompt[35000,20000,60000]*PiPi_Prompt,PiPi_N_Comb[67000,1000,90000]*PiPi_Comb)")
  

  # --- eMu ---
  
  #w.factory("EMu_N_Sig[1000,0,100000]")
  for n in (1,2,3):
    w.factory("BDT%(n)i_Sig_Eff[0.3,0,1]"%({"n":n}))
    
  w.factory("EMu_Eff[%f]"%(config['emuEff']))
  w.factory("EMu_BR[1e-8,-1e-7,1e-7]")
  
  w.factory("PiPi_Eff[%f]"%(config['pipiEff']))
  w.factory("PiPi_BR[%f]"%(config['pipiBR'][0]))
  w.obj("PiPi_BR").setError(config['pipiBR'][1])
  
  w.factory("RooFormulaVar::EMu_N_Sig('abs(PiPi_N_Sig*((EMu_BR*EMu_Eff)/(PiPi_BR*PiPi_Eff)))',{PiPi_BR,EMu_BR,EMu_Eff,PiPi_Eff,PiPi_N_Sig})")
    
    
  #  D0_M Combinatorical
  w.factory("RooGenericPdf::BDT_D0M_Blind('(D0_M<1700||D0_M>1900)',{D0_M})")
  w.factory("RooExponential::BDT_D0M_Bkg(D0_M,BDT_D0M_Bkg_Exp_Const[-0.001,-0.01,0.01])")
  w.factory("PROD::BDT_D0M_Bkg_Blind(BDT_D0M_Bkg,BDT_D0M_Blind)")
  
  #  Del_M Combinatorical
  w.factory("RooDstD0BG::BDT_DelM_Bkg(Del_M,BDT_DelM_Bkg_m0[139.5,137.5,140.5],BDT_DelM_Bkg_c[40,7,350],BDT_DelM_Bkg_a[-20,-100,-1],BDT_DelM_Bkg_b[-0.1,-2,1])"%({"n":n}))
    
  for n in (1,2,3):
    if n is not 3:
      w.factory("RooFormulaVar::BDT%(n)i_N_Sig('EMu_N_Sig*BDT%(n)i_Sig_Eff',{EMu_N_Sig,BDT%(n)i_Sig_Eff})"%({"n":n}))
    else:
      w.factory("RooFormulaVar::BDT%(n)i_N_Sig('EMu_N_Sig*(1-(BDT1_Sig_Eff+BDT2_Sig_Eff))',{EMu_N_Sig,BDT1_Sig_Eff,BDT2_Sig_Eff})"%({"n":n}))
      
    #  D0_M Signal
    w.factory("CBShape:BDT%(n)i_D0M_Sig_CB1(D0_M, BDT%(n)i_D0M_Sig_CB_Mean[1850,1750,1900], BDT%(n)i_D0M_Sig_CB1_Sigma[10,1,30], BDT%(n)i_D0M_Sig_CB1_alphaleft[0.5,0,5], BDT%(n)i_D0M_Sig_CB1_n[2,0,10])"%({"n":n}))
    w.factory("CBShape:BDT%(n)i_D0M_Sig_CB2(D0_M, BDT%(n)i_D0M_Sig_CB_Mean, BDT%(n)i_D0M_Sig_CB2_Sigma[3,1,30], BDT%(n)i_D0M_Sig_CB2_alpharight[-0.5,-5,0], BDT%(n)i_D0M_Sig_CB2_n[5,0,50])"%({"n":n}))
    w.factory("SUM::BDT%(n)i_D0M_Sig(BDT%(n)i_D0M_Sig_CB1_Frac[0.8,0,1]*BDT%(n)i_D0M_Sig_CB1,BDT%(n)i_D0M_Sig_CB2)"%({"n":n}))
  
    #  Del_M signal
    w.factory("RooGaussian::BDT%(n)i_DelM_Sig_Gaus1(Del_M,BDT%(n)i_DelM_Sig_Gaus_Mean[145.5,143,148],BDT%(n)i_DelM_Sig_Gaus_Sigma1[1,0,5] )"%({"n":n}))
    w.factory("RooGaussian::BDT%(n)i_DelM_Sig_Gaus2(Del_M,BDT%(n)i_DelM_Sig_Gaus_Mean,BDT%(n)i_DelM_Sig_Gaus_Sigma2[.1,0,2] )"%({"n":n}))
    w.factory("SUM::BDT%(n)i_DelM_Sig(BDT%(n)i_DelM_Sig_Gaus1_Frac[0.8,0,1]*BDT%(n)i_DelM_Sig_Gaus1,BDT%(n)i_DelM_Sig_Gaus2)"%({"n":n}))
    
    w.factory("PROD::BDT%(n)i_Sig(BDT%(n)i_DelM_Sig,BDT%(n)i_D0M_Sig)"%({"n":n}))
    w.factory("PROD::BDT%(n)i_Comb_Blind(BDT_DelM_Bkg,BDT_D0M_Bkg_Blind)"%({"n":n}))
    w.factory("PROD::BDT%(n)i_Comb(BDT_DelM_Bkg,BDT_D0M_Bkg)"%({"n":n}))
    
    w.factory("SUM::BDT%(n)i_Final_PDF_Blind(BDT%(n)i_N_Sig*BDT%(n)i_Sig,BDT%(n)i_N_Comb[1000,0,10000]*BDT%(n)i_Comb_Blind)"%({"n":n}))
    w.factory("SUM::BDT%(n)i_Final_PDF(BDT%(n)i_N_Sig*BDT%(n)i_Sig,BDT%(n)i_N_Comb*BDT%(n)i_Comb)"%({"n":n}))
  
  w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMax(1.0)
  w.obj('PiPi_D0M_Sig_Gaus1_Frac').setVal(0.429624062534) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setError(0.0289511133792)
  w.obj('PiPi_D0M_Sig_Gaus1_Frac').setConstant(False)
  w.obj('PiPi_D0M_Sig_Gaus_Mean').setMin(1850.0) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setMax(1880.0)
  w.obj('PiPi_D0M_Sig_Gaus_Mean').setVal(1867.01515277) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setError(0.0296569841856)
  w.obj('PiPi_D0M_Sig_Gaus_Mean').setConstant(False)
  w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMin(0.0) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMax(10.0)
  w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setVal(6.92118344347) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setError(0.117795059995)
  w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setConstant(False)
  w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setMin(5.0) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setMax(15.0)
  w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setVal(10.3140938882) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setError(0.117955520203)
  w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setConstant(False)
  w.obj('PiPi_DelM_Bkg_a').setMin(-100.0) ; w.obj('PiPi_DelM_Bkg_a').setMax(-1.0)
  w.obj('PiPi_DelM_Bkg_a').setVal(-16.1932460031) ; w.obj('PiPi_DelM_Bkg_a').setError(0.43302849663)
  w.obj('PiPi_DelM_Bkg_a').setConstant(False)
  w.obj('PiPi_DelM_Bkg_b').setMin(-0.1) ; w.obj('PiPi_DelM_Bkg_b').setMax(2.0)
  w.obj('PiPi_DelM_Bkg_b').setVal(0.178920942238) ; w.obj('PiPi_DelM_Bkg_b').setError(0.0376477247211)
  w.obj('PiPi_DelM_Bkg_b').setConstant(False)
  w.obj('PiPi_DelM_Bkg_c').setMin(7.0) ; w.obj('PiPi_DelM_Bkg_c').setMax(350.0)
  w.obj('PiPi_DelM_Bkg_c').setVal(36.1602832374) ; w.obj('PiPi_DelM_Bkg_c').setError(5.19925002062)
  w.obj('PiPi_DelM_Bkg_c').setConstant(False)
  w.obj('PiPi_DelM_Bkg_m0').setMin(137.5) ; w.obj('PiPi_DelM_Bkg_m0').setMax(140.5)
  w.obj('PiPi_DelM_Bkg_m0').setVal(139.316358242) ; w.obj('PiPi_DelM_Bkg_m0').setError(5.10021351516e-05)
  w.obj('PiPi_DelM_Bkg_m0').setConstant(False)
  w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMax(1.)
  w.obj('PiPi_DelM_Sig_Gaus1_Frac').setVal(0.279248861884) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setError(0.0191547718614)
  w.obj('PiPi_DelM_Sig_Gaus1_Frac').setConstant(False)
  w.obj('PiPi_DelM_Sig_Gaus_Mean').setMin(145.0) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setMax(146.0)
  w.obj('PiPi_DelM_Sig_Gaus_Mean').setVal(145.448069656) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setError(0.00294967951486)
  w.obj('PiPi_DelM_Sig_Gaus_Mean').setConstant(False)
  w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMin(0.0) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMax(1.0)
  w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setVal(0.429900766218) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setError(0.0119155696871)
  w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setConstant(False)
  w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMin(0.1) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMax(2.0)
  w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setVal(0.827483577936) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setError(0.00898522299303)
  w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setConstant(False)




  if config['mode'] is 'mc':
    w.factory("SIMUL::Final_PDF(DataSet,BDT1=BDT1_Sig,BDT2=BDT2_Sig,BDT3=BDT3_Sig)")
    
  elif config['mode'] is 'datapretoy':
    w.factory("SIMUL::Final_PDF(DataSet,BDT1=BDT1_Comb_Blind,BDT2=BDT2_Comb_Blind,BDT3=BDT3_Comb_Blind)")
    
  elif config['mode'] is 'toy':
    w.factory("SIMUL::Final_PDF(DataSet,PiPi=PiPi_Final_PDF,BDT1=BDT1_Final_PDF,BDT2=BDT2_Final_PDF,BDT3=BDT3_Final_PDF)")
    w.factory("SIMUL::Final_PDF_Background(DataSet,PiPi=PiPi_Final_PDF,BDT1=BDT1_Comb,BDT2=BDT2_Comb,BDT3=BDT3_Comb)")
    
  elif config['mode'] is 'data':
    w.factory("SIMUL::Final_PDF(DataSet,PiPi=PiPi_Final_PDF,BDT1=BDT1_Final_PDF,BDT2=BDT2_Final_PDF,BDT3=BDT3_Final_PDF)")
    w.factory("SIMUL::Final_PDF_Background(DataSet,PiPi=PiPi_Final_PDF,BDT1=BDT1_Comb,BDT2=BDT2_Comb,BDT3=BDT3_Comb)")
    
  if config['mode'] is 'toy':
    w.obj('BDT_D0M_Bkg_Exp_Const').setMin(-0.01) ; w.obj('BDT_D0M_Bkg_Exp_Const').setMax(0.003)
    w.obj('BDT_D0M_Bkg_Exp_Const').setVal(-0.00383788482662) ; w.obj('BDT_D0M_Bkg_Exp_Const').setError(0.000116387358186)
    w.obj('BDT_D0M_Bkg_Exp_Const').setConstant(False)
    w.obj('BDT_DelM_Bkg_a').setMin(-19.0) ; w.obj('BDT_DelM_Bkg_a').setMax(-1.0)
    w.obj('BDT_DelM_Bkg_a').setVal(-13.3201629713) ; w.obj('BDT_DelM_Bkg_a').setError(2.49499373145)
    w.obj('BDT_DelM_Bkg_a').setConstant(False)
    w.obj('BDT_DelM_Bkg_b').setMin(-0.35) ; w.obj('BDT_DelM_Bkg_b').setMax(1.0)
    w.obj('BDT_DelM_Bkg_b').setVal(-0.174366431028) ; w.obj('BDT_DelM_Bkg_b').setError(0.523782969093)
    w.obj('BDT_DelM_Bkg_b').setConstant(False)
    w.obj('BDT_DelM_Bkg_c').setMin(7.0) ; w.obj('BDT_DelM_Bkg_c').setMax(200.0)
    w.obj('BDT_DelM_Bkg_c').setVal(94.6348929704) ; w.obj('BDT_DelM_Bkg_c').setError(173.109088403)
    w.obj('BDT_DelM_Bkg_c').setConstant(False)
    w.obj('BDT_DelM_Bkg_m0').setMin(137.5) ; w.obj('BDT_DelM_Bkg_m0').setMax(140.5)
    w.obj('BDT_DelM_Bkg_m0').setVal(139.439614429) ; w.obj('BDT_DelM_Bkg_m0').setError(0.0561243850283)
    w.obj('BDT_DelM_Bkg_m0').setConstant(False)
    
    w.obj('BDT1_N_Comb').setMin(1500.0) ; w.obj('BDT1_N_Comb').setMax(10000.0)
    w.obj('BDT1_N_Comb').setVal(6300) ; w.obj('BDT1_N_Comb').setError(78.0712836713)
    w.obj('BDT1_N_Comb').setConstant(False)
    w.obj('BDT2_N_Comb').setMin(400.0) ; w.obj('BDT2_N_Comb').setMax(8000.0)
    w.obj('BDT2_N_Comb').setVal(2500) ; w.obj('BDT2_N_Comb').setError(49.6890669655)
    w.obj('BDT2_N_Comb').setConstant(False)
    w.obj('BDT3_N_Comb').setMin(0.0) ; w.obj('BDT3_N_Comb').setMax(4000.0)
    w.obj('BDT3_N_Comb').setVal(300.) ; w.obj('BDT3_N_Comb').setError(17.9550133537)
    w.obj('BDT3_N_Comb').setConstant(False)
    
  if config['mode'] is 'toy' or config['mode'] is 'data':
    w.obj('EMu_BR').setMin(-1e-07) ; w.obj('EMu_BR').setMax(1e-07)
    w.obj('EMu_BR').setVal(1e-08)
    w.obj('EMu_BR').setConstant(False)
    w.obj('PiPi_D0M_Bkg_Poly_a1').setMin(-1.) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setMax(1.0)
    w.obj('PiPi_D0M_Bkg_Poly_a1').setVal(-0.5)
    w.obj('PiPi_D0M_Bkg_Poly_a1').setConstant(False)

    w.obj('PiPi_D0M_MisId_Gaus_Mean').setMin(1760.0) ; w.obj('PiPi_D0M_MisId_Gaus_Mean').setMax(1815.0)
    w.obj('PiPi_D0M_MisId_Gaus_Mean').setVal(1798.57970965) ; w.obj('PiPi_D0M_MisId_Gaus_Mean').setError(0.298300692849)
    w.obj('PiPi_D0M_MisId_Gaus_Mean').setConstant(False)
    
    #w.obj('PiPi_D0M_MisId_Exp_Const').setMin(-0.3) ; w.obj('PiPi_D0M_MisId_Exp_Const').setMax(-0.1)
    #w.obj('PiPi_D0M_MisId_Exp_Const').setVal(-0.15) 
    #w.obj('PiPi_D0M_MisId_Exp_Const').setConstant(False)
    w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMax(7.0)
    w.obj('PiPi_D0M_Sig_Gaus1_Frac').setVal(0.3)
    w.obj('PiPi_D0M_Sig_Gaus1_Frac').setConstant(False)
    w.obj('PiPi_D0M_Sig_Gaus_Mean').setMin(1864.5) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setMax(1869.0)
    w.obj('PiPi_D0M_Sig_Gaus_Mean').setVal(1867.)
    w.obj('PiPi_D0M_Sig_Gaus_Mean').setConstant(False)
    w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMin(3.0) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMax(10.0)
    w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setVal(7)
    w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setConstant(False)
    w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setMin(7.5) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setMax(14.0)
    w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setVal(10.3140938882)
    #w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setConstant(False)
    #w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setVal(14)
    w.obj('PiPi_D0M_Sig_Gaus_Sigma2').setConstant(True)
    w.obj('PiPi_DelM_Bkg_a').setMin(-45.0) ; w.obj('PiPi_DelM_Bkg_a').setMax(-5.0)
    w.obj('PiPi_DelM_Bkg_a').setVal(-16)
    w.obj('PiPi_DelM_Bkg_a').setConstant(False)
    w.obj('PiPi_DelM_Bkg_b').setMin(-0.05) ; w.obj('PiPi_DelM_Bkg_b').setMax(1.5)
    w.obj('PiPi_DelM_Bkg_b').setVal(0.178920942238)
    w.obj('PiPi_DelM_Bkg_b').setConstant(False)
    w.obj('PiPi_DelM_Bkg_c').setMin(7.0) ; w.obj('PiPi_DelM_Bkg_c').setMax(250.0)
    w.obj('PiPi_DelM_Bkg_c').setVal(36.1602832374)
    w.obj('PiPi_DelM_Bkg_c').setConstant(False)
    w.obj('PiPi_DelM_Bkg_m0').setMin(138.2) ; w.obj('PiPi_DelM_Bkg_m0').setMax(139.6)
    w.obj('PiPi_DelM_Bkg_m0').setVal(139.2)
    w.obj('PiPi_DelM_Bkg_m0').setConstant(False)
    w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMax(.75)
    w.obj('PiPi_DelM_Sig_Gaus1_Frac').setVal(0.279248861884)
    w.obj('PiPi_DelM_Sig_Gaus1_Frac').setConstant(False)   
    w.obj('PiPi_DelM_Sig_Gaus_Mean').setMin(145.2) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setMax(145.7)
    w.obj('PiPi_DelM_Sig_Gaus_Mean').setVal(145.448069656)
    w.obj('PiPi_DelM_Sig_Gaus_Mean').setConstant(False)
    w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMin(0.2) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMax(1.0)
    w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setVal(0.429900766218)
    w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setConstant(False)  
    w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMin(0.65) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMax(1.2)
    w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setVal(0.827483577936)
    w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setConstant(False)  
    w.obj('PiPi_N_Comb').setMin(45000.0) ; w.obj('PiPi_N_Comb').setMax(100000.0)
    w.obj('PiPi_N_Comb').setVal(70000.0)
    w.obj('PiPi_N_Comb').setConstant(False)
    w.obj('PiPi_N_MisId').setMin(100.0) ; w.obj('PiPi_N_MisId').setMax(15000.0)
    w.obj('PiPi_N_MisId').setVal(5000.0)
    w.obj('PiPi_N_MisId').setConstant(False)
    w.obj('PiPi_N_MisId_Prompt').setMin(10.0) ; w.obj('PiPi_N_MisId_Prompt').setMax(10000.0)
    w.obj('PiPi_N_MisId_Prompt').setVal(3000.0)
    w.obj('PiPi_N_MisId_Prompt').setConstant(False)
    w.obj('PiPi_N_Prompt').setMin(20000.0) ; w.obj('PiPi_N_Prompt').setMax(60000.0)
    w.obj('PiPi_N_Prompt').setVal(40000.0)
    w.obj('PiPi_N_Prompt').setConstant(False)
    w.obj('PiPi_N_Sig').setMin(60000.0) ; w.obj('PiPi_N_Sig').setMax(110000.0)
    w.obj('PiPi_N_Sig').setVal(83000.0)
    w.obj('PiPi_N_Sig').setConstant(False)
    
    # nll analyse, nlls up to 1610.0 on Thu Aug 22 07:44:53 2013 run on fitResult.toy.root
    #
    # BDT1_N_Comb  has a low last bin. Orig limits 1500.0 10000.0
    w.obj('BDT1_N_Comb').setMin(2817.5) ; w.obj('BDT1_N_Comb').setMax(13836.6829458) ; w.obj('BDT1_N_Comb').setVal(6430.0) ; w.obj('BDT1_N_Comb').setError(78.16912487)
    w.obj('BDT2_N_Comb').setMin(647.0) ; w.obj('BDT2_N_Comb').setMax(7848.0) ; w.obj('BDT2_N_Comb').setVal(2528.0) ; w.obj('BDT2_N_Comb').setError(49.7511674856)
    # ---->>>> changeRatio up 1.71208468964 at 1.25 : 4 229.964766857 134.318569781
    # ---->>>> changeRatio up 1.41187435976 at 1.875 : 5 134.318569781 95.1349309894
    # ---->>>> changeRatio up 1.29156111311 at 2.5 : 6 95.1349309894 73.6588691187
    # ---->>>> changeRatio up 1.22616041265 at 3.125 : 7 73.6588691187 60.0727835924
    w.obj('BDT3_N_Comb').setMin(3.75) ; w.obj('BDT3_N_Comb').setMax(3920.0) ; w.obj('BDT3_N_Comb').setVal(320.0) ; w.obj('BDT3_N_Comb').setError(17.9773757533)
    w.obj('BDT_D0M_Bkg_Exp_Const').setMin(-0.00948) ; w.obj('BDT_D0M_Bkg_Exp_Const').setMax(0.00274) ; w.obj('BDT_D0M_Bkg_Exp_Const').setVal(-0.00376) ; w.obj('BDT_D0M_Bkg_Exp_Const').setError(9.39003902677e-05)
    # BDT_DelM_Bkg_a  has a low last bin. Orig limits -19.0 -1.0
    #w.obj('BDT_DelM_Bkg_a').setMin(-18.29125) ; w.obj('BDT_DelM_Bkg_a').setMax(6.29049000051) ; w.obj('BDT_DelM_Bkg_a').setVal(-12.52) ; w.obj('BDT_DelM_Bkg_a').setError(1.38191725362)
    # ---->>>> changeRatio up 13.5294294249 at -0.3358671875 : 52 800.737432959 59.1848634417
    # ---->>>> changeRatio up 1.58939590273 at -0.33565625 : 53 59.1848634417 37.237332335
    # ---->>>> changeRatio up 1.3038061916 at -0.3354453125 : 54 37.237332335 28.5604812853
    # BDT_DelM_Bkg_b  has a low last bin. Orig limits -0.35 1.0
    # Dont want to expand max range to 2.60885655742 too far
    #w.obj('BDT_DelM_Bkg_b').setMin(-0.335234375) ; w.obj('BDT_DelM_Bkg_b').setMax(2.0125) ; w.obj('BDT_DelM_Bkg_b').setVal(-0.188) ; w.obj('BDT_DelM_Bkg_b').setError(0.0594738541476)
    # ---->>>> changeRatio down 284.974183207 at 190.56109375 : 130 -692.863568519 -2.43132048217
    # ---->>>> changeRatio down 0.122412457239 at 190.59125 : 131 -2.43132048217 -19.8617080075
    # ---->>>> changeRatio down 1.79561662651 at 192.28 : 138 -32.96389932 -18.3579828975
    # ---->>>> changeRatio down 1.76598497828 at 192.7625 : 142 -25.5358040764 -14.4598082036
    # ---->>>> changeRatio down 1.73615628991 at 193.00375 : 146 -21.159650825 -12.1876417163
    # ---->>>> changeRatio down 0.743680534501 at 193.15453125 : 151 -23.0855347938 -31.0422738297
    # ---->>>> changeRatio down 0.630331112484 at 193.1846875 : 152 -31.0422738297 -49.2475672149
    # ---->>>> changeRatio down 0.321516357701 at 193.21484375 : 153 -49.2475672149 -153.172820093
    # ---->>>> changeRatio down 0.229905093837 at 193.245 : 154 -153.172820093 -666.243698806
    # ---->>>> changeRatio down 262.965205232 at 193.27515625 : 155 -666.243698806 -2.53358119458
    # ---->>>> changeRatio down 0.495036413738 at 193.3053125 : 156 -2.53358119458 -5.11796935392
    # ---->>>> changeRatio down 0.488109184739 at 193.365625 : 157 -5.11796935392 -10.4852961467
    # ---->>>> changeRatio down 0.477536898984 at 193.48625 : 158 -10.4852961467 -21.9570386477
    # ---->>>> changeRatio down 1.80204090934 at 194.93375 : 164 -33.5159821071 -18.598901908
    # ---->>>> changeRatio down 1.73052201772 at 195.536875 : 169 -29.5131186984 -17.0544600971
    # ---->>>> changeRatio down 1.74911685292 at 195.7178125 : 172 -22.3247476566 -12.7634398007
    # ---->>>> changeRatio down 0.782281500577 at 195.86859375 : 177 -22.6612042158 -28.9680942207
    # ---->>>> changeRatio down 0.705856006142 at 195.89875 : 178 -28.9680942207 -41.0396652698
    # ---->>>> changeRatio down 0.551968209414 at 195.92890625 : 179 -41.0396652698 -74.3515017167
    # ---->>>> changeRatio down 0.0810063093924 at 195.9590625 : 180 -74.3515017167 -917.84827965
    # ---->>>> changeRatio down 366.706525093 at 195.98921875 : 181 -917.84827965 -2.50295049814
    # ---->>>> changeRatio down 0.245873442658 at 196.019375 : 182 -2.50295049814 -10.1798326451
    # ---->>>> changeRatio down 0.479437343874 at 196.14 : 183 -10.1798326451 -21.2328738576
    # ---->>>> changeRatio down 1.81961883296 at 197.5875 : 189 -31.8853236806 -17.5230785168
    # ---->>>> changeRatio down 1.75787459068 at 198.190625 : 194 -25.471008871 -14.4896621215
    # ---->>>> changeRatio down 1.74114833751 at 198.4921875 : 199 -23.2347640618 -13.3445057846
    # ---->>>> changeRatio down 0.772284146074 at 198.64296875 : 204 -24.2451080079 -31.3940252835
    # ---->>>> changeRatio down 0.689191077574 at 198.673125 : 205 -31.3940252835 -45.5519903044
    # ---->>>> changeRatio down 0.514221320665 at 198.70328125 : 206 -45.5519903044 -88.584406118
    # ---->>>> changeRatio down 0.0973110301413 at 198.7334375 : 207 -88.584406118 -910.322354921
    # ---->>>> changeRatio down 379.317760963 at 198.76359375 : 208 -910.322354921 -2.39989383204
    # ---->>>> changeRatio down 0.12012089769 at 198.79375 : 209 -2.39989383204 -19.9789868224
    # BDT_DelM_Bkg_c  has a low first bin. Orig limits 7.0 200.0
    # Dont want to expand min range to -4953.60003746 too far
    #w.obj('BDT_DelM_Bkg_c').setMin(-137.75) ; w.obj('BDT_DelM_Bkg_c').setMax(199.5175) ; w.obj('BDT_DelM_Bkg_c').setVal(103.5) ; w.obj('BDT_DelM_Bkg_c').setError(63.3002826141)
    # ---->>>> changeRatio down 0.796474345182 at 140.35796875 : 253 -8.56707625138 -10.7562488399
    # ---->>>> changeRatio down 0.740363456953 at 140.3584375 : 254 -10.7562488399 -14.5283356963
    # ---->>>> changeRatio down 0.641610197934 at 140.35890625 : 255 -14.5283356963 -22.6435548299
    # ---->>>> changeRatio down 0.406663254322 at 140.359375 : 256 -22.6435548299 -55.6813397553
    # ---->>>> changeRatio down 0.182689811939 at 140.35984375 : 257 -55.6813397553 -304.786233915
    # ---->>>> changeRatio down 566.494784316 at 140.3603125 : 258 -304.786233915 -0.538021253422
    # ---->>>> changeRatio down 0.247223803619 at 140.36125 : 259 -0.538021253422 -2.17625182343
    # ---->>>> changeRatio down 0.237704587599 at 140.365 : 260 -2.17625182343 -9.15527901845
    # ---->>>> changeRatio down 1.84712086465 at 140.425 : 264 -11.9474589338 -6.46815222676
    # ---->>>> changeRatio down 1.78435736118 at 140.485 : 272 -12.0129713847 -6.73237976094
    # BDT_DelM_Bkg_m0  has a low first bin. Orig limits 137.5 140.5
    # Dont want to expand min range to 133.778707038 too far
    w.obj('BDT_DelM_Bkg_m0').setMin(135.25) ; w.obj('BDT_DelM_Bkg_m0').setMax(140.4925) ; w.obj('BDT_DelM_Bkg_m0').setVal(139.42) ; w.obj('BDT_DelM_Bkg_m0').setError(0.0233584431936)
    # EMu_BR  has a low first and last bin! Orig limits -1e-07 1e-07
    w.obj('EMu_BR').setMin(-1.85181371639e-07) ; w.obj('EMu_BR').setMax(1.85181374078e-07) ; w.obj('EMu_BR').setVal(0.0) ; w.obj('EMu_BR').setError(1.97646446099e-10)
    # PiPi_D0M_Bkg_Poly_a1  has a low first and last bin! Orig limits -1.0 1.0
    w.obj('PiPi_D0M_Bkg_Poly_a1').setMin(-1.1313170335) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setMax(1.28252920015) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setVal(-0.36) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setError(0.019002861715)
    # ---->>>> changeRatio down 0.494671217925 at 1813.9 : 136 -87.2210046817 -176.321163474
    w.obj('PiPi_D0M_MisId_Gaus_Mean').setMin(1775.95) ; w.obj('PiPi_D0M_MisId_Gaus_Mean').setMax(1813.9) ; w.obj('PiPi_D0M_MisId_Gaus_Mean').setVal(1798.5) ; w.obj('PiPi_D0M_MisId_Gaus_Mean').setError(0.280879010002)
    # ---->>>> changeRatio down 1.95895470153 at 0.9275 : 108 -241.185996383 -123.119741459
    # ---->>>> changeRatio down 1.97715019438 at 0.9975 : 124 -153.009435297 -77.3888780589
    # ---->>>> changeRatio down -0.00837217412633 at 0.9996875 : 125 -77.3888780589 9243.58200047
    w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMin(0.00875) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMax(0.9996875) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setVal(0.28) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setError(0.0109359284722)
    w.obj('PiPi_D0M_Sig_Gaus_Mean').setMin(1865.22) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setMax(1868.91) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setVal(1866.93) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setError(0.0297188489948)
    # PiPi_D0M_Sig_Gaus_Sigma1  has a low last bin. Orig limits 3.0 10.0
    # Attempted value 10.9672303382 hits limits 10
    w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMin(3.875) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMax(10) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setVal(6.36) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setError(0.100439812567)
    # PiPi_DelM_Bkg_a  has a low first bin. Orig limits -45.0 -5.0
    # Dont want to expand min range to -81.5589904694 too far
    w.obj('PiPi_DelM_Bkg_a').setMin(-75.0) ; w.obj('PiPi_DelM_Bkg_a').setMax(-5.4) ; w.obj('PiPi_DelM_Bkg_a').setVal(-21.0) ; w.obj('PiPi_DelM_Bkg_a').setError(0.679265382479)
    # PiPi_DelM_Bkg_b  has a low last bin. Orig limits -0.05 1.5
    w.obj('PiPi_DelM_Bkg_b').setMin(0.085625) ; w.obj('PiPi_DelM_Bkg_b').setMax(1.95995390956) ; w.obj('PiPi_DelM_Bkg_b').setVal(0.539) ; w.obj('PiPi_DelM_Bkg_b').setError(0.0436590139075)
    w.obj('PiPi_DelM_Bkg_c').setMin(13.98625) ; w.obj('PiPi_DelM_Bkg_c').setMax(245.14) ; w.obj('PiPi_DelM_Bkg_c').setVal(41.02) ; w.obj('PiPi_DelM_Bkg_c').setError(3.47326499764)
    # ---->>>> changeRatio down 0.301832916538 at 139.55996875 : 265 -222.133897789 -735.949876961
    # ---->>>> changeRatio down 790.679518213 at 139.5601875 : 266 -735.949876961 -0.930781511357
    # ---->>>> changeRatio down 0.497577576409 at 139.560625 : 267 -0.930781511357 -1.87062591943
    # ---->>>> changeRatio down 0.49119180388 at 139.5615 : 268 -1.87062591943 -3.80834106891
    # ---->>>> changeRatio down 1.96002117875 at 139.56325 : 269 -3.80834106891 -1.94301016245
    # ---->>>> changeRatio down 3.98403761505 at 139.564125 : 270 -1.94301016245 -0.487698749406
    # ---->>>> changeRatio down -0.327659645959 at 139.56434375 : 271 -0.487698749406 1.48843092343
    # ---->>>> changeRatio down -1.45170400709 at 139.5645625 : 272 1.48843092343 -1.02529917681
    # ---->>>> changeRatio down 0.0608737429954 at 139.565 : 273 -1.02529917681 -16.8430447407
    # ---->>>> changeRatio down 0.473607888615 at 139.586 : 276 -18.6379803561 -39.3531881629
    w.obj('PiPi_DelM_Bkg_m0').setMin(138.27) ; w.obj('PiPi_DelM_Bkg_m0').setMax(139.572) ; w.obj('PiPi_DelM_Bkg_m0').setVal(139.264) ; w.obj('PiPi_DelM_Bkg_m0').setError(0.007243484314)
    # PiPi_DelM_MisId_Gaus_Sigma1  has a low last bin. Orig limits 0.0 3.0
    w.obj('PiPi_DelM_MisId_Gaus_Sigma1').setMin(0.57) ; w.obj('PiPi_DelM_MisId_Gaus_Sigma1').setMax(3.38918287254) ; w.obj('PiPi_DelM_MisId_Gaus_Sigma1').setVal(1.26) ; w.obj('PiPi_DelM_MisId_Gaus_Sigma1').setError(0.0190305822536)
    # PiPi_DelM_Sig_Gaus1_Frac  has a low last bin. Orig limits 0.0 0.75
    w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMin(0.15) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMax(0.85879146712) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setVal(0.48) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setError(0.0203473773194)
    w.obj('PiPi_DelM_Sig_Gaus_Mean').setMin(145.285) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setMax(145.69) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setVal(145.45) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setError(0.00292876924391)
    w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMin(0.336) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMax(0.984) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setVal(0.504) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setError(0.00858734640507)
    # PiPi_DelM_Sig_Gaus_Sigma2  has a low last bin. Orig limits 0.65 1.2
    # Dont want to expand max range to 1.7125417475 too far
    w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMin(0.66925) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMax(1.6125) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setVal(0.969) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setError(0.0154084396619)
    w.obj('PiPi_N_Comb').setMin(53250.0) ; w.obj('PiPi_N_Comb').setMax(98900.0) ; w.obj('PiPi_N_Comb').setVal(70300.0) ; w.obj('PiPi_N_Comb').setError(386.120608487)
    w.obj('PiPi_N_MisId').setMin(2260.5) ; w.obj('PiPi_N_MisId').setMax(14702.0) ; w.obj('PiPi_N_MisId').setVal(7252.0) ; w.obj('PiPi_N_MisId').setError(127.677164888)
    # PiPi_N_MisId_Prompt  has a low first bin. Orig limits 10.0 10000.0
    # Dont want to expand min range to -35697.6658226 too far
    w.obj('PiPi_N_MisId_Prompt').setMin(-7482.5) ; w.obj('PiPi_N_MisId_Prompt').setMax(9800.2) ; w.obj('PiPi_N_MisId_Prompt').setVal(1208.8) ; w.obj('PiPi_N_MisId_Prompt').setError(157.260813023)
    w.obj('PiPi_N_Prompt').setMin(23800.0) ; w.obj('PiPi_N_Prompt').setMax(59200.0) ; w.obj('PiPi_N_Prompt').setVal(38400.0) ; w.obj('PiPi_N_Prompt').setError(339.050802418)
    w.obj('PiPi_N_Sig').setMin(66250.0) ; w.obj('PiPi_N_Sig').setMax(109000.0) ; w.obj('PiPi_N_Sig').setVal(83000.0) ; w.obj('PiPi_N_Sig').setError(362.413186073)


    # nll analyse, nlls up to 1810.0 on Thu Aug 22 10:29:36 2013 run on fitResult.toy.root
    #
    # BDT1_N_Comb  has a low first bin. Orig limits 2817.5 13836.6829458
    w.obj('BDT1_N_Comb').setMin(2301.48704846) ; w.obj('BDT1_N_Comb').setMax(13616.2992869) ; w.obj('BDT1_N_Comb').setVal(6343.63854266) ; w.obj('BDT1_N_Comb').setError(81.1294938311)
    # BDT2_N_Comb  has a low first bin. Orig limits 647.0 7848.0
    w.obj('BDT2_N_Comb').setMin(381.490801444) ; w.obj('BDT2_N_Comb').setMax(7703.98) ; w.obj('BDT2_N_Comb').setVal(2519.26) ; w.obj('BDT2_N_Comb').setError(53.668717755)
    # BDT3_N_Comb  has a low first bin. Orig limits 3.75 3920.0
    w.obj('BDT3_N_Comb').setMin(-182.700863187) ; w.obj('BDT3_N_Comb').setMax(3841.675) ; w.obj('BDT3_N_Comb').setVal(317.05) ; w.obj('BDT3_N_Comb').setError(19.4173975947)
    # BDT_D0M_Bkg_Exp_Const  has a low first bin. Orig limits -0.00948 0.00274
    w.obj('BDT_D0M_Bkg_Exp_Const').setMin(-0.0104105049975) ; w.obj('BDT_D0M_Bkg_Exp_Const').setMax(0.0024956) ; w.obj('BDT_D0M_Bkg_Exp_Const').setVal(-0.0036144) ; w.obj('BDT_D0M_Bkg_Exp_Const').setError(9.79874664085e-05)
    # ---->>>> changeRatio up 6.04865970979 at -17.523070625 : 82 658.396799425 108.850031414
    # ---->>>> changeRatio up 2.45095610137 at -17.5192297281 : 83 108.850031414 44.411252961
    # ---->>>> changeRatio up 1.49009437688 at -17.5153888312 : 84 44.411252961 29.8043222296
    # ---->>>> changeRatio up 1.28964534861 at -17.5115479344 : 85 29.8043222296 23.1104793746
    # ---->>>> changeRatio up 1.20130443854 at -17.5077070375 : 86 23.1104793746 19.2378206833
    #w.obj('BDT_DelM_Bkg_a').setMin(-17.5038661406) ; w.obj('BDT_DelM_Bkg_a').setMax(5.7988552005) ; w.obj('BDT_DelM_Bkg_a').setVal(-11.8999975999) ; w.obj('BDT_DelM_Bkg_a').setError(2.25421619355)
    # ---->>>> changeRatio up 9.47708669816 at -0.33340020752 : 7 822.883388374 86.8287285515
    # ---->>>> changeRatio up 1.72924025191 at -0.333033374023 : 8 86.8287285515 50.2120676727
    # ---->>>> changeRatio up 1.31292667959 at -0.332666540527 : 9 50.2120676727 38.2443806294
    # BDT_DelM_Bkg_b  has a low last bin. Orig limits -0.335234375 2.0125
    # Dont want to expand max range to 4.40984341438 too far
    #w.obj('BDT_DelM_Bkg_b').setMin(-0.332299707031) ; w.obj('BDT_DelM_Bkg_b').setMax(1.5) ; w.obj('BDT_DelM_Bkg_b').setVal(-0.1943703125) ; w.obj('BDT_DelM_Bkg_b').setError(1.49146639904)
    # ---->>>> changeRatio up -15.7166191974 at 0.00269453125002 : 53 -1746.66015438 111.13459787
    # ---->>>> changeRatio up 0.294857054886 at 0.108090625 : 54 111.13459787 376.910085848
    # ---->>>> changeRatio up 1.29554088539 at 0.529675 : 55 376.910085848 290.928746516
    # ---->>>> changeRatio up 1.29094640464 at 0.951259375 : 56 290.928746516 225.360824796
    # ---->>>> changeRatio up 1.29716527282 at 1.37284375 : 57 225.360824796 173.733316423
    # ---->>>> changeRatio up 1.30346938506 at 1.794428125 : 58 173.733316423 133.28530644
    # ---->>>> changeRatio up 0.740319733313 at 2.2160125 : 59 133.28530644 180.037489807
    # ---->>>> changeRatio up 1.70097229305 at 3.05918125 : 60 180.037489807 105.843869734
    # ---->>>> changeRatio down 8.64725833313 at 195.30165625 : 124 -683.936958327 -79.0929254082
    # ---->>>> changeRatio down 0.744322638105 at 196.144825 : 125 -79.0929254082 -106.261614734
    # ---->>>> changeRatio down 1.3537671607 at 196.98799375 : 126 -106.261614734 -78.4932725646
    # ---->>>> changeRatio down 1.33372996366 at 197.409578125 : 127 -78.4932725646 -58.8524474243
    # ---->>>> changeRatio down 0.535089503869 at 197.620370313 : 128 -58.8524474243 -109.986174273
    # ---->>>> changeRatio down 1.61652758711 at 197.8311625 : 129 -109.986174273 -68.038538377
    # ---->>>> changeRatio down 0.0794136634446 at 197.883860547 : 130 -68.038538377 -856.761109182
    # ---->>>> changeRatio down 95.5863346555 at 197.936558594 : 131 -856.761109182 -8.96321751713
    # ---->>>> changeRatio down 0.481548660671 at 198.041954688 : 132 -8.96321751713 -18.6133162631
    # ---->>>> changeRatio down 0.46105305385 at 198.252746875 : 133 -18.6133162631 -40.3713110837
    # ---->>>> changeRatio down 0.402286478902 at 198.67433125 : 134 -40.3713110837 -100.354630844
    # BDT_DelM_Bkg_c  has a low last bin. Orig limits -137.75 199.5175
    #w.obj('BDT_DelM_Bkg_c').setMin(0.) ; w.obj('BDT_DelM_Bkg_c').setMax(153.486837819) ; w.obj('BDT_DelM_Bkg_c').setVal(111.82795) ; w.obj('BDT_DelM_Bkg_c').setError(198.50528501)
    # ---->>>> changeRatio down 1.83506575411 at 140.45318125 : 247 -11.3933229439 -6.20867286006
    # BDT_DelM_Bkg_m0  has a low first bin. Orig limits 135.25 140.4925
    w.obj('BDT_DelM_Bkg_m0').setMin(134.930857977) ; w.obj('BDT_DelM_Bkg_m0').setMax(140.47939375) ; w.obj('BDT_DelM_Bkg_m0').setVal(139.444) ; w.obj('BDT_DelM_Bkg_m0').setError(0.0603380050646)
    w.obj('EMu_BR').setMin(-1.77774116725e-07) ; w.obj('EMu_BR').setMax(1.77774119164e-07) ; w.obj('EMu_BR').setVal(1.21949998923e-15) ; w.obj('EMu_BR').setError(2.99777876108e-09)
    # ---->>>> changeRatio up -580.98225317 at -0.999686981071 : 17 -1318.75783347 2.26987627638
    # ---->>>> changeRatio up 0.501034492139 at -0.999309817597 : 18 2.26987627638 4.53037926927
    # ---->>>> changeRatio up 0.12655774007 at -0.998555490649 : 19 4.53037926927 35.7969355865
    w.obj('PiPi_D0M_Bkg_Poly_a1').setMin(-0.95) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setMax(0.9) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setVal(-0.407163163405) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setError(0.0199885978052)
    # ---->>>> changeRatio down 0.493811613026 at 1812.7615 : 137 -57.7716767438 -116.991328717
    # PiPi_D0M_MisId_Gaus_Mean  has a low first bin. Orig limits 1775.95 1813.9
    w.obj('PiPi_D0M_MisId_Gaus_Mean').setMin(1772.87442469) ; w.obj('PiPi_D0M_MisId_Gaus_Mean').setMax(1813.141) ; w.obj('PiPi_D0M_MisId_Gaus_Mean').setVal(1798.72) ; w.obj('PiPi_D0M_MisId_Gaus_Mean').setError(0.312306521315)
    # ---->>>> changeRatio down 1.95489589615 at 0.880775 : 90 -236.117676103 -120.782736599
    # PiPi_D0M_Sig_Gaus1_Frac  has a low first bin. Orig limits 0.00875 0.9996875
    # Attempted value -0.0932481392983 hits limits 1e-05
    w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMin(1e-05) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMax(0.989778125) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setVal(0.32585) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setError(0.0128702673728)
    # PiPi_D0M_Sig_Gaus_Mean  has a low first bin. Orig limits 1865.22 1868.91
    w.obj('PiPi_D0M_Sig_Gaus_Mean').setMin(1865.00868984) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setMax(1868.8362) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setVal(1866.9174) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setError(0.0302391164113)
    # PiPi_D0M_Sig_Gaus_Sigma1  has a low first and last bin! Orig limits 3.875 10.0
    # Attempted value 11.5546630866 hits limits 10
    w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMin(3.52257699616) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMax(10) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setVal(6.325) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setError(0.116094434387)
    # PiPi_DelM_Bkg_a  has a low first bin. Orig limits -75.0 -5.4
    w.obj('PiPi_DelM_Bkg_a').setMin(-83.807523376) ; w.obj('PiPi_DelM_Bkg_a').setMax(-5.748) ; w.obj('PiPi_DelM_Bkg_a').setVal(-20.712) ; w.obj('PiPi_DelM_Bkg_a').setError(4.11827503956)
    # PiPi_DelM_Bkg_b  has a low first and last bin! Orig limits 0.085625 1.95995390956
    w.obj('PiPi_DelM_Bkg_b').setMin(0.0205360459013) ; w.obj('PiPi_DelM_Bkg_b').setMax(2.17828074726) ; w.obj('PiPi_DelM_Bkg_b').setVal(0.535463938294) ; w.obj('PiPi_DelM_Bkg_b').setError(1.14479929974)
    # PiPi_DelM_Bkg_c  has a low first bin. Orig limits 13.98625 245.14
    w.obj('PiPi_DelM_Bkg_c').setMin(7.57589078997) ; w.obj('PiPi_DelM_Bkg_c').setMax(240.516925) ; w.obj('PiPi_DelM_Bkg_c').setVal(41.7247) ; w.obj('PiPi_DelM_Bkg_c').setError(125.013315746)
    # ---->>>> changeRatio down 560.540552689 at 139.560200625 : 188 -492.213885273 -0.87810575508
    # ---->>>> changeRatio down 0.248147174376 at 139.5606075 : 189 -0.87810575508 -3.53864901862
    # ---->>>> changeRatio down 0.485980329867 at 139.562235 : 190 -3.53864901862 -7.28146552679
    # ---->>>> changeRatio down 0.481976174744 at 139.56549 : 191 -7.28146552679 -15.1075217165
    # PiPi_DelM_Bkg_m0  has a low first bin. Orig limits 138.27 139.572
    w.obj('PiPi_DelM_Bkg_m0').setMin(138.130405839) ; w.obj('PiPi_DelM_Bkg_m0').setMax(139.55979375) ; w.obj('PiPi_DelM_Bkg_m0').setVal(139.25952) ; w.obj('PiPi_DelM_Bkg_m0').setError(0.051123116657)
    # PiPi_DelM_MisId_Gaus_Sigma1  has a low first and last bin! Orig limits 0.57 3.38918287254
    w.obj('PiPi_DelM_MisId_Gaus_Sigma1').setMin(0.469556590248) ; w.obj('PiPi_DelM_MisId_Gaus_Sigma1').setMax(3.69545831663) ; w.obj('PiPi_DelM_MisId_Gaus_Sigma1').setVal(1.24660388941) ; w.obj('PiPi_DelM_MisId_Gaus_Sigma1').setError(0.0366305643512)
    # PiPi_DelM_Sig_Gaus1_Frac  has a low first bin. Orig limits 0.15 0.85879146712
    w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMin(0.0934461751464) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMax(0.851703552449) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setVal(0.490219904218) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setError(0.257434203586)
    # PiPi_DelM_Sig_Gaus_Mean  has a low first bin. Orig limits 145.285 145.69
    w.obj('PiPi_DelM_Sig_Gaus_Mean').setMin(145.259705856) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setMax(145.6819) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setVal(145.4551) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setError(0.00299945796419)
    # PiPi_DelM_Sig_Gaus_Sigma1  has a low first bin. Orig limits 0.336 0.984
    w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMin(0.308138929021) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMax(0.97104) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setVal(0.50448) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setError(0.103577751597)
    # PiPi_DelM_Sig_Gaus_Sigma2  has a low first bin. Orig limits 0.66925 1.6125
    w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMin(0.628602484886) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMax(1.593635) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setVal(0.97109) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setError(0.207173365444)
    # PiPi_N_Comb  has a low first bin. Orig limits 53250.0 98900.0
    w.obj('PiPi_N_Comb').setMin(50878.9577969) ; w.obj('PiPi_N_Comb').setMax(97987.0) ; w.obj('PiPi_N_Comb').setVal(69684.0) ; w.obj('PiPi_N_Comb').setError(421.851616813)
    # PiPi_N_MisId  has a low first and last bin! Orig limits 2260.5 14702.0
    w.obj('PiPi_N_MisId').setMin(1602.09803985) ; w.obj('PiPi_N_MisId').setMax(15181.4087371) ; w.obj('PiPi_N_MisId').setVal(7237.1) ; w.obj('PiPi_N_MisId').setError(202.313332431)
    # PiPi_N_MisId_Prompt  has a low last bin. Orig limits -7482.5 9800.2
    w.obj('PiPi_N_MisId_Prompt').setMin(-4198.787) ; w.obj('PiPi_N_MisId_Prompt').setMax(9608.85755932) ; w.obj('PiPi_N_MisId_Prompt').setVal(1158.85) ; w.obj('PiPi_N_MisId_Prompt').setError(191.003245364)
    # PiPi_N_Prompt  has a low first bin. Orig limits 23800.0 59200.0
    w.obj('PiPi_N_Prompt').setMin(21992.64478) ; w.obj('PiPi_N_Prompt').setMax(58492.0) ; w.obj('PiPi_N_Prompt').setVal(37960.0) ; w.obj('PiPi_N_Prompt').setError(1331.09040422)
    # PiPi_N_Sig  has a low first bin. Orig limits 66250.0 109000.0
    w.obj('PiPi_N_Sig').setMin(64168.9280222) ; w.obj('PiPi_N_Sig').setMax(108145.0) ; w.obj('PiPi_N_Sig').setVal(83350.0) ; w.obj('PiPi_N_Sig').setError(1409.2345)



    #w.obj('BDT_DelM_Bkg_a').setConstant(True)
    #w.obj('PiPi_DelM_Bkg_a').setConstant(True)
    #w.obj('BDT_DelM_Bkg_b').setConstant(True)
    #w.obj('PiPi_DelM_Bkg_b').setConstant(True)
    w.obj('BDT_DelM_Bkg_c').setConstant(True)
    #w.obj('PiPi_DelM_Bkg_c').setConstant(True)
    #w.obj('BDT_DelM_Bkg_m0').setConstant(True)
    #w.obj('PiPi_DelM_Bkg_m0').setConstant(True)

  if not config['mode'] is 'mc':
    w.obj('BDT1_Sig_Eff').setVal(0.293290734824) ; w.obj('BDT1_Sig_Eff').setConstant(True)
    w.obj('BDT2_Sig_Eff').setVal(0.447795527157) ; w.obj('BDT2_Sig_Eff').setConstant(True)

    w.obj('BDT1_D0M_Sig_CB1_Frac').setMin(0.0) ; w.obj('BDT1_D0M_Sig_CB1_Frac').setMax(1.0)
    w.obj('BDT1_D0M_Sig_CB1_Frac').setVal(0.799506719163) ; w.obj('BDT1_D0M_Sig_CB1_Frac').setError(0.0194458834226)
    w.obj('BDT1_D0M_Sig_CB1_Frac').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB1_Sigma').setMin(1.0) ; w.obj('BDT1_D0M_Sig_CB1_Sigma').setMax(30.0)
    w.obj('BDT1_D0M_Sig_CB1_Sigma').setVal(12.691279085) ; w.obj('BDT1_D0M_Sig_CB1_Sigma').setError(0.527065706139)
    w.obj('BDT1_D0M_Sig_CB1_Sigma').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB1_alphaleft').setMin(0.0) ; w.obj('BDT1_D0M_Sig_CB1_alphaleft').setMax(5.0)
    w.obj('BDT1_D0M_Sig_CB1_alphaleft').setVal(0.457381582333) ; w.obj('BDT1_D0M_Sig_CB1_alphaleft').setError(0.0266421384878)
    w.obj('BDT1_D0M_Sig_CB1_alphaleft').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB1_n').setMin(0.0) ; w.obj('BDT1_D0M_Sig_CB1_n').setMax(10.0)
    w.obj('BDT1_D0M_Sig_CB1_n').setVal(1.35195587241) ; w.obj('BDT1_D0M_Sig_CB1_n').setError(0.0727410769817)
    w.obj('BDT1_D0M_Sig_CB1_n').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB2_Sigma').setMin(1.0) ; w.obj('BDT1_D0M_Sig_CB2_Sigma').setMax(30.0)
    w.obj('BDT1_D0M_Sig_CB2_Sigma').setVal(29.9894090886) ; w.obj('BDT1_D0M_Sig_CB2_Sigma').setError(23.1626769702)
    w.obj('BDT1_D0M_Sig_CB2_Sigma').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB2_alpharight').setMin(-5.0) ; w.obj('BDT1_D0M_Sig_CB2_alpharight').setMax(0.0)
    w.obj('BDT1_D0M_Sig_CB2_alpharight').setVal(-1.62137253761) ; w.obj('BDT1_D0M_Sig_CB2_alpharight').setError(0.104680288901)
    w.obj('BDT1_D0M_Sig_CB2_alpharight').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB2_n').setMin(0.0) ; w.obj('BDT1_D0M_Sig_CB2_n').setMax(50.0)
    w.obj('BDT1_D0M_Sig_CB2_n').setVal(0.839249708859) ; w.obj('BDT1_D0M_Sig_CB2_n').setError(0.2368681163)
    w.obj('BDT1_D0M_Sig_CB2_n').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB_Mean').setMin(1750.0) ; w.obj('BDT1_D0M_Sig_CB_Mean').setMax(1900.0)
    w.obj('BDT1_D0M_Sig_CB_Mean').setVal(1854.90405535) ; w.obj('BDT1_D0M_Sig_CB_Mean').setError(0.543210933179)
    w.obj('BDT1_D0M_Sig_CB_Mean').setConstant(True)
    w.obj('BDT1_DelM_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('BDT1_DelM_Sig_Gaus1_Frac').setMax(1.0)
    w.obj('BDT1_DelM_Sig_Gaus1_Frac').setVal(0.336182607167) ; w.obj('BDT1_DelM_Sig_Gaus1_Frac').setError(0.0117452728642)
    w.obj('BDT1_DelM_Sig_Gaus1_Frac').setConstant(True)
    w.obj('BDT1_DelM_Sig_Gaus_Mean').setMin(143.0) ; w.obj('BDT1_DelM_Sig_Gaus_Mean').setMax(148.0)
    w.obj('BDT1_DelM_Sig_Gaus_Mean').setVal(145.455693183) ; w.obj('BDT1_DelM_Sig_Gaus_Mean').setError(0.0237795050292)
    w.obj('BDT1_DelM_Sig_Gaus_Mean').setConstant(True)
    w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setMin(0.0) ; w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setMax(5.0)
    w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setVal(4.99999767822) ; w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setError(0.0227647458547)
    w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setConstant(True)
    w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setMin(0.0) ; w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setMax(2.0)
    w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setVal(0.961734614921) ; w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setError(0.0223775032736)
    w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB1_Frac').setMin(0.0) ; w.obj('BDT2_D0M_Sig_CB1_Frac').setMax(1.0)
    w.obj('BDT2_D0M_Sig_CB1_Frac').setVal(0.874073306466) ; w.obj('BDT2_D0M_Sig_CB1_Frac').setError(0.0542478938062)
    w.obj('BDT2_D0M_Sig_CB1_Frac').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB1_Sigma').setMin(1.0) ; w.obj('BDT2_D0M_Sig_CB1_Sigma').setMax(30.0)
    w.obj('BDT2_D0M_Sig_CB1_Sigma').setVal(13.1212350967) ; w.obj('BDT2_D0M_Sig_CB1_Sigma').setError(0.402874966205)
    w.obj('BDT2_D0M_Sig_CB1_Sigma').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB1_alphaleft').setMin(0.0) ; w.obj('BDT2_D0M_Sig_CB1_alphaleft').setMax(5.0)
    w.obj('BDT2_D0M_Sig_CB1_alphaleft').setVal(0.429584956881) ; w.obj('BDT2_D0M_Sig_CB1_alphaleft').setError(0.0511793151994)
    w.obj('BDT2_D0M_Sig_CB1_alphaleft').setConstant(True) 
    w.obj('BDT2_D0M_Sig_CB1_n').setMin(0.0) ; w.obj('BDT2_D0M_Sig_CB1_n').setMax(10.0)
    w.obj('BDT2_D0M_Sig_CB1_n').setVal(2.32172444159) ; w.obj('BDT2_D0M_Sig_CB1_n').setError(0.109153577575)
    w.obj('BDT2_D0M_Sig_CB1_n').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB2_Sigma').setMin(1.0) ; w.obj('BDT2_D0M_Sig_CB2_Sigma').setMax(30.0)
    w.obj('BDT2_D0M_Sig_CB2_Sigma').setVal(29.8959821125) ; w.obj('BDT2_D0M_Sig_CB2_Sigma').setError(28.2218670113)
    w.obj('BDT2_D0M_Sig_CB2_Sigma').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB2_alpharight').setMin(-5.0) ; w.obj('BDT2_D0M_Sig_CB2_alpharight').setMax(0.0)
    w.obj('BDT2_D0M_Sig_CB2_alpharight').setVal(-0.814512823893) ; w.obj('BDT2_D0M_Sig_CB2_alpharight').setError(0.60876472424)
    w.obj('BDT2_D0M_Sig_CB2_alpharight').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB2_n').setMin(0.0) ; w.obj('BDT2_D0M_Sig_CB2_n').setMax(50.0)
    w.obj('BDT2_D0M_Sig_CB2_n').setVal(30.4976244969) ; w.obj('BDT2_D0M_Sig_CB2_n').setError(28.2337695867)
    w.obj('BDT2_D0M_Sig_CB2_n').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB_Mean').setMin(1750.0) ; w.obj('BDT2_D0M_Sig_CB_Mean').setMax(1900.0)
    w.obj('BDT2_D0M_Sig_CB_Mean').setVal(1854.90382953) ; w.obj('BDT2_D0M_Sig_CB_Mean').setError(1.00371424338)
    w.obj('BDT2_D0M_Sig_CB_Mean').setConstant(True)
    w.obj('BDT2_DelM_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('BDT2_DelM_Sig_Gaus1_Frac').setMax(1.0)
    w.obj('BDT2_DelM_Sig_Gaus1_Frac').setVal(0.32989000109) ; w.obj('BDT2_DelM_Sig_Gaus1_Frac').setError(0.00919706633475)
    w.obj('BDT2_DelM_Sig_Gaus1_Frac').setConstant(True)   
    w.obj('BDT2_DelM_Sig_Gaus_Mean').setMin(143.0) ; w.obj('BDT2_DelM_Sig_Gaus_Mean').setMax(148.0)
    w.obj('BDT2_DelM_Sig_Gaus_Mean').setVal(145.494071156) ; w.obj('BDT2_DelM_Sig_Gaus_Mean').setError(0.0170347451782)
    w.obj('BDT2_DelM_Sig_Gaus_Mean').setConstant(True)
    w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setMin(0.0) ; w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setMax(5.0)
    w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setVal(4.99989917771) ; w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setError(0.0477129507854)
    w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setConstant(True)  
    w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setMin(0.0) ; w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setMax(2.0)
    w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setVal(0.853071473289) ; w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setError(0.017080153336)
    w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setConstant(True)  
    w.obj('BDT3_D0M_Sig_CB1_Frac').setMin(0.0) ; w.obj('BDT3_D0M_Sig_CB1_Frac').setMax(1.0)
    w.obj('BDT3_D0M_Sig_CB1_Frac').setVal(0.853316740667) ; w.obj('BDT3_D0M_Sig_CB1_Frac').setError(0.0123656325394)
    w.obj('BDT3_D0M_Sig_CB1_Frac').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB1_Sigma').setMin(1.0) ; w.obj('BDT3_D0M_Sig_CB1_Sigma').setMax(30.0)
    w.obj('BDT3_D0M_Sig_CB1_Sigma').setVal(8.5881382274) ; w.obj('BDT3_D0M_Sig_CB1_Sigma').setError(0.291548864992)
    w.obj('BDT3_D0M_Sig_CB1_Sigma').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB1_alphaleft').setMin(0.0) ; w.obj('BDT3_D0M_Sig_CB1_alphaleft').setMax(5.0)
    w.obj('BDT3_D0M_Sig_CB1_alphaleft').setVal(0.259316450678) ; w.obj('BDT3_D0M_Sig_CB1_alphaleft').setError(0.0105207933141)
    w.obj('BDT3_D0M_Sig_CB1_alphaleft').setConstant(True) 
    w.obj('BDT3_D0M_Sig_CB1_n').setMin(0.0) ; w.obj('BDT3_D0M_Sig_CB1_n').setMax(10.0)
    w.obj('BDT3_D0M_Sig_CB1_n').setVal(2.805235426) ; w.obj('BDT3_D0M_Sig_CB1_n').setError(0.185995952039)
    w.obj('BDT3_D0M_Sig_CB1_n').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB2_Sigma').setMin(1.0) ; w.obj('BDT3_D0M_Sig_CB2_Sigma').setMax(30.0)
    w.obj('BDT3_D0M_Sig_CB2_Sigma').setVal(29.9999864387) ; w.obj('BDT3_D0M_Sig_CB2_Sigma').setError(2.03665347623)
    w.obj('BDT3_D0M_Sig_CB2_Sigma').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB2_alpharight').setMin(-5.0) ; w.obj('BDT3_D0M_Sig_CB2_alpharight').setMax(0.0)
    w.obj('BDT3_D0M_Sig_CB2_alpharight').setVal(-2.09888488418) ; w.obj('BDT3_D0M_Sig_CB2_alpharight').setError(0.0760528130361)
    w.obj('BDT3_D0M_Sig_CB2_alpharight').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB2_n').setMin(0.0) ; w.obj('BDT3_D0M_Sig_CB2_n').setMax(50.0)
    w.obj('BDT3_D0M_Sig_CB2_n').setVal(8.96023039654e-06) ; w.obj('BDT3_D0M_Sig_CB2_n').setError(0.0755392265426)
    w.obj('BDT3_D0M_Sig_CB2_n').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB_Mean').setMin(1750.0) ; w.obj('BDT3_D0M_Sig_CB_Mean').setMax(1900.0)
    w.obj('BDT3_D0M_Sig_CB_Mean').setVal(1859.34302847) ; w.obj('BDT3_D0M_Sig_CB_Mean').setError(0.417957873763)
    w.obj('BDT3_D0M_Sig_CB_Mean').setConstant(True)
    w.obj('BDT3_DelM_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('BDT3_DelM_Sig_Gaus1_Frac').setMax(1.0)
    w.obj('BDT3_DelM_Sig_Gaus1_Frac').setVal(0.405375129465) ; w.obj('BDT3_DelM_Sig_Gaus1_Frac').setError(0.0129454222894)
    w.obj('BDT3_DelM_Sig_Gaus1_Frac').setConstant(True)   
    w.obj('BDT3_DelM_Sig_Gaus_Mean').setMin(143.0) ; w.obj('BDT3_DelM_Sig_Gaus_Mean').setMax(148.0)
    w.obj('BDT3_DelM_Sig_Gaus_Mean').setVal(145.489875586) ; w.obj('BDT3_DelM_Sig_Gaus_Mean').setError(0.0228097445406)
    w.obj('BDT3_DelM_Sig_Gaus_Mean').setConstant(True)
    w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setMin(0.0) ; w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setMax(5.0)
    w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setVal(4.99441102888) ; w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setError(0.147485950309)
    w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setConstant(True)  
    w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setMin(0.0) ; w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setMax(2.0)
    w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setVal(0.789367067669) ; w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setError(0.0244749745567)
    w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setConstant(True) 

  return w



