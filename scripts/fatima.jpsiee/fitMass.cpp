#include <iostream>
#include "myIncludes.h"
#include "fitMass.h"
#include "momentumCut.C"
// #include "src/fitCB.C"
// #include "src/fitGauss.C"
// #include "src/fitBG.C"
#include "returnChain.C"
// #include "src/fitMethod2.C"
// #include "src/fitMethod2WithCB.C"
// #include "src/fitMethod1WithGauss.C"
// #include "src/plot_spectrum.C"
// #include "src/plotOnly.C"
// #include "src/fitJpsi2ee.C"
// #include "src/fitBG_Jpsiee.C"
// #include "src/fitJpsi2ee_1b.C"
// #include "src/fitJpsi2ee_1c.C"
// #include "src/fit_proton.C"
// #include "src/fitSingleMuEff.C"

void fitMass::rawEfficiency(TTree* useChain,  int startIT, int endIT){

  std::cout<<"=== Enter function to calculate rawEff === with Test Cut \n"<<testCut<<" and base cut \n"<<baseCut<<std::endl;
  //can = new TCanvas("can","can", 1400, 1200); can->Divide(4,3); 
  
  double x_rawEff, x_rawEffErr, x_BGEff, x_BGEffErr;
  double x_BGEffR, x_BGEffRErr, x_BGEffL, x_BGEffLErr;
  
  TTree *writeTree = new TTree ("writeTree", "writeTree");
  writeTree->Branch("rawEff", &x_rawEff,"rawEff/D");  
  writeTree->Branch("rawEffErr", &x_rawEffErr,"rawEffErr/D");  
  writeTree->Branch("BGEff", &x_BGEff,"BGEff/D");  
  writeTree->Branch("BGEffErr", &x_BGEffErr,"BGEffErr/D");
  writeTree->Branch("BGEffL", &x_BGEffL,"rawEffL/D");  
  writeTree->Branch("BGEffLErr", &x_BGEffLErr,"BGEffLErr/D");  
  writeTree->Branch("BGEffR", &x_BGEffR,"BGEffR/D");  
  writeTree->Branch("BGEffRErr", &x_BGEffRErr,"BGEffRErr/D");

  char tt[100];
  for(int i = startIT; i<endIT; i++){
    std::cout<<" \n ===> In momentum bin <===" <<i <<std::endl;
    //can->cd(i+1);
    sprintf(tt,"P%i",i);
    myCut = baseCut+" && "+(momentumCut(i));
    TString saveCut = myCut;
    BGcut = myCut+" && TMath::Abs(Dst_2010_plus_MM - 2010.0) >40.0";
    myCut = myCut+" && TMath::Abs(Dst_2010_plus_MM - 2010.0) <20.0";
    std::cout<<"for tot Eff: "<< myCut<<std::endl;
    std::cout<<"for BG Eff: "<< BGcut<<std::endl;
    
    double x = useChain->GetEntries(myCut); // denominator
    myCut = myCut+" && "+daughter+"_isMuon==1 "+testCut;
    //useChain->Draw(mother+"_MM", myCut, "same");
    double y = useChain->GetEntries(myCut); // numerator
    std::cout<<"Within +/- 20 MeV: Before and after isMuon cut "<<x<<" "<<y<<std::endl;
    y = y/x;  // y is the efficiency  
    double z = TMath::Sqrt( y*(1-y)/x ) ;
    x_rawEff = 100*y;     x_rawEffErr  = 100*z;
    if(x==0) { x_rawEff = 0;     x_rawEffErr  = 0; }
    
    x = useChain->GetEntries(BGcut); // denominator
    BGcut = BGcut+" && "+daughter+"_isMuon==1 "+testCut;
    y = useChain->GetEntries(BGcut); // numerator
    std::cout<<"In DeltaM > 40 MeV: Before and after isMuon cut "<<x<<" "<<y<<std::endl;
    y = y/x;  // y is the efficiency  
    z = TMath::Sqrt( y*(1-y)/x ) ;
    x_BGEff = 100*y;     x_BGEffErr  = 100*z;
    if(x==0) { x_BGEff = 0;     x_BGEffErr  = 0; }
    
    std::cout<<"savedCut was "<<saveCut<<std::endl;
    x = useChain->GetEntries(saveCut+" && (Dst_2010_plus_MM - 2010.0) > 40.0"); // denominator
    y = useChain->GetEntries(saveCut+" && (Dst_2010_plus_MM - 2010.0) > 40.0 && "+daughter+"_isMuon==1 "+testCut); // numerator
    std::cout<<"In Right SB (> 40 MeV): Before and after isMuon cut "<<x<<" "<<y<<std::endl;
    y = y/x;  // y is the efficiency  
    z = TMath::Sqrt( y*(1-y)/x ) ;
    x_BGEffR = 100*y;     x_BGEffRErr  = 100*z;
    if(x==0) { x_BGEffR = 0;     x_BGEffRErr  = 0; }
    
    x = useChain->GetEntries(saveCut+" && (Dst_2010_plus_MM - 2010.0) < -40.0"); // denominator
    y = useChain->GetEntries(saveCut+" && (Dst_2010_plus_MM - 2010.0) < -40.0 && "+daughter+"_isMuon==1 "+testCut); // numerator
    std::cout<<"In Left SB (< 40 MeV): Before and after isMuon cut "<<x<<" "<<y<<std::endl;
    y = y/x;  // y is the efficiency  
    z = TMath::Sqrt( y*(1-y)/x ) ;
    x_BGEffL = 100*y;     x_BGEffLErr  = 100*z;
    if(x==0) { x_BGEffL = 0;     x_BGEffLErr  = 0; }
    
    writeTree->Fill();

  }

  saveData->cd();
  writeTree->Write(saveTree);
  
  delete writeTree;
  saveData->Close();
  
}

fitMass::fitMass(int int_a, int int_b, int int_start_pt, int int_end_pt, bool dodebugging){ 
  gSystem->Load("libRooFit"); 
  using namespace RooFit;
  using namespace std;
  
  gROOT->SetStyle("Plain");
  gStyle->SetPalette(1);
  
  TString makemyfilename;
  myDebug = dodebugging;
  std::cout<<"\n Your configuration so far: mother = "<< mother <<" daughter (probe) = "<<daughter<<" \n mother mean mass, mLow, mHigh, fitRanges are "<<meanVal[0]<<", "<<mLow<<", "<<mHigh<<", ["<<fitRanges[0]<<", "<<fitRanges[1]<<"]. \n The base cut is "<<baseCut <<", \n  default 'isMuon' cut is "<<muonCut<<" and the testcut is "<<testCut<<std::endl;
  std::cout<<"==> Do you want to continue? 1 or 0 "<<std::endl;
  int temp_answer =  0;
  std::cin>>temp_answer;
  if(temp_answer==1){
    
    std::cout<<"Which ntuples to use? "<< std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<" -------- Stripping17 ntuples ------- " <<std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<" 0 ===  L0Global and Hlt1Phys TIS on the Kaon "<<std::endl;
    std::cout<<" 1 ===  L0Global and Hlt1Phys TIS on the Pion "<<std::endl;
    std::cout<<" 2 ===  L0Global and Hlt1TrackAllL0 TIS on the Kaon "<<std::endl;
    std::cout<<" 3 ===  L0Global and Hlt1TrackAllL0 TIS on the Pion "<<std::endl;
    std::cout<<" 4 === Special file, Rolf "<<std::endl;
    std::cout<<" 5 === L0GlobalTIS, HLT1PhysTIS and HLT2PhysTIS on the Kaon "<<std::endl;
    std::cout<<" 6 === L0GlobalTIS, HLT1PhysTIS and HLT2PhysTIS on the Pion "<<std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<"  The following ntuples contain another definition of isMuon called oldIsMuon. You can choose to use this definition by setting it in fitMass.h \n Details in the presentation on 26 March 2012 "<<std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<" 7 === L0Global and HLT1Phys TIS on the Pion "<<std::endl;
    std::cout<<" 8 === L0Global and HLT1Phys TIS on the Kaon "<<std::endl;
    std::cout<<" 9  === same as 7, only nPV>3 "<<std::endl; 
    std::cout<<" 10 === same as 7, only nPV>4 "<<std::endl; 
    std::cout<<" 11 === same as 8, only nPV>3 "<<std::endl; 
    std::cout<<" 12 === same as 8, only nPV>4 "<<std::endl; 
    std::cout<<" 13 === L0Global and HLT1Phys TIS on the Proton from Lambda-> p pi "<<std::endl;
    std::cout<<" 81 === L0Global and HLT1Phys TIS on Strip17 sample (B->emu, trimmed ntuples from Gaia) "<<std::endl;
    std::cout<<" 811 === L0Global and HLT1Phys TIS on Strip17 sample (B->emu, trimmed ntuples Fatima, Choosen polarity in the .h file) "<<std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<" From here on, stripping19/19a ntuples " <<std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<" 14 ===   L0Global and Hlt1Phys TIS on the daughter [74pb-1, Strip19] "<<std::endl;
    std::cout<<" 1500 ===   L0Global and Hlt1Phys TIS on the daughter [350pb-1, Strip19a] "<<std::endl;
    std::cout<<" 15 ===   L0Global and Hlt1Phys TIS on the daughter [426pb-1, Strip19a] "<<std::endl;
    std::cout<<" 150  ===   L0Global and Hlt1Phys TIS on the daughter [168pb-1, Strip19b] "<<std::endl;
    std::cout<<" 1520 ===   L0Global and Hlt1Phys TIS on the daughter [3pb-1, Strip20] "<<std::endl;
    std::cout<<" 1599 ===   L0Global and Hlt1Phys TIS on the daughter [245pb-1, Strip19c] "<<std::endl;
    std::cout<<" 2012 ===  L0Global and Hlt1Phys TIS on the proton [414pb-1, Strip19a] "<<std::endl;
    std::cout<<" 2011 ===  L0Global and Hlt1Phys TIS on the proton [~330pb-1, Strip17] "<<std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<" Stripping 20 [2012 data] and 20r1 [2011 data] " <<std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<" 2001 ===  S20 2fb-1 (Chosen Magnet polarity in the .h file, choose tot for both)"<<std::endl;
    std::cout<<" 20011 ===  S20 2fb-1 MU+MD, run only for p->mu, PT2"<<std::endl;
    std::cout<<" 2002 ===  S20, 430 pb-1 of MagnetDN, 350pb of MagnetUP, L0Glo && Hlt1Glo TIS (Chosen Magnet polarity in the .h file)"<<std::endl;
    std::cout<<" 20021 === S20, 430 + 350 pb-1, L0Glo && Hlt1Glo TIS"<<std::endl;
    std::cout<<" 20012 === S20 all data *** nPV cut *** (MU, MD or MU+MD) run *only for KAON. For MU+MD choose tot in the .h file "<<std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<" 2003 ===  Strip20r1, 335pb Magnet UP , 470pb Magnet DN  (Chosen Magnet polarity in the .h file)"<<std::endl;
    std::cout<<" 20031 ===  Strip20r1, 335pb + 470pb"<<std::endl;
    std::cout<<" 2004 ===  Strip20r1, 123pb (MU) of L0Glo && Hlt1Glo TIS"<<std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<" From here on, B->e mu ntuples " <<std::endl;
    std::cout<<" --------         -------------           -----------         ----------     ------------      ----------"<<std::endl;
    std::cout<<" 16 ===   Jpsi tuple, eminus is the probe "<<std::endl;
    std::cout<<" 17 ===   B->Jpsi(ee)K  tuple, for trigger (IP, PT) map  "<<std::endl;
    std::cout<<" 18 ===   B->Jpsi(mumu)K tuple, for trigger (IP, PT) map "<<std::endl;
    std::cout<<" 19 ===   L0Ele, HLT1Phys, HLT2Phys TIS on daughter. S17, 330pb [job 180] ==> For e->K and e->pi study"<<std::endl;
    std::cout<<" Enter the appropriate integer "<<std::endl;
    std::cin >> intChain;
    
    std::cout<<"\n  **** CHOOSE FIT METHOD: **** \n plotOnly==-1, raw = 0, fitCB && raw =1, plot_spectrum = 30713, fitGauss =2 and fitMethod2 = 3, fitMethod2WithCB = 4, rawOnly =5, fitBG =6, fitMethod1WithGauss = 7, \n fitJpsi = 8, fitBG_Jpsiee = 9, fitJpsifor trigger = 10,  fitJpsifor HLT2 = 11, fitJpsi for L0xHLT1 = 12, proton_raw = 100, fit_proton = 101 \n enter method number: "<<std::endl;
    std::cin >> whichMethod;
    
    // open root file to write graphs
    std::cout<<"enter rootfile name to open in directory -> "<<saveName<<std::endl;
    std::cin >> makemyfilename;
    makemyfilename = saveName+makemyfilename;
    std::cout<<"Will be opening root file "<<makemyfilename<<std::endl;
    
    if(intChain ==20012){
      std::cout<<"Which nPVs do you want to run for? Enter 1, 2, 3, 4, for nPVs==1, nPVs==2, nPVs==3 and nPVs>4"<<std::endl;
      std::cin>>myPV; std::cout<<"You chose "<<myPV<<std::endl;
    }

  }// temp_answer ==1

  temp_answer=0;
  
  std::cout<<"All config OK ?? 1 or 0 "<<std::endl;
  std::cin>>temp_answer;
  if(temp_answer==1){
    
    TTree *useChain;
    // if(whichMethod > 2) {
    //   useChain = (TTree *) fitMass::returnChain(); // used until 260313
    //   std::cout<<"Total entries "<<useChain->GetEntries()<<std::endl;
    // }
    
    int_c = int_end_pt;
    int max_iter = int_end_pt;
    if(int_end_pt <0) max_iter = 1;
    if(int_start_pt <0 ) int_start_pt = 0;
    TStopwatch *overall_time = new TStopwatch();
    overall_time->Start();
    
    can = new TCanvas("can","can", 1400, 1200); 
    if(whichMethod==3) can1 = new TCanvas("can1","can1", 1400, 1200); 

    for(int nIter = int_start_pt; nIter <max_iter;  nIter++ ){
      
      saveData = new TFile(makemyfilename+".root", "UPDATE");
      // prepare Tree name
      std::ostringstream tmpx; tmpx<<nIter;  string x2 = tmpx.str(); TString x3 = x2;
      myPTbin = nIter; saveTree = "PT"+x3;
      char tmpchar[10]; sprintf(tmpchar, "PT%i", nIter);  appendName = tmpchar;
      
      std::cout<<" --->> Iteration "<<nIter<<"  saveTree = "<<saveTree<<"  appendName = "<<appendName<<std::endl;
      
      //if(whichMethod<2) {
      useChain = (TTree *) fitMass::returnChain();
      std::cout<<"Total entries "<<useChain->GetEntries()<<std::endl;
            
//       if (whichMethod < 0 )  { std::cout<<"Calling method plotOnly"<<std::endl;  plotOnly(useChain, int_a, int_b); }
//       if (whichMethod == 0 || whichMethod==1)  { std::cout<<"Calling method fitCB"<<std::endl;  fitCB(useChain, int_a, int_b); }
//       if (whichMethod == 100 || whichMethod==101)  { std::cout<<"Calling method fit_proton"<<std::endl;  fit_proton(useChain, int_a, int_b); }
//       if (whichMethod == 2) { std::cout<<"Calling method fitGauss"<<std::endl;   fitGauss(useChain, int_a, int_b); } 
//       if (whichMethod == 3) { std::cout<<"Calling method fitMethod2"<<std::endl; fitMethod2(useChain, int_a, int_b);   }
//       if (whichMethod == 4) { std::cout<<"Calling method fitMethod2WithCB"<<std::endl; fitMethod2WithCB(useChain, int_a, int_b); }
//       if (whichMethod == 30713)  { std::cout<<"Calling method plot_spectrum "<<std::endl;  plot_spectrum(useChain, int_a, int_b); }
      if (whichMethod == 5) { 
	std::cout<<"Calling method rawEfficiency"<<std::endl; 
	//rawEff  = new TGraphErrors(momentumBins); 	rawBGEff  = new TGraphErrors(momentumBins);
	rawEfficiency(useChain, int_a, int_b); 
      }
//       if (whichMethod == 6)  { std::cout<<"Calling method fitBG () "<<std::endl; fitBG(useChain, int_a, int_b); }
//       if (whichMethod == 7) { std::cout<<"Calling method fitMethod1WithGauss"<<std::endl; fitMethod1WithGauss(useChain, int_a, int_b); }
//       if (whichMethod == 8) { std::cout<<"Calling method fitJpsi2ee"<<std::endl; fitJpsi2ee(useChain, int_a, int_b); }
//       if (whichMethod == 9) { std::cout<<"Calling method fitBG_Jpsi2ee"<<std::endl; fitBG_Jpsiee(useChain, int_a, int_b); }
//       if (whichMethod == 10) { std::cout<<"Calling method fitJpsi2ee_1b"<<std::endl; fitJpsi2ee_1b(useChain, int_a, int_b); }
//       if (whichMethod == 11) { std::cout<<"Calling method fitJpsi2ee_1c"<<std::endl; fitJpsi2ee_1c(useChain, int_a, int_b); }
//       if (whichMethod == 12) { std::cout<<"Calling method fitSingleMuEff"<<std::endl; fitSingleMuEff(useChain, int_a, int_b); }      
      BGcut = "";
      myCut = "";

      if(whichMethod <2) delete useChain;      
      saveData->Close();

    }
    overall_time->Stop();
    overall_time->Print();
    std::cout<<"===> made file "<<saveName<<" <=== "<<std::endl;
    if(whichMethod >2) delete useChain;      
    
    BGcut = "";
    myCut = "";
    
  }// if (temp_answer==1)

  else{
    std::cout<<"Didn't execute function... check your configuration"<<std::endl;
    temp_answer=0;
  }
  
  
  //The CrystalBall shape is Gaussian that is 'connected' to an exponential taill at 'alpha' sigma of the Gaussian.
  // The sign determines if it happens on the left or right side. The 'n' parameter control the slope of the exponential part. 
  

};
