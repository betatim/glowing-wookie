

def mode_later_than(mode,current):
  modes = ["mc","datapretoy","toy","data"]
  #try:
  mode_index = modes.index(mode)
  current_index = modes.index(current)
  return mode_index <= current_index
  #except ValueError:
    #return -1


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
  gROOT.ProcessLine(".L RooChebychevTrunk.cxx+")
  from ROOT import RooGaussianTrunk, RooChebychevTrunk

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
  w.defineSet("argsPreCutKPi","D0_M,Del_M,RAND")

  # --- PiPi ---
  if config['norm'] is "kpi":
    w.factory("{D0_M,PiPi_D0M_Min[1800],PiPi_D0M_Max[1920]}")
  else:
    w.factory("{D0_M,PiPi_D0M_Min[1826],PiPi_D0M_Max[1920]}")
  
  w.factory("RooGenericPdf::PiPi_D0M_Range('(D0_M>PiPi_D0M_Min&&D0_M<PiPi_D0M_Max)',{D0_M,PiPi_D0M_Min,PiPi_D0M_Max})")

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
  #w.factory("RooChebychev::PiPi_D0M_Bkg_Poly(D0_M,{PiPi_D0M_Bkg_Poly_a1[-0.25,-1.5,1]})")
  #w.factory("PROD::PiPi_D0M_Bkg(PiPi_D0M_Bkg_Poly,PiPi_D0M_Range)")
  w.factory("RooChebychevTrunk::PiPi_D0M_Bkg(D0_M,{PiPi_D0M_Bkg_Poly_a1[-0.25,-1.5,1]},PiPi_D0M_Min,PiPi_D0M_Max)")
  
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
  
  w.factory("{PiPi_N_MisId[1300,100,3000],PiPi_N_MisId_Prompt[500,10,1000]}")
  #w.factory("SUM::PiPi_Final_PDF(PiPi_N_Sig[65000,20000,110000]*PiPi_Sig,PiPi_N_Prompt[35000,20000,60000]*PiPi_Prompt,PiPi_N_Comb[67000,1000,90000]*PiPi_Comb,PiPi_N_MisId[1300,100,3000]*PiPi_MisId,PiPi_N_MisId_Prompt[500,10,1000]*PiPi_MisId_Prompt)")
  #w.factory("SUM::PiPi_Final_PDF(PiPi_N_Sig[65000,20000,110000]*PiPi_Sig,PiPi_N_Prompt[35000,20000,60000]*PiPi_Prompt,PiPi_N_Comb[67000,1000,90000]*PiPi_Comb,PiPi_N_MisId[1300,100,3000]*PiPi_MisId)")
  #w.factory("SUM::PiPi_Final_PDF(PiPi_N_Sig[65000,20000,110000]*PiPi_Sig,PiPi_N_Prompt[35000,20000,60000]*PiPi_Prompt,PiPi_N_Comb[67000,1000,90000]*PiPi_Comb,PiPi_N_MisId_Prompt[500,10,1000]*PiPi_MisId_Prompt)")
  w.factory("SUM::PiPi_Final_PDF(PiPi_N_Sig[65000,20000,110000]*PiPi_Sig,PiPi_N_Prompt[35000,20000,60000]*PiPi_Prompt,PiPi_N_Comb[67000,1000,90000]*PiPi_Comb)")
  

  # --- eMu ---
  
  #w.factory("EMu_N_Sig[1000,0,100000]")
  for n in (1,2,3):
    w.factory("BDT%(n)i_Sig_Eff[0.3,0,1]"%({"n":n}))
    
  w.factory("EMu_Eff[%f]"%(config['emuEff']))
  w.factory("EMu_BR[1e-8,-1e-7,1e-7]")
  
  if config['norm'] is 'pipi':
    w.factory("PiPi_Eff[%f]"%(config['pipiEff']))
    w.factory("PiPi_BR[%f]"%(config['pipiBR'][0]))
    w.obj("PiPi_BR").setError(config['pipiBR'][1])
  elif config['norm'] is 'kpi':
    w.factory("PiPi_Eff[%f]"%(config['kpiEff']))
    w.factory("PiPi_BR[%f]"%(config['kpiBR'][0]))
    w.obj("PiPi_BR").setError(config['kpiBR'][1])
  
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
    #w.obj("Final_PDF").Print("v")
    #w.obj("BDT1_Sig").Print("v")
    
  elif config['mode'] is 'datapretoy':
    w.factory("SIMUL::Final_PDF(DataSet,BDT1=BDT1_Comb_Blind,BDT2=BDT2_Comb_Blind,BDT3=BDT3_Comb_Blind)")
    
  elif config['mode'] is 'toy':
    w.factory("SIMUL::Final_PDF(DataSet,PiPi=PiPi_Final_PDF,BDT1=BDT1_Final_PDF,BDT2=BDT2_Final_PDF,BDT3=BDT3_Final_PDF)")
    w.factory("SIMUL::Final_PDF_Background(DataSet,PiPi=PiPi_Final_PDF,BDT1=BDT1_Comb,BDT2=BDT2_Comb,BDT3=BDT3_Comb)")
    
  elif config['mode'] is 'data':
    w.factory("SIMUL::Final_PDF(DataSet,PiPi=PiPi_Final_PDF,BDT1=BDT1_Final_PDF,BDT2=BDT2_Final_PDF,BDT3=BDT3_Final_PDF)")
    w.factory("SIMUL::Final_PDF_Background(DataSet,PiPi=PiPi_Final_PDF,BDT1=BDT1_Comb,BDT2=BDT2_Comb,BDT3=BDT3_Comb)")
    
    
    
    
    
    
    
    
  #w.obj('BDT1_Sig_Eff').setVal(0.293290734824) 
  #w.obj('BDT2_Sig_Eff').setVal(0.447795527157) 
  w.obj('BDT1_Sig_Eff').setVal(3.25972590627763015e-01)
  w.obj('BDT2_Sig_Eff').setVal(2.98938992042440344e-01) 
  
  w.obj('BDT1_D0M_Sig_CB1_Frac').setMin(0.0) ; w.obj('BDT1_D0M_Sig_CB1_Frac').setMax(1.0)
  w.obj('BDT1_D0M_Sig_CB1_Frac').setVal(0.826107505035) ; w.obj('BDT1_D0M_Sig_CB1_Frac').setError(0.0320321995)
  w.obj('BDT1_D0M_Sig_CB1_Frac').setConstant(False)
  w.obj('BDT1_D0M_Sig_CB1_Sigma').setMin(1.0) ; w.obj('BDT1_D0M_Sig_CB1_Sigma').setMax(30.0)
  w.obj('BDT1_D0M_Sig_CB1_Sigma').setVal(11.026891251) ; w.obj('BDT1_D0M_Sig_CB1_Sigma').setError(0.469395261788)
  w.obj('BDT1_D0M_Sig_CB1_Sigma').setConstant(False)
  w.obj('BDT1_D0M_Sig_CB1_alphaleft').setMin(0.0) ; w.obj('BDT1_D0M_Sig_CB1_alphaleft').setMax(5.0)
  w.obj('BDT1_D0M_Sig_CB1_alphaleft').setVal(0.38315360875) ; w.obj('BDT1_D0M_Sig_CB1_alphaleft').setError(0.0819209036461)
  w.obj('BDT1_D0M_Sig_CB1_alphaleft').setConstant(False)
  w.obj('BDT1_D0M_Sig_CB1_n').setMin(0.0) ; w.obj('BDT1_D0M_Sig_CB1_n').setMax(10.0)
  w.obj('BDT1_D0M_Sig_CB1_n').setVal(1.14813599762) ; w.obj('BDT1_D0M_Sig_CB1_n').setError(0.133307868039)
  w.obj('BDT1_D0M_Sig_CB1_n').setConstant(False)
  w.obj('BDT1_D0M_Sig_CB2_Sigma').setMin(1.0) ; w.obj('BDT1_D0M_Sig_CB2_Sigma').setMax(30.0)
  w.obj('BDT1_D0M_Sig_CB2_Sigma').setVal(15.4885841357) ; w.obj('BDT1_D0M_Sig_CB2_Sigma').setError(2.60238550866)
  w.obj('BDT1_D0M_Sig_CB2_Sigma').setConstant(False)
  w.obj('BDT1_D0M_Sig_CB2_alpharight').setMin(-5.0) ; w.obj('BDT1_D0M_Sig_CB2_alpharight').setMax(0.0)
  w.obj('BDT1_D0M_Sig_CB2_alpharight').setVal(-0.853616116829) ; w.obj('BDT1_D0M_Sig_CB2_alpharight').setError(0.164739132293)
  w.obj('BDT1_D0M_Sig_CB2_alpharight').setConstant(False)
  w.obj('BDT1_D0M_Sig_CB2_n').setMin(0.0) ; w.obj('BDT1_D0M_Sig_CB2_n').setMax(50.0)
  w.obj('BDT1_D0M_Sig_CB2_n').setVal(2.13464143763) ; w.obj('BDT1_D0M_Sig_CB2_n').setError(0.547329251539)
  w.obj('BDT1_D0M_Sig_CB2_n').setConstant(False)
  w.obj('BDT1_D0M_Sig_CB_Mean').setMin(1750.0) ; w.obj('BDT1_D0M_Sig_CB_Mean').setMax(1900.0)
  w.obj('BDT1_D0M_Sig_CB_Mean').setVal(1858.61558514) ; w.obj('BDT1_D0M_Sig_CB_Mean').setError(0.397023541258)
  w.obj('BDT1_D0M_Sig_CB_Mean').setConstant(False)
  w.obj('BDT1_DelM_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('BDT1_DelM_Sig_Gaus1_Frac').setMax(1.0)
  w.obj('BDT1_DelM_Sig_Gaus1_Frac').setVal(0.279598911971) ; w.obj('BDT1_DelM_Sig_Gaus1_Frac').setError(0.00890826645733)
  w.obj('BDT1_DelM_Sig_Gaus1_Frac').setConstant(False)
  w.obj('BDT1_DelM_Sig_Gaus_Mean').setMin(143.0) ; w.obj('BDT1_DelM_Sig_Gaus_Mean').setMax(148.0)
  w.obj('BDT1_DelM_Sig_Gaus_Mean').setVal(145.511905015) ; w.obj('BDT1_DelM_Sig_Gaus_Mean').setError(0.0114445981069)
  w.obj('BDT1_DelM_Sig_Gaus_Mean').setConstant(False)
  w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setMin(0.0) ; w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setMax(5.0)
  w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setVal(4.56293941693) ; w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setError(0.139716170727)
  w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setConstant(False)
  w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setMin(0.0) ; w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setMax(2.0)
  w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setVal(0.978582085338) ; w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setError(0.0150928454293)
  w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setConstant(False)
  w.obj('BDT2_D0M_Sig_CB1_Frac').setMin(0.0) ; w.obj('BDT2_D0M_Sig_CB1_Frac').setMax(1.0)
  w.obj('BDT2_D0M_Sig_CB1_Frac').setVal(0.754646749497) ; w.obj('BDT2_D0M_Sig_CB1_Frac').setError(0.031677470055)
  w.obj('BDT2_D0M_Sig_CB1_Frac').setConstant(False)
  w.obj('BDT2_D0M_Sig_CB1_Sigma').setMin(1.0) ; w.obj('BDT2_D0M_Sig_CB1_Sigma').setMax(30.0)
  w.obj('BDT2_D0M_Sig_CB1_Sigma').setVal(10.0530756102) ; w.obj('BDT2_D0M_Sig_CB1_Sigma').setError(0.509066894489)
  w.obj('BDT2_D0M_Sig_CB1_Sigma').setConstant(False)
  w.obj('BDT2_D0M_Sig_CB1_alphaleft').setMin(0.0) ; w.obj('BDT2_D0M_Sig_CB1_alphaleft').setMax(5.0)
  w.obj('BDT2_D0M_Sig_CB1_alphaleft').setVal(0.256088932092) ; w.obj('BDT2_D0M_Sig_CB1_alphaleft').setError(0.0374233960069)
  w.obj('BDT2_D0M_Sig_CB1_alphaleft').setConstant(False)
  w.obj('BDT2_D0M_Sig_CB1_n').setMin(0.0) ; w.obj('BDT2_D0M_Sig_CB1_n').setMax(10.0)
  w.obj('BDT2_D0M_Sig_CB1_n').setVal(2.97982199983) ; w.obj('BDT2_D0M_Sig_CB1_n').setError(0.491573348705)
  w.obj('BDT2_D0M_Sig_CB1_n').setConstant(False)
  w.obj('BDT2_D0M_Sig_CB2_Sigma').setMin(1.0) ; w.obj('BDT2_D0M_Sig_CB2_Sigma').setMax(30.0)
  w.obj('BDT2_D0M_Sig_CB2_Sigma').setVal(14.5157726645) ; w.obj('BDT2_D0M_Sig_CB2_Sigma').setError(0.862548774901)
  w.obj('BDT2_D0M_Sig_CB2_Sigma').setConstant(False)
  w.obj('BDT2_D0M_Sig_CB2_alpharight').setMin(-5.0) ; w.obj('BDT2_D0M_Sig_CB2_alpharight').setMax(0.0)
  w.obj('BDT2_D0M_Sig_CB2_alpharight').setVal(-0.95492570696) ; w.obj('BDT2_D0M_Sig_CB2_alpharight').setError(0.113969192601)
  w.obj('BDT2_D0M_Sig_CB2_alpharight').setConstant(False)
  w.obj('BDT2_D0M_Sig_CB2_n').setMin(0.0) ; w.obj('BDT2_D0M_Sig_CB2_n').setMax(50.0)
  w.obj('BDT2_D0M_Sig_CB2_n').setVal(2.75231370242) ; w.obj('BDT2_D0M_Sig_CB2_n').setError(0.48096297155)
  w.obj('BDT2_D0M_Sig_CB2_n').setConstant(False)
  w.obj('BDT2_D0M_Sig_CB_Mean').setMin(1750.0) ; w.obj('BDT2_D0M_Sig_CB_Mean').setMax(1900.0)
  w.obj('BDT2_D0M_Sig_CB_Mean').setVal(1859.35111228) ; w.obj('BDT2_D0M_Sig_CB_Mean').setError(0.385193613672)
  w.obj('BDT2_D0M_Sig_CB_Mean').setConstant(False)
  w.obj('BDT2_DelM_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('BDT2_DelM_Sig_Gaus1_Frac').setMax(1.0)
  w.obj('BDT2_DelM_Sig_Gaus1_Frac').setVal(0.224209172954) ; w.obj('BDT2_DelM_Sig_Gaus1_Frac').setError(0.00573054952121)
  w.obj('BDT2_DelM_Sig_Gaus1_Frac').setConstant(False)
  w.obj('BDT2_DelM_Sig_Gaus_Mean').setMin(143.0) ; w.obj('BDT2_DelM_Sig_Gaus_Mean').setMax(148.0)
  w.obj('BDT2_DelM_Sig_Gaus_Mean').setVal(145.499075614) ; w.obj('BDT2_DelM_Sig_Gaus_Mean').setError(0.0102353104876)
  w.obj('BDT2_DelM_Sig_Gaus_Mean').setConstant(False)
  w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setMin(0.0) ; w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setMax(5.0)
  w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setVal(4.99999731362) ; w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setError(0.064598228515)
  w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setConstant(False)
  w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setMin(0.0) ; w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setMax(2.0)
  w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setVal(0.90041591761) ; w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setError(0.0104294972657)
  w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setConstant(False)
  w.obj('BDT3_D0M_Sig_CB1_Frac').setMin(0.0) ; w.obj('BDT3_D0M_Sig_CB1_Frac').setMax(1.0)
  w.obj('BDT3_D0M_Sig_CB1_Frac').setVal(0.771374767547) ; w.obj('BDT3_D0M_Sig_CB1_Frac').setError(0.0287223757908)
  w.obj('BDT3_D0M_Sig_CB1_Frac').setConstant(False)
  w.obj('BDT3_D0M_Sig_CB1_Sigma').setMin(1.0) ; w.obj('BDT3_D0M_Sig_CB1_Sigma').setMax(30.0)
  w.obj('BDT3_D0M_Sig_CB1_Sigma').setVal(9.64199608622) ; w.obj('BDT3_D0M_Sig_CB1_Sigma').setError(0.59035364812)
  w.obj('BDT3_D0M_Sig_CB1_Sigma').setConstant(False)
  w.obj('BDT3_D0M_Sig_CB1_alphaleft').setMin(0.0) ; w.obj('BDT3_D0M_Sig_CB1_alphaleft').setMax(5.0)
  w.obj('BDT3_D0M_Sig_CB1_alphaleft').setVal(0.26906734931) ; w.obj('BDT3_D0M_Sig_CB1_alphaleft').setError(0.0329635191667)
  w.obj('BDT3_D0M_Sig_CB1_alphaleft').setConstant(False)
  w.obj('BDT3_D0M_Sig_CB1_n').setMin(0.0) ; w.obj('BDT3_D0M_Sig_CB1_n').setMax(10.0)
  w.obj('BDT3_D0M_Sig_CB1_n').setVal(4.30999546201) ; w.obj('BDT3_D0M_Sig_CB1_n').setError(0.609882652677)
  w.obj('BDT3_D0M_Sig_CB1_n').setConstant(False)
  w.obj('BDT3_D0M_Sig_CB2_Sigma').setMin(1.0) ; w.obj('BDT3_D0M_Sig_CB2_Sigma').setMax(30.0)
  w.obj('BDT3_D0M_Sig_CB2_Sigma').setVal(15.2311724993) ; w.obj('BDT3_D0M_Sig_CB2_Sigma').setError(0.86222470509)
  w.obj('BDT3_D0M_Sig_CB2_Sigma').setConstant(False)
  w.obj('BDT3_D0M_Sig_CB2_alpharight').setMin(-5.0) ; w.obj('BDT3_D0M_Sig_CB2_alpharight').setMax(0.0)
  w.obj('BDT3_D0M_Sig_CB2_alpharight').setVal(-1.09697599255) ; w.obj('BDT3_D0M_Sig_CB2_alpharight').setError(0.1187713618)
  w.obj('BDT3_D0M_Sig_CB2_alpharight').setConstant(False)   
  w.obj('BDT3_D0M_Sig_CB2_n').setMin(0.0) ; w.obj('BDT3_D0M_Sig_CB2_n').setMax(50.0)
  w.obj('BDT3_D0M_Sig_CB2_n').setVal(2.6305214735) ; w.obj('BDT3_D0M_Sig_CB2_n').setError(0.412694779511)
  w.obj('BDT3_D0M_Sig_CB2_n').setConstant(False)
  w.obj('BDT3_D0M_Sig_CB_Mean').setMin(1750.0) ; w.obj('BDT3_D0M_Sig_CB_Mean').setMax(1900.0)
  w.obj('BDT3_D0M_Sig_CB_Mean').setVal(1860.57732813) ; w.obj('BDT3_D0M_Sig_CB_Mean').setError(0.44403455761)
  w.obj('BDT3_D0M_Sig_CB_Mean').setConstant(False)
  w.obj('BDT3_DelM_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('BDT3_DelM_Sig_Gaus1_Frac').setMax(1.0)
  w.obj('BDT3_DelM_Sig_Gaus1_Frac').setVal(0.216478140014) ; w.obj('BDT3_DelM_Sig_Gaus1_Frac').setError(0.00621011900269)
  w.obj('BDT3_DelM_Sig_Gaus1_Frac').setConstant(False)
  w.obj('BDT3_DelM_Sig_Gaus_Mean').setMin(143.0) ; w.obj('BDT3_DelM_Sig_Gaus_Mean').setMax(148.0)
  w.obj('BDT3_DelM_Sig_Gaus_Mean').setVal(145.481932604) ; w.obj('BDT3_DelM_Sig_Gaus_Mean').setError(0.00811056883369)
  w.obj('BDT3_DelM_Sig_Gaus_Mean').setConstant(False)
  w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setMin(0.0) ; w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setMax(5.0)
  w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setVal(4.35825382829) ; w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setError(0.121425112471)
  w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setConstant(False)
  w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setMin(0.0) ; w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setMax(2.0)
  w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setVal(0.812246683308) ; w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setError(0.00927287392949)
  w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setConstant(False)

  
  if mode_later_than('datapretoy',config['mode']):
    w.obj('BDT1_Sig_Eff').setConstant(True)
    w.obj('BDT2_Sig_Eff').setConstant(True)
    
    w.obj('BDT1_D0M_Sig_CB1_Frac').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB1_Sigma').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB1_alphaleft').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB1_n').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB2_Sigma').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB2_alpharight').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB2_n').setConstant(True)
    w.obj('BDT1_D0M_Sig_CB_Mean').setConstant(True)
    w.obj('BDT1_DelM_Sig_Gaus1_Frac').setConstant(True)
    w.obj('BDT1_DelM_Sig_Gaus_Mean').setConstant(True)
    w.obj('BDT1_DelM_Sig_Gaus_Sigma1').setConstant(True)
    w.obj('BDT1_DelM_Sig_Gaus_Sigma2').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB1_Frac').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB1_Sigma').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB1_alphaleft').setConstant(True) 
    w.obj('BDT2_D0M_Sig_CB1_n').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB2_Sigma').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB2_alpharight').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB2_n').setConstant(True)
    w.obj('BDT2_D0M_Sig_CB_Mean').setConstant(True)
    w.obj('BDT2_DelM_Sig_Gaus1_Frac').setConstant(True)   
    w.obj('BDT2_DelM_Sig_Gaus_Mean').setConstant(True)
    w.obj('BDT2_DelM_Sig_Gaus_Sigma1').setConstant(True)  
    w.obj('BDT2_DelM_Sig_Gaus_Sigma2').setConstant(True)  
    w.obj('BDT3_D0M_Sig_CB1_Frac').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB1_Sigma').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB1_alphaleft').setConstant(True) 
    w.obj('BDT3_D0M_Sig_CB1_n').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB2_Sigma').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB2_alpharight').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB2_n').setConstant(True)
    w.obj('BDT3_D0M_Sig_CB_Mean').setConstant(True)
    w.obj('BDT3_DelM_Sig_Gaus1_Frac').setConstant(True)   
    w.obj('BDT3_DelM_Sig_Gaus_Mean').setConstant(True)
    w.obj('BDT3_DelM_Sig_Gaus_Sigma1').setConstant(True)  
    w.obj('BDT3_DelM_Sig_Gaus_Sigma2').setConstant(True) 
    
    
    #w.obj('BDT_D0M_Bkg_Exp_Const').setMin(-0.01) ; w.obj('BDT_D0M_Bkg_Exp_Const').setMax(0.003)
    #w.obj('BDT_D0M_Bkg_Exp_Const').setVal(-0.00434519445106) ; w.obj('BDT_D0M_Bkg_Exp_Const').setError(8.98135228359e-05)
    #w.obj('BDT_D0M_Bkg_Exp_Const').setConstant(False)
    #w.obj('BDT_DelM_Bkg_a').setMin(-19.0) ; w.obj('BDT_DelM_Bkg_a').setMax(-1.0)
    #w.obj('BDT_DelM_Bkg_a').setVal(-4.22117355455) ; w.obj('BDT_DelM_Bkg_a').setError(0.12941180654)
    #w.obj('BDT_DelM_Bkg_a').setConstant(False)
    #w.obj('BDT_DelM_Bkg_b').setMin(-0.55) ; w.obj('BDT_DelM_Bkg_b').setMax(1.0)
    #w.obj('BDT_DelM_Bkg_b').setVal(-0.349999453262) ; w.obj('BDT_DelM_Bkg_b').setError(0.00117611743417)
    #w.obj('BDT_DelM_Bkg_b').setConstant(False)
    #w.obj('BDT_DelM_Bkg_c').setMin(7.0) ; w.obj('BDT_DelM_Bkg_c').setMax(200.0)
    #w.obj('BDT_DelM_Bkg_c').setVal(199.999632865) ; w.obj('BDT_DelM_Bkg_c').setError(1.39588442902)
    #w.obj('BDT_DelM_Bkg_c').setConstant(False)
    #w.obj('BDT_DelM_Bkg_m0').setMin(137.5) ; w.obj('BDT_DelM_Bkg_m0').setMax(140.5)
    #w.obj('BDT_DelM_Bkg_m0').setVal(139.3) ; w.obj('BDT_DelM_Bkg_m0').setError(0.0561243850283)
    #w.obj('BDT_DelM_Bkg_m0').setConstant(False)
    
    w.obj('BDT_D0M_Bkg_Exp_Const').setMin(-0.01) ; w.obj('BDT_D0M_Bkg_Exp_Const').setMax(0.003)
    w.obj('BDT_D0M_Bkg_Exp_Const').setVal(-0.00434506521329) ; w.obj('BDT_D0M_Bkg_Exp_Const').setError(7.75763629291e-05)
    w.obj('BDT_D0M_Bkg_Exp_Const').setConstant(False)
    w.obj('BDT_DelM_Bkg_a').setMin(-19.0) ; w.obj('BDT_DelM_Bkg_a').setMax(-1.0)
    w.obj('BDT_DelM_Bkg_a').setVal(-4.61590546253) ; w.obj('BDT_DelM_Bkg_a').setError(0.400728132749)
    w.obj('BDT_DelM_Bkg_a').setConstant(False)
    w.obj('BDT_DelM_Bkg_b').setMin(-0.55) ; w.obj('BDT_DelM_Bkg_b').setMax(1.0)
    w.obj('BDT_DelM_Bkg_b').setVal(-0.364271880455) ; w.obj('BDT_DelM_Bkg_b').setError(0.0194366995405)
    w.obj('BDT_DelM_Bkg_b').setConstant(False)
    w.obj('BDT_DelM_Bkg_c').setMin(7.0) ; w.obj('BDT_DelM_Bkg_c').setMax(400.0)
    w.obj('BDT_DelM_Bkg_c').setVal(199.827646996) ; w.obj('BDT_DelM_Bkg_c').setError(190.783847966)
    w.obj('BDT_DelM_Bkg_c').setConstant(True)
    w.obj('BDT_DelM_Bkg_m0').setMin(137.5) ; w.obj('BDT_DelM_Bkg_m0').setMax(140.5)
    w.obj('BDT_DelM_Bkg_m0').setVal(139.315375133) ; w.obj('BDT_DelM_Bkg_m0').setError(0.00080884451495)
    w.obj('BDT_DelM_Bkg_m0').setConstant(True)

    
    
    #w.obj('BDT_D0M_Bkg_Exp_Const').setMin(-0.01) ; w.obj('BDT_D0M_Bkg_Exp_Const').setMax(0.003)
    #w.obj('BDT_D0M_Bkg_Exp_Const').setVal(-0.00383788482662) ; w.obj('BDT_D0M_Bkg_Exp_Const').setError(0.000116387358186)
    #w.obj('BDT_D0M_Bkg_Exp_Const').setConstant(False)
    #w.obj('BDT_DelM_Bkg_a').setMin(-19.0) ; w.obj('BDT_DelM_Bkg_a').setMax(-1.0)
    #w.obj('BDT_DelM_Bkg_a').setVal(-13.3201629713) ; w.obj('BDT_DelM_Bkg_a').setError(2.49499373145)
    #w.obj('BDT_DelM_Bkg_a').setConstant(False)
    #w.obj('BDT_DelM_Bkg_b').setMin(-0.35) ; w.obj('BDT_DelM_Bkg_b').setMax(1.0)
    #w.obj('BDT_DelM_Bkg_b').setVal(-0.174366431028) ; w.obj('BDT_DelM_Bkg_b').setError(0.523782969093)
    #w.obj('BDT_DelM_Bkg_b').setConstant(False)
    #w.obj('BDT_DelM_Bkg_c').setMin(7.0) ; w.obj('BDT_DelM_Bkg_c').setMax(200.0)
    #w.obj('BDT_DelM_Bkg_c').setVal(94.6348929704) ; w.obj('BDT_DelM_Bkg_c').setError(173.109088403)
    #w.obj('BDT_DelM_Bkg_c').setConstant(False)
    #w.obj('BDT_DelM_Bkg_m0').setMin(137.5) ; w.obj('BDT_DelM_Bkg_m0').setMax(140.5)
    #w.obj('BDT_DelM_Bkg_m0').setVal(139.439614429) ; w.obj('BDT_DelM_Bkg_m0').setError(0.0561243850283)
    #w.obj('BDT_DelM_Bkg_m0').setConstant(False)
    
  if mode_later_than('toy', config['mode']):
    w.obj('BDT1_N_Comb').setConstant(False)
    w.obj('BDT2_N_Comb').setConstant(False)
    w.obj('BDT3_N_Comb').setConstant(False)
    
    w.obj('BDT1_N_Comb').setMin(6410.32853707) ; w.obj('BDT1_N_Comb').setMax(21792.3826104)
    w.obj('BDT1_N_Comb').setVal(11602.1632716) ; w.obj('BDT1_N_Comb').setError(67.8190207432)
    w.obj('BDT2_N_Comb').setMin(817.028524044) ; w.obj('BDT2_N_Comb').setMax(7424.26091262)
    w.obj('BDT2_N_Comb').setVal(3000.66587751) ; w.obj('BDT2_N_Comb').setError(34.6192566872)
    w.obj('BDT3_N_Comb').setMin(275.055535903) ; w.obj('BDT3_N_Comb').setMax(6718.4545192)
    w.obj('BDT3_N_Comb').setVal(1814.38212826) ; w.obj('BDT3_N_Comb').setError(27.0289708628)

    
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


    w.obj('PiPi_N_Comb').setMin(100) ; w.obj('PiPi_N_Comb').setMax(97987.0) ; w.obj('PiPi_N_Comb').setVal(69684.0) ; w.obj('PiPi_N_Comb').setError(421.851616813)
    w.obj('PiPi_N_Prompt').setMin(100) ; w.obj('PiPi_N_Prompt').setMax(58492.0) ; w.obj('PiPi_N_Prompt').setVal(37960.0) ; w.obj('PiPi_N_Prompt').setError(1331.09040422)
    w.obj('PiPi_N_Sig').setMin(30000) ; w.obj('PiPi_N_Sig').setMax(108145.0) ; w.obj('PiPi_N_Sig').setVal(83350.0) ; w.obj('PiPi_N_Sig').setError(1409.2345)
    
    
    w.obj('PiPi_DelM_Bkg_b').setMin(-2) ; w.obj('PiPi_DelM_Bkg_b').setMax(2.17828074726) ; w.obj('PiPi_DelM_Bkg_b').setVal(0.535463938294) ; w.obj('PiPi_DelM_Bkg_b').setError(1.14479929974)
    
    
    
    
    # nll analyse, nlls up to 1610.0 on Sat Sep 07 20:02:56 2013 run on fitResult.toy.root
    #
    # EMu_BR  has a low first and last bin! Orig limits -1.77774116725e-07 1.77774119164e-07
    # Dont want to expand min range to -3.59472925008e-05 too far
    # Dont want to expand max range to 3.59472920691e-05 too far
    w.obj('EMu_BR').setMin(-4.44435293642e-07) ; w.obj('EMu_BR').setMax(4.44435296081e-07) ; w.obj('EMu_BR').setVal(1.21950004217e-15) ; w.obj('EMu_BR').setError(9.89560007869e-09)
    # ---->>>> changeRatio down 1.94804847128 at 0.863 : 142 -47.0763656159 -24.1659108128
    # PiPi_D0M_Bkg_Poly_a1  has a low first bin. Orig limits -0.95 0.9
    w.obj('PiPi_D0M_Bkg_Poly_a1').setMin(-1.26049478117) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setMax(0.89075) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setVal(-0.247) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setError(0.0200932100123)
    # ---->>>> changeRatio down 1.94630317517 at 0.831415225 : 86 -210.136978133 -107.967238
    # PiPi_D0M_Sig_Gaus1_Frac  has a low first bin. Orig limits 1e-05 0.989778125
    # Attempted value -0.472310982997 hits limits 1e-05
    w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMin(1e-05) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMax(0.97988044375) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setVal(0.23755435) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setError(0.0122650890842)
    # PiPi_D0M_Sig_Gaus_Mean  has a low first and last bin! Orig limits 1865.00868984 1868.8362
    w.obj('PiPi_D0M_Sig_Gaus_Mean').setMin(1863.80390049) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setMax(1869.21601352) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setVal(1866.76934451) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setError(0.0404046498786)
    # PiPi_D0M_Sig_Gaus_Sigma1  has a low first and last bin! Orig limits 3.52257699616 10.0
    # Dont want to expand min range to -1.58769063896 too far 
    # Attempted value -1.33549025672 hits limits 0.001
    # Dont want to expand max range to 19.8047753299 too far  
    # Attempted value 14.8580672529 hits limits 10
    w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMin(0.001) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMax(10) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setVal(5.98399773762) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setError(0.164018844414)
    # ---->>>> changeRatio up 1.21802926022 at -19.7987142077 : 406 372.827738348 306.09095407
    # ---->>>> changeRatio up 1.21492554291 at -19.0181189739 : 407 306.09095407 251.942150576
    # ---->>>> changeRatio up 1.21728965831 at -18.2375237402 : 408 251.942150576 206.969761762
    # ---->>>> changeRatio up 1.22526458611 at -17.4569285064 : 409 206.969761762 168.918423097
    # ---->>>> changeRatio up 1.23996709795 at -16.6763332726 : 410 168.918423097 136.228149421
    # ---->>>> changeRatio up 1.26393502123 at -15.8957380389 : 411 136.228149421 107.780975393
    # ---->>>> changeRatio up 1.30244983696 at -15.1151428051 : 412 107.780975393 82.7524963608
    # ---->>>> changeRatio down 1.48740740505 at 235.27575173 : 351 -184.333616851 -123.929473677
    # ---->>>> changeRatio down 0.72339218248 at 235.421339877 : 352 -123.929473677 -171.317131534
    # ---->>>> changeRatio down 1.38232201956 at 235.566928023 : 353 -171.317131534 -123.934314226
    # ---->>>> changeRatio down 0.654810600112 at 235.639722096 : 354 -123.934314226 -189.267422068
    # ---->>>> changeRatio down 0.481584657041 at 235.748913206 : 356 -158.609110796 -329.348347122
    # ---->>>> changeRatio down 0.12458558734 at 235.785310243 : 357 -329.348347122 -2643.5509448
    # ---->>>> changeRatio down 338.36838043 at 235.821707279 : 358 -2643.5509448 -7.81264177652
    # ---->>>> changeRatio down 0.0269705653437 at 235.858104316 : 359 -7.81264177652 -289.672896247
    # ---->>>> changeRatio down 1.46500508758 at 237.022809487 : 360 -289.672896247 -197.728252757
    # ---->>>> changeRatio down 0.707186871418 at 237.605162072 : 361 -197.728252757 -279.598308097
    # ---->>>> changeRatio down 1.21527790277 at 238.187514658 : 362 -279.598308097 -230.069441285
    # ---->>>> changeRatio down 1.23789510448 at 238.69707317 : 365 -163.884116411 -132.389340436
    # ---->>>> changeRatio down 0.532050595766 at 238.733470207 : 366 -132.389340436 -248.828478887
    # ---->>>> changeRatio down 0.116845982508 at 238.769867243 : 367 -248.828478887 -2129.54244165
    # ---->>>> changeRatio down 284.937899204 at 238.80626428 : 368 -2129.54244165 -7.47370724496
    # ---->>>> changeRatio down 0.494171240752 at 238.842661317 : 369 -7.47370724496 -15.1237195301
    # ---->>>> changeRatio down 0.488089404879 at 238.91545539 : 370 -15.1237195301 -30.9855517839
    # ---->>>> changeRatio down 0.475058989568 at 239.061043536 : 371 -30.9855517839 -65.2246404433
    # ---->>>> changeRatio down 0.197234493579 at 239.352219829 : 372 -65.2246404433 -330.695910537
    # PiPi_DelM_Bkg_c  has a low first bin. Orig limits 7.57589078997 240.516925
    # Dont want to expand min range to -224.173026461 too far
    w.obj('PiPi_DelM_Bkg_c').setMin(-167.129884868) ; w.obj('PiPi_DelM_Bkg_c').setMax(238.478690951) ; w.obj('PiPi_DelM_Bkg_c').setVal(35.5288148952) ; w.obj('PiPi_DelM_Bkg_c').setError(17.0567889443)
    # PiPi_DelM_Bkg_m0  has a low first and last bin! Orig limits 138.130405839 139.55979375
    # Dont want to expand min range to 135.627279555 too far
    # Dont want to expand max range to 140.676635816 too far
    w.obj('PiPi_DelM_Bkg_m0').setMin(137.058364906) ; w.obj('PiPi_DelM_Bkg_m0').setMax(140.631834683) ; w.obj('PiPi_DelM_Bkg_m0').setVal(139.302503926) ; w.obj('PiPi_DelM_Bkg_m0').setError(0.00067159541878)
    # PiPi_DelM_Sig_Gaus1_Frac  has a low first and last bin! Orig limits 0.0934461751464 0.851703552449
    w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMin(0.0510868817478) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMax(0.88410825964) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setVal(0.50290515889) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setError(0.040695759673)
    # PiPi_DelM_Sig_Gaus_Mean  has a low first bin. Orig limits 145.259705856 145.6819
    w.obj('PiPi_DelM_Sig_Gaus_Mean').setMin(145.225643035) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setMax(145.673456117) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setVal(145.453915162) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setError(0.00364494370054)
    # PiPi_DelM_Sig_Gaus_Sigma1  has a low first bin. Orig limits 0.308138929021 0.97104
    w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMin(0.300916538388) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMax(0.95778197858) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setVal(0.507009250315) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setError(0.015862428581)
    # PiPi_DelM_Sig_Gaus_Sigma2  has a low first bin. Orig limits 0.628602484886 1.593635
    w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMin(0.61322789089) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMax(1.5743343497) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setVal(0.956713540025) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setError(0.0277486971738)
    w.obj('PiPi_N_Comb').setMin(3281.3275) ; w.obj('PiPi_N_Comb').setMax(96029.26) ; w.obj('PiPi_N_Comb').setVal(9888.7) ; w.obj('PiPi_N_Comb').setError(141.690393554)
    w.obj('PiPi_N_Prompt').setMin(6815.08) ; w.obj('PiPi_N_Prompt').setMax(57324.16) ; w.obj('PiPi_N_Prompt').setVal(14114.08) ; w.obj('PiPi_N_Prompt').setError(210.872045187)
    w.obj('PiPi_N_Sig').setMin(37423.775) ; w.obj('PiPi_N_Sig').setMax(106582.1) ; w.obj('PiPi_N_Sig').setVal(50317.7) ; w.obj('PiPi_N_Sig').setError(271.475594588)


    # EMu_BR  has a low first and last bin! Orig limits -4.44435293642e-07 4.44435296081e-07
    # Dont want to expand min range to -1.87182358878e-05 too far
    # Dont want to expand max range to 1.87182358059e-05 too far
    w.obj('EMu_BR').setMin(-1.11108823593e-06) ; w.obj('EMu_BR').setMax(1.11108823837e-06) ; w.obj('EMu_BR').setVal(1.2195000157e-15) ; w.obj('EMu_BR').setError(3.32303170652e-09)
    w.obj('PiPi_D0M_Bkg_Poly_a1').setMin(-1.00503446341) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setMax(0.869237552188) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setVal(-0.227897286208) ; w.obj('PiPi_D0M_Bkg_Poly_a1').setError(0.0179270551207)
    # ---->>>> changeRatio down 1.946697207 at 0.832899877188 : 87 -209.39909036 -107.566338312
    # PiPi_D0M_Sig_Gaus1_Frac  has a low first bin. Orig limits 1e-05 0.97988044375
    # Attempted value -0.467927517871 hits limits 1e-05
    w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMin(1e-05) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setMax(0.970081739313) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setVal(0.2351789065) ; w.obj('PiPi_D0M_Sig_Gaus1_Frac').setError(0.00845565936459)
    w.obj('PiPi_D0M_Sig_Gaus_Mean').setMin(1864.50747518) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setMax(1869.10777126) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setVal(1866.83468379) ; w.obj('PiPi_D0M_Sig_Gaus_Mean').setError(0.0363274918353)
    # PiPi_D0M_Sig_Gaus_Sigma1  has a low last bin. Orig limits 0.001 10.0
    # Dont want to expand max range to 19.8553344874 too far
    # Attempted value 17.49925 hits limits 10
    w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMin(2.30077) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setMax(10) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setVal(6.0004) ; w.obj('PiPi_D0M_Sig_Gaus_Sigma1').setError(0.114233942279)
    # ---->>>> changeRatio up 1.23914416824 at -19.7987142077 : 357 399.222452558 322.175952395
    # ---->>>> changeRatio up 1.23416730948 at -19.0181189739 : 358 322.175952395 261.047225866
    # ---->>>> changeRatio up 1.23603899503 at -18.2375237402 : 359 261.047225866 211.196594053
    # ---->>>> changeRatio up 1.2448007784 at -17.4569285064 : 360 211.196594053 169.662967535
    # ---->>>> changeRatio up 1.26186854067 at -16.6763332726 : 361 169.662967535 134.453758111
    # ---->>>> changeRatio up 1.29068552434 at -15.8957380389 : 362 134.453758111 104.172360792
    # ---->>>> changeRatio up 1.33884301969 at -15.1151428051 : 363 104.172360792 77.8077483771
    # ---->>>> changeRatio up 1.42482722949 at -14.3345475714 : 364 77.8077483771 54.6085495608
    # ---->>>> changeRatio up 1.60594072713 at -13.5539523376 : 365 54.6085495608 34.0040878461
    # PiPi_DelM_Bkg_a  has a low last bin. Orig limits -83.807523376 -5.748
    w.obj('PiPi_DelM_Bkg_a').setMin(-12.7733571038) ; w.obj('PiPi_DelM_Bkg_a').setMax(15.1917791186) ; w.obj('PiPi_DelM_Bkg_a').setVal(-11.9927618701) ; w.obj('PiPi_DelM_Bkg_a').setError(0.337805703618)
    # ---->>>> changeRatio up 1.34691136762 at -0.600275949668 : 304 428.791075234 318.351367093
    # ---->>>> changeRatio up 1.30144841016 at -0.579384545932 : 305 318.351367093 244.613128424
    # ---->>>> changeRatio up 1.51876228673 at -0.495818930986 : 308 276.800253531 182.253836528
    # ---->>>> changeRatio up 1.49390252711 at -0.454036123514 : 309 182.253836528 121.998479298
    # ---->>>> changeRatio up 1.4935134453 at -0.412253316041 : 310 121.998479298 81.685558093
    # ---->>>> changeRatio up 1.51876687647 at -0.370470508569 : 311 81.685558093 53.7841319549
    # ---->>>> changeRatio up 1.58237850331 at -0.328687701096 : 312 53.7841319549 33.989422785
    # PiPi_DelM_Bkg_b  has a low last bin. Orig limits -2.0 2.17828074726
    w.obj('PiPi_DelM_Bkg_b').setMin(-0.286904893623) ; w.obj('PiPi_DelM_Bkg_b').setMax(4.85677977341) ; w.obj('PiPi_DelM_Bkg_b').setVal(-0.161556471206) ; w.obj('PiPi_DelM_Bkg_b').setError(0.0326973912343)
    # ---->>>> changeRatio up 1.3277913229 at 2.71870625621 : 60 358.684768133 270.136400162
    # ---->>>> changeRatio up 0.745658281979 at 3.22571697598 : 61 270.136400162 362.279085059
    # ---->>>> changeRatio up 1.66653719423 at 4.23973841553 : 62 362.279085059 217.384338204
    # ---->>>> changeRatio down 0.786697044944 at 210.086090644 : 114 -301.72195544 -383.53004804
    # ---->>>> changeRatio down 0.744742444684 at 214.142176402 : 115 -383.53004804 -514.983469491
    # ---->>>> changeRatio down 1.50664412585 at 218.19826216 : 116 -514.983469491 -341.808301412
    # ---->>>> changeRatio down 0.756889964357 at 220.226305039 : 117 -341.808301412 -451.595763596
    # ---->>>> changeRatio down 1.44864175295 at 222.254347918 : 118 -451.595763596 -311.737365485
    # ---->>>> changeRatio down 1.5037309655 at 223.268369358 : 119 -311.737365485 -207.309267839
    # ---->>>> changeRatio down 0.0491693095702 at 236.514024412 : 165 -444.56877646 -9041.59078795
    # ---->>>> changeRatio down 306.476894846 at 236.577400752 : 166 -9041.59078795 -29.5017045004
    # ---->>>> changeRatio down 0.48082274342 at 236.704153432 : 167 -29.5017045004 -61.356715971
    # ---->>>> changeRatio down 0.457374419558 at 236.957658792 : 168 -61.356715971 -134.149863541
    # ---->>>> changeRatio down 0.390739881994 at 237.464669511 : 169 -134.149863541 -343.322680185
    w.obj('PiPi_DelM_Bkg_c').setMin(5.25375985507) ; w.obj('PiPi_DelM_Bkg_c').setMax(233.281831073) ; w.obj('PiPi_DelM_Bkg_c').setVal(51.8987460743) ; w.obj('PiPi_DelM_Bkg_c').setError(30.9336256541)
    # ---->>>> changeRatio down 335.440242982 at 139.880289321 : 153 -264.459835423 -0.788396267162
    # ---->>>> changeRatio down 0.0585743884239 at 139.88140603 : 154 -0.788396267162 -13.4597438979
    # ---->>>> changeRatio down 1.77280687104 at 139.952875425 : 158 -20.0016253323 -11.2824615355
    # ---->>>> changeRatio down 1.7418598072 at 140.006477472 : 164 -20.6380365769 -11.8482764753
    # ---->>>> changeRatio down 1.68139160911 at 140.024344821 : 168 -18.899190974 -11.2402077372
    # ---->>>> changeRatio down 1.70126230649 at 140.031045077 : 171 -15.5428115331 -9.13604649552
    # ---->>>> changeRatio down 1.73143709067 at 140.502296404 : 267 -22.0698806287 -12.7465680086
    # ---->>>> changeRatio down 1.70254572261 at 140.511230078 : 271 -19.5530436991 -11.4845924191
    # ---->>>> changeRatio down 1.67979303646 at 140.515696915 : 275 -18.3996444228 -10.9535186915
    # ---->>>> changeRatio down 0.769910695194 at 140.517930334 : 279 -18.2124970861 -23.6553371707
    # ---->>>> changeRatio down 0.693590140343 at 140.518488689 : 280 -23.6553371707 -34.1056422155
    # ---->>>> changeRatio down 0.540128782591 at 140.519047043 : 281 -34.1056422155 -63.1435378279
    # ---->>>> changeRatio down 0.235690114487 at 140.519605398 : 282 -63.1435378279 -267.90914827
    # ---->>>> changeRatio down 43.5623031853 at 140.520163752 : 283 -267.90914827 -6.15002258099
    # ---->>>> changeRatio down 0.236143494447 at 140.52463059 : 284 -6.15002258099 -26.0435825065
    # ---->>>> changeRatio down 1.81029078953 at 140.578232636 : 287 -32.0954109223 -17.7294228683
    # PiPi_DelM_Bkg_m0  has a low first bin. Orig limits 137.058364906 140.631834683
    w.obj('PiPi_DelM_Bkg_m0').setMin(136.016898675) ; w.obj('PiPi_DelM_Bkg_m0').setMax(140.613967334) ; w.obj('PiPi_DelM_Bkg_m0').setVal(139.345385563) ; w.obj('PiPi_DelM_Bkg_m0').setError(0.0223100875922)
    w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMin(0.0760775230846) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setMax(0.875778045861) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setVal(0.50091842581) ; w.obj('PiPi_DelM_Sig_Gaus1_Frac').setError(0.0113596914391)
    w.obj('PiPi_DelM_Sig_Gaus_Mean').setMin(145.243555558) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setMax(145.664499855) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setVal(145.449549576) ; w.obj('PiPi_DelM_Sig_Gaus_Mean').setError(0.00328218672044)
    w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMin(0.305843029189) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setMax(0.944644669776) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setVal(0.511113479249) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma1').setError(0.00565248128873)
    w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMin(0.622838955478) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setMax(1.55511222052) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setVal(0.959226216062) ; w.obj('PiPi_DelM_Sig_Gaus_Sigma2').setError(0.0096554571041)
    # PiPi_N_Comb  has a low first bin. Orig limits 3281.3275 96029.26
    w.obj('PiPi_N_Comb').setMin(2855.66522209) ; w.obj('PiPi_N_Comb').setMax(94174.30135) ; w.obj('PiPi_N_Comb').setVal(8846.20345) ; w.obj('PiPi_N_Comb').setError(121.599174939)
    # PiPi_N_Prompt  has a low first bin. Orig limits 6815.08 57324.16
    w.obj('PiPi_N_Prompt').setMin(6168.97998098) ; w.obj('PiPi_N_Prompt').setMax(56313.9784) ; w.obj('PiPi_N_Prompt').setVal(13886.3512) ; w.obj('PiPi_N_Prompt').setError(165.91222371)
    # PiPi_N_Sig  has a low first bin. Orig limits 37423.775 106582.1
    w.obj('PiPi_N_Sig').setMin(36925.9456633) ; w.obj('PiPi_N_Sig').setMax(105198.9335) ; w.obj('PiPi_N_Sig').setVal(48489.107) ; w.obj('PiPi_N_Sig').setError(227.356324921)


    w.obj('PiPi_DelM_Bkg_b').setMin(-20) ; w.obj('PiPi_DelM_Bkg_b').setMax(4.85677977341) ; w.obj('PiPi_DelM_Bkg_b').setVal(-0.161556471206) ; w.obj('PiPi_DelM_Bkg_b').setError(0.0326973912343)
    w.obj('PiPi_N_Comb').setMin(2855.66522209) ; w.obj('PiPi_N_Comb').setMax(120000) ; w.obj('PiPi_N_Comb').setVal(8846.20345) ; w.obj('PiPi_N_Comb').setError(121.599174939)
    w.obj('PiPi_DelM_Bkg_a').setMin(-20) ; w.obj('PiPi_DelM_Bkg_a').setMax(15.1917791186) ; w.obj('PiPi_DelM_Bkg_a').setVal(-11.9927618701) ; w.obj('PiPi_DelM_Bkg_a').setError(0.337805703618)
    
    #w.obj('BDT_DelM_Bkg_a').setConstant(True)
    #w.obj('PiPi_DelM_Bkg_a').setConstant(True)
    #w.obj('BDT_DelM_Bkg_b').setConstant(True)
    #w.obj('PiPi_DelM_Bkg_b').setConstant(True)
    w.obj('BDT_DelM_Bkg_c').setConstant(True)
    w.obj('PiPi_DelM_Bkg_c').setConstant(True)
    #w.obj('BDT_DelM_Bkg_m0').setConstant(True)
    #w.obj('PiPi_DelM_Bkg_m0').setConstant(True)
    
    
    if config['norm'] is 'kpi':
      w.obj('EMu_BR').setMin(-1.11108823593e-04) ; w.obj('EMu_BR').setMax(1.11108823837e-04) ; w.obj('EMu_BR').setVal(1.2195000157e-15) ; w.obj('EMu_BR').setError(3.32303170652e-07)
      w.obj('PiPi_N_Comb').setMin(2000.) ; w.obj('PiPi_N_Comb').setMax(1000000) ; w.obj('PiPi_N_Comb').setVal(8846.20345) ; w.obj('PiPi_N_Comb').setError(121.599174939)
      w.obj('PiPi_N_Prompt').setMin(6000.) ; w.obj('PiPi_N_Prompt').setMax(500000) ; w.obj('PiPi_N_Prompt').setVal(13886.3512) ; w.obj('PiPi_N_Prompt').setError(165.91222371)
      w.obj('PiPi_N_Sig').setMin(30000.) ; w.obj('PiPi_N_Sig').setMax(1000000) ; w.obj('PiPi_N_Sig').setVal(48489.107) ; w.obj('PiPi_N_Sig').setError(227.356324921)

  

  return w



