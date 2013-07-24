import string
import random
import math

import ROOT as R
from ROOT import TMVA

from wookie import config

random.seed(1234)


class V(object):
    def __init__(self, branch):
        self.branch = branch
        self.name = safe_varname(branch)

    def enable_vars(self, tree):
        tree.SetBranchStatus(self.branch, True)

    def __call__(self, evt):
        return getattr(evt, self.branch)

class DeltaV(object):
    def __init__(self, branch1, branch2):
        """Computes `branch1` - `branch2`."""
        self.branch1 = branch1
        self.branch2 = branch2
        self.name = safe_varname(branch1) +"_minus_"+safe_varname(branch2)

    def enable_vars(self, tree):
        for br in (self.branch1, self.branch2):
            tree.SetBranchStatus(br, True)

    def __call__(self, evt):
        return getattr(evt, self.branch1) - getattr(evt, self.branch2)

class MinV(object):
    def __init__(self, branches):
        """Computes min(`branches`)."""
        self.branches = branches
        self.name = "min " +"_".join([safe_varname(branch) for branch in branches])

    def enable_vars(self, tree):
        for br in self.branches:
            tree.SetBranchStatus(br, True)

    def __call__(self, evt):
        return min([getattr(evt, br) for br in self.branches])

class D0Pointing(object):
    def __init__(self):
        """Computes -log(1-cos(DIRA))."""
        self.name = "D0_pointing"

    def enable_vars(self, tree):
        tree.SetBranchStatus("D0_DIRA", True)

    def __call__(self, evt):
        return -1*math.log(1-math.cos(evt.D0_DIRA))

class LeptonCosTheta(object):
    def __init__(self):
        """Computes angle of +ve charge lepton in D COM."""
        self.name = "LepCosTheta"

    def enable_vars(self, tree):
        tree.SetBranchStatus("x1_CosTheta", True)
        tree.SetBranchStatus("x2_CosTheta", True)
        tree.SetBranchStatus("x1_ID", True)

    def __call__(self, evt):
        if evt.x1_ID > 0:
            return abs(evt.x1_CosTheta)
        else:
            return abs(evt.x2_CosTheta)

class D0PtScaledIso(object):
    def __init__(self):
        self.name = "D0_PtScaledIso"

    def enable_vars(self, tree):
        tree.SetBranchStatus("D0_cpt_1.00", True)
        tree.SetBranchStatus("D0_PT", True)

    def __call__(self, evt):
        return evt.D0_PT/(evt.D0_PT + getattr(evt, "D0_cpt_1.00"))

class PIDSelection(object):
    def __init__(self, pid_mu, pid_e):
        self.pid_e = pid_e
        self.pid_mu = pid_mu
        # Stick to DLL variables for the moment
        # not sure Tim understands the shape of ProbNNmu
        self._branches = ["x2_isMuon", "x2_PIDmu", "x1_PIDe"]
        self._Ntotal = 0
        self._Npassed = 0

    def reset_counters(self):
        self._Ntotal = self._Npassed = 0
        
    @property
    def efficiency(self):
        return self._Npassed, self._Ntotal

    def enable_vars(self, tree):
        for br in self._branches:
            tree.SetBranchStatus(br, True)

    def __call__(self, evt):
        self._Ntotal += 1

        if (evt.x2_isMuon and
            evt.x1_PIDe > self.pid_e and
            evt.x2_PIDmu > self.pid_mu):
            self._Npassed += 1
            return True

        return False


def safe_varname(varname):
    """Remove characters which make TMVA think a variable is a
    formula and replace by underscores
    """
    bad_chars = "[]{}()-+*/"
    translation = string.maketrans(bad_chars, "_"*len(bad_chars))
    return varname.translate(translation)
    
def add_events(factory, tree, variables,
               select, signal=True,
               Nmax=16000):
    """Add training/testing events to TMVA

    Only events for which `select` returns True
    will be used. Will keep adding events until
    we reach `Nmax` have been accepted.
    """
    if signal:
        add_train_evt = factory.AddSignalTrainingEvent
        add_test_evt = factory.AddSignalTestEvent

    else:
        add_train_evt = factory.AddBackgroundTrainingEvent
        add_test_evt = factory.AddBackgroundTestEvent

    select.enable_vars(tree)
    for var in variables:
        var.enable_vars(tree)
        
    is_training = (True, False)
    vals = R.std.vector(R.Double)()

    Nselected = 0
    for N,evt in enumerate(tree):
        if Nselected > Nmax:
            print Nselected, Nmax
            break

        if not select(evt):
            continue
            
        vals.clear()
        for v in variables:
            vals.push_back(v(evt))

        Nselected += 1
        if random.choice(is_training):
            add_train_evt(vals, 1.)
        else:
            add_test_evt(vals, 1.)
            
def add_variables(factory, variables, spectators):
    for var in variables:
        factory.AddVariable(var.name, "F")

    for spec in spectators:
        factory.AddSpectator(spec.name, "F")


if __name__ == "__main__":
    f_sig = R.TFile(config.ntuplepath + "/mcemu/strip_emu.root")
    tree_sig = f_sig.Demu_NTuple.Get("Demu_NTuple")
    f_bg = R.TFile(config.ntuplepath + "/emu/strip_emu.root")
    tree_bg = f_bg.Demu_NTuple.Get("Demu_NTuple")

    tree_sig.SetBranchStatus("*", False)
    tree_bg.SetBranchStatus("*", False)
    
    fname = config.workingpath + "/d2emu-tmva.root"
    out_file = R.TFile(fname, "RECREATE")
    
    factory = TMVA.Factory("d2emu", out_file, "!Color")

    variables = [V("D0_CosTheta"), #theta*
                 V("D0_DOCA"),
                 D0Pointing(),
                 V("D0_VChi2_per_NDOF"),
                 V("D0_MinIPChi2_PRIMARY"),
                 V("D0_IPChi2"),
                 V("Dst_MinIPChi2_PRIMARY"),
                 #V("x1_CosTheta"),
                 LeptonCosTheta(), #theta
                 MinV(["x1_IPCHI2_OWNPV", "x2_IPCHI2_OWNPV"]),
                 MinV(["x1_PT", "x2_PT"]),
                 D0PtScaledIso(),
             ]
    spectators = [V("D0_M"),
                  V("Dst_M"),
                  V("pi_ProbNNmu"),
                  V("pi_ProbNNpi"),
                  V("x1_BremMultiplicity"),
                  V("x1_ProbNNe"),
                  V("x1_ProbNNmu"),
                  V("x1_ProbNNghost"),
                  V("x1_PIDe"),
                  V("x1_PIDmu"),
                  V("x1_PIDK"),
                  V("x1_isMuon"),
                  V("x1_cp_0.50"),
                  V("x1_cmult_0.50"),
                  V("x2_ProbNNe"),
                  V("x2_ProbNNmu"),
                  V("x2_ProbNNghost"),
                  V("x2_PIDe"),
                  V("x2_PIDmu"),
                  V("x2_PIDK"),
                  V("x2_cp_0.50"),
                  V("x2_cmult_0.50"),
                  DeltaV("Dst_M", "D0_M"),
              ]
    
    
    add_variables(factory,
                  variables,
                  spectators)

    selector = PIDSelection(pid_mu=-10., pid_e=-10.)
    
    Nmax = 16000
    add_events(factory, tree_sig, variables + spectators,
               selector, Nmax=Nmax)
    Np, Nt = selector.efficiency
    print "Signal efficiency of PID cuts %i/%i = %.5f"%(Np, Nt, Np/float(Nt))
    selector.reset_counters()
    
    add_events(factory, tree_bg, variables + spectators,
               selector, signal=False, Nmax=Nmax)
    Np, Nt = selector.efficiency
    print "Background efficiency of PID cuts %i/%i = %.5f"%(Np, Nt, Np/float(Nt))
    
    options = "NormMode=None"
    factory.PrepareTrainingAndTestTree(R.TCut(""), R.TCut(""),
                                       options)
    #bdt_options = ("NTrees=%i:UseRandomisedTrees=True:MaxDepth=%i:"
    #               "PruneMethod=NoPruning:UseNvars=%i:nCuts=-1")
    #bdt_options = bdt_options%(3)
    #import itertools
    #for trees,depth in itertools.product((1,2,3,4,5,6,7,8,9,10,20,40),
    #                                     (3,5,8)):
    #    factory.BookMethod(TMVA.Types.kBDT, "BDT_%i_%i"%(trees,depth),
    #                       bdt_options%(trees, depth, len(variables)/2))

    # For the moment ADA boost seems to perform as well
    # as all the others and does well in terms of overtraining
    for max_depth in (3,4,5,6,7,8):
        factory.BookMethod(TMVA.Types.kBDT, "BDT_ada_%i"%max_depth,
                           "BoostType=AdaBoost:nCuts=-1:MaxDepth=%i:"
                           "PruneMethod=NoPruning"%(max_depth))
    
    print "Training"
    factory.TrainAllMethods()
    print "Testing"
    factory.TestAllMethods()
    print "Evaluating"
    factory.EvaluateAllMethods()
    print "Closing"
    out_file.Close()
    print "Closed"
    
