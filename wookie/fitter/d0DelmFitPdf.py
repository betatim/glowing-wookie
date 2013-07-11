


def setup_workspace():

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

  #RooAbsReal.defaultIntegratorConfig().Print()
  #RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-10)
  #RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-10)
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
  D0_M = w.factory("D0_M[1800,1930]") #TODO: define mass ranges slightly better
  Del_M = w.factory("Del_M[139,155]")
  D0_M.setUnit("MeV")
  Del_M.setUnit("MeV")

  for dst_side in ["", "dstsig", "dsthigh", "dstlow"]:
    for d_side in ["", "dsig", "dhigh", "dlow"]:
      name = dst_side+d_side
      if dst_side == "dsthigh":
        Del_M.setRange(name,148.,155.)
      elif dst_side == "dstsig":
        Del_M.setRange(name,143.,148.)
      elif dst_side == "dstlow":
        Del_M.setRange(name,139.,143.)
        
      if d_side == "dhigh":
        Del_M.setRange(name,1885.,1930.)
      elif d_side == "dsig":
        Del_M.setRange(name,1835.,1885.)
      elif d_side == "dlow":
        Del_M.setRange(name,1800.,1835.)




  w.defineSet("args","D0_M,Del_M")
  w.defineSet("argsPreCut","D0_M,Del_M,RAND")

  w.factory("RooGaussian::D0M_Sig_Gaus1(D0_M,D0M_Sig_Gaus_Mean[1865,1850,1880],D0M_Sig_Gaus_Sigma1[10,1,30])")
  w.factory("RooGaussian::D0M_Sig_Gaus2(D0_M,D0M_Sig_Gaus_Mean,D0M_Sig_Gaus_Sigma2[3,1,30])")
  w.factory("SUM::D0M_Sig_Gaus(D0M_Sig_Gaus1_Frac[0.8,0,1]*D0M_Sig_Gaus1,D0M_Sig_Gaus2)")
  
  
  w.factory("RooGaussian::D0M_MisId_Gaus1(D0_M,D0M_MisId_Gaus_Mean[1800,1740,1820],D0M_Sig_Gaus_Sigma1)")
  w.factory("RooGaussian::D0M_MisId_Gaus2(D0_M,D0M_MisId_Gaus_Mean,D0M_Sig_Gaus_Sigma2)")
  w.factory("SUM::D0M_MisId_Gaus(D0M_Sig_Gaus1_Frac*D0M_MisId_Gaus1,D0M_MisId_Gaus2)")
  
  
  w.factory("RooChebychev::D0M_Bkg_Poly(D0_M,{D0M_Bkg_Poly_a1[0,-1,1]})")
  


  w.factory("RooGaussian::DelM_Sig_Gaus1(Del_M,DelM_Sig_Gaus_Mean[145.5,143,148],DelM_Sig_Gaus_Sigma1[1,0,5] )")
  w.factory("RooGaussian::DelM_Sig_Gaus2(Del_M,DelM_Sig_Gaus_Mean,DelM_Sig_Gaus_Sigma2[.1,0,2] )")
  w.factory("SUM::DelM_Sig_Gaus(DelM_Sig_Gaus1_Frac[0.8,0,1]*DelM_Sig_Gaus1,DelM_Sig_Gaus2)")

  w.factory("RooDstD0BG::DelM_Bkg(Del_M,DelM_Bkg_m0[139.5,134,144],DelM_Bkg_c[80,0,1000],DelM_Bkg_a[-1,-100,10],DelM_Bkg_b[0.2,-0.2,10])")

  w.factory("PROD::Sig(DelM_Sig_Gaus,D0M_Sig_Gaus)")
  w.factory("PROD::Comb(DelM_Bkg,D0M_Bkg_Poly)")
  w.factory("PROD::MisId(DelM_Sig_Gaus,D0M_MisId_Gaus)")
  w.factory("PROD::Prompt(DelM_Bkg,D0M_Sig_Gaus)")
  

  w.factory("SUM::Final_PDF(N_Sig[10000,0,50000]*Sig,N_Prompt[5000,0,20000]*Prompt,N_Comb[10000,0,50000]*Comb,N_MisId[500,0,5000]*MisId)")


  return w






