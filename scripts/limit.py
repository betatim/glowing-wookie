#!/usr/bin/env python

import ROOT
from ROOT import TFeldmanCousins, TRolke


br_pipi = 1.401e-3
e_pipi = 1.8e-2
br_exp_emu = 1e-14
e_emu = 3.1e-2

n_tot_pipi = 15102431. # (down)
n_tot_emu = 501396.  # (down)

n_norm_pipi = (br_pipi) * n_tot_pipi
n_norm_emu = (br_exp_emu) * n_tot_pipi

n_exp_pipi = n_norm_pipi * e_pipi
n_exp_emu = n_norm_emu * e_emu

br_emu = br_pipi * (n_exp_emu*e_pipi)/(n_exp_pipi*e_emu)

print n_norm_pipi, n_norm_emu
print n_exp_pipi,  n_exp_emu

back = 150.
obs = round(n_exp_emu) + back


#fc = TFeldmanCousins(.9)
#ul = fc.CalculateUpperLimit(obs,back)
#ll = fc.GetLowerLimit()
#print ll,ul, (br_pipi * (ul*e_pipi)/(n_exp_pipi*e_emu))

tr = TRolke()
#mid =1;
x = 100;    # events in the signal region
y = 100;    # events observed in the background region
tau = 1.;   # ratio between size of signal/background region
m = int(n_tot_emu);    # MC events have been produced  (signal)
z = int(n_tot_emu*e_emu);     # MC events have been observed (signal)     
e = e_emu

alpha=0.9; #Confidence Level

tr.SetCL(alpha)

ll = ROOT.Double(0.)
ul = ROOT.Double(0.)

#tr.SetPoissonBkgBinomEff(x,y,z,tau,m)
tr.SetPoissonBkgKnownEff(x,y,tau,e)
tr.GetLimits(ll,ul)

print ll, ul
print br_pipi * (ll*e_pipi)/(n_exp_pipi*e_emu), br_pipi * (ul*e_pipi)/(n_exp_pipi*e_emu)



