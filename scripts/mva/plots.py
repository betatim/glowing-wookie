import os
import operator
import random
random.seed(1234)

from scipy.stats import ks_2samp
import matplotlib.pylab as plt
import numpy as np
import root_numpy
import ROOT as R

p = os.path.dirname(__file__)
p,_ = os.path.split(p)
R.gROOT.ProcessLine(".x " +
                    os.path.join(p, "lhcbstyle.C") +
                    "+")

def draw_roccurve(bdt_name, sample):
    bg = sample[sample.classID==1][bdt_name]
    sig = sample[sample.classID==0][bdt_name]

    Nsig = len(sig)
    Nbg = len(bg)
    sig.sort()
    bg.sort()

    fig = plt.figure()
    ax = fig.add_subplot(111)

    bg_rejs = []
    sig_effs = []
    for sig_eff in np.arange(0., 1.01, 0.01):
        # cut value is value at the 1-sig_eff
        # entry in sig, this is approximate
        idx = min(int(Nsig*(1-sig_eff)), Nsig-1)
        cut_value = sig[idx]
        Nsig_pass = (sig>cut_value).sum()
        Nbg_pass = (bg>cut_value).sum()
        s, b = (Nsig_pass/float(Nsig), Nbg_pass/float(Nbg))
        #print "sig eff:%.4f bg rej:%.4f S/sqrt(B): %.2f"%(s, 1-b, s/np.sqrt(b))
        bg_rejs.append(1-b)
        sig_effs.append(s)

    ax.plot(sig_effs, bg_rejs)
    ax.set_xlabel("signal efficiency")
    ax.set_ylabel("background rejection")
    ax.grid()
    plt.show()
        
    sig_effs.append(1.)
    print "Area under ROC", np.sum(np.asarray(bg_rejs) * np.diff(np.asarray(sig_effs)))

def draw_overtraining(bdt_name, test, train):
    test_bg = test[test.classID==1]
    test_sig = test[test.classID==0]
    train_bg = train[train.classID==1]
    train_sig = train[train.classID==0]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    low = min(test[bdt_name].min(), train[bdt_name].min())
    high = max(test[bdt_name].max(), train[bdt_name].max())

    print bdt_name, "signal",
    print ks_2samp(test_sig[bdt_name], train_sig[bdt_name])[1]
    print bdt_name, "background",
    print ks_2samp(test_bg[bdt_name], train_bg[bdt_name])[1]
    
    ax.hist(train_bg[bdt_name],
            bins=50,
            normed=True,
            range=(low,high),
            label="training background",
            color="blue",
            alpha=0.75)
    ax.hist(train_sig[bdt_name],
            bins=50,
            normed=True,
            range=(low,high),
            label="training signal",
            color="red",
            alpha=0.75)

    y,binEdges = np.histogram(test_bg[bdt_name],
                              bins=50,
                              normed=True,
                              range=(low,high))
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    ax.plot(bincenters, y, 'o', color="blue", label="test background")

    y,binEdges = np.histogram(test_sig[bdt_name],
                              bins=50,
                              normed=True,
                              range=(low,high))
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    ax.plot(bincenters, y, 'o', color="red", label="test signal")
    ax.legend(loc=2)
    ax.set_xlabel("BDT output")
    ax.set_ylabel("Arbitrary units")
    fig.savefig("/tmp/overtraining_%s.pdf"%(bdt_name))

def draw_all(test, train):
    test_bg = test[test.classID==1]
    test_sig = test[test.classID==0]
    train_bg = train[train.classID==1]
    train_sig = train[train.classID==0]
    
    for field in test_bg.dtype.names:
        fig = plt.figure()
        # plot signal vs background for train
        #      test vs train for signal
        #      test vs train for background
        ax = fig.add_subplot(221)

        low = min(test[field].min(), train[field].min())
        #low = max(low, -150)
        high = max(test[field].max(), train[field].max())

        ax.set_title("S vs B")
        ax.set_xlabel(field)
        ax.hist(train_bg[field],
                bins=50,
                normed=True,
                range=(low,high),
                label="train bg",
                alpha=0.5)
        ax.hist(train_sig[field],
                bins=50,
                normed=True,
                range=(low,high),
                label="train sig",
                alpha=0.5)
        ax.legend()

        ax = fig.add_subplot(223)
        ax.set_xlabel(field)
        ax.hist(train_bg[field],
                bins=50,
                normed=True,
                range=(low,high),
                label="train bg",
                alpha=0.5,
                log=True)
        ax.hist(train_sig[field],
                bins=50,
                normed=True,
                range=(low,high),
                label="train sig",
                alpha=0.5,
                log=True)
        
        ax = fig.add_subplot(222)
        ax.set_title("test vs train S")
        ax.hist(train_sig[field],
                bins=50,
                normed=True,
                range=(low,high),
                label="train sig",
                alpha=0.5)
        ax.hist(test_sig[field],
                bins=50,
                normed=True,
                range=(low,high),
                label="test sig",
                alpha=0.5)
        ax.legend()
        print field, "signal",
        print ks_2samp(test_sig[field], train_sig[field])[1]

        ax = fig.add_subplot(224)
        ax.set_title("test vs train B")
        ax.hist(train_bg[field],
                bins=50,
                normed=True,
                range=(low,high),
                label="train bg",
                alpha=0.5)
        ax.hist(test_bg[field],
                bins=50,
                normed=True,
                range=(low,high),
                label="test bg",
                alpha=0.5)
        #ax.legend()
        print field, "background",
        print ks_2samp(test_bg[field], train_bg[field])[1]
        
        fig.savefig("/tmp/%s.pdf"%(field))

def rank_all(events, sig_eff=0.9):
    """Rank different BDT methods by background
    efficiency at given `sig_eff`
    """
    results = []
    
    methods = [name for name in events.dtype.names if name.startswith("BDT_")]
    for method in methods:
        sig = events[test.classID==0][method]
        bg = events[test.classID==1][method]
        Nsig = len(sig)
        Nbg = len(bg)

        #print method
        #print sig.min(), sig.mean(), sig.max(), len(sig)
        #print bg.min(), bg.mean(), bg.max(), len(bg)
        
        sig.sort()
        bg.sort()

        # cut value is value at the 1-sig_eff
        # entry in sig, this is approximate
        cut_value = sig[int(Nsig*(1-sig_eff))]
        Nsig_pass = (sig>cut_value).sum()
        Nbg_pass = (bg>cut_value).sum()
        #print "cut %.3f sig_eff=%.3f Nbg=%i bg_eff=%.3f"%(cut_value,
        #                                                  Nsig_pass/float(Nsig),
        #                                                  Nbg_pass,
        #                                                  Nbg_pass/float(Nbg))
        results.append((method, Nsig_pass/float(Nsig), Nbg_pass/float(Nbg)))

    for res in sorted(results, key=operator.itemgetter(2)):
        print res
        
    
if __name__ == "__main__":
    import sys
    tmva_fname = sys.argv[1]
    f = R.TFile(tmva_fname)
    
    test_tree = f.TestTree
    train_tree = f.TrainTree

    test = root_numpy.tree2rec(test_tree)
    train = root_numpy.tree2rec(train_tree)

    draw_all(test, train)

    #rank_all(test, sig_eff=0.9)

    #draw_overtraining("BDT_ada", test, train)

    #draw_roccurve("BDT_ada", test)
