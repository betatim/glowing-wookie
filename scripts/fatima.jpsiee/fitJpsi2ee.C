#include "fitMass.h"

void fitMass::fitJpsi2ee(TTree* useChain,  int startIT, int endIT){

  using namespace RooFit;
  
  std::cout<<"Executing function fitMethod2()"<<std::endl;

  can = new TCanvas("can","can", 1400, 1200); 
  can1 = new TCanvas("can1","can1", 1400, 1200); 
  if(! myDebug){
    can->Divide(3,2);
    can1->Divide(3,2);  
  }
  
  double nSig, nSigErr, nBg, nBgErr, inWindow_S, inWindow_SErr, inWindow_B, inWindow_BErr, correlation, fitChi, fitChiProb;
  double nSigisMu, nSigErrisMu, nBgisMu, nBgErrisMu, inWindow_SisMu, inWindow_SErrisMu, inWindow_BisMu, inWindow_BErrisMu, correlationisMu;
  double x_sigma, x_sigmaErr, x_sigma1b, x_sigma1bErr, x_sigma2, x_sigma2Err, x_frac, x_fracErr,  x_bkgc1, x_bkgc1Err, fitChiisMu, fitChiProbisMu;
  double x_sigmaisMu, x_sigmaErrisMu, x_sigma1bisMu, x_sigma1bErrisMu, x_sigma2isMu, x_sigma2ErrisMu, x_fracisMu, x_fracErrisMu,  x_bkgc1isMu, x_bkgc1ErrisMu;
  double sigEff, sigEffErr;
  double entries, entriesall, entriesisMu;
  
  TTree *writeTree = new TTree ("writeTree", "writeTree");
  writeTree->Branch("nSig",    &nSig,   "nSig/D");
  writeTree->Branch("nSigErr", &nSigErr,"nSigErr/D");
  writeTree->Branch("fSiginWindow",    &inWindow_S,    "fSiginWindow/D");
  writeTree->Branch("fSiginWindowErr", &inWindow_SErr, "fSiginWindowErr/D");
  writeTree->Branch("nBg",    &nBg,   "nBg/D");
  writeTree->Branch("nBgErr", &nBgErr,"nBgErr/D");
  writeTree->Branch("fBginWindow",    &inWindow_B,    "fBginWindow/D");
  writeTree->Branch("fBginWindowErr", &inWindow_BErr, "fBginWindowErr/D");  
  writeTree->Branch("correlation", &correlation,"correlation/D");
  writeTree->Branch("fitChi", &fitChi,"fitChi/D");   
  writeTree->Branch("sigma", &x_sigma,"sigma/D");
  writeTree->Branch("sigmaErr", &x_sigmaErr,"sigmaErr/D");
  writeTree->Branch("sigma1b",    &x_sigma1b,   "sigma1b/D");
  writeTree->Branch("sigma1bErr", &x_sigma1bErr,"sigma1bErr/D");
  writeTree->Branch("sigma2", &x_sigma2,"sigma2/D"); 
  writeTree->Branch("sigma2Err", &x_sigma2Err,"sigma2Err/D");
  writeTree->Branch("bkgc1", &x_bkgc1,"bkgc1/D");  
  writeTree->Branch("bkgc1Err", &x_bkgc1Err,"bkgc1Err/D");  
  writeTree->Branch("frac", &x_frac,"frac/D");  
  writeTree->Branch("fracErr", &x_fracErr,"fracErr/D");  
  writeTree->Branch("entries", &entriesall,"entries/D"); 
  
  writeTree->Branch("nSigisMu", &nSigisMu,"nSigisMu/D");
  writeTree->Branch("nSigErrisMu", &nSigErrisMu,"nSigErrisMu/D");
  writeTree->Branch("fSiginWindowisMu",    &inWindow_SisMu,    "fSiginWindowisMu/D");
  writeTree->Branch("fSiginWindowErrisMu", &inWindow_SErrisMu, "fSiginWindowErrisMu/D");
  writeTree->Branch("nBgisMu", &nBgisMu, "nBgisMu/D");
  writeTree->Branch("nBgErrisMu", &nBgErrisMu,"nBgErrisMu/D");
  writeTree->Branch("fBginWindowisMu",    &inWindow_BisMu,    "fBginWindowisMu/D");
  writeTree->Branch("fBginWindowErrisMu", &inWindow_BErrisMu, "fBginWindowErrisMu/D");
  writeTree->Branch("correlationisMu", &correlationisMu,"correlationisMu/D");
  writeTree->Branch("fitChiisMu", &fitChiisMu,"fitChiisMu/D");   
  writeTree->Branch("sigmaisMu",    &x_sigmaisMu,   "sigmaisMu/D");
  writeTree->Branch("sigmaErrisMu", &x_sigmaErrisMu,"sigmaErrisMu/D");
  writeTree->Branch("sigma1bisMu",    &x_sigma1bisMu,   "sigma1bisMu/D");
  writeTree->Branch("sigma1bErrisMu", &x_sigma1bErrisMu,"sigma1bErrisMu/D");
  writeTree->Branch("sigma2isMu",    &x_sigma2isMu,   "sigma2isMu/D"); 
  writeTree->Branch("sigma2ErrisMu", &x_sigma2ErrisMu,"sigma2Err/D");
  writeTree->Branch("bkgc1isMu",    &x_bkgc1isMu,   "bkgc1isMu/D");  
  writeTree->Branch("bkgc1ErrisMu", &x_bkgc1ErrisMu,"bkgc1ErrisMu/D");  
  writeTree->Branch("fracisMu",    &x_fracisMu,    "fracisMu/D");  
  writeTree->Branch("fracErrisMu", &x_fracErrisMu, "fracErrisMu/D"); 
  writeTree->Branch("entriesisMu", &entriesisMu,"entriesisMu/D");  
  
  writeTree->Branch("sigEff", &sigEff,"sigEff/D");   
  writeTree->Branch("sigEffErr", &sigEffErr,"sigEffErr/D");  
 
  
  char tt[100];
  //double thecoeff[11];
  
  for(int i = startIT; i<endIT; i++){
    
    sprintf(tt,"P%i",i);
    myCut = baseCut+" && "+(momentumCutJpsi(i)); 
    
    for(int j=0; j<2; j++){
      
      if(j==0) myCut = baseCut+" && "+(momentumCutJpsi(i));
      if(j==1) myCut = baseCut+" && "+(momentumCutJpsi(i))+" && "+daughter+muonCut+testCut;
      
      entries = useChain->GetEntries(myCut);
      
      if(j==0) if (myDebug) can->cd(); else  can->cd(i+1);
      if(j==1) if (myDebug) can1->cd(); else can1->cd(i+1);
      
      int minEntries =  10;  if (j==0) minEntries = 50;
      entries = useChain->GetEntries(myCut) ;
      std::cout<<j<<") In momentum bin "<<i<< "  --> entries after cut: "<<myCut<<" are "<<entries<<std::endl;
      
      if (entries>minEntries){
	gROOT->cd(); TTree *tc = useChain->CopyTree(myCut); 
	std::cout<<"inside minentries "<<std::endl;
	if(j==1) entriesisMu = entries;
	if(j==0) entriesall  = entries;
	
	//double min_x = 2200.; double max_x  = 4000.;
	int nDegrees = 0;
	double sigMin = 40.0; double sigMax = 250.0;
	
	TH1F *checkingHist = new TH1F("checkingHist", "checkingHist", bins, mLow, mHigh) ;//min_x, max_x);
	tc->Draw(mother+"_MM>>checkingHist");
	
	RooRealVar J_psi_1S_MM("J_psi_1S_MM", "J_psi_1S_MM", mLow, mHigh); //min_x, max_x);  
	RooPlot *frame = J_psi_1S_MM.frame(mLow, mHigh, bins);
	frame->GetXaxis()->SetTitle("m(ee) (MeV/c^{2})");
		
	// ======== Jpsi Mass  ====== //
	RooRealVar mean("#mu_{1}", "mean", meanVal[0], meanVal[1] , meanVal[2]); // 3096., 3000., 3200.);
	RooRealVar sigma1("#sigma_{1}", "sigma1", 40,  sigMin , sigMax);
	RooRealVar n  ("n", "n",  1.); //, -10., 20.);  nDegrees+=1;
	RooRealVar alpha  ("alpha", "alpha", 1.5, -5,5);
	RooCBShape fn ("fn","fn", J_psi_1S_MM, mean, sigma1, alpha, n);

	RooRealVar mean_b("#mu_{1b}", "mean_b", meanVal[0], meanVal[1] , meanVal[2]); //mean.getVal(), 0.95*mean.getVal(), 1.05*mean.getVal());  nDegrees+=1;
	RooRealVar sigma1b("#sigma_{1b}", "sigma1b",  50, sigma1.getVal(), 5*sigma1.getVal()) ;// sigMin , sigMax);
	RooRealVar nb  ("nb", "nb",  1.); //, -10., 20);  nDegrees+=1;
	RooRealVar alphab  ("alphab", "alphab", 1.5, -5, 5);
	RooCBShape fn_b ("fn_b","fn_b", J_psi_1S_MM, mean, sigma1b, alphab, nb);  nDegrees+=1;
	
	RooRealVar fracCore ("fracCore","fracCore", 0.6,  0.,  1.0  );
	RooAddPdf JpsiMass("JpsiMass","JpsiMass", RooArgList(fn, fn_b), fracCore);
	
	// ======== Psi2S Mass  ====== //
	RooRealVar meanPsi2S("#mu gauss", "meanPsi2S", 3686., 3600., 3750); nDegrees+=1; //  mean.getVal()+589.193); // 

	RooRealVar sigPsi2S("#sigma_{2}", "sigPsi2S", 50, sigMin ,sigMax);
	RooRealVar alpha_psi_1  ("alpha_psi_1", "alpha_psi_1", 1.5, -5, 5);
	RooCBShape sigPsi2S_1 ("sigPsi2S_1","sigPsi2S_1", J_psi_1S_MM, meanPsi2S, sigPsi2S, alpha_psi_1, n);

	RooRealVar alpha_psi_2  ("alpha_psi_2", "alpha_psi_2", 1.5, -5, 5);
	RooCBShape sigPsi2S_2 ("sigPsi2S_2","sigPsi2S_2", J_psi_1S_MM, meanPsi2S, sigPsi2S, alpha_psi_2, n);
	RooRealVar fracPsi2S ("fracPsi2S","fracPsi2S", 0.6,  0.,  1.0  );
	RooAddPdf Psi2SMass("Psi2SMass","Psi2SMass", RooArgList(sigPsi2S_1, sigPsi2S_2), fracPsi2S);
	//	RooGaussModel gauss("gauss","gauss", J_psi_1S_MM, meanPsi2S, sigPsi2S);
	
	// ======== Background   ====== //
	RooRealVar v1("Bg exp","v1", 0.01, -10, 10);
	RooExponential bkg("bkg", "bkg", J_psi_1S_MM, v1);
	
	// ======== Prepare total model  ====== //
	RooRealVar nsig1("nsig1", "nsig1", entries*0.7, entries*0.2, entries);
	RooRealVar nsig2("nsig2", "nsig2", entries*0.05, entries*0.01, 0.4*entries);
	RooRealVar nbkg("nbkg", "nbkg", entries*0.2, entries*0.001, 0.6*entries);
	
	RooExtendPdf *e_gm1   = new RooExtendPdf("e_gm1","e_gm1", Psi2SMass, nsig2);
	RooExtendPdf *e_bk1   = new RooExtendPdf("e_bk1","e_bk1", bkg, nbkg);
	RooExtendPdf *e_mass  = new RooExtendPdf("e_mass","e_mass", JpsiMass, nsig1);
	
	RooAddPdf model("model","model", RooArgList(*e_mass, *e_gm1, *e_bk1));
	std::cout<<"prepared model, reditecting output"<<std::endl;
	
	RooArgSet * obs = new RooArgSet("observables"); obs->add(J_psi_1S_MM);
	J_psi_1S_MM.setBins(bins);
	RooDataSet *hist = new RooDataSet("hist", "hist", *obs, Import(*tc));
	RooDataHist *h_data = new RooDataHist("h_data", "h_data", RooArgSet(J_psi_1S_MM), *hist, 1.0);
	h_data->plotOn(frame);
	
	gSystem->RedirectOutput("logTemp.txt");
	//model.fitTo(*h_data, RooFit::Range(mLow, mHigh ), RooFit::Extended(), RooFit::Save(true));
	RooFitResult* res = model.fitTo(*h_data, RooFit::Range(fitRanges[0], fitRanges[1]), RooFit::Extended(), RooFit::Save(true) );
	
	model.plotOn(frame); 
	model.plotOn(frame, RooFit::Components(*e_gm1), LineStyle(kDashed), LineColor(23));  nDegrees+=5;
	model.plotOn(frame, RooFit::Components(*e_bk1), LineStyle(kDashed), LineColor(kRed));     nDegrees+=2;
	model.plotOn(frame, RooFit::Components(*e_mass), LineColor(22));                       nDegrees+=6;
	model.plotOn(frame, RooFit::Components(fn), LineStyle(kDashed), LineColor(kGreen)); 
	model.plotOn(frame, RooFit::Components(fn_b), LineStyle(kDashed), LineColor(kOrange));
	
	gSystem->RedirectOutput(0);
	

	// --------------//
	// extract yields 
	// --------------//
	
	double mySigma = sigma1.getVal();
	if(true){
	  mySigma = sigma1.getVal()*fracCore.getVal() + sigma1b.getVal()*(1-fracCore.getVal());
	  std::cout<<"wted mean of sigmas: "<<sigma1.getVal()<<"*"<<fracCore.getVal()<<" + "<<sigma1b.getVal()<<"*"<<(1-fracCore.getVal())<<" = "<<mySigma<<std::endl;;
	}

	double fitLow  = mean.getVal() - mySigma;
	double fitHi   = mean.getVal() + mySigma;

	std::cout<<"sigma is "<<mySigma<<" and mass window (1Sigma) is being set to [ "<<fitLow<<", "<< fitHi<< "]" <<std::endl;
	J_psi_1S_MM.setRange( "integralRange", fitLow, fitHi );
	
	RooAbsReal *integral = e_mass->createIntegral(J_psi_1S_MM, RooFit::NormSet(J_psi_1S_MM), RooFit::Range("integralRange") );
	double sigInWindow = integral->getVal();  // gives the fraction of the function in that range
	double sigInWindowErr = integral->getPropagatedError(*res); 
	
	integral = e_bk1->createIntegral(J_psi_1S_MM, RooFit::NormSet(J_psi_1S_MM), RooFit::Range("integralRange") );
	double bkgInWindow = integral->getVal();
	double bkgInWindowErr = integral->getPropagatedError(*res);
	
	std::cout<<"Total pdf inside signal window is "<<(model.createIntegral(J_psi_1S_MM, RooFit::NormSet(J_psi_1S_MM), RooFit::Range("integralRange") ))->getVal();
 	std::cout<<" --> signal: "<< sigInWindow<<" +/- "<<sigInWindowErr<< " of bkg "<< bkgInWindow <<" +/- "<<bkgInWindowErr << std::endl; 


	// --------------------------------------- //
	// calcuated chi2 andn make residual graph //
	// --------------------------------------- //
	
	double bin_width = checkingHist->GetBinWidth(1);
	double myChi = 0.0; double myChiProb=0.0;
	double totalEvents = nsig1.getVal() +  nsig2.getVal() + nbkg.getVal();
	std::cout<<"total of nsig1, nsig2, nbkg is "<<totalEvents<<" compared to entries "<<entries<<std::endl;
	int countagain_bins=0;
	
	TGraphErrors *res_hist = new TGraphErrors(bins);
	res_hist->SetTitle("");

	for(int i_bins=1; i_bins <=bins; i_bins++){
	  double n_obs = checkingHist->GetBinContent(i_bins);
	  // if(n_obs >0)
	    {
	    countagain_bins++;
	    double x_low = checkingHist->GetBinLowEdge(i_bins);
	    J_psi_1S_MM.setRange( "integralRange", x_low, x_low+bin_width);
	    RooAbsReal *x_integ = model.createIntegral(J_psi_1S_MM, RooFit::NormSet(J_psi_1S_MM), RooFit::Range("integralRange") );
	    
	    double n_expected = totalEvents*(x_integ->getVal());
	    
	    double chi_temp = TMath::Power( (n_obs-n_expected), 2)/n_expected;
	    // std::cout<<"bin "<<i_bins<<"["<< x_low<<","<< x_low+bin_width <<"], n_Expected-obs = "<<totalEvents<<"*"<<x_integ->getVal()<<" = "<<n_expected<<"-"<<n_obs<<"  and the chi2 is ("<<n_obs<<" - "<<n_expected<<")^2/"<<n_expected<<" = "<<chi_temp<<std::endl;
	    myChi += chi_temp;
	
	    res_hist->SetPoint(i_bins, checkingHist->GetBinCenter(i_bins), chi_temp);  //BinContent(i_bins, (n_obs-n_expected)/n_expected);
	    res_hist->SetPointError(i_bins, bin_width*0.5, 0);
      

	  }// if    
	}//int i
	
	
	std::cout<<"myChi is "<<myChi<<" for dof ("<<countagain_bins<<" - "<<nDegrees<<") = ";
	myChiProb = TMath::Prob(myChi, (countagain_bins-nDegrees) );
	myChi =  myChi/(countagain_bins-nDegrees); 
	std::cout<<myChi<<" and the Chi2 prob. is "<<myChiProb<<std::endl;

	gPad->SetBottomMargin(0.35);
	//frame->SetLabelSize(0.0, "X");
	frame->SetNdivisions(505, "Y");
	frame->Draw();
	
	TPad* pad = new TPad("pad", "pad", 0., 0., 1., 1.);
	pad->SetTopMargin(0.75);
	pad->SetFillColor(0);
	pad->SetFillStyle(0);
	pad->Draw();
	pad->cd(0);
	res_hist->GetXaxis()->SetLabelSize(0.0);
	res_hist->GetXaxis()->SetRangeUser(mLow, mHigh);
	res_hist->GetYaxis()->SetRangeUser(-1, 15);
	res_hist->GetYaxis()->SetNdivisions(505);
	res_hist->Draw("AP");


	// --------------//
	// beautify frame
	// --------------//

	const int nparams = 18;
	double fitValue[nparams]; double fitError[nparams]; TString  fitText[nparams];
	
	fitValue[0] = mean.getVal();     fitError[0] = mean.getError();     fitText[0]  = "#mu_{1}" ;
	fitValue[1] = sigma1.getVal();   fitError[1] = sigma1.getError();   fitText[1]  = "#sigma_{1}" ;
	fitValue[2] = sigma1b.getVal();   fitError[2] = sigma1b.getError();   fitText[2]  = "#sigma_{1b}" ;
	fitValue[3] = alpha.getVal();    fitError[3] = alpha.getError();    fitText[3]  = "#alpha_{1}" ;
	fitValue[4] = alphab.getVal();   fitError[4] = alphab.getError();   fitText[4]  = "#alpha_{1b}" ;
	fitValue[5] = fracCore.getVal(); fitError[5] = fracCore.getError(); fitText[5]  = "fracCore" ;
	fitValue[6] = nsig1.getVal();    fitError[6] = nsig1.getError();    fitText[6]  = "nSig (Jpsi)" ;
	
	fitValue[7] = sigPsi2S.getVal();      fitError[7] = sigPsi2S.getError();      fitText[7]  = "#sigma Psi2S" ;
	fitValue[8] = alpha_psi_1.getVal();   fitError[8] = alpha_psi_1.getError();   fitText[8]  = "#alpha psi_1" ;
	fitValue[9] = alpha_psi_2.getVal();   fitError[9] = alpha_psi_2.getError();   fitText[9]  = "#alpha psi_2" ;
	fitValue[10] = fracPsi2S.getVal();     fitError[10] = fracPsi2S.getError();     fitText[10]  = "frac Psi2S" ;
	fitValue[11] = nsig2.getVal();        fitError[11] = nsig2.getError();        fitText[11]  = "nSig (psi2S)" ; 
	
	fitValue[12] = v1.getVal();        fitError[12] = v1.getError();       fitText[12]  = "slope_exp" ;
	fitValue[13] = nbkg.getVal();      fitError[13] = nbkg.getError();     fitText[13]  = "nbkg" ;
      
	fitValue[14] = sigInWindow;        fitError[14] = sigInWindowErr;      fitText[14]  = "sigInWin" ;
	fitValue[15] = bkgInWindow;        fitError[15] = bkgInWindowErr;      fitText[15]  = "bkgInWin" ;
      
	fitValue[16] = myChi;             fitError[16] = 0;    fitText[16]  = "fit chi2" ;
	fitValue[17] = mySigma;           fitError[17] = 0;    fitText[17]  = "wted sigma"; 


	TPaveText *pt = new TPaveText(0.12, 0.45, 0.38, 0.88,"NDC"); 
	pt->SetFillColor(0);   pt->SetLineColor(0);
	pt->SetBorderSize(1);
	pt->SetTextAlign(12);
	pt->SetTextSize(0.03);
	TPaveText *pt2 = new TPaveText(0.6, 0.45, 0.85, 0.88,"NDC");  /// this is on the right
	pt2->SetFillColor(0);  pt2->SetLineColor(0);
	pt2->SetBorderSize(1);
	pt2->SetTextAlign(12);
	pt2->SetTextSize(0.03);
	TText *text;
	
	for(int i_count=0; i_count<nparams; i_count++){
	  std::ostringstream x; x.precision(4);//if(i==0) x.precision(4); else if(i==2) x.precision(3); else x.precision(2);
	  x<<fitValue[i_count]; string y = x.str(); TString z= y;
	  std::ostringstream x2; x2.precision(2); x2<<fitError[i_count]; string y2 = x2.str(); TString z2= y2;
	  TString temp = fitText[i_count]+" = "+z+" #pm "+z2;
	  //	  if(i<4) temp=temp+" MeV/c^{2}";
	  if(i_count<8) text = pt->AddText(temp);
	  else text = pt2->AddText(temp);
	}
	
	pt->Draw("same");  gPad->Update();
	pt2->Draw("same"); gPad->Update();
	
	// beautify frame - ends
	
	//nDegrees =nDegrees;
	
	for(int i_count=0; i_count<nparams; i_count++){
	  std::cout<<fitText[i_count]<< " "<<fitValue[i_count]<<" #pm "<<fitError[i_count]<<std::endl;
	}
	cout<<"for DOF "<<nDegrees<<" Fit chi square/dof = "<<frame->chiSquare(nDegrees)<<"\n"<<endl; 
	
	
	if(j==0){
	  
	  x_sigma =  sigma1.getVal();  x_sigmaErr =  sigma1.getError(); 
	  x_sigma2 =  sigPsi2S.getVal();   x_sigma2Err =  sigPsi2S.getError(); 
	  x_frac = fracCore.getVal();   x_fracErr = fracCore.getError();
	  x_bkgc1 = v1.getVal();   x_bkgc1Err = v1.getError();
	  
	  nSig = nsig1.getVal(); //*sigInWindow;
	  nSigErr = nsig1.getError();
	  inWindow_S = sigInWindow;	  
	  inWindow_SErr = sigInWindowErr;	  

	  nBg = nbkg.getVal(); //*bkgInWindow;
	  nBgErr = nbkg.getError();
	  inWindow_B = bkgInWindow;	  
	  inWindow_BErr = bkgInWindowErr;
	  
	  fitChi = myChi;//frame->chiSquare(nDegrees);
	  fitChiProb = myChiProb;
	  correlation = res->correlation("nsig1", "nbkg");
	}
	
	if(j==1){
	  
	  x_sigmaisMu =  sigma1.getVal();  x_sigmaErrisMu =  sigma1.getError(); 
	  x_sigma2isMu =  sigPsi2S.getVal();   x_sigma2ErrisMu =  sigPsi2S.getError(); 
	  x_fracisMu = fracCore.getVal();   x_fracErrisMu = fracCore.getError();
	  x_bkgc1isMu = v1.getVal();   x_bkgc1ErrisMu = v1.getError();
	  	  
	  nSigisMu = nsig1.getVal();
	  nSigErrisMu = nsig1.getError();
	  inWindow_SisMu = sigInWindow;	  
	  inWindow_SErrisMu = sigInWindowErr;
	 	  
	  nBgisMu = nbkg.getVal(); 
	  nBgErrisMu = nbkg.getError();
	  inWindow_BisMu = bkgInWindow;	  
	  inWindow_BErrisMu = bkgInWindowErr;
	  //  a_err = nbkg.getError()/nbkg.getVal();
	  // 	  b_err = bkgInWindowErr/bkgInWindow;
	  // 	  nBgErrisMu = TMath::Sqrt( TMath::Power(a_err ,2) + TMath::Power(b_err, 2) );
	  // 	  nBgErrisMu = nBgisMu*nBgErrisMu;
	  
	  fitChiisMu = myChi; // frame->chiSquare(nDegrees);
	  fitChiProbisMu = myChiProb; // frame->chiSquare(nDegrees);
	  correlationisMu  = res->correlation("nsig1", "nbkg");
	}
	
	
	delete res;
	delete  e_bk1; delete e_gm1; delete e_mass;
	delete tc;   delete checkingHist;
	
      }
      
      else 
	{
	  std::cout<<"Didn't fit for bin "<<i<<" because entries were "<<entries<<std::endl;

	  nSig= -1000; nBg=-1000; nSigErr=-1000; nBgErr = -1000; correlation = -1000;
	  x_sigma =-1000; x_sigmaErr=-10; x_sigma2= -1000; x_sigma2Err=-10; x_frac =-1000; x_bkgc1=-1000;  fitChi=-1000; fitChiProb=-1000;
	  inWindow_S = -100; inWindow_SErr = -100;  inWindow_B = -100; inWindow_BErr = -100;

	  nSigisMu = -1000; nBgisMu = -1000; nSigErrisMu = -1000; nBgErrisMu = -1000; correlationisMu = -1000;
	  x_sigmaisMu =-1000; x_sigmaErrisMu = -100;  x_sigma2isMu = -1000; x_sigma2ErrisMu =-100; x_fracisMu =-1000; x_bkgc1isMu = -1000;  fitChiisMu = -1000;
	  inWindow_SisMu = -100; inWindow_SErrisMu = -100;  inWindow_BisMu = -100; inWindow_BErrisMu = -100, fitChiProbisMu=-1000;

	  sigEff =-1000; sigEffErr = -1000;
	}
      
      
    }// for int j
    
    if(nSig <0.0) { sigEff = -1;  sigEffErr = -1; }

    else {

      double tot = nSig*inWindow_S;
      double a_err = nSigErr/nSig;
      double b_err = inWindow_SErr/inWindow_S; 
      double toterr = tot*(TMath::Sqrt( TMath::Power(a_err,2) + TMath::Power(b_err ,2) ));
      
      double totisMu = nSigisMu*inWindow_SisMu;
      a_err = nSigErrisMu/nSigisMu;
      b_err = inWindow_SErrisMu/inWindow_SisMu;
      double toterrisMu = totisMu*(TMath::Sqrt( TMath::Power(a_err,2) + TMath::Power(b_err,2) ));
      
      sigEff = 100*totisMu/tot;
      sigEffErr =  sigEff*(TMath::Sqrt(TMath::Power(toterrisMu/totisMu, 2) + TMath::Power(toterr/tot, 2) - 2*(toterr/tot)*(toterrisMu/totisMu)));

      std::cout<<"In bin "<<i<<" of momentum, efficiency was "<<sigEff<<" +/- "<<sigEffErr<<std::endl;
    }
    
    writeTree->Fill();

  }// for int i
  
  
  saveData->cd();
  writeTree->Write(saveTree);
  
  can->SaveAs(saveName+saveTree+"JpsieeFit_0.pdf");
  can1->SaveAs(saveName+saveTree+"JpsieeFit_1.pdf");

  std::cout<<"fitRanges were ["<<fitRanges[0]<<", "<<fitRanges[1]<<"]"<<std::endl;
}
