

def mode_later_than(mode,current):
  modes = ["mcnorm","norm","mc","mcpipi","datapretoy","toy","data"]
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
  from math import sqrt

  gROOT.SetStyle("Plain")
  gStyle.SetPalette(1)
  gStyle.SetOptStat(0)
  gStyle.SetOptFit(0)
  gStyle.SetOptStat(1111)
  gStyle.SetOptFit(10111)
  gStyle.SetOptTitle(1)

  #gROOT.ProcessLine(".L RooGaussianTrunk.cxx+")
  #gROOT.ProcessLine(".L RooCBShapeTrunk.cxx+")
  #gROOT.ProcessLine(".L RooChebychevTrunk.cxx+")
  #from ROOT import RooGaussianTrunk, RooChebychevTrunk, RooCBShapeTrunk

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
  
  if "norm" not in config["mode"]:
    D0_Mass = w.factory("D0_Mass[1815,1915]") 
  else:
    D0_Mass = w.factory("D0_Mass[1800,1930]")
  D0_Mass.setUnit("MeV")
  D0_Mass.setBins(60)
  
  Del_Mass = w.factory("Del_Mass[139,155]")
  Del_Mass.setUnit("MeV")
  Del_Mass.setBins(60)

  if "norm" not in config["mode"]:
    Dataset = w.factory("DataSet[BDT1,BDT2,BDT3]")
  else:
    Dataset = w.factory("DataSet[Norm]")

  w.factory("classID[Sig=0,Bkg=1]")
  w.factory("BDT_ada[-1,1]")
  w.factory("x1_PIDe[-2,20]")
  w.factory("x2_ProbNNmu[0,1]")

  #D0_Mass.setRange("blinded",1700.,1900.)
  
  if "norm" not in config["mode"]:
    dataCats = ["", "BDT1", "BDT2", "BDT3"]
  else:
    dataCats = ["", "Norm"]

  for data in dataCats:
    for dst_side in ["", "delsig", "delhigh", "dellow"]:
      for d_side in ["", "dsig", "dhigh", "dlow", "dhigh1", "dlow1", "dhigh2", "dlow2"]:
        name = data+dst_side+d_side

        if data == "BDT1":
          Dataset.setRange(name,"BDT1")
        elif data == "BDT2":
          Dataset.setRange(name,"BDT2")
        elif data == "BDT3":
          Dataset.setRange(name,"BDT3")
        elif data == "Norm":
          Dataset.setRange(name,"Norm")

        if dst_side == "delhigh":
          Del_Mass.setRange(name,148.,155.)
        elif dst_side == "delsig":
          Del_Mass.setRange(name,143.,148.)
        elif dst_side == "dellow":
          Del_Mass.setRange(name,139.,143.)

        if d_side == "dhigh2":
          D0_Mass.setRange(name,1910.,1930.)
        elif d_side == "dhigh1":
          D0_Mass.setRange(name,1890.,1910.)
        elif d_side == "dhigh":
          D0_Mass.setRange(name,1890.,1930.)
        elif d_side == "dsig":
          D0_Mass.setRange(name,1840.,1890.)
        elif d_side == "dlow":
          D0_Mass.setRange(name,1800.,1840.)
        elif d_side == "dlow1":
          D0_Mass.setRange(name,1820.,1840.)
        elif d_side == "dlow2":
          D0_Mass.setRange(name,1800.,1820.)

  w.defineSet("args","D0_Mass,Del_Mass,DataSet")
  w.defineSet("argsBasic","D0_Mass,Del_Mass")
  #w.defineSet("argsPreCut","D0_Mass,Del_Mass,RAND,classID,BDT_ada")
  w.defineSet("argsPreCut","D0_Mass,Del_Mass,RAND,classID,BDT_ada,x1_PIDe,x2_ProbNNmu")
  w.defineSet("argsPreCutPiPi","D0_Mass,Del_Mass,RAND")
  w.defineSet("argsPreCutKPi","D0_Mass,Del_Mass,RAND")

  # --- Norm ---
  if config['norm'] is "kpi":
    w.factory("{D0_Mass,Norm_D0M_Min[1815],Norm_D0M_Max[1915]}")
  else:
    w.factory("{D0_Mass,Norm_D0M_Min[1826],Norm_D0M_Max[1920]}")

  w.factory("RooGenericPdf::Norm_D0M_Range('(D0_Mass>Norm_D0M_Min&&D0_Mass<Norm_D0M_Max)',{D0_Mass,Norm_D0M_Min,Norm_D0M_Max})")


  w.factory("RooFormulaVar::Norm_D0M_Sig_Gaus2_Sigma('Norm_D0M_Sig_Gaus1_Sigma+Norm_D0M_Sig_Gaus2_Sigma_Diff',{Norm_D0M_Sig_Gaus1_Sigma[5,0,10],Norm_D0M_Sig_Gaus2_Sigma_Diff[5,0.,10.]})")
  w.factory("RooFormulaVar::Norm_D0M_Sig_Gaus3_Sigma('Norm_D0M_Sig_Gaus1_Sigma+Norm_D0M_Sig_Gaus2_Sigma_Diff+Norm_D0M_Sig_Gaus3_Sigma_Diff',{Norm_D0M_Sig_Gaus1_Sigma,Norm_D0M_Sig_Gaus2_Sigma_Diff,Norm_D0M_Sig_Gaus3_Sigma_Diff[2,0.,20.]})")

  w.factory("RooFormulaVar::Norm_D0M_Sig_Gaus1_Sigma_Scaled('Norm_D0M_Sig_Gaus1_Sigma*Norm_D0M_Sig_Gaus_Sigma_Scale',{Norm_D0M_Sig_Gaus1_Sigma,Norm_D0M_Sig_Gaus_Sigma_Scale[1]})")
  w.factory("RooFormulaVar::Norm_D0M_Sig_Gaus2_Sigma_Scaled('(Norm_D0M_Sig_Gaus1_Sigma+Norm_D0M_Sig_Gaus2_Sigma_Diff)*Norm_D0M_Sig_Gaus_Sigma_Scale',{Norm_D0M_Sig_Gaus1_Sigma,Norm_D0M_Sig_Gaus2_Sigma_Diff,Norm_D0M_Sig_Gaus_Sigma_Scale})")
  w.factory("RooFormulaVar::Norm_D0M_Sig_Gaus3_Sigma_Scaled('(Norm_D0M_Sig_Gaus1_Sigma+Norm_D0M_Sig_Gaus2_Sigma_Diff+Norm_D0M_Sig_Gaus3_Sigma_Diff)*Norm_D0M_Sig_Gaus_Sigma_Scale',{Norm_D0M_Sig_Gaus1_Sigma,Norm_D0M_Sig_Gaus2_Sigma_Diff,Norm_D0M_Sig_Gaus3_Sigma_Diff,Norm_D0M_Sig_Gaus_Sigma_Scale})")

  #  D0_Mass Signal
  w.factory("RooCBShape::Norm_D0M_Sig_Gaus1(D0_Mass,Norm_D0M_Sig_Gaus_Mean[1867,1850,1880],Norm_D0M_Sig_Gaus1_Sigma_Scaled,Norm_D0M_Sig_Gaus1_alpha[1.5,0,6],Norm_D0M_Sig_Gaus1_n[2,0,20])")
  #w.factory("RooGaussian::Norm_D0M_Sig_Gaus1(D0_Mass,Norm_D0M_Sig_Gaus_Mean[1867,1850,1880],Norm_D0M_Sig_Gaus1_Sigma_Scaled)")
  w.factory("RooCBShape::Norm_D0M_Sig_Gaus2(D0_Mass,Norm_D0M_Sig_Gaus_Mean,Norm_D0M_Sig_Gaus2_Sigma_Scaled,Norm_D0M_Sig_Gaus2_alpha[1.5,0,6],Norm_D0M_Sig_Gaus2_n[2,0,20])")
  #w.factory("RooGaussian::Norm_D0M_Sig_Gaus2(D0_Mass,Norm_D0M_Sig_Gaus_Mean,Norm_D0M_Sig_Gaus2_Sigma_Scaled)")
  #w.factory("RooGaussian::Norm_D0M_Sig_Gaus3(D0_Mass,Norm_D0M_Sig_Gaus3_Mean[1867,1850,1880],Norm_D0M_Sig_Gaus3_Sigma_Scaled)")
  w.factory("RooGaussian::Norm_D0M_Sig_Gaus3(D0_Mass,Norm_D0M_Sig_Gaus_Mean,Norm_D0M_Sig_Gaus3_Sigma_Scaled)")
  #w.factory("RooCBShape::Norm_D0M_Sig_Gaus3(D0_Mass,Norm_D0M_Sig_Gaus_Mean,Norm_D0M_Sig_Gaus3_Sigma_Scaled,Norm_D0M_Sig_Gaus3_alpha[1.5,0,6],Norm_D0M_Sig_Gaus3_n[0.5,0,20])")
  #w.factory("SUM::Norm_D0M_Sig(Norm_D0M_Sig_Gaus1_Frac[0.4,0,1]*Norm_D0M_Sig_Gaus1,Norm_D0M_Sig_Gaus3_Frac[0.1,0,1]*Norm_D0M_Sig_Gaus3,Norm_D0M_Sig_Gaus2)")
  w.factory("SUM::Norm_D0M_Sig(Norm_D0M_Sig_Gaus1_Frac[0.4,0,1]*Norm_D0M_Sig_Gaus1,Norm_D0M_Sig_Gaus2)")
  #w.factory("PROD::Norm_D0M_Sig(Norm_D0M_Sig_Sum,Norm_D0M_Range)")

  #  D0_Mass MisId
  #w.factory("RooGaussian::Norm_D0M_MisId_Gaus1(D0_Mass,Norm_D0M_MisId_Gaus_Mean[1790,1720,1820],Norm_D0M_Sig_Gaus1_Sigma)")
  #w.factory("RooGaussian::Norm_D0M_MisId_Gaus2(D0_Mass,Norm_D0M_MisId_Gaus_Mean,Norm_D0M_Sig_Gaus2_Sigma)")
  #w.factory("SUM::Norm_D0M_MisId(Norm_D0M_Sig_Gaus1_Frac*Norm_D0M_MisId_Gaus1,Norm_D0M_MisId_Gaus2)")
  ##w.factory("PROD::Norm_D0M_MisId(Norm_D0M_MisId_Sum,Norm_D0M_Range)")
  ##w.factory("RooExponential::Norm_D0M_MisId_Exp(D0_Mass,Norm_D0M_MisId_Exp_Const[-0.15,-.3,-.1])")
  ##w.factory("PROD::Norm_D0M_MisId(Norm_D0M_MisId_Exp,Norm_D0M_Range)")

  #  D0_Mass Combinatorical
  w.factory('{Norm_D0M_Bkg_Cheby_1[-0.5,-1,1]}')
  #w.factory("RooChebychev::Norm_D0M_Bkg_Poly(D0_Mass,{Norm_D0M_Bkg_Cheby_1[-0.25,-1.5,1]})")
  #w.factory("PROD::Norm_D0M_Bkg(Norm_D0M_Bkg_Poly,Norm_D0M_Range)")
  w.factory("RooExponential::Norm_D0M_Bkg(D0_Mass,Norm_D0M_Bkg_Exp_c[-0.0088,-0.05,-0.001])")
  #w.factory("RooChebychev::Norm_D0M_Bkg(D0_Mass,{Norm_D0M_Bkg_Cheby_1})")
  #w.factory("RooChebychev::Norm_D0M_Bkg(D0_Mass,{Norm_D0M_Bkg_Cheby_1,Norm_D0M_Bkg_Cheby_2[-0.1,-0.7,1]})")

  
  w.factory("RooFormulaVar::Norm_DelM_Sig_Gaus_Mean_Shifted('Norm_DelM_Sig_Gaus_Mean+Norm_DelM_Sig_Gaus_Mean_Shift',{Norm_DelM_Sig_Gaus_Mean[145.5,145,146],Norm_DelM_Sig_Gaus_Mean_Shift[0]})")
  w.factory("RooFormulaVar::Norm_DelM_Sig_Gaus3_Mean_Shifted('Norm_DelM_Sig_Gaus3_Mean+Norm_DelM_Sig_Gaus_Mean_Shift',{Norm_DelM_Sig_Gaus3_Mean[145.7,144,155],Norm_DelM_Sig_Gaus_Mean_Shift})")

  w.factory("RooFormulaVar::Norm_DelM_Sig_Gaus2_Sigma('Norm_DelM_Sig_Gaus1_Sigma+Norm_DelM_Sig_Gaus2_Sigma_Diff',{Norm_DelM_Sig_Gaus1_Sigma[.4,0,1],Norm_DelM_Sig_Gaus2_Sigma_Diff[0.4,0.,1.]})")
  w.factory("RooFormulaVar::Norm_DelM_Sig_Gaus3_Sigma('Norm_DelM_Sig_Gaus1_Sigma+Norm_DelM_Sig_Gaus2_Sigma_Diff+Norm_DelM_Sig_Gaus3_Sigma_Diff',{Norm_DelM_Sig_Gaus1_Sigma,Norm_DelM_Sig_Gaus2_Sigma_Diff,Norm_DelM_Sig_Gaus3_Sigma_Diff[0.4,0.,3.]})")

  #  Del_Mass signal
  w.factory("{Norm_DelM_Sig_Gaus3_Frac[0.01,0,.7]}")
  #w.factory("RooCBShape::Norm_DelM_Sig_Gaus1(Del_Mass,Norm_DelM_Sig_Gaus_Mean_Shifted,Norm_DelM_Sig_Gaus1_Sigma[.4,0,1],Norm_DelM_Sig_CB1_alpha[1.5,0,6], BDT%(n)i_D0M_Sig_CB1_n[2,0,10] )")
  w.factory("RooGaussian::Norm_DelM_Sig_Gaus1(Del_Mass,Norm_DelM_Sig_Gaus_Mean_Shifted,Norm_DelM_Sig_Gaus1_Sigma)")
  w.factory("RooGaussian::Norm_DelM_Sig_Gaus2(Del_Mass,Norm_DelM_Sig_Gaus_Mean_Shifted,Norm_DelM_Sig_Gaus2_Sigma)")
  w.factory("RooGaussian::Norm_DelM_Sig_Gaus3(Del_Mass,Norm_DelM_Sig_Gaus3_Mean_Shifted,Norm_DelM_Sig_Gaus3_Sigma)")
  w.factory("SUM::Norm_DelM_Sig(Norm_DelM_Sig_Gaus1_Frac[0.1,0,.7]*Norm_DelM_Sig_Gaus1,Norm_DelM_Sig_Gaus3_Frac*Norm_DelM_Sig_Gaus3,Norm_DelM_Sig_Gaus2)")
  #w.factory("SUM::Norm_DelM_Sig(Norm_DelM_Sig_Gaus1_Frac[0.1,0,.7]*Norm_DelM_Sig_Gaus1,Norm_DelM_Sig_Gaus2)")
  
  # mis recod
  w.factory("RooGaussian::Norm_DelM_MisRecod_Gaus1(Del_Mass,Norm_DelM_MisRecod_Gaus_Mean[145.5,145,146],Norm_DelM_MisRecod_Gaus_Sigma1[1.2,0,5] )")


  w.factory("RooChebychev::Norm_D0M_MisRecod(D0_Mass,{Norm_D0M_MisRecod_Cheby_1[0,-1,1]})")

  #  Del_Mass Combinatorical
  #w.factory("RooDstD0BG::Norm_DelM_Bkg(Del_Mass,Norm_DelM_Bkg_m0[139.5,137.5,140.5],Norm_DelM_Bkg_c[40,7,350],Norm_DelM_Bkg_a[-20,-100,-1],Norm_DelM_Bkg_b[0.4,-1,2])")
  w.factory("RooDstD0BG::Norm_DelM_Bkg(Del_Mass,Norm_DelM_Bkg_m0[139.5,137.5,140.5],Norm_DelM_Bkg_m0,Norm_DelM_Bkg_a[-20,-100,-1],Norm_DelM_Bkg_b[0.4,-1,2])")
  w.factory("{Norm_DelM_Bkg_c[40,7,350]}")

  #  Del_Mass signal
  w.factory("RooGaussian::Norm_DelM_MisId(Del_Mass,Norm_DelM_Sig_Gaus_Mean,Norm_DelM_MisId_Gaus_Sigma1[1,0,3])")

  w.factory("PROD::Norm_Sig(Norm_DelM_Sig,Norm_D0M_Sig)")
  w.factory("PROD::Norm_Comb(Norm_DelM_Bkg,Norm_D0M_Bkg)")
  w.factory("PROD::Norm_MisRecod(Norm_DelM_MisRecod_Gaus1,Norm_D0M_MisRecod)")
  #w.factory("PROD::Norm_MisId(Norm_DelM_MisId,Norm_D0M_MisId)")
  #w.factory("PROD::Norm_MisId(Norm_DelM_Sig,Norm_D0M_MisId)")
  #w.factory("PROD::Norm_MisId_Prompt(Norm_DelM_Bkg,Norm_D0M_MisId)")
  w.factory("PROD::Norm_Prompt(Norm_DelM_Bkg,Norm_D0M_Sig)")

  w.factory("{Norm_N_Sig[65000,20000,500000],Norm_N_MisId[1300,100,3000],Norm_N_MisRecod[5000,100,30000],Norm_N_MisId_Prompt[500,10,1000]}")


  # --- eMu ---

  #w.factory("EMu_N_Sig[1000,0,100000]")
  for n in (1,2,3):
    w.factory("BDT%(n)i_Sig_Eff[0.3,0,1]"%({"n":n}))

  w.factory("EMu_Eff[%f]"%(config['emuEff']))
  w.factory("EMu_BR[1e-8,-1e-7,1e-7]")

  if config['norm'] is 'pipi':
    w.factory("Norm_Eff[%f]"%(config['pipiEff']))
    w.factory("Norm_BR[%f]"%(config['pipiBR'][0]))
    w.obj("Norm_BR").setError(config['pipiBR'][1])
  elif config['norm'] is 'kpi':
    w.factory("Norm_Eff[%f]"%(config['kpiEff']))
    w.factory("Norm_BR[%f]"%(config['kpiBR'][0]))
    w.obj("Norm_BR").setError(config['kpiBR'][1])

    w.factory("RooFormulaVar::N_PiPi('Norm_N_Sig*(%f)',{Norm_N_Sig})"%(config['pipiAsEmuEff']*config['pipiBR'][0]/config['kpiBR'][0]/config['kpiEff'],))

  w.factory("RooFormulaVar::EMu_N_Sig('abs(Norm_N_Sig*((EMu_BR*EMu_Eff)/(Norm_BR*Norm_Eff)))',{Norm_BR,EMu_BR,EMu_Eff,Norm_Eff,Norm_N_Sig})")

  w.factory("{EMu_D0M_Min[1815],EMu_D0M_Max[1915]}")

  w.factory("RooGaussian::Norm_Constraint(Norm_N_Sig,%f,%f)"%(config["normEvents"][0],config["normEvents"][1]))

  #  D0_Mass Combinatorical
  w.factory("RooGenericPdf::BDT_D0M_Blind('(D0_Mass<1700||D0_Mass>1900)',{D0_Mass})")
  w.factory("RooGenericPdf::BDT_D0M_Range('(D0_Mass>EMu_D0M_Min&&D0_Mass<EMu_D0M_Max)',{D0_Mass,EMu_D0M_Min,EMu_D0M_Max})")
  w.factory("RooChebychev::BDT_D0M_Bkg(D0_Mass,{BDT_D0M_Bkg_Cheby_1[-0.7,-3.0,0.0],BDT_D0M_Bkg_Cheby_2[-0.2,-3.0,0.0]})")
  w.factory("PROD::BDT_D0M_Bkg_Blind(BDT_D0M_Bkg,BDT_D0M_Blind)")

  #  Del_Mass Combinatorical
  w.factory("RooDstD0BG::BDT_DelM_Bkg(Del_Mass,BDT_DelM_Bkg_m0[139.5,137.5,140.5],BDT_DelM_Bkg_c[40,7,350],BDT_DelM_Bkg_a[-20,-100,-1],BDT_DelM_Bkg_b[-0.1,-2,1])"%({"n":n}))

  w.factory("{BDT_D0M_Sig_CB1_alphaleft[0.3,0,1]}")
  w.factory("{BDT_D0M_Sig_CB2_alpharight[-0.5,-5,0]}")
  for n in (1,2,3):
    if n is not 3:
      w.factory("RooFormulaVar::BDT%(n)i_N_Sig('EMu_N_Sig*BDT%(n)i_Sig_Eff',{EMu_N_Sig,BDT%(n)i_Sig_Eff})"%({"n":n}))
    else:
      w.factory("RooFormulaVar::BDT%(n)i_N_Sig('EMu_N_Sig*(1-(BDT1_Sig_Eff+BDT2_Sig_Eff))',{EMu_N_Sig,BDT1_Sig_Eff,BDT2_Sig_Eff})"%({"n":n}))

    #  D0_Mass Signal
    w.factory("{BDT%(n)i_D0M_Sig_CB2_alpharight[-0.5,-5,0],BDT%(n)i_D0M_Sig_CB1_alphaleft[0.3,0,1]}"%({"n":n}))
    
    w.factory("RooCBShape:BDT%(n)i_D0M_Sig_CB1(D0_Mass, BDT%(n)i_D0M_Sig_CB_Mean[1850,1750,1900], BDT%(n)i_D0M_Sig_CB1_Sigma[10,1,30], BDT_D0M_Sig_CB1_alphaleft, BDT%(n)i_D0M_Sig_CB1_n[2,0,10])"%({"n":n}))
    w.factory("RooCBShape:BDT%(n)i_D0M_Sig_CB2(D0_Mass, BDT%(n)i_D0M_Sig_CB_Mean, BDT%(n)i_D0M_Sig_CB2_Sigma[3,1,30], BDT_D0M_Sig_CB2_alpharight, BDT%(n)i_D0M_Sig_CB2_n[5,0,50])"%({"n":n}))
    w.factory("SUM::BDT%(n)i_D0M_Sig(BDT%(n)i_D0M_Sig_CB1_Frac[0.8,0,1]*BDT%(n)i_D0M_Sig_CB1,BDT%(n)i_D0M_Sig_CB2)"%({"n":n}))

    #  Del_Mass signal
    w.factory("{BDT%(n)i_DelM_Sig_Gaus1_Frac[0.75,0,1]}"%({"n":n}))
    w.factory("RooGaussian::BDT%(n)i_DelM_Sig_Gaus1(Del_Mass,BDT%(n)i_DelM_Sig_Gaus_Mean[145.5,143,148],BDT%(n)i_DelM_Sig_Gaus_Sigma1[1,0,5] )"%({"n":n}))
    w.factory("RooGaussian::BDT%(n)i_DelM_Sig_Gaus2(Del_Mass,BDT%(n)i_DelM_Sig_Gaus_Mean,BDT%(n)i_DelM_Sig_Gaus_Sigma2[.1,0,2] )"%({"n":n}))
    #w.factory("{BDT%(n)i_DelM_Sig_Gaus3_Frac[0.05,0,0.1],BDT%(n)i_DelM_Sig_Gaus_Mean_2[148,143,152],BDT%(n)i_DelM_Sig_Gaus_Sigma3[10,0,20]}"%({"n":n}))
    w.factory("RooGaussian::BDT%(n)i_DelM_Sig_Gaus3(Del_Mass,BDT%(n)i_DelM_Sig_Gaus_Mean_3[148,143,152],BDT%(n)i_DelM_Sig_Gaus_Sigma3[10,0,20] )"%({"n":n}))
    w.factory("SUM::BDT%(n)i_DelM_Sig(BDT%(n)i_DelM_Sig_Gaus3_Frac[0.05,0,0.1]*BDT%(n)i_DelM_Sig_Gaus3,BDT%(n)i_DelM_Sig_Gaus2_Frac[0.2,0,1]*BDT%(n)i_DelM_Sig_Gaus2,BDT%(n)i_DelM_Sig_Gaus1)"%({"n":n}))
    #w.factory("SUM::BDT%(n)i_DelM_Sig(BDT%(n)i_DelM_Sig_Gaus2_Frac[0.2,0,1]*BDT%(n)i_DelM_Sig_Gaus2,BDT%(n)i_DelM_Sig_Gaus1)"%({"n":n}))

    w.factory("PROD::BDT%(n)i_Sig(BDT%(n)i_DelM_Sig,BDT%(n)i_D0M_Sig)"%({"n":n}))
    w.factory("PROD::BDT%(n)i_Comb_Blind(BDT_DelM_Bkg,BDT_D0M_Bkg_Blind)"%({"n":n}))
    w.factory("PROD::BDT%(n)i_Comb(BDT_DelM_Bkg,BDT_D0M_Bkg)"%({"n":n}))

  w.factory("{BDT1_PiPi_Eff[0.5,0,1],BDT2_PiPi_Eff[0.3,0,1]}")
  w.factory("{BDT_D0M_PiPi_CB2_alpharight[-0.5,-5,0],BDT_D0M_PiPi_CB1_alphaleft[0.8,0,3]}")
  for n in (1,2,3):
    if n is not 3:
      w.factory("RooFormulaVar::BDT%(n)i_N_PiPi('N_PiPi*BDT%(n)i_PiPi_Eff',{N_PiPi,BDT%(n)i_PiPi_Eff})"%({"n":n}))
    else:
      w.factory("RooFormulaVar::BDT%(n)i_N_PiPi('N_PiPi*(1-(BDT1_PiPi_Eff+BDT2_PiPi_Eff))',{N_PiPi,BDT1_PiPi_Eff,BDT2_PiPi_Eff})"%({"n":n}))

    #  D0_Mass PiPi
    w.factory("{BDT%(n)i_D0M_PiPi_CB2_alpharight[-0.5,-5,0],BDT%(n)i_D0M_PiPi_CB1_alphaleft[0.8,0,3]}"%({"n":n}))
    w.factory("RooCBShape:BDT%(n)i_D0M_PiPi_CB1(D0_Mass, BDT%(n)i_D0M_PiPi_CB_Mean[1850,1750,1900], BDT%(n)i_D0M_PiPi_CB1_Sigma[10,1,30], BDT_D0M_PiPi_CB1_alphaleft, BDT%(n)i_D0M_PiPi_CB1_n[2,0,10])"%({"n":n}))
    w.factory("RooCBShape:BDT%(n)i_D0M_PiPi_CB2(D0_Mass, BDT%(n)i_D0M_PiPi_CB_Mean, BDT%(n)i_D0M_PiPi_CB2_Sigma[3,1,30], BDT_D0M_PiPi_CB2_alpharight, BDT%(n)i_D0M_PiPi_CB2_n[5,0,50])"%({"n":n}))
    w.factory("SUM::BDT%(n)i_D0M_PiPi(BDT%(n)i_D0M_PiPi_CB1_Frac[0.8,0,1]*BDT%(n)i_D0M_PiPi_CB1,BDT%(n)i_D0M_PiPi_CB2)"%({"n":n}))

    #  Del_Mass signal
    w.factory("{BDT%(n)i_DelM_PiPi_Gaus1_Frac[0.75,0,1]}"%({"n":n}))
    w.factory("RooGaussian::BDT%(n)i_DelM_PiPi_Gaus1(Del_Mass,BDT%(n)i_DelM_PiPi_Gaus_Mean[145.5,143,148],BDT%(n)i_DelM_PiPi_Gaus_Sigma1[1,0,5] )"%({"n":n}))
    w.factory("RooGaussian::BDT%(n)i_DelM_PiPi_Gaus2(Del_Mass,BDT%(n)i_DelM_PiPi_Gaus_Mean_2[145.5,143,148],BDT%(n)i_DelM_PiPi_Gaus_Sigma2[.1,0,2] )"%({"n":n}))
    #w.factory("{BDT%(n)i_DelM_PiPi_Gaus3_Frac[0.05,0,0.1],BDT%(n)i_DelM_PiPi_Gaus_Mean_2[148,143,152],BDT%(n)i_DelM_PiPi_Gaus_Sigma3[10,0,20]}"%({"n":n}))
    w.factory("RooGaussian::BDT%(n)i_DelM_PiPi_Gaus3(Del_Mass,BDT%(n)i_DelM_PiPi_Gaus_Mean_3[148,143,152],BDT%(n)i_DelM_PiPi_Gaus_Sigma3[10,0,20] )"%({"n":n}))
    w.factory("SUM::BDT%(n)i_DelM_PiPi(BDT%(n)i_DelM_PiPi_Gaus3_Frac[0.05,0,0.1]*BDT%(n)i_DelM_PiPi_Gaus3,BDT%(n)i_DelM_PiPi_Gaus2_Frac[0.2,0,1]*BDT%(n)i_DelM_PiPi_Gaus2,BDT%(n)i_DelM_PiPi_Gaus1)"%({"n":n}))
    #w.factory("SUM::BDT%(n)i_DelM_Sig(BDT%(n)i_DelM_PiPi_Gaus2_Frac[0.2,0,1]*BDT%(n)i_DelM_PiPi_Gaus2,BDT%(n)i_DelM_PiPi_Gaus1)"%({"n":n}))


    w.factory("PROD::BDT%(n)i_PiPi(BDT%(n)i_DelM_PiPi,BDT%(n)i_D0M_PiPi)"%({"n":n}))

    #w.factory("SUM::BDT%(n)i_Final_PDF_Blind(BDT%(n)i_N_Sig*BDT%(n)i_Sig,BDT%(n)i_N_Comb[1000,0,10000]*BDT%(n)i_Comb_Blind)"%({"n":n}))
    #w.factory("SUM::BDT%(n)i_Final_PDF(BDT%(n)i_N_Sig*BDT%(n)i_Sig,BDT%(n)i_N_Comb*BDT%(n)i_Comb)"%({"n":n}))

    w.factory("SUM::BDT%(n)i_Final_PDF_Blind(BDT%(n)i_N_Sig*BDT%(n)i_Sig,BDT%(n)i_N_Comb[1000,0,10000]*BDT%(n)i_Comb_Blind,BDT%(n)i_N_PiPi*BDT%(n)i_PiPi)"%({"n":n}))
    w.factory("SUM::BDT%(n)i_Final_PDF(BDT%(n)i_N_Sig*BDT%(n)i_Sig,BDT%(n)i_N_Comb*BDT%(n)i_Comb,BDT%(n)i_N_PiPi*BDT%(n)i_PiPi)"%({"n":n}))

    w.factory("PROD::BDT%(n)i_Final_PDF_Constrained(BDT%(n)i_Final_PDF,Norm_Constraint)"%({"n":n}))




  #w.obj('Norm_D0M_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('Norm_D0M_Sig_Gaus1_Frac').setMax(1.0)
  #w.obj('Norm_D0M_Sig_Gaus1_Frac').setVal(0.429624062534) ; w.obj('Norm_D0M_Sig_Gaus1_Frac').setError(0.0289511133792)
  #w.obj('Norm_D0M_Sig_Gaus1_Frac').setConstant(False)
  #w.obj('Norm_D0M_Sig_Gaus_Mean').setMin(1850.0) ; w.obj('Norm_D0M_Sig_Gaus_Mean').setMax(1880.0)
  #w.obj('Norm_D0M_Sig_Gaus_Mean').setVal(1867.01515277) ; w.obj('Norm_D0M_Sig_Gaus_Mean').setError(0.0296569841856)
  #w.obj('Norm_D0M_Sig_Gaus_Mean').setConstant(False)
  #w.obj('Norm_D0M_Sig_Gaus1_Sigma').setMin(0.0) ; w.obj('Norm_D0M_Sig_Gaus1_Sigma').setMax(10.0)
  #w.obj('Norm_D0M_Sig_Gaus1_Sigma').setVal(6.92118344347) ; w.obj('Norm_D0M_Sig_Gaus1_Sigma').setError(0.117795059995)
  #w.obj('Norm_D0M_Sig_Gaus1_Sigma').setConstant(False)
  #w.obj('Norm_D0M_Sig_Gaus2_Sigma').setMin(5.0) ; w.obj('Norm_D0M_Sig_Gaus2_Sigma').setMax(20.0)
  #w.obj('Norm_D0M_Sig_Gaus2_Sigma').setVal(10.3140938882) ; w.obj('Norm_D0M_Sig_Gaus2_Sigma').setError(0.117955520203)
  #w.obj('Norm_D0M_Sig_Gaus2_Sigma').setConstant(False)
  #w.obj('Norm_DelM_Bkg_a').setMin(-100.0) ; w.obj('Norm_DelM_Bkg_a').setMax(-1.0)
  #w.obj('Norm_DelM_Bkg_a').setVal(-16.1932460031) ; w.obj('Norm_DelM_Bkg_a').setError(0.43302849663)
  #w.obj('Norm_DelM_Bkg_a').setConstant(False)
  #w.obj('Norm_DelM_Bkg_b').setMin(-0.5) ; w.obj('Norm_DelM_Bkg_b').setMax(2.0)
  #w.obj('Norm_DelM_Bkg_b').setVal(0.178920942238) ; w.obj('Norm_DelM_Bkg_b').setError(0.0376477247211)
  #w.obj('Norm_DelM_Bkg_b').setConstant(False)
  #w.obj('Norm_DelM_Bkg_c').setMin(7.0) ; w.obj('Norm_DelM_Bkg_c').setMax(350.0)
  #w.obj('Norm_DelM_Bkg_c').setVal(36.1602832374) ; w.obj('Norm_DelM_Bkg_c').setError(5.19925002062)
  #w.obj('Norm_DelM_Bkg_c').setConstant(False)
  #w.obj('Norm_DelM_Bkg_m0').setMin(137.5) ; w.obj('Norm_DelM_Bkg_m0').setMax(140.5)
  #w.obj('Norm_DelM_Bkg_m0').setVal(139.316358242) ; w.obj('Norm_DelM_Bkg_m0').setError(5.10021351516e-05)
  #w.obj('Norm_DelM_Bkg_m0').setConstant(False)
  #w.obj('Norm_DelM_Sig_Gaus1_Frac').setMin(0.0) ; w.obj('Norm_DelM_Sig_Gaus1_Frac').setMax(1.)
  #w.obj('Norm_DelM_Sig_Gaus1_Frac').setVal(0.279248861884) ; w.obj('Norm_DelM_Sig_Gaus1_Frac').setError(0.0191547718614)
  #w.obj('Norm_DelM_Sig_Gaus1_Frac').setConstant(False)
  #w.obj('Norm_DelM_Sig_Gaus_Mean').setMin(145.0) ; w.obj('Norm_DelM_Sig_Gaus_Mean').setMax(146.0)
  #w.obj('Norm_DelM_Sig_Gaus_Mean').setVal(145.448069656) ; w.obj('Norm_DelM_Sig_Gaus_Mean').setError(0.00294967951486)
  #w.obj('Norm_DelM_Sig_Gaus_Mean').setConstant(False)
  #w.obj('Norm_DelM_Sig_Gaus1_Sigma').setMin(0.0) ; w.obj('Norm_DelM_Sig_Gaus1_Sigma').setMax(1.0)
  #w.obj('Norm_DelM_Sig_Gaus1_Sigma').setVal(0.429900766218) ; w.obj('Norm_DelM_Sig_Gaus1_Sigma').setError(0.0119155696871)
  #w.obj('Norm_DelM_Sig_Gaus1_Sigma').setConstant(False)
  #w.obj('Norm_DelM_Sig_Gaus2_Sigma').setMin(0.1) ; w.obj('Norm_DelM_Sig_Gaus2_Sigma').setMax(2.0)
  #w.obj('Norm_DelM_Sig_Gaus2_Sigma').setVal(0.827483577936) ; w.obj('Norm_DelM_Sig_Gaus2_Sigma').setError(0.00898522299303)
  #w.obj('Norm_DelM_Sig_Gaus2_Sigma').setConstant(False)




  if config['mode'] == 'mc':
    w.factory("SIMUL::Final_PDF(DataSet,BDT1=BDT1_Sig,BDT2=BDT2_Sig,BDT3=BDT3_Sig)")
    #w.obj("Final_PDF").Print("v")
    #w.obj("BDT1_Sig").Print("v")

  elif config['mode'] == 'mcpipi':
    w.factory("SIMUL::Final_PDF(DataSet,BDT1=BDT1_PiPi,BDT2=BDT2_PiPi,BDT3=BDT3_PiPi)")

  elif config['mode'] == 'datapretoy':
    w.factory("SIMUL::Final_PDF(DataSet,BDT1=BDT1_Comb_Blind,BDT2=BDT2_Comb_Blind,BDT3=BDT3_Comb_Blind)")

  elif config['mode'] == 'toy':
    w.factory("SIMUL::Final_PDF(DataSet,Norm=Norm_Final_PDF,BDT1=BDT1_Final_PDF,BDT2=BDT2_Final_PDF,BDT3=BDT3_Final_PDF)")
    w.factory("SIMUL::Final_PDF_Background(DataSet,Norm=Norm_Final_PDF,BDT1=BDT1_Comb,BDT2=BDT2_Comb,BDT3=BDT3_Comb)")
    w.factory("SIMUL::Final_PDF_Constrained(DataSet,BDT1=BDT1_Final_PDF_Constrained,BDT2=BDT2_Final_PDF_Constrained,BDT3=BDT3_Final_PDF_Constrained)")

  elif config['mode'] == 'mcnorm':
    w.factory("SIMUL::Final_PDF(DataSet,Norm=Norm_Sig)")

  elif config['mode'] == 'norm':
    #w.factory("SUM::Norm_Final_PDF(Norm_N_Sig[65000,20000,110000]*Norm_Sig,Norm_N_Prompt[35000,20000,60000]*Norm_Prompt,Norm_N_Comb[67000,1000,90000]*Norm_Comb,Norm_N_MisId[1300,100,3000]*Norm_MisId,Norm_N_MisId_Prompt[500,10,1000]*Norm_MisId_Prompt)")
    #w.factory("SUM::Norm_Final_PDF(Norm_N_Sig[65000,20000,110000]*Norm_Sig,Norm_N_Prompt[35000,20000,60000]*Norm_Prompt,Norm_N_Comb[67000,1000,90000]*Norm_Comb,Norm_N_MisId[1300,100,3000]*Norm_MisId)")
    #w.factory("SUM::Norm_Final_PDF(Norm_N_Sig[65000,20000,110000]*Norm_Sig,Norm_N_Prompt[35000,20000,60000]*Norm_Prompt,Norm_N_Comb[67000,1000,90000]*Norm_Comb,Norm_N_MisId_Prompt[500,10,1000]*Norm_MisId_Prompt)")
    #w.factory("SUM::Norm_Final_PDF(Norm_N_Sig*Norm_Sig,Norm_N_Prompt[35000,20000,60000]*Norm_Prompt,Norm_N_Comb[67000,1000,90000]*Norm_Comb,Norm_N_MisRecod*Norm_MisRecod)")
    w.factory("SUM::Norm_Final_PDF(Norm_N_Sig*Norm_Sig,Norm_N_Prompt[35000,20000,60000]*Norm_Prompt,Norm_N_Comb[67000,1000,90000]*Norm_Comb)")
    
    w.factory("SIMUL::Final_PDF(DataSet,Norm=Norm_Final_PDF)")

  elif config['mode'] == 'data':
    #w.factory("SUM::Norm_Final_PDF(Norm_N_Sig[65000,20000,110000]*Norm_Sig,Norm_N_Prompt[35000,20000,60000]*Norm_Prompt,Norm_N_Comb[67000,1000,90000]*Norm_Comb,Norm_N_MisId[1300,100,3000]*Norm_MisId,Norm_N_MisId_Prompt[500,10,1000]*Norm_MisId_Prompt)")
    #w.factory("SUM::Norm_Final_PDF(Norm_N_Sig[65000,20000,110000]*Norm_Sig,Norm_N_Prompt[35000,20000,60000]*Norm_Prompt,Norm_N_Comb[67000,1000,90000]*Norm_Comb,Norm_N_MisId[1300,100,3000]*Norm_MisId)")
    #w.factory("SUM::Norm_Final_PDF(Norm_N_Sig[65000,20000,110000]*Norm_Sig,Norm_N_Prompt[35000,20000,60000]*Norm_Prompt,Norm_N_Comb[67000,1000,90000]*Norm_Comb,Norm_N_MisId_Prompt[500,10,1000]*Norm_MisId_Prompt)")
    w.factory("SUM::Norm_Final_PDF(Norm_N_Sig*Norm_Sig,Norm_N_Prompt[35000,20000,60000]*Norm_Prompt,Norm_N_Comb[67000,1000,90000]*Norm_Comb)")
    
    w.factory("SIMUL::Final_PDF(DataSet,Norm=Norm_Final_PDF,BDT1=BDT1_Final_PDF,BDT2=BDT2_Final_PDF,BDT3=BDT3_Final_PDF)")
    w.factory("SIMUL::Final_PDF_Background(DataSet,Norm=Norm_Final_PDF,BDT1=BDT1_Comb,BDT2=BDT2_Comb,BDT3=BDT3_Comb)")
    w.factory("SIMUL::Final_PDF_Constrained(DataSet,BDT1=BDT1_Final_PDF_Constrained,BDT2=BDT2_Final_PDF_Constrained,BDT3=BDT3_Final_PDF_Constrained)")



    w.obj('Norm_N_Comb').setMin(2000.0*config["normScale"]) ; w.obj('Norm_N_Comb').setMax(15000.0*config["normScale"])
    w.obj('Norm_N_Comb').setVal(7850.56516616*config["normScale"]) ; w.obj('Norm_N_Comb').setError(177.821454726/sqrt(config["normScale"]))
    w.obj('Norm_N_MisRecod').setMin(100.0*config["normScale"]) ; w.obj('Norm_N_MisRecod').setMax(40000.0*config["normScale"])
    w.obj('Norm_N_MisRecod').setVal(20316.944222*config["normScale"]) ; w.obj('Norm_N_MisRecod').setError(248.324102117/sqrt(config["normScale"]))
    w.obj('Norm_N_Prompt').setMin(6000.0*config["normScale"]) ; w.obj('Norm_N_Prompt').setMax(60000.0*config["normScale"])
    w.obj('Norm_N_Prompt').setVal(29326.825063*config["normScale"]) ; w.obj('Norm_N_Prompt').setError(247.656992623/sqrt(config["normScale"]))
    w.obj('Norm_N_Sig').setMin(2000.0*config["normScale"]) ; w.obj('Norm_N_Sig').setMax(270000.0*config["normScale"])
    w.obj('Norm_N_Sig').setVal(135370.*config["normScale"]) ; w.obj('Norm_N_Sig').setError(430./sqrt(config["normScale"]))


  if mode_later_than('mcnorm',config['mode']):

    # nll analyse, nlls up to 1610.0 on Thu Jul 31 15:14:35 2014 run on fitResult.norm_kpi_2011_6.0.0.4.root
    #
    # WARNING  derivitive_ratio bottom is zero 169 689.330300 696.763943 696.763943
    # INFO     extrapolate lower edge [False, -0.2368609160806532, 1610.0]
    # INFO     extrapolate upper edge [False, 0.300022797868122, 1610.0]
    w.obj('Norm_D0M_Bkg_Exp_c').setMin(-0.236860916081) ; w.obj('Norm_D0M_Bkg_Exp_c').setMax(0.300022797868) ; w.obj('Norm_D0M_Bkg_Exp_c').setVal(-0.0221074305011) ; w.obj('Norm_D0M_Bkg_Exp_c').setError(0.00127007751403)
    # WARNING  derivitive_ratio bottom is zero 169 5199.217924 5509.102918 5509.102918
    w.obj('Norm_D0M_Sig_Gaus1_Sigma').setMin(5.8) ; w.obj('Norm_D0M_Sig_Gaus1_Sigma').setMax(8.6) ; w.obj('Norm_D0M_Sig_Gaus1_Sigma').setVal(7.2) ; w.obj('Norm_D0M_Sig_Gaus1_Sigma').setError(0.0305815254416)
    # WARNING  derivitive_ratio bottom is zero 119 62.077791 62.077791 62.077791
    # WARNING  Dont want to expand max range 99.112383 too far
    # INFO     extrapolate upper edge [False, 10.5, 1610.0]
    # WARNING  upper edge 10.500000 hits limit 5.000000
    w.obj('Norm_D0M_Sig_Gaus1_alpha').setMin(1.14) ; w.obj('Norm_D0M_Sig_Gaus1_alpha').setMax(5.0) ; w.obj('Norm_D0M_Sig_Gaus1_alpha').setVal(2.298) ; w.obj('Norm_D0M_Sig_Gaus1_alpha').setError(0.0393012987558)
    # WARNING  Dont want to expand max range 899.409174 too far
    # INFO     extrapolate upper edge [False, 35.0, 1610.0]
    # WARNING  upper edge 35.000000 hits limit 20.000000
    w.obj('Norm_D0M_Sig_Gaus1_n').setMin(0.3375) ; w.obj('Norm_D0M_Sig_Gaus1_n').setMax(20.0) ; w.obj('Norm_D0M_Sig_Gaus1_n').setVal(2.30375) ; w.obj('Norm_D0M_Sig_Gaus1_n').setError(0.537418026352)
    # WARNING  derivitive_ratio bottom is zero 127 1374.893616 1418.388895 1418.388895
    # INFO     extrapolate upper edge [False, 10.856461576572277, 1610.0]
    w.obj('Norm_D0M_Sig_Gaus2_Sigma_Diff').setMin(1.25) ; w.obj('Norm_D0M_Sig_Gaus2_Sigma_Diff').setMax(10.8564615766) ; w.obj('Norm_D0M_Sig_Gaus2_Sigma_Diff').setVal(5.09258463063) ; w.obj('Norm_D0M_Sig_Gaus2_Sigma_Diff').setError(0.115261989641)
    # WARNING  derivitive_ratio bottom is zero 100 768.841852 768.841850 768.841850
    # WARNING  derivitive_ratio bottom is zero 101 768.841850 768.841850 768.841850
    # WARNING  derivitive_ratio bottom is zero 102 768.841850 768.841850 768.841850
    # WARNING  derivitive_ratio bottom is zero 103 768.841850 768.841850 768.841850
    # WARNING  derivitive_ratio bottom is zero 104 768.841850 768.841850 768.841850
    # WARNING  derivitive_ratio bottom is zero 105 768.841850 768.841850 768.841850
    # WARNING  derivitive_ratio bottom is zero 106 768.841850 768.841850 768.841850
    # WARNING  derivitive_ratio bottom is zero 107 768.841850 768.841850 768.841850
    # WARNING  derivitive_ratio bottom is zero 108 768.841850 768.841850 768.841850
    # INFO     extrapolate upper edge [False, 10.11481217459233, 1610.0]
    # WARNING  upper edge 10.114812 hits limit 5.000000
    w.obj('Norm_D0M_Sig_Gaus2_alpha').setMin(1.44) ; w.obj('Norm_D0M_Sig_Gaus2_alpha').setMax(5.0) ; w.obj('Norm_D0M_Sig_Gaus2_alpha').setVal(2.152) ; w.obj('Norm_D0M_Sig_Gaus2_alpha').setError(0.0415387821092)
    # WARNING  derivitive_ratio bottom is zero 230 629.750229 630.182190 630.182190
    # INFO     extrapolate lower edge [False, -0.9760496583225814, 1610.0]
    # WARNING  Dont want to expand max range 50.491612 too far
    # INFO     extrapolate upper edge [False, 35.0, 1610.0]
    # WARNING  lower edge -0.976050 hits limit 0.000000
    # WARNING  upper edge 35.000000 hits limit 20.000000
    w.obj('Norm_D0M_Sig_Gaus2_n').setMin(0.0) ; w.obj('Norm_D0M_Sig_Gaus2_n').setMax(20.0) ; w.obj('Norm_D0M_Sig_Gaus2_n').setVal(1.0) ; w.obj('Norm_D0M_Sig_Gaus2_n').setError(0.0563707589481)
    # WARNING  derivitive_ratio bottom is zero 102 100475.575388 104489.200281 104489.200281
    w.obj('Norm_D0M_Sig_Gaus_Mean').setMin(1864.1) ; w.obj('Norm_D0M_Sig_Gaus_Mean').setMax(1868.6) ; w.obj('Norm_D0M_Sig_Gaus_Mean').setVal(1866.35) ; w.obj('Norm_D0M_Sig_Gaus_Mean').setError(0.0282504176865)
    # WARNING  derivitive_ratio bottom is zero 102 950.574510 1090.331482 1090.331482
    # INFO     extrapolate upper edge [False, 8.675242367234118, 1610.0]
    w.obj('Norm_DelM_Bkg_a').setMin(-30.7) ; w.obj('Norm_DelM_Bkg_a').setMax(8.67524236723) ; w.obj('Norm_DelM_Bkg_a').setVal(-14.9499030531) ; w.obj('Norm_DelM_Bkg_a').setError(0.352110679985)
    # WARNING  derivitive_ratio bottom is zero 286 2509.484557 2524.607389 2524.607389
    # INFO     extrapolate lower edge [False, 135.51700895240305, 1610.0]
    w.obj('Norm_DelM_Bkg_m0').setMin(135.517008952) ; w.obj('Norm_DelM_Bkg_m0').setMax(140.245) ; w.obj('Norm_DelM_Bkg_m0').setVal(139.29940179) ; w.obj('Norm_DelM_Bkg_m0').setError(0.00278162353152)
    # WARNING  derivitive_ratio bottom is zero 168 12637.921551 12941.900194 12941.900194
    w.obj('Norm_DelM_Sig_Gaus1_Sigma').setMin(0.275) ; w.obj('Norm_DelM_Sig_Gaus1_Sigma').setMax(0.58) ; w.obj('Norm_DelM_Sig_Gaus1_Sigma').setVal(0.4275) ; w.obj('Norm_DelM_Sig_Gaus1_Sigma').setError(0.00623690681335)
    # WARNING  derivitive_ratio bottom is zero 140 7646.478871 7794.222379 7794.222379
    w.obj('Norm_DelM_Sig_Gaus2_Sigma_Diff').setMin(0.145) ; w.obj('Norm_DelM_Sig_Gaus2_Sigma_Diff').setMax(0.56) ; w.obj('Norm_DelM_Sig_Gaus2_Sigma_Diff').setVal(0.311) ; w.obj('Norm_DelM_Sig_Gaus2_Sigma_Diff').setError(0.00961908230633)
    # WARNING  derivitive_ratio bottom is zero 135 7889.258317 7968.149060 7968.149060
    w.obj('Norm_DelM_Sig_Gaus3_Mean').setMin(144.385) ; w.obj('Norm_DelM_Sig_Gaus3_Mean').setMax(147.52) ; w.obj('Norm_DelM_Sig_Gaus3_Mean').setVal(145.9525) ; w.obj('Norm_DelM_Sig_Gaus3_Mean').setError(0.0297743321414)
    # WARNING  derivitive_ratio bottom is zero 127 1441.937761 1456.115731 1456.115731
    # INFO     extrapolate lower edge [False, -1.562458158266192, 1610.0]
    # INFO     extrapolate upper edge [False, 3.2886360831918586, 1610.0]
    # WARNING  lower edge -1.562458 hits limit 0.000000
    w.obj('Norm_DelM_Sig_Gaus3_Sigma_Diff').setMin(0.0) ; w.obj('Norm_DelM_Sig_Gaus3_Sigma_Diff').setMax(3.28863608319) ; w.obj('Norm_DelM_Sig_Gaus3_Sigma_Diff').setVal(0.657727216638) ; w.obj('Norm_DelM_Sig_Gaus3_Sigma_Diff').setError(0.037812360311)
    # WARNING  derivitive_ratio bottom is zero 102 17487.965272 18067.587218 18067.587218
    w.obj('Norm_DelM_Sig_Gaus_Mean').setMin(145.25) ; w.obj('Norm_DelM_Sig_Gaus_Mean').setMax(145.6) ; w.obj('Norm_DelM_Sig_Gaus_Mean').setVal(145.425) ; w.obj('Norm_DelM_Sig_Gaus_Mean').setError(0.00389207378424)
    # WARNING  derivitive_ratio bottom is zero 171 1440.310455 1466.512994 1466.512994
    # INFO     extrapolate lower edge [False, -1161.7298062300902, 1610.0]
    # INFO     extrapolate upper edge [False, 6502.909990291508, 1610.0]
    # WARNING  lower edge -1161.729806 hits limit 0.000000
    w.obj('Norm_N_Comb').setMin(0.0*config["normScale"]) ; w.obj('Norm_N_Comb').setMax(6502.90999029*config["normScale"]) ; w.obj('Norm_N_Comb').setVal(1300.58199806*config["normScale"]) ; w.obj('Norm_N_Comb').setError(69.7188799676/sqrt(config["normScale"]))
    # WARNING  derivitive_ratio bottom is zero 142 1629.344232 1679.974917 1679.974917
    # INFO     extrapolate lower edge [False, 10931.649121116747, 1610.0]
    w.obj('Norm_N_Prompt').setMin(10931.6491211*config["normScale"]) ; w.obj('Norm_N_Prompt').setMax(30995.7616494*config["normScale"]) ; w.obj('Norm_N_Prompt').setVal(18957.2941324*config["normScale"]) ; w.obj('Norm_N_Prompt').setError(247.513270145/sqrt(config["normScale"]))
    # WARNING  derivitive_ratio bottom is zero 148 1585.358526 1642.672043 1642.672043
    # INFO     extrapolate lower edge [False, 64907.007351854576, 1610.0]
    w.obj('Norm_N_Sig').setMin(64907.0073519*config["normScale"]) ; w.obj('Norm_N_Sig').setMax(99148.5248*config["normScale"]) ; w.obj('Norm_N_Sig').setVal(82027.7660759*config["normScale"]) ; w.obj('Norm_N_Sig').setError(349.170253164/sqrt(config["normScale"]))



    #w.obj('Norm_DelM_Bkg_b').setVal(0)
    #w.obj('Norm_DelM_Bkg_b').setConstant(True)

    w.obj('Norm_D0M_Sig_Gaus1_Frac').setVal(0.7)
    #w.obj('Norm_D0M_Sig_Gaus3_Frac').setVal(0.35)
    w.obj('Norm_DelM_Sig_Gaus1_Frac').setVal(0.25)
    w.obj('Norm_DelM_Sig_Gaus3_Frac').setVal(0.15)

    w.obj('Norm_D0M_Sig_Gaus1_Frac').setConstant(True)
    #w.obj('Norm_D0M_Sig_Gaus3_Frac').setConstant(True)
    w.obj('Norm_DelM_Sig_Gaus1_Frac').setConstant(True)
    w.obj('Norm_DelM_Sig_Gaus3_Frac').setConstant(True)



  config['postHook'](w)
  return w



