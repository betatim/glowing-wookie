#!/usr/bin/env python

from ROOT import gROOT
gROOT.SetBatch(True)
gROOT.ProcessLine(".x ../lhcbstyle.C")

import ROOT
from ROOT import TCanvas, TFile, gPad, TLine

import sys

#particles = [("e","e")]
#particles = [("Pi","Pi")]
particles = [("Pi","Pi"),("K","K")]
#particles = [("e","e"), ("Mu","Mu"), ("Pi","Pi")]
#particles = [("e","e"), ("Pi","e"), ("Mu","Mu"), ("Pi","Mu")]
#particles = [("e","e"), ("Pi","e"), ("Mu","Mu"), ("Pi","e"), ("Pi","Pi")]
variables = ["P", "ETA", "nTracks"]
years = [2011,2012]
#years = [2011]
magnets = ["MagUp", "MagDown"]
#magnets = ["MagDown"]

stripping = {2011:"20r1", 2012:"20"}

tc = TCanvas("tc","tc",800,600)



def file_names(particle,misid,var,year,magnet):
  d = "/afs/cern.ch/user/t/tbird/cmtuser/Urania_v2r1/PIDCalib/PIDPerfScripts/scripts/python/Plots/"
  #d = "/afs/cern.ch/user/t/tbird/cmtuser/Urania_v2r3/PIDCalib/PIDPerfScripts/scripts/python/Plots/"
  particle_lower = misid.lower()
  a = [
    ("PubPlots_{part}_as_{part}_Strip{strip}_{pol}_kpi{year}{lowPart}_{var}.root",ROOT.kRed+2,"e1"),
    ("PlotCalibDistribution_{part}_{var}_Strip{strip}_{pol}_100bins{lowPart}_{var}.root",ROOT.kRed,"same hist ]["),
    ("PlotRefDistribution_{misid}_{var}_100bins{lowPart}_{var}_{year}.root",ROOT.kBlack,"same hist ]["),
    ("PlotCalibDistribution_{part}_{var}_Strip{strip}_{pol}_kpi{year}{lowPart}_{var}.root",ROOT.kRed,"same hist ]["),
    ("PlotRefDistribution_{misid}_{var}_kpi{year}{lowPart}_{var}_{year}.root",ROOT.kBlack,"same hist ]["),
    ]
  return [(d+f.format(part=particle,lowPart=particle_lower,var=var,misid=misid,strip=stripping[year],year=year,pol=magnet),color,opts) for f,color,opts in a]

def calculate_binning(plot,nBins,colour):
  tlines = []
  totalIntegral = plot.Integral()
  plotBins = plot.GetNbinsX()
  for i in xrange(nBins-1):
    j = 1
    integral = 0.
    xPos = None
    for j in xrange(1,plotBins+2):
      integral += plot.GetBinContent(j)
      #print i,j,integral,(i,1.),totalIntegral,nBins
      if integral > (i+1.)*totalIntegral/nBins:
        xPos = plot.GetBinCenter(j)
        break
      j += 1
    tlines.append(TLine(xPos,1.1,xPos,1.))
    tlines[-1].SetLineColor(colour)
  return tlines

for year in years:
  for magnet in magnets:
    for particle,misid in particles:
      for var in variables:
        tfs = []
        plots = []

        for f,color,opts in file_names(particle,misid,var,year,magnet):
          tfs.append(TFile(f))
          it = tfs[-1].GetListOfKeys().MakeIterator()
          found = False
          while True:
            k = it.Next()
            if not k:
              break
            if "_All" in k.GetName():
              if "PubPlots" in f and particle == "Pi":
                if misid == "Pi" and ("ProbNNpi" not in k.GetName() and "Hlt1TrackMuon_TOS" not in k.GetName() and "DLLK<0" not in k.GetName()):
                  continue
                if misid == "e" and "DLLe>4" not in k.GetName():
                  continue
                if misid == "Mu" and "ProbNNmu" not in k.GetName():
                  continue
                if misid == "Pi" and "DLLK<0" not in k.GetName():
                  continue
              plots.append(k.ReadObj())
              found = True
              break
            if "{misid}_{var}".format(part=particle,var=var,misid=misid) == k.GetName():
              plots.append(k.ReadObj())
              found = True
              break
          if not found: 
            print "Not found a plot in",f
            print "Avalible plots are:"
            it = tfs[-1].GetListOfKeys().MakeIterator()
            found = False
            while True:
              k = it.Next()
              if not k: break
              print k.GetName()
            sys.exit(1)

          if len(plots) > 1:
            firstsize = plots[-1].GetMaximum()
            if firstsize > 0.:
              scale = 0.9*gPad.GetUymax()/firstsize
              plots[-1].Scale(scale)
            else:
              print "Plot with zero maximum in",f

          plots[-1].SetMarkerColor(color)
          plots[-1].SetLineColor(color)
          if len(plots) in [4,5]:
            plots[-1].SetLineStyle(ROOT.kDashed)
          plots[-1].GetYaxis().SetRangeUser(0.,1.1)
          plots[-1].Draw(opts)

        tlines = []
        tenTLines = calculate_binning(plots[1],10,ROOT.kRed)
        tlines += tenTLines[:1]
        tlines += tenTLines[-1:]
        tlines += calculate_binning(plots[1],5,ROOT.kRed+2)
        for tl in tlines:
          tl.Draw()
          print "  AddBinBoundary(trType, '%s', 'kpi%i%s', %f)"%(var,year,particle.lower(),tl.GetX1())

        #print len(plots)

        tc.SaveAs("Calib_{part}_as_{misid}_{year}_{pol}_{var}.pdf".format(part=particle,year=year,pol=magnet,var=var,misid=misid))
        tc.SaveAs("Calib_{part}_as_{misid}_{year}_{pol}_{var}.png".format(part=particle,year=year,pol=magnet,var=var,misid=misid))
        for f in tfs:
          f.Close()
