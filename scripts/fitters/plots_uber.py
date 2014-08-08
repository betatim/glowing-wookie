#!/usr/bin/python

import sys

if len(sys.argv) != 2+1:
  sys.exit("This program takes two arguments, the file name to analyse and the output directory")

from ROOT import gROOT
gROOT.ProcessLine(".x ../lhcbstyle.C")
gROOT.SetBatch(True)

import ROOT
from ROOT import TFile, TCanvas, TPaveText, TPad, TGraph, TLegend, gPad, TH1D, TLine

ROOT.gErrorIgnoreLevel = ROOT.kError +20

out_dir = sys.argv[2]

f = TFile.Open(sys.argv[1])
keys = f.GetListOfKeys()
keyIt = keys.MakeIterator()

cNorm = TCanvas("canvNorm","canvNorm",600,450)
cLong = TCanvas("canvLong","canvLong",800,450)

def inTitle(plotName,field,name):
  try:
    return plotName.split("_")[field-1 if field>0 else field] == name
  except IndexError:
    return False

def d0Plot(plotName):
  return inTitle(plotName,3,"D0M")
def delmPlot(plotName):
  return inTitle(plotName,3,"DelM")

def nllPlot(plotName):
  return inTitle(plotName,1,"NllOf")

def corrsPlot(plotName):
  return plotName == "CorrelationHist"

#def fullData(plotName):
  #return inTitle(plotName,1,"FullData")
#def asymData(plotName):
  #return (inTitle(plotName,1,"AsymData") or inTitle(plotName,-1,"fullDataSet"))
#def midData(plotName):
  #return inTitle(plotName,1,"MidData")
#def lowData(plotName):
  #return inTitle(plotName,1,"LowData")
#def dataPlot(plotName):
  #return inTitle(plotName,1,"DataSet") )


def removeThings(plotName):
  for i in ["nopull","log","logx"]:
    if plotName[-len(i)-1:] == "-"+i:
      plotName = plotName[-len(i)-1:]
  return plotName

resizedOnce = []

lines = []


def savePlot(plot,plotPull,filename,longPlot=True):

  if plotPull:
    plotPull.GetYaxis().SetRangeUser(-5,5)
    #plotPull.SetMarkerStyle(2)
    #plotPull.SetMarkerColor(ROOT.kBlue)
    plotPull.SetFillColor(ROOT.kBlue-2)
    lines.append( TLine(plotPull.GetXaxis().GetXmax(),0.,plotPull.GetXaxis().GetXmax(),0.) )

  cNorm.Clear()
  cLong.Clear()

  plotPullTh1 = False

  tmpLogy = False
  tmpLogx = False

  plot.GetXaxis().SetDecimals(True)
  plot.GetXaxis().SetLabelOffset(0.023)

  if plotPull:
    tmpLogy = gPad.GetLogy()
    tmpLogx = gPad.GetLogx()
    gPad.SetLogy(False)
    gPad.SetLogx(False)

    pNorm1 = TPad("pNorm1","pNorm1",0,0.28,1,1)
    pNorm2 = TPad("pNorm2","pNorm2",0,0,1,0.28)
    cNorm.cd()
    pNorm1.Draw()
    pNorm2.Draw()
    pNorm1.SetFillColor(0)
    pNorm2.SetFillColor(0)
    pNorm2.SetBottomMargin(0.33)

    pNorm1.SetLogy(tmpLogy)
    pNorm1.SetLogx(tmpLogx)
    pNorm2.SetLogx(tmpLogx)

    #pNorm1.SetBottomMargin(0.00001)
    pNorm1.SetBottomMargin(0.025)
    pNorm1.SetBorderMode(0)
    pNorm2.SetTopMargin(0.01)
    #pNorm2.SetTopMargin(0.05)
    #pNorm2.SetBottomMargin(0.1)
    pNorm2.SetBorderMode(0)


    plot.GetXaxis().SetLabelOffset(0.023)
    plot.GetXaxis().SetLabelSize(0.06)
    plot.GetXaxis().SetTitleOffset(1.1)
    plot.GetYaxis().SetLabelSize(0.06)

    plot.GetXaxis().SetNdivisions(511)

    pNorm1.SetLeftMargin(0.13)
    pNorm2.SetLeftMargin(0.13)

    pxa = plot.GetXaxis()
    plotPullTh1 = TH1D("plotPullTh1","plotPullTh1",100,pxa.GetBinLowEdge(pxa.GetFirst()),pxa.GetBinUpEdge(pxa.GetLast()))
    plotPullTh1.SetStats(False)
    plotPullTh1.GetXaxis().SetDecimals(True)

  if plotPull:
    plotPullTh1.GetYaxis().SetRangeUser(-5,5)
    plotPullTh1.GetXaxis().SetTitle(plot.GetXaxis().GetTitle())

    plotPullTh1.GetXaxis().SetNdivisions(511)
    plotPullTh1.GetXaxis().SetTickLength(0.1)

    plotPullTh1.GetYaxis().SetTitle("Pull / #sigma")
    plotPullTh1.GetYaxis().SetTitleFont(132)
    plotPullTh1.GetYaxis().SetNdivisions(205)

    plotPullTh1.GetXaxis().SetLabelSize(0.15)
    plotPullTh1.GetXaxis().SetLabelOffset(0.022)
    plotPullTh1.GetXaxis().SetTitleSize(0.18)
    plotPullTh1.GetXaxis().SetTitleOffset(0.78)
    plotPullTh1.GetXaxis().SetTitleFont(132)

    plotPullTh1.GetYaxis().SetLabelSize(0.15)
    plotPullTh1.GetYaxis().SetLabelOffset(0.009)
    plotPullTh1.GetYaxis().SetTitleSize(0.17)
    plotPullTh1.GetYaxis().SetTitleOffset(0.32)
    ##plotPull.GetZaxis().SetLabelSize(0.05)
    ##plotPull.GetZaxis().SetTitleSize(0.06)
    ##plotPull.GetZaxis().SetTitleFont(42)


  plot.GetYaxis().SetTitleOffset(1)
  plot.GetXaxis().SetTitleSize(0.06)
  plot.GetYaxis().SetTitleSize(0.06)
  plot.GetXaxis().SetTitleFont(132)
  plot.GetYaxis().SetTitleFont(132)
  plot.GetXaxis().SetLabelFont(132)
  plot.GetYaxis().SetLabelFont(132)


  tl = False
  #if "asym" not in filename and "data" not in filename and "nll" not in filename:
    #tl = genLegend(plot)

  cNorm.cd()
  if plotPull:
    pNorm1.cd()
  gPad.SetTopMargin(0.12)
  plot.Draw()
  gPad.Update()
  
  #if "asym" not in filename and "nll" not in filename:
    ##if gPad.GetLogy():
      ##plot.GetYaxis().SetRangeUser(.8,plot.GetMinimum()*1.3)
    ##else:
      ##plot.GetYaxis().SetRangeUser(plot.GetMinimum()*.8,plot.GetMinimum()*1.3)

    ##if gPad.GetLogy():
      ##plot.GetYaxis().SetRangeUser(.8,plot.GetBinContent(plot.GetMinimumBin())*1.3)
    ##else:
      ##plot.GetYaxis().SetRangeUser(plot.GetBinContent(plot.GetMinimumBin())*.8,plot.GetBinContent(plot.GetMinimumBin())*1.3)

    #gPad.Update()
    ##if "mass" in filename:
      ##plot.GetYaxis().SetRangeUser(200,150000)
    ##if removeThings(filename) not in resizedOnce:
      ##resizedOnce.append(removeThings(filename))
    ##if tmpLogy:#gPad.GetLogy():
      ##print "FIND: ",gPad.GetLogy(),gPad.GetUymin(), gPad.GetUymax()
      ###if gPad.GetUymax() < 10:
        ###plot.GetYaxis().SetRangeUser(0.8,10**(gPad.GetUymax()*1.15))
      ###else:
        ###plot.GetYaxis().SetRangeUser(.8,gPad.GetUymax()*1.15)
      ####plot.GetYaxis().SetRangeUser(10**gPad.GetUymin(),10**gPad.GetUymax()*1)
    ##else:
      ###if gPad.GetUymax() < 10:
        ###plot.GetYaxis().SetRangeUser(pNorm1.GetUymin(),pNorm1.GetUymax()*1.15)
      ###else:
      ##plot.GetYaxis().SetRangeUser(gPad.GetUymin(),gPad.GetUymax()*1.15)
  gPad.Update()

  #if "data" in filename:
    #if "mass" in filename:
      #if "log" in filename:
        #plot.GetYaxis().SetRangeUser(1000,100000)
        #gPad.Update()
    #elif "time" in filename:
      #if "log" in filename and not "logx" in filename:
        #plot.GetYaxis().SetRangeUser(10,30000)
        #gPad.Update()

  #plot.Draw()
  #if plot.getObject(int(plot.numItems())-1).ClassName() == "TPave":
    #plot.getObject(int(plot.numItems())-1).Draw()


  if tl:
    tl.Draw()
  gPad.Update()
  if plotPull:
    pNorm2.cd()
    plotPullTh1.Draw("AXIS")
    lines[-1].Draw()
    plotPull.Draw("B")

  print "   ",out_dir+"/"+filename+".pdf"
  cNorm.SaveAs(out_dir+"/"+filename+".pdf")
  cNorm.SaveAs(out_dir+"/"+filename+".png")

  if longPlot and plotPull:
    cLong.cd()
    gPad.SetTopMargin(0.12)
    plot.Draw()
    if tl:
      tl.Draw()
    print "   ",out_dir+"/"+filename+"-nopull.pdf"
    cLong.SaveAs(out_dir+"/"+filename+"-nopull.pdf")
    cLong.SaveAs(out_dir+"/"+filename+"-nopull.png")

def saveCorrs(corrs):
  corrs.GetXaxis().SetLabelOffset(0.004)
  corrs.GetYaxis().SetLabelSize(0.02)
  corrs.GetXaxis().SetLabelSize(0.01)

  from ROOT import gStyle, gPad, TPaletteAxis, TColor

  c=TCanvas("autoPlots/corrs","autoPlots/corrs",500,700)
  gStyle.SetOptStat(0)
  gPad.SetBottomMargin(0.12)
  gPad.SetRightMargin(0.15)
  gPad.SetLeftMargin(0.23)

  palette = TPaletteAxis(85.14702,7.550805,88.31997,72.82681,corrs);
  palette.SetLabelColor(1);
  palette.SetLabelFont(132);
  palette.SetLabelOffset(0.005);
  palette.SetLabelSize(0.04);
  palette.SetTitleOffset(1);
  palette.SetTitleSize(0.06);
  palette.GetAxis().SetLabelSize(0.03)

  ci = TColor.GetColor("#850100");
  palette.SetFillColor(ci);
  palette.SetFillStyle(1001);
  palette.SetLineWidth(3);
  corrs.GetListOfFunctions().Add(palette,"br");

  corrs.Draw("colz")
  c.SaveAs(out_dir+"/corrs.pdf")
  c.SaveAs(out_dir+"/corrs.png")

def genLegend(plot):
  dataAdded = False
  sumAdded = False
  #i = 0
  tl = TLegend(.75,.6,.99,.99)
  for i in  range(int(plot.numItems())):
    obj = plot.getObject(i)
    if not obj:
      break

    if obj.ClassName() == "RooHist" and not dataAdded:
      dataAdded = True
      tl.AddEntry(obj,"Data")
    else:
      name = obj.GetName()
      if "TM_Peak_" in name:
        tl.AddEntry(obj,"Prompt D background")
      elif "TM_NSide1" in name:
        tl.AddEntry(obj,"Prompt sideband componant")
      elif "TM_NSide2" in name:
        tl.AddEntry(obj,"Detached sideband componant")
      elif "TM_Bplus_" in name:
        tl.AddEntry(obj,"B^{+} background")
      elif "TM_Sig_Bs" in name:
        tl.AddEntry(obj,"B_{s} signal")
      elif "TM_Sig_Bd" in name:
        tl.AddEntry(obj,"B_{d} signal")
      elif not sumAdded:
        sumAdded = True
        tl.AddEntry(obj,"Sum of PDFs")
    #i+=1
  return tl


def savePlotLogLin(plot,plotPull,filename,xLog=True,yLog=True):
  #plotLog = plot.Clone()
  #plotLog.SetLogy(yLog)
  #plotLog.SetLogx(xLog)

  logs = [(plotPull,False,False,"")]

  if xLog:
    logs.append((False,True,False,"-logx"))
    logs.append((plotPull,True,False,"-logx-pull"))
  if yLog:
    logs.append((False,False,True,"-log"))
    logs.append((plotPull,False,True,"-log-pull"))
  #if xLog and yLog:
    #logs.append((False,True,True,"-logxy"))

  for pull,xLog,yLog,fileAddition in logs:

    cNorm.SetLogy(yLog)
    cNorm.SetLogx(xLog)
    cLong.SetLogy(yLog)
    cLong.SetLogx(xLog)

    savePlot(plot,pull,filename+fileAddition)

  #savePlot(plot,filename+"-log")

  cNorm.SetLogy(False)
  cNorm.SetLogx(False)
  cLong.SetLogy(False)
  cLong.SetLogx(False)

def giveTitle(plot,plotName):
  if nllPlot(plotName):
    plot.GetXaxis().SetTitle("Fitted Value of "+plotName[6:])
    plot.GetYaxis().SetTitle("Projection of -log(likelihood)")
    #"nll-all-"+plotName[6:]
  else:
    if d0Plot(plotName):
      plot.GetXaxis().SetTitle("m(D^{0}) [MeV c^{-2}]")
    elif delmPlot(plotName):
      plot.GetXaxis().SetTitle("m(D^{*}) - m(D^{0}) [MeV c^{-2}]")
    plot.GetYaxis().SetTitle("Candidates")
  if plotName[-5:] == "_Pull":
    plot.GetYaxis().SetTitle("Pull / #sigma")

def resizePlot(plot,plotName):
  pass
  #if timePlot(plotName):
    #if midData(plotName):
      #plot.GetXaxis().SetRangeUser(0,1.8)
    #elif lowData(plotName):
      #plot.GetXaxis().SetRangeUser(0,.5)
  #elif asymPlot(plotName):
    #if inTitle(plotName,-1,"ds"):
      #plot.GetXaxis().SetRangeUser(0,5)
      #plot.GetYaxis().SetRangeUser(-.2,.2)



#tmpPlot = f.Get("FullData_Time_Combined_lowm")
#led = genLegend(tmpPlot)
#cNorm.cd()
#led.Draw()
#cNorm.SaveAs(out_dir+"/legend.pdf")


#dmdNll = f.Get("NllOf_T_Sig_Bd_dM")
#dmsNll = f.Get("NllOf_T_Sig_Bs_dM")

#dmdNll.GetXaxis().SetTitle("Fitted Value of #Delta m_{d}")
#dmsNll.GetXaxis().SetTitle("Fitted Value of #Delta m_{s}")

#dmdNll.GetYaxis().SetTitle("Projection of -log(likelihood)")
#dmsNll.GetYaxis().SetTitle("Projection of -log(likelihood)")

#dmsNll.GetXaxis().SetRangeUser(0,50)
#dmsNll.GetYaxis().SetRangeUser(0,80)

#savePlot(dmdNll,False,"nll-dmd",False)
#savePlot(dmsNll,False,"nll-dms",False)



#if True:
  #plotName = "AsymData_Mass_Combined"
while True:
  key = keyIt.Next()
  if not key:
    break
  plotName = key.GetName()
  if plotName[-5:] == "_Pull":
    continue
  # This was me trying to be concise, fail
  skip = False
  for area in ["highm","dstar","midml","midmr"]:
    if inTitle(plotName,-1,area) or inTitle(plotName,-2,area):
      skip = True
  if skip:
    continue
  # Thats not a plot!
  if plotName == "RooFitResults":
    continue
  # Thats not a plot!
  if "DataSet" in plotName:
    continue
  # Thats not a plot!
  if "ProcessID" in plotName:
    continue
  ## for testing ...
  #if timePlot(plotName):
    #continue
  #if nllPlot(plotName):
    #continue
  # We dont need two copies of the mass plots with slightly differenet binning
  if inTitle(plotName,1,"FullData") and inTitle(plotName,2,"Mass"):
    continue
  # this script doesnt do the correlations too well, just use the old one
  if corrsPlot(plotName):
    continue


  print plotName

  plot = key.ReadObj()
  #plot = f.Get(plotName)
  giveTitle(plot,plotName)
  resizePlot(plot,plotName)

  plotPull = False
  if not nllPlot(plotName) and not corrsPlot(plotName):
    print "   ",plotName+"_Pull"
    plotPull = TGraph(f.Get(plotName+"_Pull"))
    giveTitle(plotPull,plotName+"_Pull")
    #resizePlot(plotPull,plotName)
    plotPull.GetXaxis().SetNdivisions(plot.GetXaxis().GetNdivisions())
    plotPull.GetXaxis().SetRangeUser(plot.GetXaxis().GetXmin(),plot.GetXaxis().GetXmax())
    plotPull.GetXaxis().SetTitle("Corrected Proper Time / ps")

  fileTokens = []
  titleTokens = []

  if nllPlot(plotName):
    fileTokens = ["nll",plotName[6:]]
    plot.GetYaxis().SetRangeUser(0.,2000.)
    savePlot(plot,plotPull,"-".join(fileTokens),False)
  #elif corrsPlot(plotName):
    #saveCorrs(plot)
    
  else:
    if inTitle(plotName,2,"BDT1"):
      fileTokens.append("BDT1")
    elif inTitle(plotName,2,"BDT2"):
      fileTokens.append("BDT2")
    elif inTitle(plotName,2,"BDT3"):
      fileTokens.append("BDT3")
    elif inTitle(plotName,2,"Norm"):
      fileTokens.append("Norm")
      
    if d0Plot(plotName):
      fileTokens.append("d0m")
    elif delmPlot(plotName):
      fileTokens.append("delm")
      
    if inTitle(plotName,3,"D0M") and inTitle(plotName,5,"d0all"):
      if inTitle(plotName,4,"delhigh"):
        fileTokens.append("delhigh")
      elif inTitle(plotName,4,"delsig"):
        fileTokens.append("delsig")
      elif inTitle(plotName,4,"dellow"):
        fileTokens.append("dellow")

    if inTitle(plotName,3,"DelM") and inTitle(plotName,4,"delall"):
      if inTitle(plotName,5,"dlow1"):
        fileTokens.append("d0low1")
      elif inTitle(plotName,5,"dlow2"):
        fileTokens.append("d0low2")
      elif inTitle(plotName,5,"dlow"):
        fileTokens.append("d0low")
      elif inTitle(plotName,5,"dsig"):
        fileTokens.append("d0sig")
      elif inTitle(plotName,5,"dhigh"):
        fileTokens.append("d0high")
      elif inTitle(plotName,5,"dhigh1"):
        fileTokens.append("d0high1")
      elif inTitle(plotName,5,"dhigh2"):
        fileTokens.append("d0high2")
    
    savePlotLogLin(plot,plotPull,"_".join(fileTokens),False)



