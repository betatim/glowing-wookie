# -*- coding: utf-8 -*-

import sys, os, argparse

parser = argparse.ArgumentParser(description='Fitter to determine Dms and Dmd from semi-leptonic B decays')
parser.add_argument("systematic", help='Name of the systematic to run')
parser.add_argument("nCPUs", type=int, help='Number of CPU cores to use')

args = parser.parse_args()

#print args
#sys.exit(0)

#if len(sys.argv) != 2+1:
  #print "To use this script run it like so:"
  #print sys.argv[0], "<systematic name> <number of CPUs>"
  #print ""
  #sys.exit(0)

sys.path.append("../..")

systName   = args.systematic
nCPUs   = args.nCPUs

print "script args:", systName, nCPUs
print ""

import subprocess, ROOT, datetime, array

config = {
  'outFileName': "fitResult."+systName+".root",
  'loadFileName': "fitResult.blank.root",

  'dataFile': "/afs/cern.ch/work/t/tbird/demu/ntuples/pipi/strip_pipi_fitter.root",

  'doFit': True,
  'loadFit': False,
  #'loadFit': not doFit,
  'doNlls': True,
  'doBinned': True,
  'doBinnedNll': True,
  'doPlots': True,
  'visError': False,
  'doGof': False,
  'doPlotsAsymLong': False,
  'partialNlls': False,

  'cutStr': "RAND<0.1",

  'binScale': 1.,

  'niceness': 3
}


sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

doKinitCheck = True
hostProc = subprocess.Popen(["hostname"],stdout=subprocess.PIPE)
hostOut = hostProc.stdout.readlines()
for line in hostOut:
  if "blackbook" in line:
    doKinitCheck = False
  elif "rigel" in line:
    doKinitCheck = False
hostProc.poll()

timeStr = False
if doKinitCheck:
  tocProc = subprocess.Popen(["tokens"],stdout=subprocess.PIPE)
  tocOut = tocProc.stdout.readlines()
  for line in tocOut:
    if "afs@cern.ch" in line and "[Expires " in line:
      timeStr = line.strip()[9+line.find("[Expires "):-1]

  if timeStr:
    now = datetime.datetime.today()
    tleft = datetime.datetime.strptime(timeStr+" "+str(now.year),"%b %d %H:%M %Y") - now
    if tleft < datetime.timedelta(0,1*3600):
      sys.exit("need longer afs token, run kinit")
    elif tleft < datetime.timedelta(0,12*3600):
      print ""
      print "----------------------------------------------------"
      print "WARNING: Will soon need longer afs token, run kinit!"
      print "----------------------------------------------------"
      print ""
  else:
    sys.exit("need longer afs token, run kinit")

  tocProc.poll()


from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT
from ROOT import TStopwatch, TFile, RooFit, RooAbsData, RooDataSet, RooDataHist
from ROOT import RooCategory, RooArgSet, RooMsgService, RooCmdArg, RooLinkedList

timers = {
  "startup":TStopwatch(),
  "fitting":TStopwatch(),
  "plotting":TStopwatch(),
  "nlls":TStopwatch(),
  "gof":TStopwatch(),
  "total":TStopwatch()
  }
timers["total"].Start()
timers["startup"].Start()


from wookie.fitter.variableUtils import *
import wookie.fitter.d0DelmFitPdf as pdf

w = pdf.setup_workspace()

D0_M = w.obj("D0_M")
Del_M = w.obj("Del_M")
Final_PDF = w.obj("Final_PDF")


componantColours = [
    ["Sig", 16, ROOT.kSolid,16,1001],
    ["Comb", 14, 7],
    ["Prompt", ROOT.kRed+4, 4],
    ["MisId", ROOT.kMagenta+2, ROOT.kSolid,0,0,1],
    ["D0M_Bkg_Exp", ROOT.kGreen+4],
    ["D0M_Bkg_Poly", ROOT.kGreen+2],
    ["*", ROOT.kBlue]
  ]



exec("import syst_"+systName+" as syst")

#config += syst.config #TODO: make a merger



checkVarRanges(w)
printVarLimits(w)
printSetVarLimits(w)
#printSetVarConst(w)
checkVarLimits(w)

print '{:<12}'.format('doFit:')+'{:<12}'.format(str(config['doFit']))+'{:<18}'.format('loadFit:')+'{:<12}'.format((loadFileName if config['loadFit'] else "False"))
print '{:<12}'.format('doPlots:')+'{:<12}'.format(str(config['doPlots']))+'{:<18}'.format('visError:')+'{:<12}'.format(str(config['visError']))
print '{:<12}'.format('doNlls:')+'{:<12}'.format(str(config['doNlls']))+'{:<18}'.format('partialNlls:')+'{:<12}'.format(str(config['partialNlls']))
print '{:<12}'.format('doBinned:')+'{:<12}'.format(str(config['doBinned']))+'{:<18}'.format('doBinnedNll:')+'{:<12}'.format(str(config['doBinnedNll']))
print '{:<12}'.format('doGof:')+'{:<12}'.format(str(config['doGof']))+'{:<18}'.format('doPlotsAsymLong:')+'{:<12}'.format(str(config['doPlotsAsymLong']))
print ''






#RooAbsData.setDefaultStorageType(RooAbsData.Tree);





tf = TFile(config['dataFile'],"OPEN")
ttree = tf.Get("subTree")
fullUnbDataSet = RooDataSet("fullUnbDataSet","fullUnbDataSet",ttree,w.set("argsPreCut"),config['cutStr'])
fullUnbDataSet.Print()

binnedDataSet = False
fullDataSet = False
highResDataSet = False

fullDataSet = RooDataHist("fullDataSet","fullDataSet",w.set("args"),fullUnbDataSet)
fullDataSet.Print()


print "Dataset imported to workspace"

ds = fullDataSet

timers["startup"].Stop()
timers["startup"].Print()

timers["fitting"].Start()

print "To MINUIT! Fitting to %s::%s at %s, saving result in %s" % (Final_PDF.ClassName(), Final_PDF.GetName(), datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"), config['outFileName'])

r=False
if config['doFit']:
  if config['doBinned']:
    r=Final_PDF.fitTo(fullDataSet,RooFit.Save(),RooFit.NumCPU(nCPUs,True),RooFit.Timer(True),RooFit.PrintEvalErrors(1))
  else:
    r=Final_PDF.fitTo(fullUnbDataSet,RooFit.Save(),RooFit.NumCPU(nCPUs,True),RooFit.Timer(True),RooFit.PrintEvalErrors(1))
elif config['loadFit']:
  fitResultsFile = TFile.Open(loadFileName,"OPEN")
  r = fitResultsFile.Get("RooFitResults")
  fitResultsFile.Close()

RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

r.SetName("RooFitResults")
getattr(w, 'import')(r)

if r:
  finalPars = r.floatParsFinal()
  it=finalPars.createIterator()
  while True:
    var = it.Next()
    if not var:
      print "End of variables"
      break
    else:
      w.obj(var.GetName()).setVal(var.getVal())
      w.obj(var.GetName()).setError(var.getError())

  printTexRes(r)
  print "Minimum value of NLL:", r.minNll()
  r.Print()

  initPars = r.floatParsInit()
  iterI=initPars.createIterator()
  iterF=finalPars.createIterator()
  ret = []
  while True:
    varI = iterI.Next()
    varF = iterF.Next()
    if not varI or not varF:
      print "End of variables"
      break
    else:
      if varI.getVal() == varF.getVal():
        ret.append(varI.GetName() + "'s final value of "+str(varF.getVal())+" is the same as it's initial value!")

printSetVarLimits(w)
checkTitles(w)
checkVarLimits(w)
sys.stdout.flush()

timers["fitting"].Stop()
timers["fitting"].Print()

timers["plotting"].Start()







#w.obj("D_DMASS_Ds").setBins(100)
#w.obj("B_CORTAU").setBins(int(round(100*maxtau/5.)))
#lowResDataSet = RooDataHist("lowResDataSet","lowResDataSet",w.set("args"),fullUnbDataSet)
#lowResDataSet.Print()


colours = [ROOT.kBlack, ROOT.kBlue]
coloursAsym = [ROOT.kBlack, ROOT.kBlue]

for index, default in [[2, ROOT.kSolid],[3,0],[4,0],[5,3]]:
  for componentItem in componantColours:
    try:
      componentItem[index]
    except IndexError:
      if len(componentItem) == index:
        componentItem.append(default)

simultaneousFit = (Final_PDF.ClassName() == "RooSimultaneous")

def largePlotOn(pdf,frame,*args):
  l = RooLinkedList()
  for arg in args:
    l.Add(arg)
  pdf.plotOn(frame,l)

def ueberPlot(w,plotName,plotVar,cpus,mixState,massCat,cut,dataArr,varMax=-1,asym=False,numBins=False):
  frame = False
  if numBins!=False:
    frame = plotVar.frame(plotVar.getMin(),varMax if varMax != -1 else plotVar.getMax(),numBins)
  else:
    frame = plotVar.frame(plotVar.getMin(),varMax if varMax != -1 else plotVar.getMax())
  dsName = "dsBinnedMassCat-"+cut
  dataRedArr = []
  i=0
  for data in dataArr:
    dataRedArr.append((getattr(data,"reduce")(RooFit.CutRange(cut)),i))
    i += 1

  visRooCmdArg = RooCmdArg.none()
  if config['visError'] and (config['doFit'] or config['loadFit']):
    if r.covQual() == 3:
      visRooCmdArg = RooFit.VisualizeError(r)

  if massCat != "":
    massCat = massCat + "_"

  asymVar = asym
  if mixState == "":
    oscSlice = RooCmdArg.none()
  elif mixState == "Mixed":
    oscSlice = RooFit.Slice(B0_OSCIL,"Oscil")
  elif mixState == "Unmixed":
    oscSlice = RooFit.Slice(B0_OSCIL,"NonOscil")
  #elif mixState == "Pos":
    #oscSlice = RooFit.Slice(w.obj("Mu_CHARGE_CAT"),"positive")
  #elif mixState == "Neg":
    #oscSlice = RooFit.Slice(w.obj("Mu_CHARGE_CAT"),"negitive")

  cpus = 1

  #dataB.Print()
  if not asym:
    print "Plotting:" ,plotName
    sys.stdout.flush()
    for data,icolour in dataRedArr:
      data.plotOn(frame, RooFit.MarkerColor(colours[icolour]), RooFit.MarkerSize(0.8))
    #for component, lineColour in [ ["*TM_Side1", ROOT.kRed], ["*TM_Side2", ROOT.kGreen], ["*TM_Peak_*", ROOT.kOrange], ["*TM_Sig_Bs", ROOT.kMagenta], ["*TM_Sig_Bd,*TM_Sig_Bd_in_Bs", ROOT.kMagenta+2], ["*TM_Bplus*",ROOT.kGray+1], ["*TM_Sig_BdDStar", ROOT.kCyan], ["*", ROOT.kBlue] ]:
    for component, lineColour, lineStyle, fillColour, fillStyle, lineWidth in componantColours:
      arguments = RooLinkedList()
      for arg in [RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.LineWidth(lineWidth), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.Precision(1e-4)]:
        arguments.Add(arg)
      if fillStyle is not 0:
        arguments.Add(RooFit.DrawOption("F"))
      if mixState == "Mixed":
        arguments.Add(RooFit.Slice(B0_OSCIL,"Oscil"))
      elif mixState == "Unmixed":
        arguments.Add(RooFit.Slice(B0_OSCIL,"NonOscil"))
      if config['visError'] and (config['doFit'] or config['loadFit']):
        if r.covQual() == 3:
          arguments.Add(RooFit.VisualizeError(r))
      #print("+")
      #if massCat == "":
      if False:
        dataB = RooDataHist(dsName, dsName, RooArgSet(B0_MASS_CAT), dataRedArr[-1][0], 1.0)
        arguments.Add(RooFit.ProjWData(dataB))
        arguments.Add(RooFit.NumCPU(nCPUs,True))
        if cut != "":
          arguments.Add(RooFit.ProjectionRange(cut))
          arguments.Add(RooFit.NormRange(cut))
          #largePlotOn(Final_PDF, frame, RooFit.ProjectionRange(cut), RooFit.NormRange(cut), RooFit.ProjWData(dataB), RooFit.NumCPU(nCPUs,True), RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.Precision(1e-4), visRooCmdArg, oscSlice)
          #Final_PDF.plotOn(frame, RooFit.ProjectionRange(cut), RooFit.NormRange(cut), RooFit.ProjWData(dataB), RooFit.NumCPU(nCPUs,True), RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.DrawOption("F"), RooFit.Precision(1e-4), visRooCmdArg, oscSlice) #12 args
          Final_PDF.plotOn(frame, arguments)
        else:
          #Final_PDF.plotOn(frame, RooFit.ProjWData(dataB), RooFit.NumCPU(nCPUs,True), RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.Precision(1e-4), visRooCmdArg, oscSlice) #10 args
          Final_PDF.plotOn(frame, arguments)
        dataB.Delete()
      else:
        if config['visError'] and (config['doFit'] or config['loadFit']):
          if r.covQual() == 3:
            arguments.Add(RooFit.VisualizeError(r))
        if cut != "":
          arguments.Add(RooFit.ProjectionRange(cut))
          arguments.Add(RooFit.NormRange(cut))
          #w.obj(massCat+"Final_PDF").plotOn(frame, RooFit.ProjectionRange(cut), RooFit.NormRange(cut), RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.Precision(1e-4), visRooCmdArg, oscSlice) #10 args
          w.obj(massCat+"Final_PDF").plotOn(frame, arguments)
        else:
          #w.obj(massCat+"Final_PDF").plotOn(frame, RooFit.Components(component), RooFit.LineColor(lineColour), RooFit.LineStyle(lineStyle), RooFit.FillColor(fillColour), RooFit.FillStyle(fillStyle), RooFit.Precision(1e-4), visRooCmdArg, oscSlice) #8 args
          w.obj(massCat+"Final_PDF").plotOn(frame, arguments)
    for data,icolour in dataRedArr:
      data.plotOn(frame, RooFit.MarkerColor(colours[icolour]), RooFit.MarkerSize(0.8))
  else: # its an asym plot
    print "Plotting:" ,plotName
    sys.stdout.flush()
    timeThisBit = TStopwatch()
    timeThisBit.Start()
    for data,icolour in dataRedArr:
      data.plotOn(frame, RooFit.Asymmetry(asymVar), RooFit.MarkerColor(coloursAsym[icolour]),RooFit.Binning(numBins))
    arguments = RooLinkedList()
    for arg in [RooFit.Asymmetry(asymVar), RooFit.LineColor(ROOT.kRed), RooFit.Precision(1e-4)]:
      arguments.Add(arg)
    #if massCat == "":
    if False:
      dataB = RooDataHist(dsName, dsName, RooArgSet(B0_MASS_CAT), dataRedArr[-1][0], 1.0)
      dataB.Print()
      print "nCPUs:",nCPUs
      if visRooCmdArg != RooCmdArg.none():
        print "Ignoring the visualise errors command when creating asymmetry plots over multiple categories"
      if cut != "":
        arguments.Add(RooFit.ProjectionRange(cut))
        arguments.Add(RooFit.NormRange(cut))
        arguments.Add(RooFit.ProjWData(dataB))
        #Final_PDF.plotOn(frame, RooFit.Asymmetry(asymVar), RooFit.ProjectionRange(cut), RooFit.NormRange(cut), RooFit.ProjWData(dataB), RooFit.NumCPU(nCPUs,True), RooFit.LineColor(ROOT.kRed), RooFit.Precision(1e-4))
        Final_PDF.plotOn(frame, arguments)
      else:
        #Final_PDF.plotOn(frame, RooFit.Asymmetry(asymVar), RooFit.ProjWData(dataB), RooFit.NumCPU(nCPUs,True), RooFit.LineColor(ROOT.kRed), RooFit.Precision(1e-4))
        Final_PDF.plotOn(frame, arguments)
      dataB.Delete()
    else:
      if cut != "":
        arguments.Add(RooFit.ProjectionRange(cut))
        arguments.Add(RooFit.NormRange(cut))
        #w.obj(massCat+"Final_PDF").plotOn(frame, RooFit.Asymmetry(asymVar), RooFit.ProjectionRange(cut), RooFit.NormRange(cut), RooFit.NumCPU(1), RooFit.LineColor(ROOT.kRed), RooFit.Precision(1e-4), visRooCmdArg)
        w.obj(massCat+"Final_PDF").plotOn(frame, arguments)
      else:
        #w.obj(massCat+"Final_PDF").plotOn(frame, RooFit.Asymmetry(asymVar), RooFit.NumCPU(1), RooFit.LineColor(ROOT.kRed), RooFit.Precision(1e-4), visRooCmdArg)
        w.obj(massCat+"Final_PDF").plotOn(frame, arguments)
    frame.SetAxisRange(-.4,.4,"y")
    timeThisBit.Stop()
    timeThisBit.Print()
  for data,icolour in dataRedArr:
    data.Delete()
  sys.stdout.flush()
  return frame

def plotData(var,data):
  print "Plotting: Data_"+var+"_"+data.GetName()
  frame = w.obj(var).frame()
  data.plotOn(frame)
  return ["Data_"+var+"_"+data.GetName(),frame]

from multiprocessing import Process, Queue

def makePlotArray(q,w,plotName,plotVar,cpus,mixState,massCat,cut,dataArr,varMax=-1,asym=False,numBins=False):
  os.nice(config['niceness'])
  plot = [plotName,ueberPlot(w,plotName,plotVar,cpus,mixState,massCat,cut,dataArr,varMax,asym,numBins)]
  histNameSuffix = "" if asym == False else "_Asym["+asym.GetName()+"]"
  q.put([plot,
         [plotName+"_Pull",plot[1].pullHist("h_"+dataArr[-1].GetName()+histNameSuffix)]])


timePlots = []

queueList = []
processList = []

if config['doPlots']:

  #w.obj("D_DMASS_Ds").setBins(massBinning.numBins())
  #w.obj("B_CORTAU").setBins(tauBinning.numBins())
  binnedDataSet = RooDataHist("binnedDataSet","binnedDataSet",w.set("args"),fullUnbDataSet)
  binnedDataSet.Print()
  ##getattr(w,"import")(binnedDataSet)
  #w.obj("D_DMASS_Ds").setBins(100)
  #w.obj("B_CORTAU").setBins(int(round(maxtau*50./.12)))
  ##w.obj("B_CORTAU").setBinning(tauBinningHigZoom)
  ##w.obj("B_CORTAU").setMax(0.12)
  ##w.obj("B_CORTAU").setBins(int(round(2200*maxtau/5.)))
  ##w.obj("B_CORTAU").setBins(50)
  ##w.obj("B_CORTAU").setBinning(tauBinningHigZoom)
  ##highResDataSet = RooDataHist("highResDataSet","highResDataSet",w.set("args"),getattr(fullUnbDataSet,'reduce')('B_CORTAU<0.12'))
  #highResDataSet = RooDataHist("highResDataSet","highResDataSet",w.set("args"),fullUnbDataSet)
  #highResDataSet.Print()
  #w.obj("D_DMASS_Ds").setBins(100)
  #w.obj("B_CORTAU").setBins(int(round(maxtau*50./.5)))
  ##w.obj("B_CORTAU").setBinning(tauBinningMidZoom)
  ##w.obj("B_CORTAU").setMax(0.5)
  ##w.obj("B_CORTAU").setBins(int(round(400*maxtau/5.)))
  ##w.obj("B_CORTAU").setBins(50)
  ##midResDataSet = RooDataHist("midResDataSet","midResDataSet",w.set("args"),getattr(fullUnbDataSet,'reduce')('B_CORTAU<0.5'))
  #midResDataSet = RooDataHist("midResDataSet","midResDataSet",w.set("args"),fullUnbDataSet)
  #midResDataSet.Print()
  #w.obj("B_CORTAU").setMax(maxtau)

  timePlots = [plotData("D0_M",binnedDataSet),plotData("Del_M",binnedDataSet)]
  
  mixState = ""
  nRegion = ""

  for dsN,data in [("FullData",[binnedDataSet])]:
    for dst_side in ["", "dstsig", "dsthigh", "dstlow"]:
      for d_side in ["", "dsig", "dhigh", "dlow"]:
        cutName = dst_side+d_side
        plotName = dsN + "_" + "DelM_" + (dst_side if dst_side != "" else "dstall") + "_" + (d_side if d_side != "" else "d0all")
        queueList.append(Queue())
        processList.append(Process(target=makePlotArray, args=(queueList[-1],w,plotName,w.obj("Del_M"),nCPUs,mixState,nRegion,cutName,data,-1,False)))

  for dsN,data in [("FullData",[binnedDataSet])]:
    for dst_side in ["", "dstsig", "dsthigh", "dstlow"]:
      for d_side in ["", "dsig", "dhigh", "dlow"]:
        cutName = dst_side+d_side
        plotName = dsN + "_" + "D0M_" + (dst_side if dst_side != "" else "dstall") + "_" + (d_side if d_side != "" else "d0all")
        queueList.append(Queue())
        processList.append(Process(target=makePlotArray, args=(queueList[-1],w,plotName,w.obj("D0_M"),nCPUs,mixState,nRegion,cutName,data,-1,False)))

  startAt = 0
  if config['doPlotsAsymLong']:
    startAt = 2
    for i in range(startAt):
      #print "starting", i
      processList[i].start()

  minPlotNumber = startAt
  while len(processList) > minPlotNumber:
    threads = spareThreads = (nCPUs - startAt - 1) if (nCPUs - startAt - 1) > 0 else 1
    if len(processList) - minPlotNumber < spareThreads:
      threads = len(processList) - minPlotNumber
    for i in range(threads):
      #print "starting", i+minPlotNumber
      sys.stdout.flush()
      processList[i+minPlotNumber].start()
    for i in range(threads):
      #print "getting", i+minPlotNumber
      sys.stdout.flush()
      timePlots += queueList[i+minPlotNumber].get()
      #print "joining", i+minPlotNumber
      processList[i+minPlotNumber].join()
    minPlotNumber += threads

  #timePlots.sort()

  binnedDataSet.Delete()
  #highResDataSet.Delete()
  #midResDataSet.Delete()
  #lowResDataSet.Delete()

def nllPlot(var,dpll):
  nframe = var.frame(RooFit.Title("nll plot of " + var.GetName()))
  arguments = RooLinkedList()
  for arg in [RooFit.Precision(1e-4),RooFit.ShiftToZero(),RooFit.PrintEvalErrors(-1),RooFit.EvalErrorValue(nll.getVal()+10),RooFit.LineStyle(ROOT.kDashed)]:
    arguments.Add(arg)
  nll.plotOn(nframe,arguments)
  #nll.plotOn(nframe,RooFit.Precision(1e-4),RooFit.ShiftToZero(),RooFit.PrintEvalErrors(-1),RooFit.EvalErrorValue(nll.getVal()+10),RooFit.LineStyle(ROOT.kDashed))
  #nll.plotOn(nframe,RooFit.Precision(1e-4),RooFit.ShiftToZero(),RooFit.PrintEvalErrors(-1),RooFit.EvalErrorValue(nll.getVal()+10),RooFit.LineStyle(ROOT.kSolid))
  #nframe.GetYaxis().SetRangeUser(0,2000)
  if dpll:
    pll = nll.createProfile(RooArgSet(var))
    pll.plotOn(nframe,RooFit.NumCPU(nCPUs,True),RooFit.PrintEvalErrors(-1))
    #nframe.SetTitle( "nll plot of " + var.GetName()) ;
    #ncanv=TCanvas("ncanv" + var.GetName() ,nframe.GetTitle(),800,600)
    #nframe.Draw()
  return nframe

def allNlls(cpus=10,mixedSignals=False):
  doPll = False
  varList = Final_PDF.getParameters(fullDataSet)

  it=varList.createIterator()
  out=[]
  while True:
    var = it.Next()
    if not var:
      print "End of variables"
      sys.stdout.flush()
      break
    if var.Class().GetName() == "RooCategory":
      print var.GetName(), "is a RooCategory, skipping"
      sys.stdout.flush()
      continue
    if var.isConstant():
      print var.GetName(), "is constant, skipping"
      sys.stdout.flush()
      continue
    if config['partialNlls'] != False:
      if not config['partialNlls'] in var.GetName():
        print var.GetName(), "doesn't have", config['partialNlls'], "in its name"
        continue
    print var.GetName(), "looks good calculating nll plot"
    sys.stdout.flush()
    np = nllPlot(var,doPll)
    out.append([var.GetName(),np])
    #nll_file = TFile.Open("nllPlots.root","UPDATE")
    #np.Write("NllOf_"+var.GetName())
    #nll_file.Close()

  return out



hcorr = False
if config['doFit'] or config['loadFit']:
  if r:
    hcorr = r.correlationHist()

print "Saving plots to file..."
sys.stdout.flush()
save_file = TFile.Open(config['outFileName'],"RECREATE")
save_file.cd()
for i in timePlots:
  i[1].Write(i[0])
if config['doFit'] or config['loadFit']:
  if r:
    hcorr.Write("CorrelationHist")
    r.Write("RooFitResults")
save_file.Close()
print "Plots saved"
sys.stdout.flush()

save_file = False

timers["plotting"].Stop()
timers["plotting"].Print()

timers["nlls"].Start()
print "Starting nll plots"
sys.stdout.flush()

if config['doNlls']:
  nll = False
  if config['doBinnedNll']:
    nll = Final_PDF.createNLL(fullDataSet, RooFit.NumCPU(nCPUs,True))
  else:
    nll = Final_PDF.createNLL(fullUnbDataSet, RooFit.NumCPU(nCPUs,True))

  nlllist = allNlls()

  for i in nlllist:
    timePlots.append(["NllOf_"+i[0],i[1]])

print "Getting high CPU asym Plots..."#, startAt, doPlots, config['doPlotsAsymLong']
#print "Getting Long asym Plots", startAt, doPlots, config['doPlotsAsymLong']
if config['doPlots']:
  if config['doPlotsAsymLong']:
    for i in range(startAt):
      #print "getting", i
      sys.stdout.flush()
      timePlots += queueList[i].get()
      #print "joining", i
      sys.stdout.flush()
      processList[i].join()



save_file = TFile.Open(config['outFileName'],"RECREATE")
save_file.cd()
for i in timePlots:
  i[1].Write(i[0])
if config['doFit'] or config['loadFit']:
  if r:
    hcorr.Write("CorrelationHist")
    r.Write("RooFitResults")
save_file.Close()


timers["nlls"].Stop()
timers["nlls"].Print()

timers["gof"].Start()
sys.stdout.flush()


def gofCalcL(queue,gof,radius):
  os.nice(config['niceness'])
  queue.put(gof.calculateL(radius))

gofPlot = False
if config['doGof']:
  print "Starting gof calculation"


  cuts = [["UnmixedLowBMass","B0_MASS_CAT == 0 && "+B0_OSCIL.GetName()+" == -1"],["MixedLowBMass","B0_MASS_CAT == 0 && "+B0_OSCIL.GetName()+" == 1"],["UnmixedHighBMass","B0_MASS_CAT == 1 && "+B0_OSCIL.GetName()+" == -1"],["MixedHighBMass","B0_MASS_CAT == 1 && "+B0_OSCIL.GetName()+" == 1"]]

  globalPulls = []
  from math import sqrt
  from ROOT import TH1D

  for name,cut in cuts:
    data = getattr(fullDataSet,"reduce")(cut)
    nEntries = data.numEntries()

    observables = Final_PDF.getObservables(data)
    #normVars = observables
    normVars = RooArgSet(w.obj("D_DMASS_Ds"),w.obj("B_CORTAU"))

    globalPulls.append(["GlobalBinVol_"+name,TH1D("GlobalBinVol_"+name,"GlobalBinVol_"+name,400,0,.2)])
    globalPulls.append(["GlobalPull_"+name,TH1D("GlobalPull_"+name,"GlobalPull_"+name,400,-50,50)])
    globalPulls.append(["GlobalPdf_"+name,TH1D("GlobalPdf_"+name,"GlobalPdf_"+name,400,0,.2)])
    globalPulls.append(["GlobalEntries_"+name,TH1D("GlobalEntries_"+name,"GlobalEntries_"+name,200,0,200)])

    print "Calculating global pull for",name

    emptyBins = 0
    pdfSum = 0.

    timeThisBit = TStopwatch()
    timeThisBit.Start()
    for i in xrange(nEntries):
      if i%(nEntries/10) == 0:
        print 100*i/nEntries, "% complete"
      if i%10==0:
        argSet = data.get(i)
        entries = data.weight(argSet)
        volume = data.binVolume(argSet)
        if entries == 0.:
          emptyBins += 1
          continue
        obsIter = argSet.createIterator()
        while True:
          obj = obsIter.Next()
          if not obj:
            break
          if "RooCategory" == obj.ClassName():
            value = argSet.find(obj.GetName()).getBin()
            observables.find(obj.GetName()).setBin(value)
          elif "RooRealVar" == obj.ClassName():
            value = argSet.find(obj.GetName()).getVal()
            observables.find(obj.GetName()).setVal(value)
        pdf = Final_PDF.getVal(normVars)
        pdfSum += pdf*nEntries*volume
        globalPulls[-4][1].Fill(volume)
        globalPulls[-3][1].Fill((entries-pdf*nEntries*volume)/sqrt(entries))
        globalPulls[-2][1].Fill(pdf)
        globalPulls[-1][1].Fill(entries)

    print "There are",emptyBins," empty bins of",nEntries,"total bins,",emptyBins*100/nEntries,"% in",name,"pdfSum",pdfSum
    timeThisBit.Stop()
    timeThisBit.Print()

  globalPulls.sort()
  timePlots += globalPulls


  print "Calculating gof with density method"

  from ROOT import TGraph

  processList = []
  queueList = []
  resultList = []
  gof = {}

  nPoints = 40
  maxR = 0.2

  print "Radius going from", maxR*float(1)/nPoints, "to", maxR*float(nPoints)/nPoints, "in", nPoints, "steps"

  datasets = {}
  for name,cut in cuts:
    datasets[name] = getattr(fullUnbDataSet,"reduce")(cut)
    gof[name] = RooGofSquareDensity(Final_PDF, datasets[name], w.obj("B_CORTAU"), w.obj("D_DMASS_Ds"))
    gof[name].readData(1./10.)
    for i in range(nPoints):
      radius = maxR*float(i+1)/nPoints
      queueList.append(Queue())
      processList.append(Process(target=gofCalcL, args=(queueList[-1],gof[name],radius)))

  startAt = 0
  minPlotNumber = startAt
  while len(processList) > minPlotNumber:
    threads = spareThreads = (nCPUs - startAt - 1) if (nCPUs - startAt - 1) > 0 else 1
    if len(processList) - minPlotNumber < spareThreads:
      threads = len(processList) - minPlotNumber
    for i in range(threads):
      #print "starting", i+minPlotNumber
      sys.stdout.flush()
      processList[i+minPlotNumber].start()
    for i in range(threads):
      #print "getting", i+minPlotNumber
      sys.stdout.flush()
      resultList.append(queueList[i+minPlotNumber].get())
      #print "joining", i+minPlotNumber
      processList[i+minPlotNumber].join()
    minPlotNumber += threads

  offset = 0
  for name,cut in cuts:
    tg = TGraph(nPoints)
    for i in range(nPoints):
      tg.SetPoint(i,maxR*float(i+1)/nPoints,resultList[i+offset])
    offset += nPoints
    timePlots.append(["Gof_"+name,tg])

  save_file = TFile.Open(config['outFileName'],"RECREATE")
  save_file.cd()
  for i in timePlots:
    i[1].Write(i[0])
  #if doGof:
    #gofPlot.Write("Gof_LDist")
  if config['doFit'] or config['loadFit']:
    if r:
      hcorr.Write("CorrelationHist")
      r.Write("RooFitResults")
  save_file.Close()

timers["gof"].Stop()
timers["total"].Stop()

#sshProc = subprocess.call("ssh -f thomas@`who | grep tbird | grep -v \":pts\" | cut -d'(' -f 2 | sed \"s/)//\"` \"DISPLAY=:0 kdialog --msgbox \\\"Fitter finished on `hostname`\\\"\"", shell=True)




if config['doFit'] or config['loadFit']:
  if r:
    printSetVarLimits(w)
    printTexRes(r)
    checkVarLimits(w)
    print "Minimum value of NLL:", r.minNll()
    r.Print()
    sys.stdout.flush()
else:
  printSetVarLimits(w)
  checkVarLimits(w)
  sys.stdout.flush()


for key in ['startup', 'fitting', 'plotting', 'gof', 'nlls', 'total']:
  sys.stdout.write('{:<13}'.format(key+":"))
  timers[key].Print()

print "Done at %s, saved in" % datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"), config['outFileName']

