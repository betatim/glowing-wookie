#include "fitMass.h"


TString fitMass::momentumCut(int i){
  
  TString pBins [11] = { 
    daughter+"_P/1000>0.0 && "+daughter+"_P/1000<= 5.0" 
    ,daughter+"_P/1000>5.0 && "+daughter+"_P/1000 <=10.0"
    ,daughter+"_P/1000>10.0 && "+daughter+"_P/1000 <=15.0"
    ,daughter+"_P/1000>15.0 && "+daughter+"_P/1000 <=20.0"
    ,daughter+"_P/1000>20.0 && "+daughter+"_P/1000 <=25.0"
    ,daughter+"_P/1000>25.0 && "+daughter+"_P/1000 <=30.0"
    ,daughter+"_P/1000>30.0 && "+daughter+"_P/1000 <=35.0"
    ,daughter+"_P/1000>35.0 && "+daughter+"_P/1000 <=40.0"
    ,daughter+"_P/1000>40.0 && "+daughter+"_P/1000 <=50.0"
    ,daughter+"_P/1000>50.0 && "+daughter+"_P/1000 <=60.0"
    ,daughter+"_P/1000>60.0 && "+daughter+"_P/1000 <=70.0"
  };
  
  if(daughter == "lab1" && myPTbin>1. && i <2.){
    pBins[0] = daughter+"_P/1000>0.0 && "+daughter+"_P/1000<= 40.0";
    pBins[1] = daughter+"_P/1000>40.0";// && "+daughter+"_P/1000<= 70.0";
    std::cout<<"daughter was "<<daughter<<" and PTbin "<<myPTbin<<" so the cut "<<i<<" is "<<pBins[i]<<std::endl;
  }
  //pBins[0] = daughter+"_PT <=55000"; // special bin, 220613
    
  // TString pBins [3] = { daughter+"_P/1000>0.0 && "+daughter+"_P/1000< 20.0"
  // 			,daughter+"_P/1000>20.0 && "+daughter+"_P/1000 <40.0"
  // 			,daughter+"_P/1000>40.0"
  // };
  

  TString PtBins[4] = { daughter+"_PT/1000 >0.8 && "+daughter+"_PT/1000 < 1.7"
			,daughter+"_PT/1000 >1.7 && "+daughter+"_PT/1000 < 3.0"
			,daughter+"_PT/1000 >3.0 && "+daughter+"_PT/1000 < 5.0"
			,daughter+"_PT/1000 >5.0 && "+daughter+"_PT/1000 < 10.0"
  };

  std::cout<<"\n \n pBin = "<<i<<" PTBin "<<myPTbin<<std::endl;
  //"  (and int_c = "<< int_c<<". Remember that if int_c <0, loop will be executed only for one PT bin. In other words, will make no PT binning) "<<std::endl;
  TString theCut = pBins[i]+" && "+PtBins[myPTbin];   
  if( (int_c < 0) || 1)  theCut = pBins[i];   
  
  //// Or you can write, by hand, any cut you want to make, such as below, and run the code ovr just one 'bin'  
  //theCut =            "piplus0_P/1000<70.0 && piplus0_PT/1000>0.8 && piplus0_PT/1000 <10.0";
  // theCut = theCut+ "&& Kminus_P/1000 <70.0 && Kminus_PT/1000> 0.8 && Kminus_PT/1000  <10.0";
  
  std::cout<<" ---> Returning momentum cut: "<<theCut<<" note that I do not make PT binning anymore !!! \n"<<std::endl;
  
  return theCut;

}


TString fitMass::momentumCutJpsi(int i){

  TString pBins [6] = { daughter+"_P/1000>5.0 && "+daughter+"_P/1000 <10.0"
  			,daughter+"_P/1000>10.0 && "+daughter+"_P/1000 <20.0"
  			,daughter+"_P/1000>20.0 && "+daughter+"_P/1000 <30.0"
  			,daughter+"_P/1000>30.0 && "+daughter+"_P/1000 <40.0"
  			,daughter+"_P/1000>40.0 && "+daughter+"_P/1000 <60.0"
  			,daughter+"_P/1000>60.0 && "+daughter+"_P/1000 <100.0"
			
  };

  // // // 5-10, 10-20, 20-30, 30-40, 40-60, 60-100 [used at least until 220812]

  TString ptBins [6] = { daughter+"_PT/1000>0.0 && "+daughter+"_PT/1000 <1.0"
  			,daughter+"_PT/1000>1.0 && "+daughter+"_PT/1000 <2.0"
  			,daughter+"_PT/1000>2.0 && "+daughter+"_PT/1000 <3.0"
  			,daughter+"_PT/1000>3.0 && "+daughter+"_PT/1000 <4.0"
  			,daughter+"_PT/1000>4.0 && "+daughter+"_PT/1000 <6.0"
  			,daughter+"_PT/1000>6.0 && "+daughter+"_PT/1000 <20.0"
			
  };

  TString mycircle = "( (12000/"+daughter+"_PZ)*TMath::Sqrt("+daughter+"_PX*"+daughter+"_PX +"+daughter+"_PY*"+daughter+"_PY) )";
  TString circle_bin[6] = { mycircle+"<500."
			    ,mycircle+">500 && "+mycircle+"<700."
			    ,mycircle+">700 && "+mycircle+"<900."
			    ,mycircle+">900 && "+mycircle+"<1100."
			    ,mycircle+">1100 && "+mycircle+"<1500."
			    ,mycircle+">1500."
  };
  
  TString my_x = "12000.*TMath::Abs("+daughter+"_PX/"+daughter+"_PZ) ";
  TString my_y = "12000.*TMath::Abs("+daughter+"_PY/"+daughter+"_PZ) ";
  TString square_bin[3] = { "("+my_x+"> 325.1  || "+my_y+"> 243.8 ) && ("+my_x+"< 975.2  && "+my_y+"< 731.4)",
  			    "("+my_x+"> 975.2  || "+my_y+"> 731.4 ) && ("+my_x+"< 1950.4 && "+my_y+"< 1219.0)",
  			    "("+my_x+"> 1950.4 || "+my_y+"> 1219.0) && ("+my_x+"< 3900.8 && "+my_y+"< 3169.4)" };
  // TString square_bin[6] = { "("+my_x+"> 325.1  || "+my_y+"> 243.8 ) && ("+my_x+"< 600.0  && "+my_y+"< 430.0)",
  // 			    "("+my_x+"> 600.0  || "+my_y+"> 430.0 ) && ("+my_x+"< 975.2  && "+my_y+"< 731.4)",
  // 			    "("+my_x+"> 975.2  || "+my_y+"> 731.4 ) && ("+my_x+"< 1450.4 && "+my_y+"< 980.0)",
  // 			    "("+my_x+"> 1450.0 || "+my_y+"> 980.0 ) && ("+my_x+"< 1950.4 && "+my_y+"< 1219.0)",
  // 			    "("+my_x+"> 1950.4 || "+my_y+"> 1219.0) && ("+my_x+"< 2900.0 && "+my_y+"< 2100.4)",
  // 			    "("+my_x+"> 2900.0 || "+my_y+"> 2100.0) && ("+my_x+"< 3900.8 && "+my_y+"< 3169.4)" };


  std::cout<<"\n \n pBin = "<<i<<" PTBin "<<myPTbin<<std::endl;
  
  TString theCut = "";
  if(i<0 || i>5) theCut = daughter+"_P>0.0"; 
  else {
    if(int_c < 0)  theCut = pBins[i];   
    else theCut = ptBins[i]+" && "+pBins[myPTbin]; 
  }
  
  if(false) theCut = circle_bin[i];
  if(true && i<3) theCut = square_bin[i];
  
  std::cout<<" ---> Returning momentum cut: "<<theCut<<"\n"<<std::endl;
  
  return theCut;
  
}

 
 

TString fitMass::TwoDCutJpsi(int ip_int){
  
  TString theCut = "";
  
  TString tisCut = "BplusHlt2Phys_TIS == 1 ";
  TString tosCut = "BplusHlt2Phys_TOS == 1 ";
  //  TString tisCut = "BplusHlt2Topo2BodyBBDTDecision_TIS == 1 ";
  //  TString tosCut = "BplusHlt2Topo2BodyBBDTDecision_TOS == 1 ";
  
  // TString tisCut = "KplusHlt2Topo2BodyBBDTDecision_TIS == 1 && ((Kplus_ID>0 && eminusHlt2Topo2BodyBBDTDecision_TIS == 1 ) || (Kplus_ID<0 && eplusHlt2Topo2BodyBBDTDecision_TIS == 1))";
  //  TString tosCut = "KplusHlt2Topo2BodyBBDTDecision_TOS == 1 && ((Kplus_ID>0 && eminusHlt2Topo2BodyBBDTDecision_TOS == 1 ) || (Kplus_ID<0 && eplusHlt2Topo2BodyBBDTDecision_TOS == 1))";
  
  // TString tisCut = "BplusHlt2Topo2BodyBBDTDecision_TIS == 1 ";
  // TString tosCut = "BplusHlt2Topo2BodyBBDTDecision_TOS == 1 ";
  
  TString pBins [4] = { tisCut+" && "+tosCut
			,tosCut
			," Bplus_MM>2000."
			,tisCut
  };
  
  theCut = pBins[ip_int];
  
  // //  n(tis&tos),   ntos,   ntrig,   ntis
  
  // TString ip_Bins [6] = { "max(eplus_IP_OWNPV,  eminus_IP_OWNPV)>0.0  && max(eplus_IP_OWNPV, eminus_IP_OWNPV)<0.05"
  // 			  ,"max(eplus_IP_OWNPV, eminus_IP_OWNPV)>0.05 && max(eplus_IP_OWNPV, eminus_IP_OWNPV)<0.1"
  // 			  ,"max(eplus_IP_OWNPV, eminus_IP_OWNPV)>0.1  && max(eplus_IP_OWNPV, eminus_IP_OWNPV)<0.15"
  // 			  ,"max(eplus_IP_OWNPV, eminus_IP_OWNPV)>0.15 && max(eplus_IP_OWNPV, eminus_IP_OWNPV)<0.2"
  // 			  ,"max(eplus_IP_OWNPV, eminus_IP_OWNPV)>0.2  && max(eplus_IP_OWNPV, eminus_IP_OWNPV)<0.5"
  // 			  ,"max(eplus_IP_OWNPV, eminus_IP_OWNPV)>0.5  && max(eplus_IP_OWNPV, eminus_IP_OWNPV)<10."
  // };
  // TString pt_Bins [5] = { "max(eplus_PT/1000., eminus_PT/1000.) >0.0 && max(eplus_PT/1000., eminus_PT/1000.)<2."
  // 			  ,"max(eplus_PT/1000., eminus_PT/1000.) >2.0 && max(eplus_PT/1000., eminus_PT/1000.)<4."
  // 			  ,"max(eplus_PT/1000., eminus_PT/1000.) >4.0 && max(eplus_PT/1000., eminus_PT/1000.)<6."
  // 			  ,"max(eplus_PT/1000., eminus_PT/1000.) >6.0 && max(eplus_PT/1000., eminus_PT/1000.)<10."
  // 			  ,"max(eplus_PT/1000., eminus_PT/1000.) >10.0 && max(eplus_PT/1000., eminus_PT/1000.)<15."
  // };
  
  std::cout<<"===>  in 2Dcut for Jpsi, I am returning cut: "<<theCut<<"\n"<<std::endl;
  return theCut;
  
}



TString fitMass::CutSingleMuonTriggerEff(int i){

 TString ip_Bins [6] = {   daughter+"_IP_OWNPV> 0.0   && "+daughter+"_IP_OWNPV <0.05"
			  ,daughter+"_IP_OWNPV >0.05 && "+daughter+"_IP_OWNPV <0.1"
			  ,daughter+"_IP_OWNPV >0.1  && "+daughter+"_IP_OWNPV <0.15"
			  ,daughter+"_IP_OWNPV >0.15 && "+daughter+"_IP_OWNPV <0.2"
			  ,daughter+"_IP_OWNPV >0.2  && "+daughter+"_IP_OWNPV <0.5"
			  ,daughter+"_IP_OWNPV >0.5  && "+daughter+"_IP_OWNPV <10."
  };
  
  TString pt_Bins [5] = { daughter+"_PT/1000.  >0.0  && "+daughter+"_PT/1000. <2."
			  ,daughter+"_PT/1000. >2.0  && "+daughter+"_PT/1000. <4."
			  ,daughter+"_PT/1000. >4.0  && "+daughter+"_PT/1000. <6."
			  ,daughter+"_PT/1000. >6.0  && "+daughter+"_PT/1000. <10."
			  ,daughter+"_PT/1000. >10.0 && "+daughter+"_PT/1000. <15."
  };
  
  TString theCut = pt_Bins[i]+" && "+ip_Bins[myPTbin];   
  if( (int_c < 0) )  theCut = pt_Bins[i];   
  std::cout<<"\n \n In function CutSingleMuonTriggerEff: ptBin = "<<i<<" ipBin "<<myPTbin<<" I am returning cut \n "<<theCut<<" int_c was "<<int_c<<std::endl;
  
  return theCut;
  
}

TString fitMass::CutJpsiMuonPlusTrack(int ip_int){
  
  TString tisCut = "BplusHlt2Phys_TIS == 1";
  TString tosCut = "BplusHlt2Phys_TOS == 1 ";
  
  TString pBins [4] = { tisCut+" && "+tosCut
			,tosCut
			," Bplus_MM>2000."
			,tisCut
  };
  
  TString theCut = pBins[ip_int];
  
  // //  n(tis&tos),   ntos,   ntrig,   ntis
  
  std::cout<<"===>  in 2Dcut for Jpsi, I am returning cut: "<<theCut<<"\n"<<std::endl;
  return theCut;
  
}




