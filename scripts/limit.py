#!/usr/bin/env python

import ROOT
from ROOT import TFeldmanCousins, TRolke


br_pipi = 1.401e-3

#        strip e|st pre|hlt2 p|  tr e  |  off e
e_pipi = 1.8e-2 * 0.5 * 0.03 * 15.44e-2 * 63.17e-2
br_exp_emu = 1e-14
#       strip e|tr e
e_emu = 3.1e-2 * 36.61e-2

n_tot_pipi = 15102431. # (down)
n_tot_emu = 501396.  # (down)

#n_pipi = 8.2733e+03
#n_pipi = 8.4571e+04
n_pipi = 51143 # (680e-6*.68*1.4e-3*3/1e-15)*1.8e-2 * 0.5 * 0.03 * 15.44e-2 * 63.17e-2


#fc = TFeldmanCousins(.9)
#ul = fc.CalculateUpperLimit(obs,back)
#ll = fc.GetLowerLimit()
#print ll,ul, (br_pipi * (ul*e_pipi)/(n_exp_pipi*e_emu))

tr = TRolke()
#mid =1;
x = 50;    # events in the signal region
y = 50;    # events observed in the background region
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
print br_pipi * (ll*e_pipi)/(n_pipi*e_emu), br_pipi * (ul*e_pipi)/(n_pipi*e_emu)

# aim better than 2.6e-7

