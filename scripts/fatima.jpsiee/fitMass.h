#ifndef FITMASS
#define FITMASS

#include <TString.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TChain.h>
#include <TFile.h>
#include <TH1.h>
#include <TROOT.h>
#include <iostream>
#include <TGraphErrors.h>
#include "myIncludes.h"
#include "computeErr.C"

const int momentumBins= 11;
double ranges[momentumBins] = { 2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 45, 55, 65 };
double rangesErr[momentumBins] = { 2.5, 2.5 ,  2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 5, 5, 5};

// declare to avoid problems when running muon, electron efficiencies for B->emu
/* TString mass_values[3] = { "", "", ""};  */
/* double fit_boundaries[2] = { 0., 0.}; */
/* double sigma_values[6] = { 0.,  0., 0., 0., 0.0, 0.0}; */

//TString cleanupCuts = "(Dst_2010_plus_MM-D0_MM)>100 && (Dst_2010_plus_MM-D0_MM)<180 && D0_FD_OWNPV<6000  && Kminus_PIDK>10.0"; 
// TString cleanupCuts = "(Dst_2010_plus_MM-D0_MM)>100 && (Dst_2010_plus_MM-D0_MM)<180 && D0_FD_OWNPV<6000  && piplus0_PIDK<0.0";
//TString cleanupCuts = "lab4_PIDK>10.0";

/*
TString daughter = "lab4";//   ;// [lab3 =pion, lab4 = kaon in D*-> D0(K pi) pi_slow]
TString mother   =  "lab0"; //
double meanVal[3] = { 2012.86, 2012.86*0.95, 2012.86*1.05};
const double mLow =  1978.;// 1910;
const double mHigh = 2066.;//2110;
int bins = 50;
//double fitRanges[2] = { mLow+48, mHigh-32}; //change to 50, was +-30 until 290613
double fitRanges[2] = {1978., 2066.}; //change to 50, was +-30 until 290613
TString mass_cut = mother+"_MM > 1978. && "+mother+"_MM <2066.";
TString mass_values[3] = { "2010.0", "40.", "20."};
double fit_boundaries[2] = { 1990., 2030.};
double sigma_values[6] ={ 5., 3., 10., 8, 3, 15.}; // was 40, 28/6/13
//RooArgSet *obs = new RooArgSet(lab0_MM, lab3_PT, lab3_P, lab4_PT, lab4_P);
*/

// // ===>  fit the D0 mass
TString daughter = "lab4";//   ;// [lab3 =pion, lab4 = kaon in D*-> D0(K pi) pi_slow]
TString mother   =  "lab2"; //
double meanVal[3] = { 1868., 1862., 1870.};
const double mLow =  1840. ;
const double mHigh = 1910.;
int bins = 60;
TString mass_cut = mother+"_MM > 1840. && "+mother+"_MM <1910."; 
double fitRanges[2] = {mLow, mHigh};
TString mass_values[3] = { "1868.0", "25.", "15."};
double fit_boundaries[2] = { 1850., 1880.};
double sigma_values[6] ={ 5., 2., 10., 8, 2, 10.};


//lambda 
/*
TString daughter = "lab1";  // lab1 in Strip20, lab2 in others
TString mother = "lab0";
double meanVal[3] = { 1116., 1110., 1120.};
const double mLow  = 1100.;//   1110.;// 
const double mHigh =  1135.0; // 1125.; // 
double fitRanges[2] = { mLow, mHigh};
int bins = 150; 
TString mass_values[3] = { "1116.0", "6.", "4."}; 
double fit_boundaries[2] = { 1112., 1120.};
double sigma_values[6] = { 0.5,  0.1, 3.0, 1.0, 0.1, 3.0};
*/
// Jpsi
/* TString mother =  "J_psi_1S"; */
/* TString daughter = "eminus"; */
/* double meanVal[3] = {3096., 3000., 3200.}; */
/* const double mLow = 2200.; // 2200./2600 for electrons/muons */
/* const double mHigh = 4000.; // 4200./3600 for electrons/muons */
/* int bins = 30; */
/* double fitRanges[2] = { mLow, mHigh}; */

/* /// Bplus , for HLT2 */
/* TString mother =  "Bplus"; */
/* TString daughter = "muminus"; TString part = "mu"; */
/* double meanVal[3] =  { 5280., 5200., 5500.}; */
/* const double mLow = 4800.; */
/* const double mHigh = 5600.; */
/* int bins = 40; */
/* double fitRanges[2] = { mLow, mHigh}; */

//TString truthCut = "TMath::Abs(Bplus_TRUEID)==521 && TMath::Abs(J_psi_1S_TRUEID)==443 && TMath::Abs(Kplus_TRUEID)==321 && TMath::Abs(eplus_TRUEID)==11 && TMath::Abs(eminus_TRUEID) ==11";
//TString myTIS = daughter+"L0ElectronDecision_TIS == 1 && "+daughter+"Hlt1Phys_TIS == 1 && "+daughter+"Hlt2Phys_TIS ==1";
//TString pos_calo = " (12000*eminus_PY/eminus_PZ)<500. && (12000*eminus_PX/eminus_PZ)<500. ";
//TString hlt2 = "BplusHlt1Phys_Dec==1 && BplusL0Global_Dec==1 &&  muplusHlt2Phys_TIS==1 && KplusHlt2Phys_TIS==1  && muplus_isMuon==1 && muminus_isMuon==1";
//TString baseCut = hlt2+" &&"+daughter+"_IP_OWNPV<0.1 && "+daughter+"_PT<30000.";
//TString hlt2 = "BplusHlt1Phys_Dec==1 && BplusL0Global_Dec==1 && ( (Kplus_ID>0 && "+part+"plusHlt2Phys_TIS==1) || (Kplus_ID<0 && "+part+"minusHlt2Phys_TIS==1) ) "; // Used until 19feb
//TString hlt2 = "BplusHlt1Phys_TOS==1 && BplusL0Global_TOS==1 && ( (Kplus_ID>0 && "+part+"plusHlt2Topo2BodyBBDTDecision_TIS==1) || (Kplus_ID<0 && "+part+"minusHlt2Topo2BodyBBDTDecision_TIS==1) ) "; 
//TString hardcuts = "Kplus_IPCHI2_OWNPV>25. && eplus_IPCHI2_OWNPV>25. && eminus_IPCHI2_OWNPV>25. && Kplus_TRACK_CHI2NDOF<3. && eplus_TRACK_CHI2NDOF<3. && eminus_TRACK_CHI2NDOF<3. && Bplus_IPCHI2_OWNPV <25. && Bplus_FDCHI2_OWNPV >225.";
//TString baseCut = hlt2+" && ((Kplus_ID>0 && max("+part+"minus_IP_OWNPV,Kplus_IP_OWNPV)>0.1 && max("+part+"minus_PT,Kplus_PT) >3000. ) || (Kplus_ID<0 && max("+part+"plus_IP_OWNPV,Kplus_IP_OWNPV)>0.1 && max("+part+"plus_PT, Kplus_PT)>3000.) )  && Bplus_ENDVERTEX_CHI2<3. && J_psi_1S_ENDVERTEX_CHI2<3. "; 

//TString baseCut = "J_psi_1SHlt2Phys_TIS==1 && muplusHlt2Phys_TIS==1 && muminusHlt2Phys_TIS==1";

TString mydelmcut =  "delta_MM>144.5 && delta_MM<146.5";//TIGHT//   "delta_MM>144.0 && delta_MM<147.0";//Loose //
TString baseCut = daughter+"_P >0. && nLongTracks > 80 && nLongTracks <=800 && "+mydelmcut; //" myTIS+" && "+daughter+"_P>0.&& nSPDHits> 450";
TString testCut = " && "+daughter+"_PIDK<10. && "+daughter+"_PIDmu>-5.";// " && ("+daughter+"_MuonMuLL - "+daughter+"_MuonBkgLL) >0.5"; 
TString muonCut = "isMuon==1"; // "_PIDe>3.0 "; //      "oldIsMuon";//  requires "_PIDe>x" for jpsi methods

//TString saveName        = "/Users/fatimasoomro/WorkFiles/EMu/EfficiencyCodeFiles/eminus_pid3_Square_L0EleHlt1_2TIS_SPD450_040513_"; //Proton_Strip17_all_PIDe_3_200413_";// 
//std::string saveNameStr = "/Users/fatimasoomro/WorkFiles/EMu/EfficiencyCodeFiles/eminus_pid3_Square_L0EleHlt1_2TIS_SPD450_040513_"; //Proton_Strip17_all_PIDe_3_200413_";
TString saveName        = "/Users/fatimasoomro/WorkFiles/MisIDCode/MisID2013/Kaon_Strip20_MD_nTR_d_D0_poly_delmtight_010713_PID_";
std::string saveNameStr = "/Users/fatimasoomro/WorkFiles/MisIDCode/MisID2013/Kaon_Strip20_MD_nTR_d_D0_poly_delmtight_010713_PID_";
TString mypolarity_str = "MD"; // "tot" to pick up both

TString myPV;
TString saveTree; // = "PT1";
int myPTbin ; //= 1;
int int_c;
int intChain;
  

class fitMass {
public:
  
  
  fitMass(int, int, int, int, bool); 
  
  void fitCB(TTree* ,  int, int );
  void fitBG(TTree* ,  int, int );
  void fitGauss(TTree*, int, int );
  void fitMethod2(TTree*, int, int);
  void fitMethod2WithCB(TTree*, int, int);
  void fitMethod1WithGauss(TTree*, int, int);
  void plot_spectrum(TTree* ,  int, int );
  void plotOnly(TTree* ,  int, int );
  void fitJpsi2ee(TTree* ,  int, int );
  void fitJpsi2ee_1b(TTree* ,  int, int );
  void fitJpsi2ee_1c(TTree* ,  int, int );
  void fitSingleMuEff(TTree* ,  int, int );
  void fitBG_Jpsiee(TTree* ,  int, int );
  void fit_proton(TTree*, int, int);
  TString momentumCut(int);
  TString momentumCutJpsi(int);
  TString TwoDCutJpsi(int);
  TString CutJpsiMuonPlusTrack(int);
  TString CutSingleMuonTriggerEff(int);
  TTree* returnChain();
  void rawEfficiency(TTree*,  int, int);
  TFile *saveData;
  
  bool myDebug;
  //bool drawOnly;
  //bool doRawEff;
  bool fitForMass;
  TString isMu;
  std::string appendName;
  int whichMethod;

  // TGraphErrors *g[20];
  TGraphErrors *rawEff ;
  TGraphErrors *rawBGEff ;
  TCanvas *can;
  TCanvas *can1;
  TCanvas *c ;
  TCanvas *graphs;
  TString myCut;
  TString BGcut;

  };

#endif // FITMASS 
