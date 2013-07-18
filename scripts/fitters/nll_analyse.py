#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, datetime, argparse

from math import fabs

parser = argparse.ArgumentParser(description='Analyse -log(likelihood) curves and adjust paramter ranges to aid in fit convergance.')
parser.add_argument("maximum", type=float, help='Search for max*100+10 on -log(likelihood) curve')
parser.add_argument("filename", help='Name of ROOT file containing RooFitResults and -log(likelihood) curves')
parser.add_argument("-s","--shrink", action='store_true', help='Only make ranges smaller, unless at limit')
args = parser.parse_args()
#print args
#sys.exit()

#if len(sys.argv) != 3:
  #sys.exit("This program takes two arguments, the maximum limit of the nll plots (x100+10) and the file name to analyse.")

#print sys.argv

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT
from ROOT import TFile

#nllarg = float(sys.argv[1])
nllarg = args.maximum
nllHeight = nllarg * 100. + 10.

#f = TFile.Open(sys.argv[2])
f = TFile.Open(args.filename)
keys = f.GetListOfKeys()
keyIt = keys.MakeIterator()

r=f.Get("RooFitResults")

#print f, nllarg, nllHeight

def printVarLimits(name,v,mi,ma,err=False) :
  print "w.obj('"+name+"').setMin("+str(mi)+") ; w.obj('"+name+"').setMax("+str(ma)+") ; w.obj('"+name+"').setVal("+str(v)+")" + ( (" ; w.obj('"+name+"').setError("+str(err)+")") if err!=False else "" )

def findMin(xs,ys,xMin,xMax,n):
  minVal=[1e10,1e10]
  for i in range(1,n-1):
    #print y[i], minVal
    if y[i]<minVal[1]:
      minVal[0] = xs[i]
      minVal[1] = ys[i]

  return minVal[0]

def validateMinMax(name,val):
  if "Bd_in_Bs" in name:
    if val > 1.:
      print "# Attempted value", val, "hits limits", 1.
      return 1.
    elif val < -0.05:
      print "# Attempted value", val, "hits limits", -0.05
      return -0.05
  elif "Tau_Scale" in name:
    if val < .05:
      print "# Attempted value", val, "hits limits", .05
      return .05
    elif val > 5.:
      print "# Attempted value", val, "hits limits", 5.
      return 5.
  elif "Frac_Dd_Prompt" in name:
    if val > .1:
      print "# Attempted value", val, "hits limits", .1
      return .1
    elif val < 0.0:
      print "# Attempted value", val, "hits limits", 0.0
      return 0.0
  elif "T_Side2_Acc_diff" in name:
    if val < 0.:
      print "# Attempted value", val, "hits limits", 0.
      return 0.
    elif val > 1.7:
      print "# Attempted value", val, "hits limits", 1.4
      return 1.7
  elif ( "Frac" in name and not "Kink" in name ) or "Acc_f" in name:
    if val > 1.:
      print "# Attempted value", val, "hits limits", 1.
      return 1.
    elif val < 0.00001:
      print "# Attempted value", val, "hits limits", 0.00001
      return 0.00001
  elif "M_Dd_N" in name or "M_Ds_N" in name:
    if val > 130.:
      print "# Attempted value", val, "hits limits", 130.
      return 130.
    elif val < 0.00001:
      print "# Attempted value", val, "hits limits", 0.00001
      return 0.00001

  elif "Asym" in name:
    if val > 1.:
      print "# Attempted value", val, "hits limits", 1.
      return 1.
    elif val < -1.:
      print "# Attempted value", val, "hits limits", -1.
      return -1.
  elif "diff" in name:
    if val < 0.:
      print "# Attempted value", val, "hits limits", 0.
      return 0.
    elif val > 1.25:
      print "# Attempted value", val, "hits limits", 1.25
      return 1.25
  elif "T_Sig_Bs_Mistag_Asym" in name:
    if val > .45:
      print "# Attempted value", val, "hits limits", .45
      return .45
    elif val < -.6:
      print "# Attempted value", val, "hits limits", -.6
      return -.6
  elif "Mistag" in name:
    if val > .7:
      print "# Attempted value", val, "hits limits", .7
      return .7
    elif val < -.02:
      print "# Attempted value", val, "hits limits", -.02
      return -.02
  elif "T_Dstar_Tau" in name:
    if val > 7.:
      print "# Attempted value", val, "hits limits", 7.
      return 7.
    elif val < 0.1:
      print "# Attempted value", val, "hits limits", 0.1
      return 0.1
  elif "M_Dstar_Mean" in name:
    if val > 70.:
      print "# Attempted value", val, "hits limits", 70.
      return 70.
    elif val < 24.:
      print "# Attempted value", val, "hits limits", 24.
      return 24.
  elif "T_Dstar_Acc_a" in name:
    if val < 0.001:
      print "# Attempted value", val, "hits limits", 0.001
      return 0.001
    elif val > 4.:
      print "# Attempted value", val, "hits limits", 4.
      return 4.
  elif "_x" in name:
    if val > 1.:
      print "# Attempted value", val, "hits limits", 1.
      return 1.
    elif val < -1.:
      print "# Attempted value", val, "hits limits", -1.
      return -1.
  elif "DAfs" in name:
    if val > .2:
      print "# Attempted value", val, "hits limits", .2
      return .2
    elif val < -.2:
      print "# Attempted value", val, "hits limits", -.2
      return -.2
  #elif "M_a" in name:
    #if val > 1.:
      #print "# Attempted value", val, "hits limits", 1.
      #return 1.
    #elif val < -1.:
      #print "# Attempted value", val, "hits limits", -1.
      #return -1.
  elif "T_t0" in name:
    if val > 0.015 and "Low" in name:
      print "# Attempted value", val, "hits limits", 0.015
      return 0.015
    elif val > 0.012 and "High" in name:
      print "# Attempted value", val, "hits limits", 0.012
      return 0.012
    elif val > 0.012:
      print "# Attempted value", val, "hits limits", 0.012
      return 0.012
    elif val < 0.:
      print "# Attempted value", val, "hits limits", 0.
      return 0.
  elif "Acc_Scale" in name:
    if val > .99:
      print "# Attempted value", val, "hits limits", .99
      return .99
    elif val < .001:
      print "# Attempted value", val, "hits limits", .001
      return .001
  elif "Tau" in name :
    if val < 0.01:
      print "# Attempted value", val, "hits limits", 0.01
      return 0.01
    elif val > 10:
      print "# Attempted value", val, "hits limits", 10
      return 10
  elif ("Acc_a" in name or "Acc_b" in name) and not "Scale" in name:
    if val < 0.001:
      print "# Attempted value", val, "hits limits", 0.001
      return 0.001
    elif val > 4.5:
      print "# Attempted value", val, "hits limits", 4.5
      return 4.5
  elif "Sigma" in name:
    if val < 0.001:
      print "# Attempted value", val, "hits limits", 0.001
      return 0.001
    elif val > 10:
      print "# Attempted value", val, "hits limits", 10
      return 10
  elif "Scale" in name:
    if val < 0.0001:
      print "# Attempted value", val, "hits limits", 0.0001
      return 0.0001
  return val


def findRoughMin(xs,ys,xMin,xMax,n):
  minVal = findMin(xs,ys,xMin,xMax,n)
  rang = xMin-xMax
  percent = round(50.*(minVal-xMin)/rang)
  #print minVal, xMin, rang, percent, percent*rang/100+xMin
  return percent*rang/50.+xMin


def extrapMax(x,y,xMin,xMax,xLen,name):
  minVal = findMin(x,y,xMin,xMax,xLen)
  if xMax-minVal>0.:
    m = (y[xLen-3])/(xMax-minVal)
    #m = (xMax-minVal)/y[xLen-3]
    new = xMax
    if m == 0.:
      new = xMax+(xMax-xMin)
    else:
      c = -m*minVal
      new = (nllHeight-c)/m
    sf = .75
    if new > xMax+(xMax-xMin)*sf:
      print "# Dont want to expand max range to",new, "too far"
      new = xMax+(xMax-xMin)*sf
    #print "extrapMax:", minVal, m, c, new, new-minVal, new-minVal < (xMax-xMin)*sf, (xMax-xMin)*sf
    return validateMinMax(name,new)
  else:
    return validateMinMax(name,xMax+(xMax-xMin))
  ## High_Frac_Ds_Detached  has a low first and last bin! Orig limits 0.18 0.31
  #extrapMin: 0.2606 -12045.0061679 3138.92860735 0.131915964608 0.128684035392 True -0.2418
  #extrapMax: 0.2606 6525.32652887 -1700.50009342 0.498136005768 0.237536005768 False 0.1482
  #w.obj('High_Frac_Ds_Detached').setMin(0.131915964608) ; w.obj('High_Frac_Ds_Detached').setMax(0.1482) ; w.obj('High_Frac_Ds_Detached').setVal(0.284)


def extrapMin(x,y,xMin,xMax,xLen,name):
  minVal = findMin(x,y,xMin,xMax,xLen)
  if xMin-minVal<0.:
    m = y[1]/(xMin-minVal)
    #m = (xMin-minVal)/y[1]
    c = -m*minVal
    new = (nllHeight-c)/m
    sf = .75
    if new < xMin-(xMax-xMin)*sf:
      print "# Dont want to expand min range to",new, "too far"
      new = xMin-(xMax-xMin)*sf
    #print "extrapMin:", minVal, m, c, new , minVal-new,minVal-new < (xMax-xMin)*sf,(xMax-xMin)*sf
    return validateMinMax(name,new)
  else:
    return validateMinMax(name,xMin-(xMax-xMin))

def nllError(nllVal,badValues):
  if nllVal < 10. + (1./10.) and nllVal > 10. - (1./10.):
    return True
  elif nllVal in badValues:
    return True
  else:
    return False

def error(name,r):
  return r.floatParsFinal().find(name).getError()

print "# nll analyse, nlls up to", nllHeight, "on", datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"), "run on", f.GetName()
print "#"

while True:
  key = keyIt.Next()
  if not key:
    break
  if "NllOf_" not in key.GetName():
    continue
  if "dM" in key.GetName():
    continue
  #if not "Low_T_Sig_Bs_Mistag" in key.GetName():
    #continue

  curve=key.ReadObj().getCurve()

  name = key.GetName().strip()[len("NllOf_"):]

  fitVal = r.floatParsFinal().find(name).getVal()


  x=curve.GetX()
  #y=curve.GetY()
  yOrig=curve.GetY()
  xLen = curve.GetN()

  nllMin = yOrig[sorted([[fabs(x[ix]-fitVal),ix] for ix in xrange(xLen)])[0][1]]

  y = [(yOrig[iy]-nllMin)+.1 if (yOrig[iy]-nllMin+.1)>0 else 10. for iy in xrange(xLen)]


  #xMin = curve.GetMinimum()
  #xMax = curve.GetMaximum()
  #xMin = curve.GetXaxis().GetXmin()
  #xMax = curve.GetXaxis().GetXmax()
  xMin = x[2]
  xMax = x[xLen-3]

  #if y[1] < nllHeight and y[xLen - 2] < nllHeight:
    #print "#",name," has a low first and last bin"
    #printVarLimits(name,findMin(x,y,xMin,xMax,xLen),xMin,xMax)
    #continue

  minFound = False
  maxFound = False

  lowestFound = False
  highestFound = False

  #print "starting nll data loop"

  valueCounter = {}

  for i in xrange(2,xLen-3):
    try:
      valueCounter[y[i]] += 1
    except KeyError:
      valueCounter[y[i]] = 1

  badValues = [yVal for yVal,nEntries in valueCounter.iteritems() if nEntries>5]

  for i in xrange(2,xLen-3):
    #print minFound,maxFound,x[i], y[i], nllError(y[i])
    if not minFound:
      #print y[i] < nllHeight, not nllError(y[i]) , not nllError(y[i+1]) , not nllError(y[i+2])
      if y[i] < nllHeight and not nllError(y[i],badValues) and not nllError(y[i+1],badValues) and not nllError(y[i+2],badValues) and y[i]!=y[i+1]:
        changeRatio = (y[i-1]-y[i])/(y[i]-y[i+1]) if i > 2 else 1.
        if y[i] < nllHeight*0.02 or (changeRatio < 1.2 and changeRatio > 0.8):
          minFound = x[i]
        elif changeRatio > 1.2 or changeRatio < 0.8:
          print "# ---->>>> changeRatio up",changeRatio,"at",x[i],":",i, (y[i-1]-y[i]),(y[i]-y[i+1])
        #print "found min range"
    elif minFound:
      if y[i] > nllHeight and not nllError(y[i-1],badValues) and not nllError(y[i-2],badValues) and not nllError(y[i-3],badValues) and y[i]!=y[i+1]:
        changeRatio = (y[i-1]-y[i])/(y[i]-y[i+1]) if i > 2 else 1.
        if y[i] < nllHeight*0.02 or (changeRatio < 1.2 and changeRatio > 0.8):
          maxFound = x[i-1]
        elif changeRatio > 1.2 or changeRatio < 0.8:
          print "# ---->>>> changeRatio down",changeRatio,"at",x[i],":",i, (y[i-1]-y[i]),(y[i]-y[i+1])
      elif nllError(y[i],badValues) and nllError(y[i+1],badValues) and nllError(y[i+2],badValues) and not nllError(y[i-1],badValues) and not nllError(y[i-2],badValues) and not nllError(y[i-3],badValues):
        maxFound = x[i-1]
        #print y[i], y[i-1],x[i-1]
        #print "#ELEPHANT", i, x[i-1], y[i-3], y[i-2], y[i-1], y[i], y[i+1], y[i+2]

    if not lowestFound:
      #print y[i] < nllHeight, not nllError(y[i]) , not nllError(y[i+1]) , not nllError(y[i+2])
      if not nllError(y[i],badValues) and not nllError(y[i+1],badValues) and not nllError(y[i+2],badValues) and y[i]!=y[i+1]:
        changeRatio = (y[i-1]-y[i])/(y[i]-y[i+1]) if i > 2 else 1.
        if y[i] < nllHeight*0.02 or (changeRatio < 1.2 and changeRatio > 0.8):
          lowestFound = x[i]
        #elif changeRatio > 1.2 or changeRatio < 0.8:
          #print "# ---->>>> changeRatio up",changeRatio,"at",x[i],":",i, (y[i-1]-y[i]),(y[i]-y[i+1])
        #print "found min range"
    elif lowestFound:
      if not nllError(y[i-1],badValues) and not nllError(y[i-2],badValues) and not nllError(y[i-3],badValues) and y[i]!=y[i+1]:
        changeRatio = (y[i-1]-y[i])/(y[i]-y[i+1]) if i > 2 else 1.
        if y[i] < nllHeight*0.02 or (changeRatio < 1.2 and changeRatio > 0.8):
          highestFound = x[i-1]
        #elif changeRatio > 1.2 or changeRatio < 0.8:
          #print "# ---->>>> changeRatio down",changeRatio,"at",x[i],":",i, (y[i-1]-y[i]),(y[i]-y[i+1])
      elif nllError(y[i],badValues) and nllError(y[i+1],badValues) and nllError(y[i+2],badValues) and not nllError(y[i-1],badValues) and not nllError(y[i-2],badValues) and not nllError(y[i-3],badValues):
        highestFound = x[i-1]
        #print "found max range"
    #print x[i], y[i], minFound, maxFound
    #print y[i], minFound, maxFound

  #print "finished nll data loop:",name,minFound,maxFound,lowestFound,highestFound

  #print "#DEBUG:",lowestFound,minFound,nllHeight,maxFound,highestFound

  if minFound == x[2]:
    minFound = False

  if args.shrink: #TODO: produces "setMax(False)" for some reason
    newMin = minFound
    newMax = maxFound

    if not newMin: newMin = lowestFound
    if not newMax: newMax = highestFound
    if not newMin: newMin = extrapMin(x,y,xMin,xMax,xLen,name)
    if not newMax: newMax = extrapMax(x,y,xMin,xMax,xLen,name)

    if minFound and not maxFound:
      print "#",name," has a low last bin. Orig limits",xMin,xMax
    elif not minFound and maxFound:
      print "#",name," has a low first bin. Orig limits",xMin,xMax
    elif not minFound and not maxFound:
      print "#",name," has a low first and last bin! Orig limits", xMin,xMax

    if lowestFound and not highestFound:
      print "#",name," has errors at low end of range. Orig limits",xMin,xMax
    elif not lowestFound and highestFound:
      print "#",name," has errors at low high of range. Orig limits",xMin,xMax
    elif not lowestFound and not highestFound:
      print "#",name," has errors at low and high ends of range! Orig limits", xMin,xMax

    printVarLimits(name,findRoughMin(x,y,xMin,xMax,xLen),newMin,newMax,error(name,r))
  else:
    if minFound and maxFound:
      printVarLimits(name,findRoughMin(x,y,xMin,xMax,xLen),minFound,maxFound,error(name,r))
      continue
    elif minFound and not maxFound:
      print "#",name," has a low last bin. Orig limits",xMin,xMax
      printVarLimits(name,findRoughMin(x,y,xMin,xMax,xLen),minFound,extrapMax(x,y,xMin,xMax,xLen,name),error(name,r))
      continue
    elif not minFound and maxFound:
      print "#",name," has a low first bin. Orig limits",xMin,xMax
      printVarLimits(name,findRoughMin(x,y,xMin,xMax,xLen),extrapMin(x,y,xMin,xMax,xLen,name),maxFound,error(name,r))
      continue
    elif not minFound and not maxFound:
      print "#",name," has a low first and last bin! Orig limits", xMin,xMax
      printVarLimits(name,findRoughMin(x,y,xMin,xMax,xLen),extrapMin(x,y,xMin,xMax,xLen,name),extrapMax(x,y,xMin,xMax,xLen,name),error(name,r))
      continue






