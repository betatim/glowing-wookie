#!/usr/bin/python

import sys

if len(sys.argv) != 2:
  sys.exit("This program takes one argument, the file name to analyse")

from ROOT import gROOT
gROOT.ProcessLine(".x lhcbstyle.C")
#gROOT.SetBatch(True)

import ROOT
from ROOT import TFile, TCanvas, TPaveText, TPad, TGraph, TLegend, gPad, TH1D

ROOT.gErrorIgnoreLevel = ROOT.kError +20

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

def asymPlot(plotName):
  return inTitle(plotName,2,"Asym")
def timePlot(plotName):
  return inTitle(plotName,2,"Time")
def massPlot(plotName):
  return inTitle(plotName,2,"Mass")
def nllPlot(plotName):
  return inTitle(plotName,1,"NllOf")
def corrsPlot(plotName):
  return plotName == "CorrelationHist"
def fullData(plotName):
  return inTitle(plotName,1,"FullData")
def asymData(plotName):
  return (inTitle(plotName,1,"AsymData") or inTitle(plotName,-1,"fullDataSet"))
def midData(plotName):
  return inTitle(plotName,1,"MidData")
def lowData(plotName):
  return inTitle(plotName,1,"LowData")
def dataPlot(plotName):
  return inTitle(plotName,1,"Data") and ( inTitle(plotName,3,"CORTAU") or inTitle(plotName,3,"DMASS") )


def removeThings(plotName):
  for i in ["nopull","log","logx"]:
    if plotName[-len(i)-1:] == "-"+i:
      plotName = plotName[-len(i)-1:]
  return plotName

resizedOnce = []


def savePlot(plot,plotPull,filename,longPlot=True):

  if plotPull:
    plotPull.GetYaxis().SetRangeUser(-5,5)
    plotPull.SetMarkerStyle(2)

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
    plotPullTh1.GetYaxis().SetTitleFont(62)
    plotPullTh1.GetYaxis().SetNdivisions(205)

    plotPullTh1.GetXaxis().SetLabelSize(0.15)
    plotPullTh1.GetXaxis().SetLabelOffset(0.022)
    plotPullTh1.GetXaxis().SetTitleSize(0.18)
    plotPullTh1.GetXaxis().SetTitleOffset(0.78)

    plotPullTh1.GetYaxis().SetLabelSize(0.15)
    plotPullTh1.GetYaxis().SetLabelOffset(0.009)
    plotPullTh1.GetYaxis().SetTitleSize(0.17)
    plotPullTh1.GetYaxis().SetTitleOffset(0.32)
    ##plotPull.GetZaxis().SetLabelSize(0.05)
    ##plotPull.GetZaxis().SetTitleSize(0.06)
    ##plotPull.GetZaxis().SetTitleFont(42)


  plot.GetYaxis().SetTitleOffset(1)
  plot.GetYaxis().SetTitleSize(0.06)
  plot.GetXaxis().SetTitleSize(0.06)


  tl = False
  #if "asym" not in filename and "data" not in filename and "nll" not in filename:
    #tl = genLegend(plot)

  cNorm.cd()
  if plotPull:
    pNorm1.cd()
  gPad.SetTopMargin(0.12)
  plot.Draw()
  #gPad.Update()
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

  if "data" in filename:
    if "mass" in filename:
      if "log" in filename:
        plot.GetYaxis().SetRangeUser(1000,100000)
        gPad.Update()
    elif "time" in filename:
      if "log" in filename and not "logx" in filename:
        plot.GetYaxis().SetRangeUser(10,30000)
        gPad.Update()

  #plot.Draw()
  #if plot.getObject(int(plot.numItems())-1).ClassName() == "TPave":
    #plot.getObject(int(plot.numItems())-1).Draw()


  if tl:
    tl.Draw()
  gPad.Update()
  if plotPull:
    pNorm2.cd()
    plotPullTh1.Draw("AXIS")
    plotPull.Draw("P")

  print "   ","autoPlots/"+filename+".pdf"
  cNorm.SaveAs("autoPlots/"+filename+".pdf")

  if longPlot and plotPull:
    cLong.cd()
    gPad.SetTopMargin(0.12)
    plot.Draw()
    if tl:
      tl.Draw()
    print "   ","autoPlots/"+filename+"-nopull.pdf"
    cLong.SaveAs("autoPlots/"+filename+"-nopull.pdf")

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
  palette.SetLabelFont(62);
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
  c.SaveAs("autoPlots/corrs.pdf")

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
    "nll-all-"+plotName[6:]
  else:
    if "Time" in plotName or "B_CORTAU" in plotName:
      plot.GetXaxis().SetTitle("Corrected Proper Time / ps")
    elif "Mass" in plotName or "D_DMASS_Ds" in plotName:
      plot.GetXaxis().SetTitle("KK#pi Mass - D^{+}_{s} PDG Mass / MeV c^{-2}")
    if asymPlot(plotName):
      plot.GetXaxis().SetTitle("Corrected Proper Time / ps")
      plot.GetYaxis().SetTitle("Asymmetry")
    else:
      plot.GetYaxis().SetTitle("Candidates")
  if plotName[-5:] == "_Pull":
    plot.GetYaxis().SetTitle("Pull / #sigma")

def resizePlot(plot,plotName):
  if timePlot(plotName):
    if midData(plotName):
      plot.GetXaxis().SetRangeUser(0,1.8)
    elif lowData(plotName):
      plot.GetXaxis().SetRangeUser(0,.5)
  elif asymPlot(plotName):
    if inTitle(plotName,-1,"ds"):
      plot.GetXaxis().SetRangeUser(0,5)
      plot.GetYaxis().SetRangeUser(-.2,.2)



#tmpPlot = f.Get("FullData_Time_Combined_lowm")
#led = genLegend(tmpPlot)
#cNorm.cd()
#led.Draw()
#cNorm.SaveAs("autoPlots/legend.pdf")


dmdNll = f.Get("NllOf_T_Sig_Bd_dM")
dmsNll = f.Get("NllOf_T_Sig_Bs_dM")

dmdNll.GetXaxis().SetTitle("Fitted Value of #Delta m_{d}")
dmsNll.GetXaxis().SetTitle("Fitted Value of #Delta m_{s}")

dmdNll.GetYaxis().SetTitle("Projection of -log(likelihood)")
dmsNll.GetYaxis().SetTitle("Projection of -log(likelihood)")

dmsNll.GetXaxis().SetRangeUser(0,50)
dmsNll.GetYaxis().SetRangeUser(0,80)

savePlot(dmdNll,False,"nll-dmd",False)
savePlot(dmsNll,False,"nll-dms",False)



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
  if not nllPlot(plotName) and not dataPlot(plotName) and not corrsPlot(plotName):
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
    fileTokens = ["nll","all",plotName[6:]]
    savePlot(plot,plotPull,"-".join(fileTokens),False)
  #elif corrsPlot(plotName):
    #saveCorrs(plot)
  elif dataPlot(plotName):
    fileTokens = ["data"]
    if inTitle(plotName,3,"CORTAU"):
      fileTokens.append("time")
    elif inTitle(plotName,3,"DMASS"):
      fileTokens.append("mass")
    if asymData(plotName):
      if inTitle(plotName,3,"CORTAU"):
        savePlotLogLin(plot,plotPull,"-".join(fileTokens))
      elif inTitle(plotName,3,"DMASS"):
        savePlotLogLin(plot,plotPull,"-".join(fileTokens),False)
  else:
    if timePlot(plotName):
      fileTokens.append("time")
    elif massPlot(plotName):
      fileTokens.append("mass")
    elif asymPlot(plotName):
      fileTokens.append("asym")

    if massPlot(plotName):
      if inTitle(plotName,3,"High"):
        fileTokens.append("high")
        titleTokens.append("High-n")
      elif inTitle(plotName,3,"Low"):
        fileTokens.append("low")
        titleTokens.append("Low-n")
    else:
      if inTitle(plotName,3,"High"):
        fileTokens.append("highn")
        titleTokens.append("High-n")
      elif inTitle(plotName,3,"Low"):
        fileTokens.append("lown")
        titleTokens.append("Low-n")

    if inTitle(plotName,4,"lowm"):
      fileTokens.append("lowm")
    elif inTitle(plotName,4,"dd"):
      fileTokens.append("dd")
    elif inTitle(plotName,4,"midm"):
      fileTokens.append("midm")
    elif inTitle(plotName,4,"ds"):
      fileTokens.append("ds")
    elif inTitle(plotName,4,"dstarhighm"):
      fileTokens.append("dstarhighm")
    elif inTitle(plotName,4,"lowt"):
      fileTokens.append("lowt")
    elif inTitle(plotName,4,"midt"):
      fileTokens.append("midt")
    elif inTitle(plotName,4,"hight"):
      fileTokens.append("hight")

    if massPlot(plotName):
      if inTitle(plotName,4,"Mixed"):
        fileTokens.append("mixed")
        titleTokens.append("Odd Tagged")
      elif inTitle(plotName,4,"Unmixed"):
        fileTokens.append("unmixed")
        titleTokens.append("Even Tagged")
    else:
      if inTitle(plotName,5,"Mixed"):
        fileTokens.append("mixed")
        titleTokens.append("Odd tagged")
      elif inTitle(plotName,5,"Unmixed"):
        fileTokens.append("unmixed")
        titleTokens.append("Even tagged")

    if timePlot(plotName):
      if midData(plotName):
        fileTokens.append("zoom")
        titleTokens.append("t<1.8ps")
      elif lowData(plotName):
        fileTokens.append("highzoom")
        titleTokens.append("t<0.5ps")

    if inTitle(plotName,4,"lowm"):
      titleTokens.append("low kk#pi mass sideband")
    elif inTitle(plotName,4,"dd"):
      titleTokens.append("Dd signal")
    elif inTitle(plotName,4,"midm"):
      titleTokens.append("middle kk#pi mass sideband")
    elif inTitle(plotName,4,"ds"):
      titleTokens.append("Ds signal")
    elif inTitle(plotName,4,"dstarhighm"):
      titleTokens.append("high kk#pi mass sideband")
    elif inTitle(plotName,4,"lowt"):
      titleTokens.append("t<1ps")
    elif inTitle(plotName,4,"midt"):
      titleTokens.append("1<t<2ps")
    elif inTitle(plotName,4,"hight"):
      titleTokens.append("2<t<10ps")


    #pt = TPaveText(.2,.8,.6,.9,"BRNDC")
    #pt = TPaveText(.2,.9,.55,.99,"BRNDC")
    pt = TPaveText(.3,.83+.09,.8,.99,"BRNDC")
    pt.SetName("TPaveText_"+plotName)
    pt.SetFillColor(19)
    pt.SetLineWidth(3)
    if len(titleTokens)>0:
      pt.AddText(", ".join(titleTokens)+" region")
      plot.addObject(pt)

    if asymPlot(plotName):
      savePlot(plot,plotPull,"-".join(fileTokens))
    elif massPlot(plotName):
      savePlotLogLin(plot,plotPull,"-".join(fileTokens),False)
    elif midData(plotName) or lowData(plotName):
      savePlot(plot,plotPull,"-".join(fileTokens))
    else:
      savePlotLogLin(plot,plotPull,"-".join(fileTokens))




