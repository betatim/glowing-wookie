
from ROOT import gROOT
gROOT.ProcessLine(".x ../lhcbstyle.C")
gROOT.SetBatch(True)

from itertools import combinations
from array import array
from random import gauss, random, uniform, expovariate

import ROOT
from ROOT import TLorentzVector, TGenPhaseSpace, TH1D, TCanvas, THStack, TLine

br_kk = 3.96e-3*0.9e-5
br_kpi = 3.88e-2*1.5e-5
br_pik = 3.88e-2*2.3e-5
br_pipi = 1.402e-3*3.4e-5

#frac_kpi = 0.33

##ratio of sig/bkg
#frac_sig_kk = 2338./8692.
#frac_sig_kpi = 361./860. # from strippted trigger
#frac_sig_pipi = 361./860. # from kk strippted trigger
##frac_sig_pipi = 749./3769. # from non stripped trigger

frac_sig_kk = 0.7
frac_sig_kpi = 0.7
frac_sig_pipi = 0.7

weights = {
  "kk_sig"    : frac_sig_kk*br_kk/br_pik,
  "kpi_sig"   : frac_sig_kpi*br_kpi/br_pik,
  "pik_sig"   : frac_sig_kpi*br_pik/br_pik,
  "pipi_sig"  : frac_sig_pipi*br_pipi/br_pik,
  "kk_back"   : (1.-frac_sig_kk)*br_kk/br_pik,
  "kpi_back"  : (1.-frac_sig_kpi)*br_kpi/br_pik,
  "pik_back"  : (1.-frac_sig_kpi)*br_pik/br_pik,
  "pipi_back" : (1.-frac_sig_pipi)*br_pipi/br_pik,
}

#frac_kpi = 0.4

#frac_sig_kk = 2338./8692.
#frac_sig_kpi = 361./860. # from strippted trigger
#frac_sig_pipi = 749./3769. # from non stripped trigger

#n_kk = 291./.28
#n_kpi = 860.
#n_pipi = 106.

#e_kk = n_kk/n_kk
#e_kpi = n_kpi/n_kk
#e_pipi = n_pipi/n_kk

##eff_k = 10. # kaons are eff_k more efficient than pions

#weights = {
  #"kk_sig"    : frac_sig_kk*e_kk,
  #"kpi_sig"   : frac_sig_kpi*frac_kpi*e_kpi,
  #"pik_sig"   : frac_sig_kpi*(1.-frac_kpi)*e_kpi,
  #"pipi_sig"  : frac_sig_pipi*e_pipi,
  #"kk_back"   : (1.-frac_sig_kk)*e_kk,
  #"kpi_back"  : (1.-frac_sig_kpi)*frac_kpi*e_kpi,
  #"pik_back"  : (1.-frac_sig_kpi)*(1.-frac_kpi)*e_kpi,
  #"pipi_back" : (1.-frac_sig_pipi)*e_pipi,
#}

pi = 0.1396
k  = 0.4937
mu = 0.1056
e  = 0.000511
d  = 1.864

dmin = d*1000.-300.
dmax = d*1000.+300.

for i,j in weights.iteritems():
  print i,j

def new_mass(old_p, target_mass):
  momentum = old_p.Clone()
  new_E = (target_mass**2 + sum(n**2 for n in (momentum.Px(),momentum.Py(),momentum.Pz())))**0.5
  momentum.SetE(new_E)
  return momentum

def new_mass_arr(old_p_arr, target_mass_arr):
  new_p_arr = []
  for old_p, target_mass in zip(old_p_arr,target_mass_arr):
    new_p_arr.append(new_mass(old_p,target_mass))
  return new_p_arr

def masses(true, assumed, function, a1, a2, weight):
  assumed_masses = []
  true_masses = []
  for _ in xrange(int(round(50000*weight))):
    D = TLorentzVector()
    trueM = function(a1, a2)
    true_masses.append(trueM*1000.)
    D.SetPtEtaPhiM(pt(), uniform(2.,5.), uniform(-3.14159,3.14159), trueM)
    gen = TGenPhaseSpace()
    m = array("d", true)
    gen.SetDecay(D, 2, m, "default")
    gen.Generate()
    p1, p2 = [new_mass(gen.GetDecay(n), m) for n,m in enumerate(assumed)]
    assumed_masses.append([p1,p2])
    #assumed_masses.append((p1+p2).M()*1000)
  return zip(assumed_masses,true_masses)

def get_mass(p_arr):
  p_tot = TLorentzVector()
  for x in p_arr:
    p_tot += x

  return p_tot.M()*1000.

def style_plot(plot, colour, ytitle="Entries", xtitle="D^{0} mass [MeV]"):
  plot.SetFillColor(colour)
  #plot.SetStats(True)
  plot.GetYaxis().SetTitle(ytitle)
  plot.GetXaxis().SetTitle(xtitle)


assumed_plots = []
true_plots = []
tc = TCanvas("tc", "tc",800,600)
ts_assumed = THStack("ts_assumed","ts_assumed")
ts_true = THStack("ts_true","ts_true")

def background(t=1.,b=1.):
  c = t - 1815.*(b-t)/100.
  while True:
    x = uniform(1.815,1.915)
    y = (b-t)/100.*x+c
    val = uniform(0.,t)
    if val < y:
      break
  return x

def signal(a,b):
  return gauss(1.868,7./1000.)

def pt():
  pt = 0.
  while pt < 500:
    pt = expovariate(4.10318e-04)
  pt /= 1000.
  return pt

def gauss_funct(x, mean, sigma):
  return exp(-.5*((x-mean)/sigma)**2)

def emu_sig(a,b):
  Aa  = 3.52897e+04
  Am  = 1.86214e+03
  As1 = 3.00707e+01
  As2 = 1.13122e+01
  Ba  = 5.83197e+03
  Bm  = 1.81140e+03
  Bs1 = 1.18648e+02
  Bs2 = 7.59641e+01

  while True:
    x = uniform(1500.,2100.)
    y = uniform(0.,45000.)
    val = 0.
    if x < Am:
      val += Aa*gauss_funct(x,Am,As1)
    else:
      val += Aa*gauss_funct(x,Am,As2)
    if x < Bm:
      val += Ba*gauss_funct(x,Bm,Bs1)
    else:
      val += Ba*gauss_funct(x,Bm,Bs2)

    if val < y:
      break

  return x

mass_hytpotheses = [("kk",[k,k]),("emu",[e,mu]),("mue",[mu,e]),("kpi",[k,pi]),("pik",[pi,k]),("pipi",[pi,pi])]

ts_assumed = [ THStack("ts_assumed_"+rec_name,"ts_assumed_%s;Reconstructed %s mass [MeV];Entries"%(rec_name,rec_name.replace("mu","#mu").replace("pi","#pi"))) for rec_name,hyp in mass_hytpotheses ]
ts_true = [ THStack("ts_true_"+rec_name,"ts_true_%s;True mass [MeV];Entries"%(rec_name,)) for rec_name,hyp in mass_hytpotheses ]

lines = []

for gen_name,true_hyp,bargs,colour in [("pipi",[pi,pi],[28.,19.],ROOT.kRed),("kpi",[k,pi],[1.,1.],ROOT.kBlue),("pik",[pi,k],[1.,1.],ROOT.kCyan),("kk",[k,k],[90.,58.],ROOT.kYellow)]:

  print "Making plot",gen_name,true_hyp

  for type_name, function, args, colour_add in [("back",background,bargs,1),("sig",signal,[1.,1.],0)]:

    generated_massses = []
    n_tot = 0
    n_acc = 0
    for p_arr,true_mass in masses(true_hyp, [e,mu], function, args[0], args[1], weights["%s_%s"%(gen_name,type_name)]):
      m = get_mass(p_arr)
      n_tot += 1
      if True:
      #if (dmin<(m)<1700.) or (1900.<(m)<dmax):
        n_acc += 1
        generated_massses.append((p_arr,true_mass))
    print "Fraction of generated events %s %s passing emu mass cuts: %.2f" % (gen_name,type_name,float(n_acc)/n_tot)

    for i,(rec_name,hyp) in enumerate(mass_hytpotheses):

      assumed_plot = TH1D("assumed_%s_%s_%s"%(gen_name,type_name,rec_name),"assumed_%s_%s"%(gen_name,type_name),100,1550,2150)
      true_plot = TH1D("true_%s_%s_%s"%(gen_name,type_name,rec_name),"true_%s_%s"%(gen_name,type_name),100,1550,2150)

      for p_arr,true_mass in generated_massses:
        assumed_plot.Fill(get_mass(new_mass_arr(p_arr,hyp)))
        if i==0:
          true_plot.Fill(get_mass(new_mass_arr(p_arr,true_hyp)))

      style_plot(assumed_plot,colour+colour_add,xtitle="Reconstructed %s mass [MeV]"%(rec_name.replace("mu","#mu").replace("pi","#pi")))
      assumed_plots.append(assumed_plot)

      ts_assumed[i].Add(assumed_plots[-1])
      assumed_plots[-1].Draw()

      lines.append(TLine(d*1000.,0.,d*1000.,assumed_plots[-1].GetMaximum()))
      lines[-1].SetLineColor(ROOT.kGreen+2)
      lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
      lines[-1].Draw("same")

      lines.append(TLine(1815.,0.,1815.,assumed_plots[-1].GetMaximum()))
      lines[-1].SetLineColor(ROOT.kGreen)
      lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
      lines[-1].Draw("same")

      lines.append(TLine(1915.,0.,1915.,assumed_plots[-1].GetMaximum()))
      lines[-1].SetLineColor(ROOT.kGreen)
      lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
      lines[-1].Draw("same")

      tc.SaveAs("assumed_mass_%s_%s_%s.pdf"%(gen_name,type_name,rec_name))
      tc.SaveAs("assumed_mass_%s_%s_%s.png"%(gen_name,type_name,rec_name))

      if i==0:
        style_plot(true_plot,colour+colour_add,xtitle="True %s mass [MeV]"%(gen_name.replace("mu","#mu").replace("pi","#pi")))
        true_plots.append(true_plot)

        ts_true[i].Add(true_plots[-1])
        true_plots[-1].Draw()

        lines.append(TLine(d*1000.,0.,d*1000.,true_plots[-1].GetMaximum()))
        lines[-1].SetLineColor(ROOT.kGreen+2)
        lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
        lines[-1].Draw("same")

        lines.append(TLine(1815.,0.,1815.,true_plots[-1].GetMaximum()))
        lines[-1].SetLineColor(ROOT.kGreen)
        lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
        lines[-1].Draw("same")

        lines.append(TLine(1915.,0.,1915.,true_plots[-1].GetMaximum()))
        lines[-1].SetLineColor(ROOT.kGreen)
        lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
        lines[-1].Draw("same")

        tc.SaveAs("true_mass_%s_%s.pdf"%(gen_name,type_name))
        tc.SaveAs("true_mass_%s_%s.png"%(gen_name,type_name))

for i,(rec_name,hyp) in enumerate(mass_hytpotheses):

  ts_assumed[i].Draw()

  lines.append(TLine(d*1000.,0.,d*1000.,ts_assumed[i].GetMaximum()))
  lines[-1].SetLineColor(ROOT.kGreen+2)
  lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
  lines[-1].Draw("same")

  lines.append(TLine(1815.,0.,1815.,ts_assumed[i].GetMaximum()))
  lines[-1].SetLineColor(ROOT.kGreen)
  lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
  lines[-1].Draw("same")

  lines.append(TLine(1915.,0.,1915.,ts_assumed[i].GetMaximum()))
  lines[-1].SetLineColor(ROOT.kGreen)
  lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
  lines[-1].Draw("same")

  tc.SaveAs("stacked_assumed_mass_%s.pdf"%(rec_name))
  tc.SaveAs("stacked_assumed_mass_%s.png"%(rec_name))

  if i==0:
    ts_true[i].Draw()

    lines.append(TLine(d*1000.,0.,d*1000.,ts_true[i].GetMaximum()))
    lines[-1].SetLineColor(ROOT.kGreen+2)
    lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
    lines[-1].Draw("same")

    lines.append(TLine(1815.,0.,1815.,ts_true[i].GetMaximum()))
    lines[-1].SetLineColor(ROOT.kGreen)
    lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
    lines[-1].Draw("same")

    lines.append(TLine(1915.,0.,1915.,ts_true[i].GetMaximum()))
    lines[-1].SetLineColor(ROOT.kGreen)
    lines[-1].SetLineWidth(2*lines[-1].GetLineWidth())
    lines[-1].Draw("same")

    tc.SaveAs("stacked_true_mass.pdf")
    tc.SaveAs("stacked_true_mass.png")

