/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id: RooGaussianTrunk.h,v 1.16 2007/07/12 20:30:49 wouter Exp $
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
#ifndef ROO_GAUSSIAN_TRUNK
#define ROO_GAUSSIAN_TRUNK

#include "RooAbsPdf.h"
#include "RooRealProxy.h"

class RooRealVar;

class RooGaussianTrunk : public RooAbsPdf {
public:
  RooGaussianTrunk() {} ;
  RooGaussianTrunk(const char *name, const char *title,
	      RooAbsReal& _x, RooAbsReal& _mean, RooAbsReal& _sigma, RooAbsReal& _min, RooAbsReal& _max);
  RooGaussianTrunk(const RooGaussianTrunk& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new RooGaussianTrunk(*this,newname); }
  inline virtual ~RooGaussianTrunk() { }

  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;

  Int_t getGenerator(const RooArgSet& directVars, RooArgSet &generateVars, Bool_t staticInitOK=kTRUE) const;
  void generateEvent(Int_t code);

protected:

  RooRealProxy x ;
  RooRealProxy mean ;
  RooRealProxy sigma ;
  RooRealProxy min ;
  RooRealProxy max ;
  
  Double_t evaluate() const ;

private:

  ClassDef(RooGaussianTrunk,1) // Gaussian PDF
};

#endif
