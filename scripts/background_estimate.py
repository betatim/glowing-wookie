#!/usr/bin/env python 


from uncertainties import ufloat

fempto =  1e-15
br_d_pipi = ufloat(1.402e-3,0.026e-3)
br_d_kpi = ufloat(3.88e-2,0.05e-2)

def pipiasemu_eff():
  pipi_mc_cut = (ufloat(20.27e-2,0.0364e-2)+ufloat(20.14e-2,0.0362e-2))/2.
  pipiasemu_sel = ufloat(1.090e-2,0.010e-2)
  pipiasemu_l0 = ufloat(0.4719e-2,0.0017e-2)
  pipiasemu_hlt1 = ufloat(60.01e-2,0.10e-2)
  pipiasemu_pid1 = ufloat(9.9990e-2,0.0012e-2)
  pipiasemu_pid2 = ufloat(3.88e-2,0.25e-2)
  
  return pipi_mc_cut*pipiasemu_sel*pipiasemu_l0*pipiasemu_hlt1*pipiasemu_pid1*pipiasemu_pid2
  
def n_pipiasemu_from_lumi():
  dstar_cross_section = ufloat(676e-6,137e-6)
  br_dstar_dpi = ufloat(0.677,0.005)
  
  raw_n = integrated_lumi*dstar_cross_section*br_dstar_dpi*br_d_pipi
  
  return raw_n * pipiasemu_eff()

def kpi_eff():
  kpi_mc_cut = (ufloat(21.41e-2,0.0381e-2)+ufloat(21.42e-2,0.0381e-2))/2.
  kpi_prescale = 0.00995819
  kpi_sel = ufloat(0.2410e-2,0.0026e-2)
  
  return kpi_mc_cut*kpi_prescale*kpi_sel
  
def n_kpi_from_fitter():
  return n_kpi / kpi_eff()

def n_pipiasemu_from_norm():
  """
  calculate efficiency and error
  In [1]: (30800./(3.88e-2*21.405e-2*0.00995819*0.2410e-2))*1.402e-3*20.205e-2*1.090e-2*0.4719e-2*60.01e-2*9.9990e-2*3.88e-2
  Out[1]: 5.242054988582384
  """
  
  return ( n_kpi_from_fitter()*br_d_pipi/br_d_kpi ) * pipiasemu_eff()

def emu_eff():
  emu_mc_eff = (ufloat(6.93e-2,0.0135e-2)+ufloat(6.95e-2,0.0135e-2))/2.
  emu_sel_eff = ufloat(10.537e-2,0.021e-2)*ufloat(60.93e-2,0.11e-2)*ufloat(53.29e-2,0.14e-2)*ufloat(25.12e-2,0.16e-2)*ufloat(99.852e-2,0.029e-2)*ufloat(87.52e-2,0.25e-2)*ufloat(79.97e-2,0.32e-2)
  emu_pid_eff = ((ufloat(95.675e-2,0.028e-2)+ufloat(96.093e-2,0.052e-2))/2.)*((ufloat(77.597e-2,0.059e-2)+ufloat(78.675e-2,0.050e-2))/2.)
  return emu_mc_eff*emu_sel_eff*emu_pid_eff

def ses():
  return (br_d_kpi*kpi_eff())/(n_kpi*emu_eff())


print "Calculating values for unblinded sample"

n_kpi = ufloat(30801.401,210.0)
integrated_lumi = ufloat(0.25/fempto,0.25*0.03/fempto)

lumi = n_pipiasemu_from_lumi()
norm = n_pipiasemu_from_norm()

print "pipi as emu lumi:", '{:.2uL}'.format(lumi)
print "pipi as emu norm:", '{:.2uL}'.format(norm)

diff = norm-lumi
sigma = diff.n/diff.s

print "pipi as emu diff:", diff, "sigma:", sigma

val = ses()
print "ses:", '{:.2uL}'.format(val)

print
print "Calculating values for full sample"

n_kpi *= 100./7.6
integrated_lumi = ufloat(3./fempto,3.*0.03/fempto)

lumi = n_pipiasemu_from_lumi()
norm = n_pipiasemu_from_norm()

print "pipi as emu lumi:", '{:.2uL}'.format(lumi)
print "pipi as emu norm:", '{:.2uL}'.format(norm)

diff = norm-lumi
sigma = diff.n/diff.s

print "pipi as emu diff:", diff, "sigma:", sigma

val = ses()
print "ses:", '{:.2uL}'.format(val)


