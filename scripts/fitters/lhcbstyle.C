{
////////////////////////////////////////////////////////////////////
// PURPOSE:
//
// This macro defines a reasonable style for (black-and-white) 
// "publication quality" ROOT plots. The default settings contain 
// many features that are either not desirable for printing on white 
// paper or impair the general readibility of plots.
//
// USAGE:
//
// Simply include the line
//   gROOT->ProcessLine(".x $LHCBSTYLE/root/lhcbstyle.C");
// at the beginning of your root macro.
//
// SOME COMMENTS:
//
// Statistics and fit boxes:
//
// "Decorative" items around the histogram are kept to a minimum.
// In particular there is no box with statistics or fit information.
// You can easily change this either by editing your private copy
// of this style file or by calls to "gStyle" in your macro.
// For example, 
//   gStyle->SetOptFit(1011);
// will add some fit information.
//
// Font:
// 
// The font is chosen to be 62, i.e.helvetica-bold-r-normal with
// precision 2. Font is of course a matter of taste, but most people
// will probably agree that Helvetica bold gives close to optimal
// readibility in presentations. It appears to be the ROOT default, 
// and since there are still some features in ROOT that simply won't 
// respond to any font requests, it is the wise choice to avoid 
// ugly font mixtures on the same plot... The precision of the font (2)
// is chosen in order to have a rotatable and scalable font. Be sure
// to use true-type fonts! I.e.
// Unix.*.Root.UseTTFonts: true  in your .rootrc file. 
//
// "Landscape histograms":
//
// The style here is designed for more or less quadratic plots.
// For very long histograms, adjustements are needed. For instance, 
// for a canvas with 1x5 histograms:
//  TCanvas* c1 = new TCanvas("c1", "L0 muons", 600, 800);
//  c1->Divide(1,5);
// adaptions like the following will be needed:
//  gStyle->SetTickLength(0.05,"x");
//  gStyle->SetTickLength(0.01,"y");
//  gStyle->SetLabelSize(0.15,"x");
//  gStyle->SetLabelSize(0.1,"y");
//  gStyle->SetStatW(0.15);
//  gStyle->SetStatH(0.5);
//
////////////////////////////////////////////////////////////////////

/*cout << "executing lhcbStyle.C:" << endl;
cout << "                      " << endl;
cout << "                      " << endl;
cout << "                         $      $   $   $$$   $    " << endl;
cout << "                         $      $   $  $      $    " << endl;
cout << "                         $      $$$$$  $      $$$  " << endl;
cout << "                         $      $   $  $      $  $ " << endl;
cout << "                         $$$$$  $   $   $$$   $$$  " << endl;
cout << " " << endl;
cout << "                           LHCb ROOT style file " << endl;
cout << " " << endl;
cout << 
"     Problems, suggestions, contributions to Thomas.Schietinger@cern.ch" << endl;
cout << " " << endl;*/

//gROOT->Reset();

TStyle *lhcbStyle= new TStyle("lhcbStyle","Thomas personal plots style");

// use helvetica-bold-r-normal, precision 2 (rotatable)
Int_t lhcbFont = 62;
// line thickness
Double_t lhcbWidth = 3.00;

// use plain black on white colors
lhcbStyle->SetFrameBorderMode(0);
lhcbStyle->SetCanvasBorderMode(0);
lhcbStyle->SetPadBorderMode(0);
//lhcbStyle->SetPadColor(0); // test for colour
lhcbStyle->SetCanvasColor(0);
lhcbStyle->SetStatColor(0);
//lhcbStyle->SetPalette(1);
//lhcbStyle->SetTitleColor(0);
//lhcbStyle->SetFillColor(0); // test for colour
lhcbStyle->SetTitleBorderSize(0);

// set the paper & margin sizes
//lhcbStyle->SetPaperSize(20,26);
lhcbStyle->SetPadTopMargin(0.02);
lhcbStyle->SetPadRightMargin(0.02); // increase for colz plots!!
lhcbStyle->SetPadBottomMargin(0.14);
lhcbStyle->SetPadLeftMargin(0.14);

// use large fonts
lhcbStyle->SetTextFont(lhcbFont);
lhcbStyle->SetTextSize(0.08);
lhcbStyle->SetLabelFont(lhcbFont,"x");
lhcbStyle->SetLabelFont(lhcbFont,"y");
lhcbStyle->SetLabelFont(lhcbFont,"z");
lhcbStyle->SetLabelSize(0.05,"x");
lhcbStyle->SetLabelSize(0.05,"y");
lhcbStyle->SetLabelSize(0.05,"z");
lhcbStyle->SetTitleFont(lhcbFont);
lhcbStyle->SetTitleSize(0.06,"x");
lhcbStyle->SetTitleSize(0.06,"y");
lhcbStyle->SetTitleSize(0.06,"z");

lhcbStyle->SetTitleYOffset(1.15);


// use bold lines and markers
lhcbStyle->SetLineWidth(lhcbWidth);
lhcbStyle->SetFrameLineWidth(lhcbWidth);
lhcbStyle->SetHistLineWidth(lhcbWidth);
lhcbStyle->SetFuncWidth(lhcbWidth);
lhcbStyle->SetGridWidth(lhcbWidth);
lhcbStyle->SetLineStyleString(2,"[12 12]"); // postscript dashes
//lhcbStyle->SetMarkerStyle(15);
lhcbStyle->SetMarkerStyle(20);
lhcbStyle->SetMarkerSize(1.5);

// label offsets
lhcbStyle->SetLabelOffset(0.015);

// by default, do not display histogram decorations:
lhcbStyle->SetOptStat(0);  
lhcbStyle->SetOptStat(1110);  // show only nent, mean, rms
//lhcbStyle->SetOptStat(10); // entries only
lhcbStyle->SetOptTitle(0);
lhcbStyle->SetOptFit(111); 
//lhcbStyle->SetOptFit(1011); // show probability, parameters and errors

// look of the statistics box:
lhcbStyle->SetStatBorderSize(1);
lhcbStyle->SetStatFont(lhcbFont);
lhcbStyle->SetStatFontSize(0.05);
lhcbStyle->SetStatX(0.94);
lhcbStyle->SetStatY(0.9);
lhcbStyle->SetStatW(0.25);
lhcbStyle->SetStatH(0.05);

// put tick marks on top and RHS of plots
lhcbStyle->SetPadTickX(1);
lhcbStyle->SetPadTickY(1);


    const Int_t NRGBs = 5;
    const Int_t NCont = 255;

    Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
    Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
    Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
    Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    lhcbStyle->SetNumberContours(NCont);


// histogram divisions: only 5 in x to avoid label overlaps
lhcbStyle->SetNdivisions(505,"x");
lhcbStyle->SetNdivisions(510,"y");

TPaveText *lhcbName = new TPaveText(0.65,0.8,0.9,0.9,"BRNDC");
lhcbName->SetFillColor(0);
lhcbName->SetTextAlign(12);
lhcbName->SetBorderSize(0);
lhcbName->AddText("LHCb");

TPaveText *lhcbPrelimR = new TPaveText(0.70 - lhcbStyle->GetPadRightMargin(),
				       0.80 - lhcbStyle->GetPadTopMargin(),
				       0.95 - lhcbStyle->GetPadRightMargin(),
				       0.85 - lhcbStyle->GetPadTopMargin(),
				       "BRNDC");
lhcbPrelimR->SetFillColor(0);
lhcbPrelimR->SetTextAlign(12);
lhcbPrelimR->SetBorderSize(0);
lhcbPrelimR->AddText("#splitline{LHCb}{#scale[1.0]{Preliminary}}");

TPaveText *lhcbPrelimL = new TPaveText(lhcbStyle->GetPadLeftMargin() + 0.05,
				       0.87 - lhcbStyle->GetPadTopMargin(),
				       lhcbStyle->GetPadLeftMargin() + 0.30,
				       0.95 - lhcbStyle->GetPadTopMargin(),
				       "BRNDC");
lhcbPrelimL->SetFillColor(0);
lhcbPrelimL->SetTextAlign(12);
lhcbPrelimL->SetBorderSize(0);
lhcbPrelimL->AddText("#splitline{LHCb}{#scale[1.0]{Preliminary}}");

TPaveText *lhcb7TeVPrelimR = new TPaveText(0.70 - lhcbStyle->GetPadRightMargin(),
					   0.75 - lhcbStyle->SetPadTopMargin(0.05),
					   0.95 - lhcbStyle->GetPadRightMargin(),
					   0.85 - lhcbStyle->SetPadTopMargin(0.05),
					   "BRNDC");
lhcb7TeVPrelimR->SetFillColor(0);
lhcb7TeVPrelimR->SetTextAlign(12);
lhcb7TeVPrelimR->SetBorderSize(0);
lhcb7TeVPrelimR->AddText("#splitline{#splitline{LHCb}{Preliminary}}{#scale[0.7]{#sqrt{s} = 7 TeV Data}}");

TPaveText *lhcb7TeVPrelimL = new TPaveText(lhcbStyle->GetPadLeftMargin() + 0.05,
					   0.78 - lhcbStyle->SetPadTopMargin(0.05),
					   lhcbStyle->GetPadLeftMargin() + 0.30,
					   0.88 - lhcbStyle->SetPadTopMargin(0.05),
					   "BRNDC");
lhcb7TeVPrelimL->SetFillColor(0);
lhcb7TeVPrelimL->SetTextAlign(12);
lhcb7TeVPrelimL->SetBorderSize(0);
lhcb7TeVPrelimL->SetTextSize(0.06);
lhcb7TeVPrelimL->AddText("#splitline{#splitline{LHCb}{Preliminary}}{#scale[0.7]{#sqrt{s} = 7 TeV Data}}");

TPaveText *lhcb7TeVPrelimR = new TPaveText(0.70 - lhcbStyle->GetPadRightMargin(),
					   0.75 - lhcbStyle->SetPadTopMargin(0.05),
					   0.95 - lhcbStyle->GetPadRightMargin(),
					   0.85 - lhcbStyle->SetPadTopMargin(0.05),
					   "BRNDC");
lhcb7TeVPrelimR->SetFillColor(0);
lhcb7TeVPrelimR->SetTextAlign(12);
lhcb7TeVPrelimR->SetBorderSize(0);
lhcb7TeVPrelimR->AddText("#splitline{#splitline{LHCb}{Preliminary}}{#scale[0.7]{#sqrt{s} = 900 eV Data}}");

TPaveText *lhcb0_9TeVPrelimL = new TPaveText(lhcbStyle->GetPadLeftMargin() + 0.05,
					   0.78 - lhcbStyle->SetPadTopMargin(0.05),
					   lhcbStyle->GetPadLeftMargin() + 0.30,
					   0.88 - lhcbStyle->SetPadTopMargin(0.05),
					   "BRNDC");
lhcb0_9TeVPrelimL->SetFillColor(0);
lhcb0_9TeVPrelimL->SetTextAlign(12);
lhcb0_9TeVPrelimL->SetBorderSize(0);
lhcb0_9TeVPrelimL->SetTextSize(0.06);
lhcb0_9TeVPrelimL->AddText("#splitline{#splitline{LHCb}{Preliminary}}{#scale[0.7]{#sqrt{s} = 900 GeV Data}}");

TText *lhcbLabel = new TText();
lhcbLabel->SetTextFont(lhcbFont);
lhcbLabel->SetTextColor(1);
lhcbLabel->SetTextSize(0.04);
lhcbLabel->SetTextAlign(12);

TLatex *lhcbLatex = new TLatex();
lhcbLatex->SetTextFont(lhcbFont);
lhcbLatex->SetTextColor(1);
lhcbLatex->SetTextSize(0.04);
lhcbLatex->SetTextAlign(12);

gROOT->SetStyle("lhcbStyle");
gROOT->ForceStyle();



}

