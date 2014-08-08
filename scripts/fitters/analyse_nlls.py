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

import logging
logging.basicConfig(format='# %(levelname)-9s%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from copy import deepcopy

from ROOT import gROOT
#gROOT.SetBatch(True)
gROOT.ProcessLine(".x /afs/cern.ch/user/t/tbird/lhcbstyle.C")

import ROOT
from ROOT import TFile, TGraph

nllarg = args.maximum
nllHeight = nllarg * 100. + 10.

class Point:
  def __init__(self,i,x,y):
    self.i = i
    self.x = x
    self.y = y

class Curve:
  def __init__(self, name, curve, r):
    self.name = name
    self.length = curve.GetN()
    x_vals = curve.GetX()
    y_vals = curve.GetY()
    self.x = [x_vals[i] for i in xrange(self.length)]
    self.y = [y_vals[i] for i in xrange(self.length)]
    self.e = [False for i in xrange(self.length)]
    
    self.finalError = r.floatParsFinal().find(name).getError()
    self.finalValue = r.floatParsFinal().find(name).getVal()
    
    self.start = 2
    self.end = self.length-3
    
    self.xMin = self.x[self.start]
    self.xMax = self.x[self.end]

    #self.shiftToZero(r)
    
    self.findErrorValues()
    
    self.minimum = False
    self.lowerEdge = False
    self.upperEdge = False
    self.findMinimum()
    
  def shiftToZero(self, r):
    logger.debug("Shifting y values to zero")
    fitted_min = r.minNll()
    self.y = [i-fitted_min for i in self.y]
    for i,(val) in enumerate(self.y):
      if val < 0.:
        self.e[i] = True
    #self.y = [i if i>0. else 10. for i in self.y]
    
  def getPoints(self):
    return [(i,self.x[i],self.y[i]) for i in xrange(self.start,self.end)]
  
  def getPoint(self,i):
    x,y = self.x[i],self.y[i]
    if self.e[i]:
      y = 10.
    return [i,x,y]
    
  def findErrorValues(self):
    logger.debug("Finding error values")
    values = {}
    for i in xrange(self.start,self.end):
      try:
        values[self.y[i]] += 1
      except KeyError:
        values[self.y[i]] = 1

    duplicates = [yVal for yVal,nEntries in values.iteritems() if nEntries>5]
    
    for i,x,y in self.getPoints():
      if y in duplicates:
        self.e[i] = True
        
    for i,(y) in enumerate(self.y):
      if 9.9 < y < 10.1:
        self.e[i] = True
    
    for i in xrange(self.start,self.end):
      if self.y[i] > 0.02*nllHeight:
        if self.y[i]-self.y[i+1] != 0.:
          derivitive_ratio = (self.y[i-1]-self.y[i])/(self.y[i]-self.y[i+1])
          if derivitive_ratio < 0.8 or derivitive_ratio > 1.2:
            self.e[i] = True
        else:
          logger.warning("derivitive_ratio bottom is zero %i %f %f %f", i, self.y[i-1], self.y[i], self.y[i+1])
          
  def findMinimum(self):
    self.minimum = [False,self.finalValue,0.]
    return self.minimum 
  
  def pointIsSafe(self,i):
    return (not self.e[i-2]) and (not self.e[i-1]) and (not self.e[i]) and (not self.e[i+1]) and (not self.e[i+2])
  
  def findUpperEdge(self,nllHeight,extrapolate=True):
    logger.debug("finding upper edge")
    points = self.getPoints()
    if not self.minimum:
      self.findMinimum()
    self.upperEdge = self.findEdge(nllHeight,points)
    if not self.upperEdge and extrapolate:
      self.upperEdge = self.extrapolateEdge(nllHeight,points,self.xMax)
      logger.info("extrapolate upper edge %s",str(self.upperEdge))
    logger.debug("lower edge %s", str(self.upperEdge))
    return self.upperEdge
    
  def findLowerEdge(self,nllHeight,extrapolate=True):
    logger.debug("finding lower edge")
    points = self.getPoints()
    points.reverse()
    points = [(i,-x,y) for i,x,y in points]
    if not self.minimum:
      self.findMinimum()
    self.minimum[1] *= -1.
    self.lowerEdge = self.findEdge(nllHeight,points)
    if not self.lowerEdge and extrapolate:
      self.lowerEdge = self.extrapolateEdge(nllHeight,points,-self.xMin)
      tmp = deepcopy(self.lowerEdge)
      tmp[1] *= -1.
      logger.info("extrapolate lower edge %s",str(tmp))
    self.minimum[1] *= -1.
    self.lowerEdge[1] *= -1.
    logger.debug("lower edge %s", str(self.lowerEdge))
    return self.lowerEdge
    
  def findEdge(self,nllHeight,points):
    for i,x,y in points:
      #logger.debug("find edge %s %f %f %s", str([i,x,y]), self.minimum[1], nllHeight, str(self.pointIsSafe(i)))
      if x < self.minimum[1]:
        continue
      if y < nllHeight:
        continue
      if not self.pointIsSafe(i):
        continue
      logger.debug("edge found %s", str([i,x,y]))
      return [i,x,y]
    logger.debug("edge not found")
    return False
  
  def extrapolateEdge(self,nllHeight,points,edge):
    if (edge-self.minimum[1]) > 0.:
      m = (points[-2][2])/(edge-self.minimum[1])
      new = edge
      if m == 0.:
        new = edge+(self.xMax-self.xMin)
      else:
        c = -m*self.minimum[1]
        new = (nllHeight-c)/m
      logger.debug("extrap values %f %f %f %f %f %f %f", points[-2][2], edge, self.minimum[1], edge-self.minimum[1], m, c, new)
      sf = .75
      if new > edge+(self.xMax-self.xMin)*sf:
        logger.warning("Dont want to expand max range %f too far ",new)
        new = edge+(self.xMax-self.xMin)*sf
      logger.debug("extrapolate edge %s",str([False,new,nllHeight]))
      return [False,new,nllHeight]
    else:
      raise ValueError("Extrapolation range is smaller than zero")
      
  def __repr__(self):
    return self.__str__()
  def __str__(self):
    return "Curve(name='%s', min=%s, max=%s)" % (self.name, str(self.lowerEdge), str(self.upperEdge))
    
    
  def makeTGraph(self):
    self.tgv = TGraph() # valid points
    self.tge = TGraph() # error points
    self.tgl = TGraph() # calculated limits
    self.tga = TGraph() # all points mostly for axis
    ie, iv, ia = 0, 0, 0
    for i,x,y in self.getPoints():
      self.tga.SetPoint(ia,x,y)
      ia += 1
      if self.e[i]:
        self.tge.SetPoint(ie,x,y)
        ie += 1
      else:
        self.tgv.SetPoint(iv,x,y)
        iv += 1
    self.tgl.SetPoint(0, self.lowerEdge[1], self.lowerEdge[2])
    self.tgl.SetPoint(1, self.upperEdge[1], self.upperEdge[2])
    self.tgl.SetPoint(2, self.roughValue(), 0)
    self.tgl.SetPoint(3, self.finalValue, 0)
    
    self.tga.SetPoint(ia, self.lowerEdge[1], self.lowerEdge[2])
    self.tga.SetPoint(ia+1, self.upperEdge[1], self.upperEdge[2])
    self.tga.SetPoint(ia+2, self.roughValue(), 0)
    self.tga.SetPoint(ia+3, self.finalValue, 0)
    
    self.tgv.SetMarkerColor(ROOT.kGreen)
    self.tge.SetMarkerColor(ROOT.kRed)
    self.tgl.SetMarkerColor(ROOT.kBlue)
  
  def addTGraphTitles(self):
    #for p in [self.tgl]:
    for p in [self.tga, self.tgl, self.tge, self.tgv]:
      p.GetXaxis().SetTitle(self.name)
      p.GetYaxis().SetTitle("-log(likelihood)")
    
  def roughValue(self):
    steps = 10.
    new_range = self.upperEdge[1]-self.lowerEdge[1]
    norm = round((self.finalValue - self.lowerEdge[1])*steps/new_range)
    return (self.lowerEdge[1] + norm*new_range/steps)
    
  def printLimit(self):
    val = self.roughValue()
    print "w.obj('"+self.name+"').setMin("+str(self.lowerEdge[1])+") ; w.obj('"+self.name+"').setMax("+str(self.upperEdge[1])+") ; w.obj('"+self.name+"').setVal("+str(val)+")" + ( (" ; w.obj('"+self.name+"').setError("+str(self.finalError)+")") if self.finalError!=False else "" )

  def applyHardLimits(self):
    var_list = [
        ("Frac",0.,1.),
        ("Cheby",-1.,1.),
        ("alpha",0.,5.),
        ("Sigma",0.,30.),
        ("_N_",0.,None),
        ("_n",0.,20.),
      ]
    for name_fragment, lower, upper in var_list:
      if name_fragment in self.name:
        if lower != None:
          if self.lowerEdge[1] < lower:
            logger.warning("lower edge %f hits limit %f", self.lowerEdge[1],lower)
            self.lowerEdge[1] = lower
        if upper != None:
          if self.upperEdge[1] > upper:
            logger.warning("upper edge %f hits limit %f", self.upperEdge[1], upper)
            self.upperEdge[1] = upper


f = TFile.Open(args.filename)
keys = f.GetListOfKeys()
keyIt = keys.MakeIterator()

r=f.Get("RooFitResults")

print "# nll analyse, nlls up to", nllHeight, "on", datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"), "run on", f.GetName()
print "#"

#loopedVars = 0

curves = []

while True:
  key = keyIt.Next()
  if not key:
    break
  #if loopedVars > 20:
    #break
  if "NllOf_" not in key.GetName():
    continue
  #if "Prompt" not in key.GetName():
    #continue
  
  name = key.GetName().strip()[len("NllOf_"):]
  curve = key.ReadObj().getCurve()
  
  #print "# Make curve object"
  logger.debug("Creating curve object")
  curves.append(Curve(name,curve,r))

  logger.debug("calculating edges")
  curves[-1].findLowerEdge(nllHeight, extrapolate=(not args.shrink))
  curves[-1].findUpperEdge(nllHeight, extrapolate=(not args.shrink))
  curves[-1].applyHardLimits()
  #print "#", curves[-1]
  curves[-1].printLimit()

  #loopedVars += 1

from math import ceil, sqrt
from ROOT import TCanvas
tc=TCanvas("tc","tc",800,600)

#for c in curves:
#tc.Clear()

canv_x = int(ceil(sqrt(float(len(curves)))))
canv_y = int(ceil(float(len(curves))/canv_x))

logger.debug("Canvas %ix%i for %i plots", canv_x, canv_y, len(curves))

tc.Divide(canv_x, canv_y)
for i,(c) in enumerate(curves):
  tc.cd(i+1)
  c.makeTGraph()
  c.tga.Draw("A*")
  c.addTGraphTitles()
  c.tga.Draw("A*")
  c.tga.GetYaxis().SetRangeUser(0,2000.)
  c.tgv.Draw("*")
  c.tge.Draw("*")
  c.tgl.Draw("*")
  

