#include "fitMass.h"


TTree* fitMass::returnChain(){
  
  // #### User configuration #### //
  // set this variable to the appropriate integer // 
  
  // 0 ===  L0Global and Hlt1Phys TIS on the Kaon //
  // 1 ===  L0Global and Hlt1Phys TIS on the Pion //
  // 2 ===  L0Global and Hlt1TrackAllL0 TIS on the Kaon //
  // 3 ===  L0Global and Hlt1TrackAllL0 TIS on the Pion //
  // 4 === Special file, Rolf //
  // 5 === L0GlobalTIS, HLT1PhysTIS and HLT2PhysTIS on the Kaon //
  // 6 === L0GlobalTIS, HLT1PhysTIS and HLT2PhysTIS on the Pion //

  // --------         -------------           -----------         ----------     ------------      ----------//
  //  The following ntuples contain another definition of isMuon called oldIsMuon. This ignores the presence of hit in M2.
  // More details in the presentation on 26 March 2012
  // --------         -------------           -----------         ----------     ------------      ----------//
  
  // 7 === L0Global and HLT1Phys TIS on the Pion //
  // 8 === L0Global and HLT1Phys TIS on the Kaon //
  // 9  === same as 7, only nPV>3 // 
  // 10 === same as 7, only nPV>4 // 
  // 11 === same as 8, only nPV>3 // 
  // 12 === same as 8, only nPV>4 // 
  // 13 === L0Global and HLT1Phys TIS on the Proton //
  // --------         -------------           -----------         ----------     ------------      ----------//
  // From here on, stripping19/19a ntuples 
  // --------         -------------           -----------         ----------     ------------      ----------//
  //  14 ===   14  L0Global and Hlt1Phys TIS on the daughter [74pb-1, Strip19] 
  //  15 ===   L0Global and Hlt1Phys TIS on the Kaon, [426pb-1, strip19a]
  //  150 ===   L0Global and Hlt1Phys TIS on the daughter [168pb-1, Strip19b]
  // --------         -------------           -----------         ----------     ------------      ----------//
  // From here on, B->e mu ntuples
  // --------         -------------           -----------         ----------     ------------      ----------//
  //  16 ===   Jpsi file, eminus is the probe
  //  17 ===   B->Jpsi(ee)K  tuple, for trigger (IP, PT) map
  //  18 ===   B->Jpsi(mumu)K tuple, for trigger (IP, PT) map
  //  19 ===   L0Ele, HLT1Phys, HLT2Phys TIS on daughter. S17, 330pb [job 180] ==> For e->K and e->pi study



  TString setPath = "/Users/fatimasoomro/WorkFiles/AllRootFiles/MisIDNtuples/";
  std::cout<<"====> from returnChain <====="<<std::endl;
  TString file_Str = "";
  TString daughter_str = "";
  TString pt_str = "";
  
  if(intChain<0) {
    intChain = 11;
    std::cout<<"=====> \n Attention, intChain was not set by user. I am setting it to 11 whatever that means! "<<std::endl;
  }
  
  
  TTree *t;
  TChain *Dst;
  
  
  if(intChain == 0) {
    Dst = new TChain ("HLTTest", "");
    Dst->AddFile(setPath+"Jose2_Kaon_a.root");
    Dst->AddFile(setPath+"Jose2_Kaon_b.root");
    Dst->AddFile(setPath+"Jose2_Kaon_c.root");
    t = Dst->CopyTree(baseCut);
  }
  
  
  if(intChain == 1) {
    Dst = new TChain ("HLTTest", "");
    Dst->AddFile(setPath+"Jose2_Pion_a.root");
    Dst->AddFile(setPath+"Jose2_Pion_b.root");
    Dst->AddFile(setPath+"Jose2_Pion_c.root");
    t = Dst->CopyTree(baseCut);
  }
  
  
  if(intChain == 2){
    Dst = new TChain ("HLTTest", "");
    Dst->AddFile(setPath+"Jose_Kaon_a.root");
    Dst->AddFile(setPath+"Jose_Kaon_b.root");
    Dst->AddFile(setPath+"Jose_Kaon_c.root");
    t = Dst->CopyTree(baseCut);
  }
  
  
  if(intChain == 3){
    Dst = new TChain ("HLTTest", "");
    Dst->AddFile(setPath+"Jose_Pion_a.root");
    Dst->AddFile(setPath+"Jose_Pion_b.root");
    Dst->AddFile(setPath+"Jose_Pion_c.root");
    t = Dst->CopyTree(baseCut);
  }
  
  if(intChain == 4){
    Dst = new TChain ("HLTTest", "");
    Dst->AddFile(setPath+"Rolf_noCuts.root");
    t = Dst->CopyTree(baseCut);
  }    
  
  
  if(intChain == 5){
    Dst = new TChain ("AllTIS", "");
    Dst->AddFile(setPath+"Kaon900pb.root"); 
    t = Dst->CopyTree(baseCut);
  }
  
  if(intChain == 6){
    Dst = new TChain ("AllTIS", "");
    Dst->AddFile(setPath+"Pion900pb.root"); 
    t = Dst->CopyTree(baseCut);
  }
  
  
  if(intChain == 7 ){
    Dst = new TChain ("DecayTree", "");
    Dst->AddFile(setPath+"180/Pion_v1/Merged100.root");
    Dst->AddFile(setPath+"180/Pion_v1/Merged200.root");
    Dst->AddFile(setPath+"180/Pion_v1/Merged300.root");
    Dst->AddFile(setPath+"180/Pion_v1/Merged400.root");
    Dst->AddFile(setPath+"180/Pion_v1/Merged502.root");
    t = (TTree *) Dst;
  }
  
  
  if(intChain == 8){
    Dst = new TChain ("DecayTree", "");
    Dst->AddFile(setPath+"180/Kaon_v1/Merged200.root");
    Dst->AddFile(setPath+"180/Kaon_v1/Merged400.root");
    Dst->AddFile(setPath+"180/Kaon_v1/Merged502.root");
    t = (TTree *) Dst;
  }

  if(intChain == 81){
    
    Dst = new TChain ("DecayTree", "");

    std::stringstream ss_tmp; ss_tmp<<myPTbin; std::string ss_tmp_str = ss_tmp.str();
    pt_str = ss_tmp_str;
    if(daughter=="lab3") daughter_str = "Pion";
    if(daughter=="lab4") daughter_str = "Kaon";
    
    file_Str = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/FromGaia/Strip17_"+daughter_str+"_PT"+pt_str+"_180413.root";
    std::cout<<"Adding to chain "<<file_Str<<std::endl;
    Dst->AddFile(file_Str);
    t = (TTree *) Dst;
  }

 if(intChain == 811){
    
    Dst = new TChain ("DecayTree", "");
    std::stringstream ss_tmp; ss_tmp<<myPTbin; std::string ss_tmp_str = ss_tmp.str();
    pt_str = ss_tmp_str;
    if(daughter=="lab3") daughter_str = "Pion";
    if(daughter=="lab4") daughter_str = "Kaon";

    if(daughter=="lab3" || daughter=="lab4"){
      
      if (mypolarity_str!="tot") {
	file_Str = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Strip17_wPIDe_"+daughter_str+"_"+mypolarity_str+"_PT"+pt_str+"_200413.root";
	std::cout<<"Adding to chain "<<file_Str<<std::endl;
	Dst->AddFile(file_Str);
      }
      else {
	file_Str = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Strip17_wPIDe_"+daughter_str+"_MU_PT"+pt_str+"_200413.root"; std::cout<<"Adding to chain "<<file_Str<<std::endl;
	Dst->AddFile(file_Str);
	file_Str = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Strip17_wPIDe_"+daughter_str+"_MD_PT"+pt_str+"_200413.root"; std::cout<<"Adding to chain "<<file_Str<<std::endl;
	Dst->AddFile(file_Str);
      }
    } // lab3 or 4


    //// for proton, lab2 in Strip17
    else{
   
      if (mypolarity_str!="tot") {   

	if(myPTbin<2){
	  file_Str = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Strip17_wPIDe_Proton_"+mypolarity_str+"_PT"+pt_str+"_200413.root";
	  std::cout<<"Adding to chain "<<file_Str<<std::endl; Dst->AddFile(file_Str);
	}
	else {
	  //	  Strip17_wPIDe_Proton_MD_PT3_430pb_200413.root
	  file_Str = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Strip17_wPIDe_Proton_"+mypolarity_str+"_PT3_430pb_200413.root";
	  std::cout<<"Adding to chain "<<file_Str<<std::endl; Dst->AddFile(file_Str);
	} //else
      } // if !tot
      
      else {
	
	if(myPTbin<2){
	  file_Str = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Strip17_wPIDe_Proton_MU_PT"+pt_str+"_200413.root";
	  std::cout<<"Adding to chain "<<file_Str<<std::endl; Dst->AddFile(file_Str);
	  file_Str = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Strip17_wPIDe_Proton_MD_PT"+pt_str+"_200413.root";
	  std::cout<<"Adding to chain "<<file_Str<<std::endl; Dst->AddFile(file_Str);
	}
	else {
	  file_Str = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Strip17_wPIDe_Proton_MU_PT3_430pb_200413.root";
	  std::cout<<"Adding to chain "<<file_Str<<std::endl; Dst->AddFile(file_Str);
	  file_Str = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Strip17_wPIDe_Proton_MD_PT3_430pb_200413.root";
	  std::cout<<"Adding to chain "<<file_Str<<std::endl; Dst->AddFile(file_Str);
	} //else
	
      }  // if tot
    }
    
    t = (TTree *) Dst;
 } // 822


  if(intChain == 9){
    Dst = new TChain ("DecayTree", "");
    Dst->AddFile(setPath+"180/Pion_v1/MergedPV4.root");
    Dst->AddFile(setPath+"181/Pion_v1/MergedPV4.root");
    t = (TTree *) Dst;
  }
  
  if(intChain == 10){
    Dst = new TChain ("DecayTree", "");
    Dst->AddFile(setPath+"180/Pion_v1/MergedPV5.root");
    Dst->AddFile(setPath+"181/Pion_v1/MergedPV5.root");
    t = (TTree *) Dst;
  }
  
  if(intChain == 11){
    Dst = new TChain ("DecayTree", "");
    Dst->AddFile(setPath+"180/Kaon_v1/MergedPV4.root");
    Dst->AddFile(setPath+"181/Kaon_v1/MergedPV4.root");
    t = (TTree *) Dst;
  }
  
  if(intChain == 12){
    Dst = new TChain ("DecayTree", "");
    Dst->AddFile(setPath+"180/Kaon_v1/MergedPV5.root");
    Dst->AddFile(setPath+"181/Kaon_v1/MergedPV5.root");
    t = (TTree *) Dst;
  }
  
  if(intChain == 13 ){
    Dst = new TChain ("DecayTree", "");
    Dst->AddFile(setPath+"180/Proton_v1/Merged100.root");
    Dst->AddFile(setPath+"180/Proton_v1/Merged300.root");
    Dst->AddFile(setPath+"180/Proton_v1/Merged502.root");
    t = (TTree *) Dst;
  }
  
  if(intChain == 14){ // stripping19 74pb-1
    Dst = new TChain("DecayTree", "");
    
    std::cout<<"===> from return chain, daughter was "<<daughter<<std::endl;
    if(daughter=="lab3") { 
      // // ///  L0Global, HLT1PhysTIS
      //Dst->AddFile(setPath+"Strip19_Pion_31pb_22Aug.root"); std::cout<<"adding Strip19_Pion_31pb_22Aug.root"<<std::endl;
      //Dst->AddFile(setPath+"Strip19_Pion_43pb_22Aug.root"); std::cout<<"adding Strip19_Pion_43pb_22Aug.root"<<std::endl; 
      // // ///  L0Global, HLT1GlobalTIS
      Dst->AddFile(setPath+"Strip19_Pion_74pb_27Aug.root"); std::cout<<"adding Strip19_Pion_74pb_27Aug.root"<<std::endl;
    }
    if(daughter=="lab4"){
      
      // // ///  L0Global, HLT1PhysTIS
      //Dst->AddFile(setPath+"Strip19_Kaon_31pb_22Aug.root"); std::cout<<"adding Strip19_Kaon_31pb_22Aug.root"<<std::endl;
      //Dst->AddFile(setPath+"Strip19_Kaon_43pb_22Aug.root"); std::cout<<"adding Strip19_Kaon_43pb_22Aug.root"<<std::endl;  
      // // ///  L0Global, HLT1GlobalTIS
      Dst->AddFile(setPath+"Strip19_Kaon_74pb_27Aug.root"); std::cout<<"adding Strip19_Kaon_74pb_27Aug.root"<<std::endl;

    }
    
    std::cout<<"\n Chain prepared... "<<std::endl;
    t = (TTree *) Dst;
  }
    
  if(intChain == 1500){ 
    Dst = new TChain("DecayTree", "");
    std::cout<<"[Strip19a, 350pb-1] daughter was "<<daughter<<", so adding to chain: ";
    
    std::stringstream ss_tmp; ss_tmp<<myPTbin; std::string ss_tmp_str = ss_tmp.str();
    pt_str = ss_tmp_str;

    if(daughter=="lab3"){
            
      //Dst->AddFile(setPath+"Strip19a_Dn_156pb_Pion_Job294_25July.root"); std::cout<<"Strip19a_Dn_156pb_Pion_Job294_25July.root  ";
      //Dst->AddFile(setPath+"Strip19a_Up_200pb_Pion_Job295_25July.root"); std::cout<<"Strip19a_Up_200pb_Pion_Job295_25July.root  ";
      file_Str = "Strip19a_Pion_350pb_PT"+pt_str+"_030713.root";       Dst->AddFile(setPath+file_Str); std::cout<<file_Str<<"  "<<std::endl;
    }
    
    if(daughter=="lab4"){
      // Dst->AddFile(setPath+"Strip19a_Dn_156pb_Kaon_Job294_25July.root"); std::cout<<"Strip19a_Dn_156pb_Kaon_Job294_25July.root, " ;  
      // Dst->AddFile(setPath+"Strip19a_Up_110pb_Kaon_Job295_25July.root"); std::cout<<"Strip19a_Up_110pb_Kaon_Job295_25July.root, ";
      // Dst->AddFile(setPath+"Strip19a_Up_090pb_Kaon_Job295_25July.root"); std::cout<<"Strip19a_Up_090pb_Kaon_Job295_25July.root";
      file_Str = "Strip19a_Kaon_350pb_PT"+pt_str+"_030713.root";       Dst->AddFile(setPath+file_Str); std::cout<<file_Str<<"  "<<std::endl;
    }
    std::cout<<"\n Chain prepared... "<<std::endl;
    t =(TTree *) Dst;
  }
  
  
  if(intChain == 15){ 
    Dst = new TChain("DecayTree", "");
    std::cout<<"[Strip19a, 425pb-1 ][for syst check, change date in file to 27Aug] daughter was "<<daughter<<", so adding to chain: ";
    // //// 426 pb-1 ////
    
    if(daughter=="lab3"){
      //Dst->AddFile(setPath+"Strip19a_Pion_115pb_c_22Aug.root");  std::cout<<"Strip19a_Pion_115pb_c_22Aug.root "<<std::endl;    
      Dst->AddFile(setPath+"Strip19a_Pion_085pb_d_27Aug.root");    std::cout<<"Strip19a_Pion_085pb_d_27Aug.root"<<std::endl;
      Dst->AddFile(setPath+"Strip19a_Pion_118pb_a_27Aug.root");    std::cout<<"Strip19a_Pion_118pb_a_27Aug.root"<<std::endl;   
      // Dst->AddFile(setPath+"Strip19a_Pion_118pb_b_22Aug.root"); std::cout<<"Strip19a_Pion_118pb_b_22Aug.root"<<std::endl;

    }
    
    if(daughter=="lab4"){
      //Dst->AddFile(setPath+"Strip19a_Kaon_115pb_c_22Aug.root");  std::cout<<"Strip19a_Kaon_115pb_c_22Aug.root "<<std::endl;  
      Dst->AddFile(setPath+"Strip19a_Kaon_085pb_d_27Aug.root");     std::cout<<"Strip19a_Kaon_085pb_d_27Aug.root"<<std::endl;
      Dst->AddFile(setPath+"Strip19a_Kaon_118pb_a_27Aug.root");     std::cout<<"Strip19a_Kaon_118pb_a_27Aug.root"<<std::endl;
      //Dst->AddFile(setPath+"Strip19a_Kaon_118pb_b_22Aug.root");  std::cout<<"Strip19a_Kaon_118pb_b_22Aug.root"<<std::endl;

    }
    std::cout<<"\n Chain prepared... "<<std::endl;
    t =(TTree *) Dst;
  }
  
  
  if(intChain == 150){ 
    Dst = new TChain("DecayTree", "");
    std::cout<<"[strip19b, 170pb-1] daughter was "<<daughter<<", so adding to chain: ";    
    
    if(daughter=="lab3"){
      // // L0Global, HLT1Phys 
      // Dst->AddFile(setPath+"Strip19b_Pion_76pb_22Aug.root"); 
      // Dst->AddFile(setPath+"Strip19b_Pion_92pb_22Aug.root"); 
      // std::cout<<"adding Strip19b_Pion_76pb_22Aug.root and Strip19b_Pion_92pb_22Aug.root"<<std::endl;
      
      // // L0Global HLT1Global
      Dst->AddFile(setPath+"Strip19b_Pion_170pb_27Aug.root"); std::cout<<"adding Strip19b_Pion_170pb_27Aug.root"<<std::endl;
      
    }
    
    if(daughter=="lab4"){
      // // L0Global, HLT1Phys 
      //Dst->AddFile(setPath+"Strip19b_Kaon_76pb_22Aug.root");
      //Dst->AddFile(setPath+"Strip19b_Kaon_92pb_22Aug.root");
      //std::cout<<"adding Strip19b_Kaon_76pb_22Aug.root and Strip19b_Kaon_92pb_22Aug.root"<<std::endl;

      // // L0Global HLT1Global
      Dst->AddFile(setPath+"Strip19b_Kaon_76pb_27Aug.root"); 
      Dst->AddFile(setPath+"Strip19b_Kaon_92pb_27Aug.root"); 
      std::cout<<"adding Strip19b_Kaon_76pb_27Aug.root and Strip19b_Kaon_92pb_27Aug.root  "<<std::endl;
    }

    t =(TTree *) Dst;
    std::cout<<"prepared chain "<<std::endl;
  }
  
  if(intChain == 1520){ // // // Strip20 validation sample
    Dst = new TChain("DecayTree", "");
    
    if(daughter =="lab3") {
      Dst->AddFile(setPath+"Strip20_Pion_3pb.root");
      std::cout<<"chain prepared, added Strip20_Pion_3pb.root"<<std::endl;
    }
    if(daughter == "lab4"){
      Dst->AddFile(setPath+"Strip20_Kaon_3pb.root");
      std::cout<<"chain prepared, added Strip20_Kaon_3pb.root"<<std::endl;
    }
    
    t =(TTree *) Dst;
  }


  if(intChain == 1599){ // // // Strip19c 84pb
    Dst = new TChain("DecayTree", "");
    
    if(daughter =="lab3") {
      Dst->AddFile(setPath+"Strip19c_Pion_84pb_170912.root");
      Dst->AddFile(setPath+"Strip19c_Pion_67pb_170912.root");
      Dst->AddFile(setPath+"Strip19c_Pion_94pb_170912.root");
      std::cout<<"chain prepared, added Strip19c_Pion_84pb_170912.root, Strip19c_Pion_67pb_170912.root and Strip19c_Pion_94pb_170912.root "<<std::endl;
    }
    if(daughter == "lab4"){
      Dst->AddFile(setPath+"Strip19c_Kaon_84pb_170912.root");
      Dst->AddFile(setPath+"Strip19c_Kaon_67pb_170912.root");
      Dst->AddFile(setPath+"Strip19c_Kaon_94pb_170912.root");
      std::cout<<"chain prepared, added Strip19c_Kaon_84pb_170912.root Strip19c_Kaon_67pb_170912.root and Strip19c_Kaon_94pb_170912.root"<<std::endl;
    }
    
    t =(TTree *) Dst;
  }
 
  if(intChain == 2011){ // // // Strip17, proton 
    Dst = new TChain("DecayTree", "");
    
    //    Dst->AddFile(setPath+"S17_proton_PT0.root"); 
    //Dst->AddFile(setPath+"S17_proton_PT1.root"); 
    Dst->AddFile(setPath+"S17_proton_PT2.root"); 
    Dst->AddFile(setPath+"S17_proton_PT3.root"); 

    // int ptint; std::cout<<"************* Adding S17 proton file ********** which PT bin??  enter pt int 0 to 3"<<std::endl; std::cin>>ptint;        
    // if(ptint==0) { Dst->AddFile(setPath+"S17_proton_PT0.root"); std::cout<<" ==>  added file "<<setPath<<"S17_proton_PT0.root and int_pt = "<<ptint<<std::endl; }
    // else if(ptint==1) { Dst->AddFile(setPath+"S17_proton_PT1.root"); std::cout<<" ==>  added file "<<setPath<<"S17_proton_PT1.root and int_pt = "<<ptint<<std::endl; }
    // else if(ptint==2) { Dst->AddFile(setPath+"S17_proton_PT2.root"); std::cout<<" ==>  added file "<<setPath<<"S17_proton_PT2.root and int_pt = "<<ptint<<std::endl; }
    // else if(ptint==3) { Dst->AddFile(setPath+"S17_proton_PT3.root"); std::cout<<" ==>  added file "<<setPath<<"S17_proton_PT3.root and int_pt = "<<ptint<<std::endl; }
    // else {  Dst->AddFile(setPath+"S17_proton_PT3.root");  std::cout<<"pt int was wrong: "<<ptint<<"! \n I have added file "<<setPath<<"S17_proton_PT3.root" <<std::endl; }
    
    t = (TTree *) Dst;
  }
  
 if(intChain == 2012){ // // // Strip19a, proton 
    Dst = new TChain("DecayTree", "");
    
    //    Dst->AddFile(setPath+"S19a_proton_PT0.root");
    // Dst->AddFile(setPath+"S19a_proton_PT1.root");
    Dst->AddFile(setPath+"S19a_proton_PT2.root");
    Dst->AddFile(setPath+"S19a_proton_PT3.root");

    // int ptint; std::cout<<"************* Adding S19a proton file ********** which PT bin?? enter pt int 0 to 3"<<std::endl; std::cin>>ptint;
    // if(ptint==0) { Dst->AddFile(setPath+"S19a_proton_PT0.root"); std::cout<<" ==>  added file "<<setPath<<"S19a_proton_PT0.root and int_pt = "<<ptint<<std::endl; }
    // else if(ptint==1) { Dst->AddFile(setPath+"S19a_proton_PT1.root"); std::cout<<" ==>  added file "<<setPath<<"S19a_proton_PT1.root and int_pt = "<<ptint<<std::endl; }
    // else if(ptint==2) { Dst->AddFile(setPath+"S19a_proton_PT2.root"); std::cout<<" ==>  added file "<<setPath<<"S19a_proton_PT2.root and int_pt = "<<ptint<<std::endl; }
    // else if(ptint==3) { Dst->AddFile(setPath+"S19a_proton_PT3.root"); std::cout<<" ==>  added file "<<setPath<<"S19a_proton_PT3.root and int_pt = "<<ptint<<std::endl; }
    // else {  Dst->AddFile(setPath+"S19a_proton_PT3.root");  std::cout<<"pt int was wrong: "<<ptint<<"! \n I have added file "<<setPath<<"S19a_proton_PT3.root" <<std::endl; }

    t = (TTree *) Dst;
  }
  
  if(intChain == 2001){ // // // 2 fb-1 Strip20
    
    Dst = new TChain("DecayTree", "");
    
    std::stringstream ss_tmp; ss_tmp<<myPTbin; std::string ss_tmp_str = ss_tmp.str();
    pt_str = ss_tmp_str;
    
    if(daughter == "lab3") daughter_str="Pion";
    if(daughter == "lab4") daughter_str="Kaon";
    
    TString choose_magnet;
    if(mypolarity_str !="tot") choose_magnet = mypolarity_str;
    else choose_magnet = "MU";

    if(daughter == "lab4" || daughter == "lab3"){
      
      //file_Str = "Strip20_"+daughter_str+"_"+choose_magnet+"_PT"+pt_str+"_260313.root";
      file_Str = "Strip20_"+daughter_str+"_"+choose_magnet+"_PT"+pt_str+"_030713.root";
      std::cout<<"adding to chain "<<file_Str<<std::endl;   Dst->AddFile(setPath+file_Str);
    
      if(mypolarity_str =="tot") {
	//file_Str = "Strip20_"+daughter_str+"_MD_PT"+pt_str+"_260313.root";
	file_Str = "Strip20_"+daughter_str+"_MD_PT"+pt_str+"_030713.root";
	std::cout<<"adding to chain "<<file_Str<<std::endl;   Dst->AddFile(setPath+file_Str);
      }

    } // lab3/4
    
    else{
      if(myPTbin ==0) file_Str = "Strip20_Proton_"+mypolarity_str+"_PT0_260313.root";
      if(myPTbin ==1) file_Str = "Strip20_Proton_"+mypolarity_str+"_PT1_260313.root";
      if(myPTbin ==2) file_Str = "Strip20_Proton_"+mypolarity_str+"_PT3_1fb_260313.root"  ; // PT>3GeV
      if(myPTbin ==3) file_Str = "Strip20_Proton_"+mypolarity_str+"_PT3_1fb_260313.root"  ; // PT>3GeV
      Dst->AddFile(setPath+file_Str);
    }

    std::cout<<" chain prepared, ......  "<<std::endl;
    t =(TTree *) Dst;
  }

  
  if(intChain == 20011){ // // // 2fb-1 Strip20
    Dst = new TChain("DecayTree", "");
    if(daughter == "lab1"){
      
	file_Str = "Strip20_Proton_MU_PT3_1fb_260313.root"  ; // PT>3GeV
	Dst->AddFile(setPath+file_Str); std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;
	file_Str = "Strip20_Proton_MD_PT3_1fb_260313.root"  ; // PT>3GeV
	Dst->AddFile(setPath+file_Str); std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;

      std::cout<<" chain prepared, ......  "<<std::endl;
    }// lab 1
    
    else {
      std::cout<<"==> this should not be happening"<<std::endl;
      if(daughter == "lab4"){
	file_Str = "Strip20_Kaon_MU_PT0_260313.root";
	std::cout<<"adding to chain "<<setPath+file_Str<<" chain prepared, ......  "<<std::endl;
      }
      if(daughter == "lab3"){
	file_Str = "Strip20_Pion_MU_PT0_260313.root";
	std::cout<<"adding to chain "<<setPath+file_Str<<" chain prepared, ......  "<<std::endl;
      }
    } // else
    
    t =(TTree *) Dst;
  } // 20011

  
 if(intChain == 2002){ // // // Strip20, 430pb Magnet DN 350pb MagnetUP
    Dst = new TChain("DecayTree", "");
        
    if(daughter =="lab3") {
      
      if(myPTbin ==0) file_Str = "Strip20_Pion_Hlt1Glo_"+mypolarity_str+"_PT0_110413.root";
      if(myPTbin ==1) file_Str = "Strip20_Pion_Hlt1Glo_"+mypolarity_str+"_PT1_110413.root";
      if(myPTbin ==2) file_Str = "Strip20_Pion_Hlt1Glo_"+mypolarity_str+"_PT2_110413.root";
      if(myPTbin ==3) file_Str = "Strip20_Pion_Hlt1Glo_"+mypolarity_str+"_PT3_110413.root";
      Dst->AddFile(setPath+file_Str);
    }

    if(daughter == "lab4"){
      
      if(myPTbin ==0) file_Str = "Strip20_Kaon_Hlt1Glo_"+mypolarity_str+"_PT0_110413.root";
      if(myPTbin ==1) file_Str = "Strip20_Kaon_Hlt1Glo_"+mypolarity_str+"_PT1_110413.root";
      if(myPTbin ==2) file_Str = "Strip20_Kaon_Hlt1Glo_"+mypolarity_str+"_PT2_110413.root";
      if(myPTbin ==3) file_Str = "Strip20_Kaon_Hlt1Glo_"+mypolarity_str+"_PT3_110413.root";
      Dst->AddFile(setPath+file_Str);
    }
    
    if(daughter == "lab1"){
      
      if(myPTbin ==0) file_Str = "Strip20_Proton_Hlt1Glo_"+mypolarity_str+"_PT0_110413.root";
      if(myPTbin ==1) file_Str = "Strip20_Proton_Hlt1Glo_"+mypolarity_str+"_PT1_110413.root";
      if(myPTbin ==2) file_Str = "Strip20_Proton_Hlt1Glo_"+mypolarity_str+"_PT3_1fb_110413.root"  ; // PT>3GeV
      if(myPTbin ==3) file_Str = "Strip20_Proton_Hlt1Glo_"+mypolarity_str+"_PT3_1fb_110413.root"  ; // PT>3GeV
      Dst->AddFile(setPath+file_Str);
    }

    std::cout<<"adding to chain "<<setPath+file_Str<<" chain prepared, ......  "<<std::endl;
    t =(TTree *) Dst;
 }

 
 if(intChain == 20021){ // // // 880 pb of S20, L0Global,Hlt1Global
   
    Dst = new TChain("DecayTree", "");
    std::stringstream ss_tmp; ss_tmp<<myPTbin; std::string ss_tmp_str = ss_tmp.str();
    pt_str = ss_tmp_str;

    if(daughter == "lab1"){
      
      if(myPTbin ==0) {
	file_Str = "Strip20_Proton_Hlt1Glo_MU_PT0_110413.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl; Dst->AddFile(setPath+file_Str);
	file_Str = "Strip20_Proton_Hlt1Glo_MD_PT0_110413.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl; Dst->AddFile(setPath+file_Str);
      }
      if(myPTbin ==1) {
	file_Str = "Strip20_Proton_Hlt1Glo_MU_PT1_110413.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl; Dst->AddFile(setPath+file_Str);
	file_Str = "Strip20_Proton_Hlt1Glo_MD_PT1_110413.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl; Dst->AddFile(setPath+file_Str);
      }
      if(myPTbin ==2 || myPTbin==3){
	file_Str = "Strip20_Proton_Hlt1Glo_MU_PT3_1fb_110413.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl; Dst->AddFile(setPath+file_Str);
	file_Str = "Strip20_Proton_Hlt1Glo_MD_PT3_1fb_110413.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl; Dst->AddFile(setPath+file_Str);
      }
    } // lab1
    
    else {
      if(daughter == "lab3") daughter_str="Pion";
      if(daughter == "lab4") daughter_str="Kaon";    
      
      file_Str = "Strip20_"+daughter_str+"_Hlt1Glo_MU_PT"+pt_str+"_110413.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;  Dst->AddFile(setPath+file_Str);
      file_Str = "Strip20_"+daughter_str+"_Hlt1Glo_MD_PT"+pt_str+"_110413.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;  Dst->AddFile(setPath+file_Str);
    }

    std::cout<<" chain prepared, ......  "<<std::endl;
    t =(TTree *) Dst;
 }

 if(intChain == 20012){// S20, Kaon, with nPV binning
   
   Dst = new TChain("DecayTree", "");
   std::stringstream ss_tmp; ss_tmp<<myPTbin; std::string ss_tmp_str = ss_tmp.str();
   pt_str = ss_tmp_str;
   
   if(mypolarity_str !="tot"){
     file_Str = "Strip20_Kaon_"+mypolarity_str+"_PV"+myPV+"_PT"+pt_str+"_290613.root";
     std::cout<<"Adding to chain "<<file_Str<<std::endl;   Dst->AddFile(setPath+file_Str);
   }
   else{
     file_Str = "Strip20_Kaon_MU_PV"+myPV+"_PT"+pt_str+"_290613.root";     std::cout<<"Adding to chain "<<file_Str<<std::endl;   Dst->AddFile(setPath+file_Str);
     file_Str = "Strip20_Kaon_MD_PV"+myPV+"_PT"+pt_str+"_290613.root";     std::cout<<"Adding to chain "<<file_Str<<std::endl;   Dst->AddFile(setPath+file_Str);
   }

   std::cout<<" chain prepared, ......  "<<std::endl;
   t =(TTree *) Dst;   
   
 } // if intChain
 



 if(intChain == 2003){ 
   
   std::cout<<"Strip20r1, 335pb Magnet UP , 470pb Magnet DN "<<std::endl;
   std::stringstream ss_tmp; ss_tmp<<myPTbin; std::string ss_tmp_str = ss_tmp.str();
   pt_str = ss_tmp_str;

   Dst = new TChain("DecayTree", "");

   if(daughter =="lab3") daughter_str ="Pion";
   if(daughter =="lab4") daughter_str ="Kaon";
   if(daughter =="lab1") daughter_str ="Proton";
   
   if(daughter != "lab1") file_Str = "Strip20r1_"+daughter_str+"_"+mypolarity_str+"_PT"+pt_str+"_030713.root"; // 1204
   
   else {
     if(myPTbin ==0) file_Str = "Strip20r1_"+daughter_str+"_"+mypolarity_str+"_PT0_120413.root";
     if(myPTbin ==1) file_Str = "Strip20r1_"+daughter_str+"_"+mypolarity_str+"_PT1_120413.root";
     if(myPTbin >=2) file_Str = "Strip20r1_"+daughter_str+"_"+mypolarity_str+"_PT3_120413.root";
   }
   
   
   Dst->AddFile(setPath+file_Str);
   std::cout<<"adding to chain "<<setPath+file_Str<<" chain prepared, ......  "<<std::endl;
   t =(TTree *) Dst;
   
 } // 2003

if(intChain == 20031){ 
   
   std::cout<<"Strip20r1, 335pb+470pb"<<std::endl;
   
   Dst = new TChain("DecayTree", "");
   std::stringstream ss_tmp; ss_tmp<<myPTbin; std::string ss_tmp_str = ss_tmp.str();
   pt_str = ss_tmp_str;

   if(daughter != "lab1" || myPTbin <2){
     
     if(daughter =="lab3") daughter_str ="Pion";
     if(daughter =="lab4") daughter_str ="Kaon";
     if(daughter =="lab1") daughter_str ="Proton";
     
     //file_Str = "Strip20r1_"+daughter_str+"_MD_PT"+pt_str+"_120413.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;  Dst->AddFile(setPath+file_Str);
     //file_Str = "Strip20r1_"+daughter_str+"_MU_PT"+pt_str+"_120413.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;  Dst->AddFile(setPath+file_Str);

     file_Str = "Strip20r1_"+daughter_str+"_MD_PT"+pt_str+"_030713.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;  Dst->AddFile(setPath+file_Str);
     file_Str = "Strip20r1_"+daughter_str+"_MU_PT"+pt_str+"_030713.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;  Dst->AddFile(setPath+file_Str);
   } 
   
   else {
     daughter_str ="Proton";
     file_Str = "Strip20r1_"+daughter_str+"_MU_PT3_120413.root";  std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;  Dst->AddFile(setPath+file_Str);
     file_Str = "Strip20r1_"+daughter_str+"_MD_PT3_120413.root";  std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;  Dst->AddFile(setPath+file_Str);
   }
   
   std::cout<<"  chain prepared, ......  "<<std::endl;
   t =(TTree *) Dst;
   
 } // 20031


 if(intChain == 2004){ 
   
   std::cout<<"Strip20r1, 123pb (Mag UP)"<<std::endl;
   
   Dst = new TChain("DecayTree", "");
   std::stringstream ss_tmp; ss_tmp<<myPTbin; std::string ss_tmp_str = ss_tmp.str();
   pt_str = ss_tmp_str;

   if(daughter != "lab1" || myPTbin <2){
     
     if(daughter =="lab3") daughter_str ="Pion";
     if(daughter =="lab4") daughter_str ="Kaon";
     if(daughter =="lab1") daughter_str ="Proton";
     
     file_Str = "Strip20r1_"+daughter_str+"_Hlt1Glo_123pb_MU_PT"+pt_str+"_090613.root"; std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;  Dst->AddFile(setPath+file_Str);
   }
   
   // else {
   //   daughter_str ="Proton";
   //   file_Str = "Strip20r1_"+daughter_str+"_MD_PT3_120413.root";  std::cout<<"adding to chain "<<setPath+file_Str<<std::endl;  Dst->AddFile(setPath+file_Str);
   // }
   
   std::cout<<"  chain prepared, ......  "<<std::endl;
   t =(TTree *) Dst;
   
 } // 2004
 

                                                                                                            
 if(intChain == 16){ 
    Dst = new TChain("DecayTree", "");
    TString adding_file = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Fatima_file4.root";
    Dst->AddFile(adding_file);
    t =(TTree *) Dst;
    std::cout<<"added to chain:  "<<adding_file<<std::endl;
  }
  
  if(intChain == 17){ 
    Dst = new TChain("DecayTree", "");
    //TString adding_file = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/JpsieeK_S17_994pb_Job341_FileTrigger.root";
    //TString adding_file = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/Fatima_fileTrigger.root";
    TString adding_file = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/JpsieeK_MC11a_Sim05a_MD_Job434_FileTrigger.root"; // MC file 
    Dst->AddFile(adding_file);

    t =(TTree *) Dst->CopyTree(baseCut);
    std::cout<<"added to chain: "<<adding_file<<" with baseCut \n "<<baseCut<<" \n so has entries "<<t->GetEntries()<<std::endl;
   
  }

  if(intChain == 18){ 
    Dst = new TChain("DecayTree", "");
    
    //    TString adding_file = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/JpsimmK_S17_1011pb_Job342_FileTrigger.root";
    TString adding_file = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/JpsimmK_S17_1011pb_Job342_For_L0HLT1.root";
    //TString adding_file = "/Users/fatimasoomro/WorkFiles/AllRootFiles/B2EMuNtuples/JpsimmK_MC11a_Sim05_MD_Job344_FileTrigger.root";
    Dst->AddFile(adding_file);

    t =(TTree *) Dst->CopyTree(baseCut);
    std::cout<<"added to chain: "<<adding_file<<" with baseCut \n "<<baseCut<<" \n so has entries "<<t->GetEntries()<<std::endl;
    
  }

  if(intChain == 19){ 

    Dst = new TChain("AllTIS", "");
    std::cout<<"daughter was "<<daughter<<std::endl;
    
    if(daughter=="piplus0"){
      Dst->AddFile(setPath+"180/Pion_v2/Merged0_250.root");   std::cout<<"adding 180/Pion_v2/Merged0_250.root"<<std::endl;
      Dst->AddFile(setPath+"180/Pion_v2/Merged250_502.root"); std::cout<<"adding 180/Pion_v2/Merged250_502.root"<<std::endl;
    }
    
    if(daughter=="Kminus"){
      Dst->AddFile(setPath+"180/Kaon_v2/Merged0_250.root");   std::cout<<"adding 180/Kaon_v2/Merged0_250.root"<<std::endl;
      Dst->AddFile(setPath+"180/Kaon_v2/Merged250_502.root"); std::cout<<"adding 180/Kaon_v2/Merged250_502.root"<<std::endl;
    }
    
    t =(TTree *) Dst;
    std::cout<<"==> prepared Chain <=="<<std::endl;
  }

  
  return t;

}


// For results in June 2012
// Dst->AddFile(setPath+"267/Pion_50_v2.root");  // 154pb, stripping19, 19a, June2012
// Dst->AddFile(setPath+"267/Pion_100_v2.root");
// Dst->AddFile(setPath+"267/Pion_150_v2.root");
// Dst->AddFile(setPath+"267/Pion_200_v2.root");
// Dst->AddFile(setPath+"267/Pion_224_v2.root");

// Dst->AddFile(setPath+"267/Kaon_50_v2.root");   // 154pb, stripping19, 19a, June2012
// Dst->AddFile(setPath+"267/Kaon_100_v2.root");
// Dst->AddFile(setPath+"267/Kaon_150_v2.root");
// Dst->AddFile(setPath+"267/Kaon_200_v2.root");
// Dst->AddFile(setPath+"267/Kaon_224_v2.root");
    

  //TChain *lam = new TChain ("LamTuple/DecayTree", "");
  //TChain *ks = new TChain ("KsTuple/DecayTree", "");
  //TChain *Dst = new TChain ("DstTuple/DecayTree", "");
  //char tt[100];
  //const int myFiles = 318;
  //  std::cout<<"===> using  "<<myFiles<<" files only "<<std::endl;
  
  //   for (int i=0; i<425; i++){  //425 subjobs
  //     {
  //       sprintf(tt,"/Shared/gangadir/workspace/fsoomro/LocalXML/110/%i/output/MisIDtuple.root",i);
  //       Dst->AddFile(tt);   
  //     }
  //   }
  
  //   for (int i=0; i<myFiles; i++) {   // 318 subjobs
  
  //     sprintf(tt,"/Shared/gangadir/workspace/fsoomro/LocalXML/123/%i/output/MisIDtuple.root",i);
  //     Dst->AddFile(tt);
  //   }
  //   TTree *t = (TTree *) Dst;
  //   return t;
  
  ///   123 -> 318 subjobs, 124-> 246 subjobs
  // // ====== 600 + 392 pb (job 123, 124) with ALL TIS on the pion ===== // //
  //  TChain *Dst = new TChain ("AllTIS", "");
  //   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/123/PionAllTIS_a.root");
  //   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/123/PionAllTIS_b.root");
  //   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/123/PionAllTIS_c.root");
  //   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/123/PionAllTIS_d.root");
  //Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/124/PionAllTIS_e.root");
  //Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/124/PionAllTIS_f.root");
 

// used until 11 Dec 2011  
  // // ====== the 600 + 300 pb (job 120, 110) with ALL TIS on the pion ===== // //
  //  TChain *Dst = new TChain ("AllTIS", "");
//   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/120/PionAllTIS_a.root");
//   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/120/PionAllTIS_b.root");
//   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/120/PionAllTIS_c.root");
//   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/120/PionAllTIS_d.root");
//   //Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/110/PionAllTIS.root"); // 300pb, all TIS on the pion
//   TTree *t = Dst->CopyTree(baseCut);
//   return t;
 
  
  // //  ======= the 300pb, without any cut =======// //
  //   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/110/output/50.root");
   //   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/110/output/100.root");
   //   Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/110/output/150.root");
//    Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/110/output/200.root");
//    Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/110/output/250.root");
//    Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/110/output/300.root");
//    Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/110/output/350.root");
//    Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/110/output/400.root");
//    Dst->AddFile("/Shared/gangadir/workspace/fsoomro/LocalXML/110/output/425.root");




