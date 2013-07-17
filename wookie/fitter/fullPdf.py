


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
  #RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-10)
  #RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-10)
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
  Del_M = w.factory("Del_M[139,155]")
  Del_M.setUnit("MeV")
  D0_M.setUnit("MeV")
  D0_M.setBins(100)

  Dataset = w.factory("DataSet[BDT1,BDT2,BDT3,PiPi]")
  
  w.factory("classID[Sig=0,Bkg=1]")
  w.factory("BDT_ada[-1,1]")
  
  for data in ["", "BDT1", "BDT2", "BDT3", "PiPi"]:
    for dst_side in ["", "dstsig", "dsthigh", "dstlow"]:
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
        
        if dst_side == "dsthigh":
          Del_M.setRange(name,148.,155.)
        elif dst_side == "dstsig":
          Del_M.setRange(name,143.,148.)
        elif dst_side == "dstlow":
          Del_M.setRange(name,139.,143.)
          
        if d_side == "dhigh":
          D0_M.setRange(name,1885.,1930.)
        elif d_side == "dsig":
          D0_M.setRange(name,1835.,1885.)
        elif d_side == "dlow":
          D0_M.setRange(name,1800.,1835.)

  w.defineSet("args","D0_M,Del_M,DataSet")
  w.defineSet("argsBasic","D0_M,Del_M")
  w.defineSet("argsPreCut","D0_M,Del_M,RAND,classID,BDT_ada")
  w.defineSet("argsPreCutPiPi","D0_M,Del_M,RAND")

  # --- PiPi ---
  w.factory("RooGenericPdf::PiPi_D0M_Range('(D0_M>PiPi_D0M_Min&&D0_M<PiPi_D0M_Max)',{D0_M,PiPi_D0M_Min[1798],PiPi_D0M_Max[1930]})")

  #  D0_M Signal
  w.factory("RooGaussianTrunk::PiPi_D0M_Sig_Gaus1(D0_M,PiPi_D0M_Sig_Gaus_Mean[1865,1850,1880],PiPi_D0M_Sig_Gaus_Sigma1[10,1,30],PiPi_D0M_Min,PiPi_D0M_Max)")
  w.factory("RooGaussianTrunk::PiPi_D0M_Sig_Gaus2(D0_M,PiPi_D0M_Sig_Gaus_Mean,PiPi_D0M_Sig_Gaus_Sigma2[3,1,30],PiPi_D0M_Min,PiPi_D0M_Max)")
  w.factory("SUM::PiPi_D0M_Sig(PiPi_D0M_Sig_Gaus1_Frac[0.8,0,1]*PiPi_D0M_Sig_Gaus1,PiPi_D0M_Sig_Gaus2)")
  #w.factory("PROD::PiPi_D0M_Sig(PiPi_D0M_Sig_Sum,PiPi_D0M_Range)")
  
  #  MisId
  w.factory("RooGaussianTrunk::PiPi_D0M_MisId_Gaus1(D0_M,PiPi_D0M_MisId_Gaus_Mean[1800,1740,1820],PiPi_D0M_Sig_Gaus_Sigma1,PiPi_D0M_Min,PiPi_D0M_Max)")
  w.factory("RooGaussianTrunk::PiPi_D0M_MisId_Gaus2(D0_M,PiPi_D0M_MisId_Gaus_Mean,PiPi_D0M_Sig_Gaus_Sigma2,PiPi_D0M_Min,PiPi_D0M_Max)")
  w.factory("SUM::PiPi_D0M_MisId(PiPi_D0M_Sig_Gaus1_Frac*PiPi_D0M_MisId_Gaus1,PiPi_D0M_MisId_Gaus2)")
  #w.factory("PROD::PiPi_D0M_MisId(PiPi_D0M_MisId_Sum,PiPi_D0M_Range)")
  
  #  D0_M Combinatorical
  w.factory("RooChebychev::PiPi_D0M_Bkg_Poly(D0_M,{PiPi_D0M_Bkg_Poly_a1[0,-1,1]})")
  w.factory("PROD::PiPi_D0M_Bkg(PiPi_D0M_Bkg_Poly,PiPi_D0M_Range)")
  
  #  Del_M signal
  w.factory("RooGaussian::PiPi_DelM_Sig_Gaus1(Del_M,PiPi_DelM_Sig_Gaus_Mean[145.5,143,148],PiPi_DelM_Sig_Gaus_Sigma1[1,0,5] )")
  w.factory("RooGaussian::PiPi_DelM_Sig_Gaus2(Del_M,PiPi_DelM_Sig_Gaus_Mean,PiPi_DelM_Sig_Gaus_Sigma2[.1,0,2] )")
  w.factory("SUM::PiPi_DelM_Sig(PiPi_DelM_Sig_Gaus1_Frac[0.8,0,1]*PiPi_DelM_Sig_Gaus1,PiPi_DelM_Sig_Gaus2)")

  #  Del_M Combinatorical
  w.factory("RooDstD0BG::PiPi_DelM_Bkg(Del_M,PiPi_DelM_Bkg_m0[139.5,134,144],PiPi_DelM_Bkg_c[80,0,1000],PiPi_DelM_Bkg_a[-1,-100,10],PiPi_DelM_Bkg_b[0.2,-0.2,10])")

  w.factory("PROD::PiPi_Sig(PiPi_DelM_Sig,PiPi_D0M_Sig)")
  w.factory("PROD::PiPi_Comb(PiPi_DelM_Bkg,PiPi_D0M_Bkg)")
  w.factory("PROD::PiPi_MisId(PiPi_DelM_Sig,PiPi_D0M_MisId)")
  w.factory("PROD::PiPi_Prompt(PiPi_DelM_Bkg,PiPi_D0M_Sig)")
  
  w.factory("SUM::PiPi_Final_PDF(PiPi_N_Sig[10000,0,100000]*PiPi_Sig,PiPi_N_Prompt[5000,0,50000]*PiPi_Prompt,PiPi_N_Comb[10000,0,100000]*PiPi_Comb,PiPi_N_MisId[1000,0,10000]*PiPi_MisId)")
  

  # --- eMu ---
  
  #w.factory("EMu_N_Sig[1000,0,100000]")
  for n in (1,2,3):
    w.factory("BDT%(n)i_Sig_Eff[0.3,0,1]"%({"n":n}))
    
  w.factory("EMu_Eff[%f]"%(config['emuEff']))
  w.factory("EMu_BR[1e-4,0,1e-3]")
  
  w.factory("PiPi_Eff[%f]"%(config['pipiEff']))
  w.factory("PiPi_BR[%f]"%(config['pipiBR'][0]))
  w.obj("PiPi_BR").setError(config['pipiBR'][1])
  
  w.factory("RooFormulaVar::EMu_N_Sig('PiPi_N_Sig*((EMu_BR*EMu_Eff)/(PiPi_BR*PiPi_Eff))',{PiPi_BR,EMu_BR,EMu_Eff,PiPi_Eff,PiPi_N_Sig})")
    
  for n in (1,2,3):
    if n is not 3:
      w.factory("RooFormulaVar::BDT%(n)i_N_Sig('EMu_N_Sig*BDT%(n)i_Sig_Eff',{EMu_N_Sig,BDT%(n)i_Sig_Eff})"%({"n":n}))
    else:
      w.factory("RooFormulaVar::BDT%(n)i_N_Sig('EMu_N_Sig*(1-(BDT1_Sig_Eff+BDT2_Sig_Eff))',{EMu_N_Sig,BDT1_Sig_Eff,BDT2_Sig_Eff})"%({"n":n}))
      
    #  D0_M Signal
    w.factory("CBShape:BDT%(n)i_D0M_Sig_CB1(D0_M, BDT%(n)i_D0M_Sig_CB_Mean[1850,1750,1900], BDT%(n)i_D0M_Sig_CB1_Sigma[10,1,30], BDT%(n)i_D0M_Sig_CB1_alphaleft[0.5,0,5], BDT%(n)i_D0M_Sig_CB1_n[2,0,10])"%({"n":n}))
    w.factory("CBShape:BDT%(n)i_D0M_Sig_CB2(D0_M, BDT%(n)i_D0M_Sig_CB_Mean, BDT%(n)i_D0M_Sig_CB2_Sigma[3,1,30], BDT%(n)i_D0M_Sig_CB2_alpharight[-0.5,-5,0], BDT%(n)i_D0M_Sig_CB2_n[5,0,50])"%({"n":n}))
    w.factory("SUM::BDT%(n)i_D0M_Sig(BDT%(n)i_D0M_Sig_CB1_Frac[0.8,0,1]*BDT%(n)i_D0M_Sig_CB1,BDT%(n)i_D0M_Sig_CB2)"%({"n":n}))
    #w.factory("RooGaussian::BDT%(n)i_D0M_Sig_Gaus1(D0_M,BDT%(n)i_D0M_Sig_Gaus_Mean[1865,1850,1880],BDT%(n)i_D0M_Sig_Gaus_Sigma1[10,1,30])"%({"n":n}))
    #w.factory("RooGaussian::BDT%(n)i_D0M_Sig_Gaus2(D0_M,BDT%(n)i_D0M_Sig_Gaus_Mean,BDT%(n)i_D0M_Sig_Gaus_Sigma2[3,1,30])"%({"n":n}))
    #w.factory("SUM::BDT%(n)i_D0M_Sig(BDT%(n)i_D0M_Sig_Gaus1_Frac[0.8,0,1]*BDT%(n)i_D0M_Sig_Gaus1,BDT%(n)i_D0M_Sig_Gaus2)"%({"n":n}))
  
    #  D0_M Combinatorical
    w.factory("RooGenericPdf::BDT%(n)i_D0M_Blind('(D0_M<1700||D0_M>1900)',{D0_M})"%({"n":n}))
    w.factory("RooChebychev::BDT%(n)i_D0M_Bkg_Poly(D0_M,{})"%({"n":n}))
    w.factory("RooExponential::BDT%(n)i_D0M_Bkg_Exp(D0_M,BDT%(n)i_D0M_Bkg_Exp_Const[-0.001,-0.01,0])"%({"n":n}))
    w.factory("PROD::BDT%(n)i_D0M_Bkg_Poly_Blind(BDT%(n)i_D0M_Bkg_Poly,BDT%(n)i_D0M_Blind)"%({"n":n}))
    w.factory("PROD::BDT%(n)i_D0M_Bkg_Exp_Blind(BDT%(n)i_D0M_Bkg_Exp,BDT%(n)i_D0M_Blind)"%({"n":n}))
    w.factory("SUM::BDT%(n)i_D0M_Bkg_Blind(BDT%(n)i_D0M_Bkg_Poly_Frac[0.5,0,1]*BDT%(n)i_D0M_Bkg_Poly_Blind, BDT%(n)i_D0M_Bkg_Exp_Blind)"%({"n":n}))
    w.factory("SUM::BDT%(n)i_D0M_Bkg(BDT%(n)i_D0M_Bkg_Poly_Frac*BDT%(n)i_D0M_Bkg_Poly, BDT%(n)i_D0M_Bkg_Exp)"%({"n":n}))

    #  Del_M Combinatorical
    w.factory("RooDstD0BG::BDT%(n)i_DelM_Bkg(Del_M,BDT%(n)i_DelM_Bkg_m0[139.5,134,144],BDT%(n)i_DelM_Bkg_c[80,0,1000],BDT%(n)i_DelM_Bkg_a[-1,-100,10],BDT%(n)i_DelM_Bkg_b[0.2,-0.2,10])"%({"n":n}))
    
    #  Del_M signal
    w.factory("RooGaussian::BDT%(n)i_DelM_Sig_Gaus1(Del_M,BDT%(n)i_DelM_Sig_Gaus_Mean[145.5,143,148],BDT%(n)i_DelM_Sig_Gaus_Sigma1[1,0,5] )"%({"n":n}))
    w.factory("RooGaussian::BDT%(n)i_DelM_Sig_Gaus2(Del_M,BDT%(n)i_DelM_Sig_Gaus_Mean,BDT%(n)i_DelM_Sig_Gaus_Sigma2[.1,0,2] )"%({"n":n}))
    w.factory("SUM::BDT%(n)i_DelM_Sig(BDT%(n)i_DelM_Sig_Gaus1_Frac[0.8,0,1]*BDT%(n)i_DelM_Sig_Gaus1,BDT%(n)i_DelM_Sig_Gaus2)"%({"n":n}))
    
    w.factory("PROD::BDT%(n)i_Sig(BDT%(n)i_DelM_Sig,BDT%(n)i_D0M_Sig)"%({"n":n}))
    w.factory("PROD::BDT%(n)i_Comb_Blind(BDT%(n)i_DelM_Bkg,BDT%(n)i_D0M_Bkg_Blind)"%({"n":n}))
    #w.factory("PROD::BDT%(n)i_Prompt(BDT%(n)i_DelM_Bkg,BDT%(n)i_D0M_Sig_Gaus)"%({"n":n}))
    
    w.factory("SUM::BDT%(n)i_Final_PDF(BDT%(n)i_N_Sig*BDT%(n)i_Sig,BDT%(n)i_N_Comb[1000,0,5000]*BDT%(n)i_Comb_Blind)"%({"n":n}))
    #w.factory("SUM::BDT%(n)i_Final_PDF(BDT%(n)i_N_Sig[10000,0,50000]*BDT%(n)i_Sig,BDT%(n)i_N_Prompt[5000,0,20000]*BDT%(n)i_Prompt,BDT%(n)i_N_Comb[10000,0,50000]*BDT%(n)i_Comb,BDT%(n)i_N_MisId[500,0,5000]*BDT%(n)i_MisId)"%({"n":n}))
  



  if config['mc']:
    w.factory("SIMUL::Final_PDF(DataSet,BDT1=BDT1_Sig,BDT2=BDT2_Sig,BDT3=BDT3_Sig)")
  else:
    w.factory("SIMUL::Final_PDF(DataSet,PiPi=PiPi_Final_PDF,BDT1=BDT1_Final_PDF,BDT2=BDT2_Final_PDF,BDT3=BDT3_Final_PDF)")
    
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



