/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id: RooChebychevTrunk.h,v 1.6 2007/05/11 09:13:07 verkerke Exp $
 * Authors:                                                                  *
 *   GR, Gerhard Raven,   UC San Diego, Gerhard.Raven@slac.stanford.edu
 *                                                                           *
 * Copyright (c) 2000-2005, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/
#ifndef ROO_CHEBYCHEV
#define ROO_CHEBYCHEV

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooListProxy.h"

class RooRealVar;
class RooArgList ;

class RooChebychevTrunk : public RooAbsPdf {
public:

  RooChebychevTrunk() ;
  RooChebychevTrunk(const char *name, const char *title,
               RooAbsReal& _x, const RooArgList& _coefList,
               RooAbsReal& _min, RooAbsReal& _max) ;

  RooChebychevTrunk(const RooChebychevTrunk& other, const char* name = 0);
  virtual TObject* clone(const char* newname) const { return new RooChebychevTrunk(*this, newname); }
  inline virtual ~RooChebychevTrunk() { }

  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;

private:

  RooRealProxy _x;
  RooListProxy _coefList ;
  RooRealProxy _min ;
  RooRealProxy _max ;

  Double_t evaluate() const;
  Double_t evalAnaInt(const Double_t x) const;

  ClassDef(RooChebychevTrunk,1) // Chebychev polynomial PDF
};

#endif
