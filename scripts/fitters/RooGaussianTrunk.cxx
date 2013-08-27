/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 * @(#)root/roofit:$Id: RooGaussianTrunk.cxx 44982 2012-07-10 08:36:13Z moneta $
 * Authors:                                                                  *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *                                                                           *
 * Copyright (c) 2000-2005, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/

//////////////////////////////////////////////////////////////////////////////
//
// BEGIN_HTML
// Plain Gaussian p.d.f
// END_HTML
//

#include "RooFit.h"

#include "Riostream.h"
#include "Riostream.h"
#include <math.h>

#include "RooGaussianTrunk.h"
#include "RooAbsReal.h"
#include "RooRealVar.h"
#include "RooRandom.h"
#include "RooMath.h"

using namespace std;

ClassImp(RooGaussianTrunk)


//_____________________________________________________________________________
RooGaussianTrunk::RooGaussianTrunk(const char *name, const char *title,
			 RooAbsReal& _x, RooAbsReal& _mean,
			 RooAbsReal& _sigma,
                         RooAbsReal& _min,
                         RooAbsReal& _max) :
  RooAbsPdf(name,title),
  x("x","Observable",this,_x),
  mean("mean","Mean",this,_mean),
  sigma("sigma","Width",this,_sigma),
  min("min","min",this,_min),
  max("max","max",this,_max)
{
}



//_____________________________________________________________________________
RooGaussianTrunk::RooGaussianTrunk(const RooGaussianTrunk& other, const char* name) : 
  RooAbsPdf(other,name), x("x",this,other.x), mean("mean",this,other.mean),
  sigma("sigma",this,other.sigma),min("min",this,other.min),
  max("max",this,other.max)
{
}



//_____________________________________________________________________________
Double_t RooGaussianTrunk::evaluate() const
{
  Double_t var = x;
  if (var<min) {return 0.;}
  if (var>max) {return 0.;}
  Double_t arg= var - mean;  
  Double_t sig = sigma ;
  Double_t ret =exp(-0.5*arg*arg/(sig*sig)) ;
//   cout << "gauss(" << GetName() << ") x = " << x << " mean = " << mean << " sigma = " << sigma << " ret = " << ret << endl ;
  return ret ;
}



//_____________________________________________________________________________
Int_t RooGaussianTrunk::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* /*rangeName*/) const 
{
  if (matchArgs(allVars,analVars,x)) return 1 ;
  if (matchArgs(allVars,analVars,mean)) return 2 ;
  return 0 ;
}



//_____________________________________________________________________________
Double_t RooGaussianTrunk::analyticalIntegral(Int_t code, const char* rangeName) const 
{
  assert(code==1 || code==2) ;

  static const Double_t root2 = sqrt(2.) ;
  static const Double_t rootPiBy2 = sqrt(atan2(0.0,-1.0)/2.0);
  Double_t xscale = root2*sigma;
  Double_t ret = 0;
  if(code==1){
    Double_t range_min = x.min(rangeName);
    Double_t range_max = x.max(rangeName);
    if (range_min < min) { range_min = min; }
    if (range_max > max) { range_max = max; }
    ret = rootPiBy2*sigma*(RooMath::erf((range_max-mean)/xscale)-RooMath::erf((range_min-mean)/xscale));
//     cout << "Int_gauss_dx(mean=" << mean << ",sigma=" << sigma << ", xmin=" << x.min(rangeName) << ", xmax=" << x.max(rangeName) << ")=" << ret << endl ;
  } else if(code==2) {
    ret = rootPiBy2*sigma*(RooMath::erf((mean.max(rangeName)-x)/xscale)-RooMath::erf((mean.min(rangeName)-x)/xscale));
  } else{
    cout << "Error in RooGaussianTrunk::analyticalIntegral" << endl;
  }
  return ret ;

}




//_____________________________________________________________________________
Int_t RooGaussianTrunk::getGenerator(const RooArgSet& directVars, RooArgSet &generateVars, Bool_t /*staticInitOK*/) const
{
//   if (matchArgs(directVars,generateVars,x)) return 1 ;  
//   if (matchArgs(directVars,generateVars,mean)) return 2 ;  
  return 0 ;
}



//_____________________________________________________________________________
void RooGaussianTrunk::generateEvent(Int_t code)
{
  assert(code==1 || code==2) ;
  Double_t xgen ;
  if(code==1){
    while(1) {    
      xgen = RooRandom::randomGenerator()->Gaus(mean,sigma);
      if (xgen<x.max() && xgen>x.min()) {
	x = xgen ;
	break;
      }
    }
  } else if(code==2){
    while(1) {    
      xgen = RooRandom::randomGenerator()->Gaus(x,sigma);
      if (xgen<mean.max() && xgen>mean.min()) {
	mean = xgen ;
	break;
      }
    }
  } else {
    cout << "error in RooGaussianTrunk generateEvent"<< endl;
  }

  return;
}

