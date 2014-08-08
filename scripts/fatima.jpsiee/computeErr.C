#include "myIncludes.h"

double *myError(double etot,double etoterr, double ebg, double ebgerr, double nsig, double  nsigerr, double nbg, double nbgerr, double rho, bool doVerbose ){

  double *theResult = new double[2];

  if( nsig>0 && etot > 0.0 && ebg >0.0 && nbg >0.0){ 
    
    double sb = nsig+nbg;
    //double errsb = TMath::Sqrt( nsigerr*nsigerr + nbgerr*nbgerr + 2*nbgerr*nsigerr );
    
    double esig = etot*(sb/nsig) - ebg*(nbg/nsig);  //( etot - ebg*nbg/(sb))*(sb/nsig); 
    
    // (a*etoterr)**2 +(b*ebgerr)**2+(c*nsigerr)**2+(d*nbgerr)**2+2*c*rho*d*nsigerr*nbgerr 

    // a=d/detot  =  (S+B)/S 
    // b=d/debg =  -B/S
    // c=d/dS = -B/S**2*(etot-ebg)
    // d=d/dB = (etot-ebg)/S

    double var_a = sb/nsig;
    double var_b = -nbg/nsig;
    double var_c = - (etot-ebg)*nbg/(nsig*nsig);
    double var_d = (etot-ebg)/nsig;

    double esigerr = TMath::Sqrt( (var_a*etoterr)*(var_a*etoterr) + (var_b*ebgerr)*(var_b*ebgerr) + (var_c*nsigerr)*(var_c*nsigerr)+ (var_d*nbgerr)*(var_d*nbgerr)+ 2*var_c*var_d*rho*nsigerr*nbgerr );
    
    if( esigerr/esig > 0.1 && doVerbose ) 
      {
	std::cout<<"--> etot "<<etot<<" -> "<<100*etoterr/etot<<"%,  ebg "<<ebg<<" -> "<<100*ebgerr/ebg<<"%, nSig "<<nsig<<" -> "<<100*nsigerr/nsig<<"%, nBG "<<nbg<<" -> "<<100*nbgerr/nbg<<"%, rho is "<<rho;
	std::cout<<" \n The vars "<< var_a<<" "<<var_b<<" "<<var_c<<" "<<var_d<<" and the error "<<esigerr<<std::endl;
	
	std::cout<<"TMath::Sqrt( ("<<var_a<<"*"<<etoterr<<")*("<<var_a<<"*"<<etoterr<<") + ("<<var_b<<"*"<<ebgerr<<")*("<<var_b<<"*"<<ebgerr<<") + ("<<var_c<<"*"<<nsigerr<<")*("<<var_c<<"*"<<nsigerr<<")+ ("<<var_d<<"*"<<nbgerr<<")*("<<var_d<<"*"<<nbgerr<<")+ 2*"<<var_c<<"*"<<var_d<<"*"<<rho<<"*"<<nsigerr<<"*"<<nbgerr<<")"<<std::endl;

      }
    theResult[0] = esig; theResult[1] =  esigerr;
    
  }
  else {
    theResult[0] = 0; theResult[1]=0;
    if(doVerbose) std::cout<<"Didnt do calculation, nsig, nbg = "<<nsig<<" "<<nbg<<std::endl;
  }
  


  return  theResult;
}


//    Floating Parameter    FinalValue +/-  Error
//   --------------------  --------------------------
//                  alpha    4.0737e+00 +/-  5.53e+00
//                  bkgc1    8.1253e-01 +/-  4.48e-01
//                  bkgc2   -3.8663e-04 +/-  2.13e-04
//                      n    2.2938e+00 +/-  1.16e+01
//                    nbg    5.4998e+00 +/-  5.45e+00
//                   nsig    6.8795e+00 +/-  4.17e+00
//                  sigma    1.5000e+01 +/-  1.43e+00
