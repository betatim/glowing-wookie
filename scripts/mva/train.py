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

class Selection(object):
    def __init__(self, branches):
        """Selects events and reports the efficiency of the cut"""
        self._branches = branches
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

class Trigger(Selection):
    def __init__(self, lines):
        Selection.__init__(self, lines)

    def __call__(self, evt):
        self._Ntotal += 1
        if any([getattr(evt, l) == 1 for l in self._branches]):
            self._Npassed += 1
            return True
        else:
            return False

class PIDSelection(Selection):
    def __init__(self, x1_e=0.45, pi_ghost=0.05, x2_ghost=0.05, x2_mu=0.3, x2_k=0.55, pi_pi=0.45, x1_k=0.8):
        """Selects events for which PIDe and PIDmu are above
        `pid_mu` and `pid_e`.
        """
        # Stick to DLL variables for the moment
        # not sure Tim understands the shape of ProbNNmu
        #Selection.__init__(self,
        #                   ["x2_isMuon", "x2_PIDmu", "x1_PIDe"])
        #x1_ProbNNe>0.45&&pi_ProbNNghost<0.05&&x2_ProbNNghost<0.05&&x2_ProbNNmu>0.3&&x2_ProbNNk<0.55&&pi_ProbNNpi>0.45&&x1_ProbNNk<0.8
        Selection.__init__(self,
                           ["x1_ProbNNe", "pi_ProbNNghost", "x2_ProbNNghost", "x2_ProbNNmu", "x2_ProbNNk", "pi_ProbNNpi", "x1_ProbNNk"])
        self.x1_e = x1_e
        self.pi_ghost = pi_ghost
        self.x2_ghost = x2_ghost
        self.x2_mu = x2_mu
        self.x2_k = x2_k
        self.pi_pi = pi_pi
        self.x1_k = x1_k

    def __call__(self, evt):
        self._Ntotal += 1

        #print evt.x1_isMuon, evt.x1_ProbNNe> self.x1_e,evt.pi_ProbNNghost < self.pi_ghost,evt.x2_ProbNNghost < self.x2_ghost,evt.x2_ProbNNmu > self.x2_mu,evt.x2_ProbNNk < self.x2_k,evt.pi_ProbNNpi > self.pi_pi,evt.x1_ProbNNk < self.x1_k

        if (#evt.x2_isMuon and
            evt.x1_ProbNNe > self.x1_e and
            evt.pi_ProbNNghost < self.pi_ghost and
            evt.x2_ProbNNghost < self.x2_ghost and
            evt.x2_ProbNNmu > self.x2_mu and
            evt.x2_ProbNNk < self.x2_k and
            evt.pi_ProbNNpi > self.pi_pi and
            evt.x1_ProbNNk < self.x1_k):
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
               selectors, signal=True,
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

    for select in selectors:
        select.enable_vars(tree)
        
    for var in variables:
        var.enable_vars(tree)
        
    is_training = (True, False)
    vals = R.std.vector(R.Double)()

    Nselected = 0
    for N,evt in enumerate(tree):
        if Nselected > Nmax:
            print "Selected: %i, requested: %i, tried %i events."%(Nselected, Nmax, N)
            break

        if not all([s(evt) for s in selectors]):
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
    
    #fname = config.workingpath + "/d2emu-tmva.root"
    fname = "./d2emu-tmva.root"
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
                  V("pi_ProbNNe"),
                  V("pi_ProbNNpi"),
                  V("pi_ProbNNp"),
                  V("pi_ProbNNk"),
                  V("pi_ProbNNmu"),
                  V("pi_ProbNNghost"),
                  V("x1_BremMultiplicity"),
                  V("x1_ProbNNk"),
                  V("x1_ProbNNpi"),
                  V("x1_ProbNNp"),
                  V("x1_ProbNNe"),
                  V("x1_ProbNNmu"),
                  V("x1_ProbNNghost"),
                  V("x1_PIDe"),
                  V("x1_PIDmu"),
                  V("x1_PIDK"),
                  V("x1_isMuon"),
                  V("x1_cp_0.50"),
                  V("x1_cmult_0.50"),
                  V("x2_ProbNNk"),
                  V("x2_ProbNNp"),
                  V("x2_ProbNNpi"),
                  V("x2_ProbNNe"),
                  V("x2_ProbNNmu"),
                  V("x2_ProbNNghost"),
                  V("x2_PIDe"),
                  V("x2_PIDmu"),
                  V("x2_PIDK"),
                  V("x2_cp_0.50"),
                  V("x2_cmult_0.50"),
                  DeltaV("Dst_M", "D0_M"),
                  V("Dst_L0MuonDecision_TOS"),
                  V("Dst_L0ElectronDecision_TOS"),
              ]
    
    
    add_variables(factory,
                  variables,
                  spectators)

    pid_selection = PIDSelection()
    hlt2_selection = Trigger(["Dst_Hlt2CharmHadD02HH_D02PiPiDecision_TOS",
                              "Dst_Hlt2CharmHadD02HH_D02KPiDecision_TOS",
                              "Dst_Hlt2CharmHadD02HH_D02KKDecision_TOS",
                              #"Dst_Hlt2Dst2PiD02KKDecision_TOS",
                              #"Dst_Hlt2Dst2PiD02PiPiDecision_TOS",
                              #"Dst_Hlt2Dst2PiD02KPiDecision_TOS"
                              ])
    hlt1_selection = Trigger(["Dst_Hlt1TrackMuonDecision_TOS",
                              #"Dst_Hlt1TrackAllL0Decision_TOS",
                              ])
    l0_selection = Trigger(["Dst_L0MuonDecision_TOS",
                            #"Dst_L0ElectronDecision_TOS",
                            ])
    selectors = [pid_selection, l0_selection,
                 hlt1_selection, hlt2_selection]

    # Aim to get 2*Nmax events both for signal and background
    # so we can train on Nmax events and test on Nmax
    # This means looping over more than Nmax events unless
    # the selectors are 100% efficient
    Nmax = 16000
    print "Signal tree has %i events in total."%(tree_sig.GetEntries())
    add_events(factory, tree_sig, variables + spectators,
               selectors, Nmax=Nmax)
    for select in selectors:
        Np, Nt = select.efficiency
        print "Signal efficiency of %s cuts %i/%i = %.5f"%(select, Np, Nt, Np/float(Nt))
        select.reset_counters()

    print "Background tree has %i events in total."%(tree_bg.GetEntries())
    add_events(factory, tree_bg, variables + spectators,
               selectors, signal=False, Nmax=Nmax)
    for select in selectors:
        Np, Nt = select.efficiency
        print "Background efficiency of %s cuts %i/%i = %.5f"%(select, Np, Nt, Np/float(Nt))
        select.reset_counters()
    
    options = "NormMode=None"
    factory.PrepareTrainingAndTestTree(R.TCut(""), R.TCut(""),
                                       options)
    bdt_options = ("NTrees=%i:UseRandomisedTrees=True:MaxDepth=%i:"
                   "PruneMethod=NoPruning:UseNvars=%i:nCuts=-1")
    import itertools
    max_depths = (1,2,3,4,5,6,7,8,9)
    n_trees = (1,2,3,4,5,6,7,8,9,10,20,40,80,160,320,640)

    xxx ="""
    max_depths = (2,3,4)
    n_trees = (320, 480, 640)
    for trees,depth in itertools.product(n_trees,
                                         max_depths):
        factory.BookMethod(TMVA.Types.kBDT,
                           "BDT_random_%i_%i"%(trees,depth),
                           bdt_options%(trees, depth, len(variables)/2))

    # For the moment ADA boost seems to perform as well
    # as all the others and does well in terms of overtraining
    for trees,max_depth,weighted in itertools.product(n_trees, max_depths, (1, 0)):
            factory.BookMethod(TMVA.Types.kBDT,
                               "BDT_ada_%i_%i_%i"%(trees, max_depth, weighted),
                               "DoBoostMonitor=1:"
                               "NTrees=%i:BoostType=AdaBoost:nCuts=-1:MaxDepth=%i:"
                               "PruneMethod=NoPruning:UseWeightedTrees=%i"%(trees,
                                                                            max_depth,
                                                                            weighted))

    max_depths = (1,2,3,4,5,6,7,8,9)
    n_trees = (1,2,3,4,5,6,7,8,9,10,20,40,80,160,320,640)
    for trees,max_depth,weighted,shrink in itertools.product(n_trees,
                                                             max_depths,
                                                             (1, 0),
                                                             (0.01,0.02,0.05,0.1,0.2,0.3,0.7,1.)):
            factory.BookMethod(TMVA.Types.kBDT,
                               "BDT_grad_%i_%i_%i_%i"%(trees, max_depth, weighted, shrink*100),
                               "DoBoostMonitor=1:Shrinkage=%f:"
                               "NTrees=%i:BoostType=Grad:nCuts=-1:MaxDepth=%i:"
                               "PruneMethod=NoPruning:UseWeightedTrees=%i"%(shrink,
                                                                            trees,
                                                                            max_depth,
                                                                            weighted))"""
    #n_trees = (1,2,3,4,5,6,7,8,9,10,20,40,80,160,320,640)
    #max_depths = (1,2,3,4,5,6,7,8,9,10)
    n_trees = (1,2,3,4,5,6,7,8,9,10,20,40,80,160,320,640)
    max_depths = (1,2,3,4,5,6,7,8,9,10)
#BDT_grad_30_120_7_1_10:    
    n_trees = (120,)
    max_depths = (7,)
    for trees,max_depth,weighted,shrink,nnodes in itertools.product(n_trees,
                                                                    max_depths,
                                                                    (1,),
                                                                    #(0.01,0.02,0.05,0.1,0.2,0.3,0.7,1.),
                                                                    (0.05,),
                                                                    #(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
                                                                    (30,)
                                                                    ):
            factory.BookMethod(TMVA.Types.kBDT,
			       #"BDT_ada",
                               "BDT_grad_%i_%i_%i_%i_%i"%(nnodes, trees, max_depth, weighted, shrink*100),
                               "NNodesMax=%i:"
                               "DoBoostMonitor=1:Shrinkage=%f:"
                               "NTrees=%i:BoostType=Grad:nCuts=100:MaxDepth=%i:" # nCuts=-1 is better but errors so its 20
                               "PruneMethod=NoPruning:UseWeightedTrees=%i"%(nnodes,
                                                                            shrink,
                                                                            trees,
                                                                            max_depth,
                                                                            weighted))
                                                                            
    #method = factory.BookMethod(TMVA.Types.kBDT, "BDT",
                   #":".join([
                       #"!H",
                       #"!V",
                       #"NTrees=850",
                       #"nEventsMin=150",
                       #"MaxDepth=3",
                       #"BoostType=AdaBoost",
                       #"AdaBoostBeta=0.5",
                       #"SeparationType=GiniIndex",
                       #"nCuts=20",
                       #"PruneMethod=NoPruning",
                       #]))
                                                                            
    
    print "Training"
    factory.TrainAllMethods()
    print "Testing"
    factory.TestAllMethods()
    print "Evaluating"
    factory.EvaluateAllMethods()
    print "Closing"
    out_file.Close()
    print "Closed"
    
