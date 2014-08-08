//// From file 
////  Using ALL TIS, All files from Job 210, 600 pb (checking the new code)

#include "myIncludes.h"
#include "computeErr.C"

void PlotMisID(bool drawPlot, bool doVerbose, int startBin, int endBin)
{
  
  gROOT->SetStyle("Plain");
  gStyle->SetPalette(1);
  gStyle->SetOptTitle(0);
  
  // final ones, looked at for the note, do not touch these lines
  //TString openFile = "/home/fsoomro/MisIDCode/Pictures/Strip17/DecStudy/1fbFolder/900pbPionfitCB-Jose2.root";
  //TString openFile = "/home/fsoomro/MisIDCode/Pictures/Strip17/DecStudy/1fbFolder/900pbKaonfitCB-pioncut0-Jose2.root";
  
  //TString openFile = "/home/fsoomro/MisIDCode/Pictures/Strip17/DecStudy/1fbFolder/UpgradeM2R1/20MarchPion_v1_newTest.root"; // Pion, isMuonNew, 330pb
  //TString openFile = "/home/fsoomro/MisIDCode/Pictures/Strip17/DecStudy/1fbFolder/UpgradeM2R1/20MarchKaon_v1_newTest.root"; // Pion, isMuonNew, 330pb
  //TString openFile = "/home/fsoomro/MisIDCode/June2012/Pion_154pb_300612_file.root";
  //  TString openFile = "/Users/fatimasoomro/WorkFiles/MisIDCode/MisID2013/Kaon_Strip20r1_800pb_average_120413_file.root"; //Pion_Strip20_1fb_average_260313_file.root
  //  TString openFile = "/Users/fatimasoomro/WorkFiles/MisIDCode/MisID2013/Proton_Strip20_1fb_MUc_260313_file_written.root"; // // MU/MD
  //TString openFile = "/Users/fatimasoomro/WorkFiles/MisIDCode/MisID2013/Proton_Strip20r1_800pb_average_120413_file.root";
  //  TString openFile = "/Users/fatimasoomro/WorkFiles/MisIDCode/June2012/Proton_Strip17_330pb_PID_151012_AllBins_EMu_written.root";
  //TString openFile = "/Users/fatimasoomro/WorkFiles/MisIDCode/June2012/Proton_Strip17_330pb_PID_sigma_151012_file.root";
  //TString openFile = "/Users/fatimasoomro/WorkFiles/MisIDCode/MisID2013/Proton_Strip20_1fb_averagec_260313_PID_file_mixed_written.root";
  TString openFile = "/Users/fatimasoomro/WorkFiles/MisIDCode/MisID2013/Proton_Strip20r1_800pb_average_120413_PID_file_mixed_written.root";
  //TString openFile = "/Users/fatimasoomro/WorkFiles/MisIDCode/June2012/Kaon_Strip19a_350pb_2012_allowsigma_PID_220812_file.root";
  //TString openFile = "/Users/fatimasoomro/WorkFiles/MisIDCode/MisID2013/Kaon_Strip20r1_800pb_D0_poly_delmtight_010713_PID_file.root";
  //TString openFile = "/Users/fatimasoomro/WorkFiles/MisIDCode/MisID2013/misID_Kp_fromSB/KaonSt20r1_UD_PIDcut_SBtune2.root"; // PionSt20r1_PIDcut_UD_LIN_All_Tuned040713.root"; // 

  std::cout<<"File to read the numbers from: "<<openFile<<std::endl;
  TFile *readFile = TFile::Open(openFile); 
  TString treeNames [4] = {"PT0", "PT1", "PT2", "PT3" };
  
  const int nBins= 4;
  
  TLegend *leg = new TLegend( 0.48,0.7,0.88,0.9 );  leg->SetFillColor(0);
  TString ptBinning[4] = {"0.8 < PT < 1.7 (GeV)", "1.7 < PT < 3.0 (GeV)", "3.0 < PT <5.0 (GeV)", "5.0 < PT < 10.0 (GeV)" };
  int myColor[4] = {1,  2,  4,  8 };
  int myStyle[4] = {25, 24, 26, 28 };
  TString drawOpt[4] = { "Ap", "samep", "samep", "samep" };
  
  TCanvas *can;
  if(drawPlot) can = new TCanvas("can", "can", 1400, 1200); 
  
  
  TGraphErrors *g[4]; 
  for(int i=0; i<4; i++) { 
    g[i] = new TGraphErrors(12);
    g[i]->SetMarkerSize(1.5);
  }
  
  
  double ranges[12] = { 2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 45, 55, 65, 100 };
  double rangesErr[12] = { 2.5, 2.5 ,  2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 30};
  
  double effTimesP_test [nBins][12];    double effTimesPErr_test [nBins][12];
  
  for(int i=startBin; i<endBin; i++){

    TTree *t = (TTree *)  readFile->Get(treeNames[i]);
    
    double x_test, x_testErr;
    t->SetBranchAddress("sigEff", & x_test);    t->SetBranchAddress("sigEffErr", & x_testErr);
    
    for(int j=0; j<11; j++){
      t->GetEntry(j);
      if(x_test<=0) { x_test=0; x_testErr=0;}
      effTimesP_test[i][j] = x_test; effTimesPErr_test[i][j] = x_testErr;
    } // int j (P bins)
    
    effTimesP_test[i][11] = effTimesP_test[i][10];
    effTimesPErr_test[i][11] = effTimesPErr_test[i][10];
    
  }// int i (PT bins)
  
  readFile->Close();
  
  double effTimesP [nBins][12];    double effTimesPErr [nBins][12];
  double finalEff[2] = { 0.0, 0.0};
  
  for(int myBin=startBin; myBin<endBin; myBin++){


    
    for(int i=0; i<11; i++){ // replace this with 12

            
      g[myBin]->SetPoint(i+1,       ranges[i],    effTimesP_test[myBin][i]);
      g[myBin]->SetPointError(i+1,  rangesErr[i], effTimesPErr_test[myBin][i]);
      
    }
    
    char tt [10]; sprintf(tt, "PT bin %i", myBin);
    leg->AddEntry(g[myBin], ptBinning[myBin], "lep") ; //  tt, "lep");
    std::cout<<"Added entry "<<tt<<" color/style "<<myColor[myBin]<<"/"<<myStyle[myBin]<<" drawOpt = "<<drawOpt[myBin]<<std::endl;
    if(drawPlot) { 
      can->cd(); 
      g[myBin]->GetYaxis()->SetTitle("misID efficiency (%)");
      g[myBin]->GetXaxis()->SetTitle("Kaon momentum (GeV)");
      g[myBin]->SetMarkerColor(myColor[myBin]);
      g[myBin]->SetLineColor(myColor[myBin]);
      g[myBin]->SetMarkerStyle(myStyle[myBin]);
      g[myBin]->Draw(drawOpt[myBin]);
    }
    
  }
 
    
  if(drawPlot) { can->cd(); leg->DrawClone(); }
    
  
  if(true) {
    std::cout<<"\n Printing for note, note that file is "<< openFile<<" \n" <<std::endl;
    
    TString trackP[11] = {"0.0< P <5.0" , "5.0< P <10.0", "10.0< P <15.0", "15.0< P <20.0", "20.0< P <15.0", "25.0< P <30.0", "30.0< P <35.0", "35.0< P <40.0", 
			  "40.0< P <50.0", "50.0< P <60.0", "60.0< P <70.0" };
    std::cout<<"\\begin{table}"<<" \n  \\begin{center} \n {\\tiny{  \n \\caption{ } \n \\begin{tabular}{|c|c|c|c|} \n \\hline"<<std::endl;
    std::cout<<" %"<<openFile<<std::endl;
 
    for(int i=0; i<11; i++){
      std::cout<<"$"<<trackP[i]<<"$  & "<<setprecision(3)<<effTimesP_test[0][i]<<" $\\pm$ "<<setprecision(2)<<effTimesPErr_test[0][i];
      std::cout<<" &  "<< setprecision(3)<<effTimesP_test[1][i]<<" $\\pm$ "<<setprecision(2)<<effTimesPErr_test[1][i];
      std::cout<<" &  "<< setprecision(3)<<effTimesP_test[2][i]<<" $\\pm$ "<<setprecision(2)<<effTimesPErr_test[2][i];
      std::cout<<" &  "<< setprecision(3)<<effTimesP_test[3][i]<<" $\\pm$ "<<setprecision(2)<<effTimesPErr_test[3][i] <<"\\\\ \\hline "<<std::endl;
      
      // printing value and error in diff rows
      //std::cout<<"\\multirow{2}{*} {$"<<trackP[i]<<"$}  & "<<setprecision(3) <<effTimesP_test[0][i]<<" & "<<effTimesP_test[1][i]<<" & "<<effTimesP_test[2][i]<<" & "<<effTimesP_test[3][i]<<" \\\\ "<<std::endl;
      //std::cout<<" & $\\pm$"<<setprecision(2)<<effTimesPErr_test[0][i]<<" & $\\pm$"<<effTimesPErr_test[1][i]<<" & $\\pm$"<<effTimesPErr_test[2][i]<<" & $\\pm$"<<effTimesPErr_test[3][i]<<" \\\\ \\hline "<<std::endl;
    }
   std::cout<<"\\end{tabular}"<<" \n }} \n \\end{center} \n \\end{table}"<<std::endl;
 	
  }// printing for note 

}



