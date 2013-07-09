rootlogon() {
  gSystem->Load("libRooFit");
  using namespace RooFit;
//  gROOT->ProcessLine(".L RooGausLandau.cxx+");
//  gROOT->ProcessLine(".L src/RooSimpleAcceptance.cxx+");
//  gROOT->ProcessLine(".L src/RooExpAcceptance.cxx+");
//  gROOT->ProcessLine(".L Bs2DsKTool.cxx+");
//  gROOT->ProcessLine(".L Simulation.C");
//  gROOT->ProcessLine(".L Fit.C");
//  gROOT->ProcessLine(".x Style.C");
  gROOT->ProcessLine(".x lhcbstyle.C");
//  gROOT->SetStyle("Plain");
  gROOT->ProcessLine("TBrowser t;");
}
