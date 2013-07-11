import string
import random

import ROOT as R
from ROOT import TMVA


random.seed(1234)


class V(object):
    def __init__(self, branch):
        self.branch = branch
        self.name = safe_varname(branch)

    def enable(self, tree):
        tree.SetBranchStatus(self.branch, True)

    def __call__(self, evt):
        return getattr(evt, self.branch)

        
def safe_varname(varname):
    """Remove characters which make TMVA think a variable is a
    formula and replace by underscores
    """
    bad_chars = "[]{}()-+*/"
    translation = string.maketrans(bad_chars, "_"*len(bad_chars))
    return varname.translate(translation)
    
def add_events(factory, tree, variables, signal=True, Nmax=10000):
    if signal:
        add_train_evt = factory.AddSignalTrainingEvent
        add_test_evt = factory.AddSignalTestEvent

    else:
        add_train_evt = factory.AddBackgroundTrainingEvent
        add_test_evt = factory.AddBackgroundTestEvent

    for var in variables:
        var.enable(tree)
        
    is_training = (True, False)
    vals = R.std.vector(R.Double)()
    
    for N,evt in enumerate(tree):
        if N > Nmax:
            break
            
        vals.clear()
        for v in variables:
            vals.push_back(v(evt))

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
    f_sig = R.TFile("/tmp/emu-mc-magdown.root")
    tree_sig = f_sig.Demu_NTuple.Get("Demu_NTuple")
    f_bg = R.TFile("/tmp/emu-data-magup.root")
    tree_bg = f_bg.Demu_NTuple.Get("Demu_NTuple")

    tree_sig.SetBranchStatus("*", False)
    tree_bg.SetBranchStatus("*", False)
    
    fname = "/tmp/d2emu-tmva.root"
    out_file = R.TFile(fname, "RECREATE")
    
    factory = TMVA.Factory("d2emu", out_file, "!Color")

    variables = [V("D0_CosTheta"),
                 #V("D0_DOCA"),
                 V("D0_DIRA"),
                 ##V("D0_DIRA_ORIVX"),
                 ##V("D0_DIRA_OWNPV"),
                 V("D0_VChi2_per_NDOF"),
                 V("D0_MinIP_PRIMARY"),
                 V("D0_IP_OWNPV"),
                 ##V("D0_FD_ORIVX"),
                 V("D0_FD_OWNPV"),
                 ##V("Dst_DOCA"),
                 ##V("Dst_DIRA"),
                 ##V("Dst_DIRA_OWNPV"),
                 V("Dst_VChi2_per_NDOF"),
                 ##V("Dst_MinIP_PRIMARY"),
                 ##V("Dst_IP_OWNPV"),
                 ##V("Dst_FD_OWNPV"),
                 V("x1_IP_OWNPV"),
                 V("x2_IP_OWNPV"),
                 ##V("x1_IPCHI2_OWNPV"),
                 ##V("x2_IPCHI2_OWNPV"),
                 ##V("x1_TRGHOSTPROB"),
                 ##V("x2_TRGHOSTPROB"),
                 V("x1_TRACK_CHI2NDOF"),
                 V("x2_TRACK_CHI2NDOF"),
                 V("x1_TRACK_MatchCHI2"),
                 V("x2_TRACK_MatchCHI2"),
             ]
    spectators = [#V("D0_MinIPChi2_PRIMARY"),
                  V("D0_IPChi2"),
                  V("D0_MM"),
                  V("Dst_MM"),
                  #V("x1_BremMultiplicity"),
              ]
    
    
    add_variables(factory,
                  variables,
                  spectators)

    Nmax = 16000
    add_events(factory, tree_sig, variables + spectators, Nmax=Nmax)
    add_events(factory, tree_bg, variables + spectators,
               signal=False, Nmax=Nmax)

    options = "NormMode=None"
    factory.PrepareTrainingAndTestTree(R.TCut(""), R.TCut(""),
                                       options)
    bdt_options = ("NTrees=%i:UseRandomisedTrees=True:MaxDepth=%i:"
                   "PruneMethod=NoPruning:UseNvars=%i:nCuts=-1")
    #bdt_options = bdt_options%(3)
    import itertools
    for trees,depth in itertools.product((1,2,3,4,5,6,7,8,9,10,20,40),
                                         (3,5,8)):
        factory.BookMethod(TMVA.Types.kBDT, "BDT_%i_%i"%(trees,depth),
                           bdt_options%(trees, depth, len(variables)/2))

    factory.BookMethod(TMVA.Types.kBDT, "BDT_ada",
                       "BoostType=AdaBoost:nCuts=-1:MaxDepth=3:"
                       "PruneMethod=NoPruning")
    
    print "Training"
    factory.TrainAllMethods()
    print "Testing"
    factory.TestAllMethods()
    print "Evaluating"
    factory.EvaluateAllMethods()
    print "Closing"
    out_file.Close()
    print "Closed"
    