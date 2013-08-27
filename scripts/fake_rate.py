import math
from array import array

import ROOT as R
R.TH1.SetDefaultSumw2()

from wookie import config

def eff((na, uncert_a), (nb, uncert_b)):
    eff = na / float(nb)
    variance = (((1.-2.*eff)*uncert_a*uncert_a + eff*eff*uncert_b*uncert_b) /
                (nb*nb))
    variance = abs(variance)
    uncert = math.sqrt(variance)
    return (eff, uncert)

class Particle(object):
    def __init__(self, name, pid_cut, species="Pi"):
        self.species = species
        self.name = name
        self.pid_cut = pid_cut

        eta_bin_boundaries = array("d", (1.9,2.3,2.6,2.9,3.2,3.5,3.8,4.1,4.4,4.7,5.0))
        eta_bins = (len(eta_bin_boundaries)-1, eta_bin_boundaries)
        pt_bin_boundaries = array("d", (0.5,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.5,3.0,4.0,6.0,12))
        pt_bins = (len(pt_bin_boundaries)-1, pt_bin_boundaries)
        p_bin_boundaries = array("d", (5,10,12,14,16,18,20,22,25,28,32,38,45,55,70,100))
        p_bins = (len(p_bin_boundaries)-1, p_bin_boundaries)
        
        self.pt_eta_all = R.TH2F("%s_to_%s_pt_eta_all"%(species, name),
                                 ";pt;eta", *(pt_bins+eta_bins))
        self.pt_eta_pass = R.TH2F("%s_to_%s_pt_eta_pass"%(species, name),
                                  ";pt;eta", *(pt_bins+eta_bins))

        self.p_eta_all = R.TH2F("%s_to_%s_p_eta_all"%(species, name),
                                ";p;eta", *(p_bins+eta_bins))
        self.p_eta_pass = R.TH2F("%s_to_%s_p_eta_pass"%(species, name),
                                 ";p;eta", *(p_bins+eta_bins))

        self.p_pt_all = R.TH2F("%s_to_%s_p_pt_all"%(species, name),
                               ";p;pt", *(p_bins+pt_bins))
        self.p_pt_pass = R.TH2F("%s_to_%s_p_pt_pass"%(species, name),
                                ";p;pt", *(p_bins+pt_bins))

    def eval_efficiency(self, event):
        eta = event.getRealValue(self.species + "_Eta")
        pt = event.getRealValue(self.species + "_PT")/1000
        p = event.getRealValue(self.species + "_P")/1000
        #phi = event.getRealValue(self.species + "_Phi")
        w = event.getRealValue("nsig_sw")
        
        self.pt_eta_all.Fill(pt, eta, w)
        self.p_eta_all.Fill(p, eta, w)
        self.p_pt_all.Fill(p, pt, w)
        if self.pid_cut(event):
            self.pt_eta_pass.Fill(pt, eta, w)
            self.p_eta_pass.Fill(p, eta, w)
            self.p_pt_all.Fill(p, pt, w)

    def save_histograms(self, file_name):
        f = R.TFile(file_name, "UPDATE")
        for h1,h2 in ((self.pt_eta_all,self.pt_eta_pass),
                      (self.p_eta_all,self.p_eta_pass),
                      (self.phi_eta_all,self.phi_eta_pass)):
            h1.Write()
            h2.Write()
            eff = h1.Clone(h1.GetName().replace("all", "") + "fake_rate")
            eff.SetTitle(self.species + " to %s fake rate"%(self.name))
            eff.Divide(h2, h1, 1,1,"B")
            eff.Write()
            
        f.Close()

def fake_rate(working_points):
    # XXX Need a more sophisticated way to select
    # XXX the input files, checking they exist etc
    fname = "/castor/cern.ch/grid/lhcb/user/p/powell/CalibData/Reco14_DATA/MagUp/DSt_%s_MagUp_Strip20_%i.root"

    # all workping points must use the same species
    assert(len(set([wp.species for wp in working_points])) == 1)
    
    fnames = [fname%(working_points[0].species, n) for n in xrange(10)]

    for fname in fnames:
        print "Processing", fname
        f = R.TFile.Open("rfio:"+fname)
        w = f.RSDStCalib
        data = w.data("data")
    
        for n in xrange(data.numEntries()):
            d = data.get(n)
            if n == 0:
                d.Print()
                
            for wp in working_points:
                wp.eval_efficiency(d)

        f.Close()

def PIDe_cutter(species, val):
    def _f(d):
        return d.getRealValue(species + "_CombDLLe") > val
    return _f
def MuonPID(species, val):
    def _f(d):
        return ((d.getRealValue(species + "_IsMuon") == 1) and
                (d.getRealValue(species + "_CombDLLmu") > val))
    return _f
def B2emuMuon(species):
    def _f(d):
        return ((d.getRealValue(species + "_IsMuon") == 1) and
                (d.getRealValue(species + "_CombDLLK") < 10) and
                (d.getRealValue(species + "_CombDLLmu") > -5))
    return _f

wp1 = Particle("loose_electron", PIDe_cutter("Pi", -1))
wp2 = Particle("tight_electron", PIDe_cutter("Pi", 3))
wp3 = Particle("basic_muon", MuonPID("Pi", 0))
wp4 = Particle("B2emu_muon", B2emuMuon("Pi"))
wps = [wp1, wp2, wp3, wp4]

fake_rate(wps)
for wp in wps:
    wp.save_histograms(config.workingpath + "fake_rates.root")

