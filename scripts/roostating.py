import ROOT as R

file = R.TFile.Open("/tmp/toyfit.root")

w1 = file.Get("w1")
model = w1.obj("ModelConfig")
data = w1.data("data")

plh = R.RooStats.ProfileLikelihoodCalculator(data, model)

plh.SetConfidenceLevel(0.683)
interval = plh.GetInterval()
mu = w1.var("mu")
print "68% CL interval for mu:"
print "[%.4f %.4f]"%(interval.LowerLimit(mu), interval.UpperLimit(mu))

# Now for some significance testing
# background only model
bModel = model.Clone()
bModel.SetName("Background only")
mu.setVal(0)
bModel.SetSnapshot(w1.set("interestingParameter"))

asym_calc = R.RooStats.AsymptoticCalculator(data, model, bModel)
asym_calc.SetOneSidedDiscovery(True)
result = asym_calc.GetHypoTest()
result.Print()
