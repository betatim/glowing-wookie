import ROOT as R

file = R.TFile.Open("/tmp/toyfit.root")

R.RooRandom.randomGenerator().SetSeed(12346)

w1 = file.Get("w1")
sbModel = w1.obj("ModelConfig")
data = w1.data("data")
mu = w1.var("mu")

# Now for some significance testing
# background only model
bModel = sbModel.Clone()
bModel.SetName("Background only")
mu.setVal(0)
bModel.SetSnapshot(w1.set("interestingParameter"))

# last parameter tells it to use nominal asimov data, which means??
asym_calc = R.RooStats.AsymptoticCalculator(data, bModel, sbModel, True)
# used these things before extending things with the HypoTestInverter
# turning on OneSidedDiscovery gives weird results
#asym_calc.SetOneSidedDiscovery(True)
#result = asym_calc.GetHypoTest()
#result.Print()

# Hypothesis test inversion, this is where the
# Brazil plot comes from
hypo_inv = R.RooStats.HypoTestInverter(asym_calc)
hypo_inv.UseCLs(True)

toy_mcs = asym_calc.GetTestStatSampler()
profll = R.RooStats.ProfileLikelihoodTestStat(sbModel.GetPdf())
# for CLs (bounded intervals) use one-sided profile likelihood
profll.SetOneSided(True)
toy_mcs.SetTestStatistic(profll);
# configure and run the scan
hypo_inv.SetFixedScan(40, 0, 4)
r = hypo_inv.GetInterval();
# get result and plot it
upperLimit = r.UpperLimit()
expectedLimit = r.GetExpectedUpperLimit(0)
plot = R.RooStats.HypoTestInverterPlot("hi","",r)
plot.Draw()
print "observed:", upperLimit
print "expected:", expectedLimit
raw_input("ff")
