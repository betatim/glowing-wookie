import ROOT as R

# Exploring the options of RooFit and RooStats
# when it comes to setting limits and such
# Run this script first to create some "data"
# for two channels which both contain signal
# Then run roostating.py to have an interval
# calculated as well as a significance

R.RooRandom.randomGenerator().SetSeed(12345)

w1 = R.RooWorkspace("w1", True)
w1_import = getattr(w1, "import")

# Two channels which we combine to discover a
# new particle sitting at a mass of 2
w1.factory('Gaussian::signal(x[0,10],mass[2],0.3)')

# Channel One has a background that falls exponentially
# 20 signal events on a background of 1000
w1.factory('Exponential::bg1(x,abg1[-0.5,-2.5,0])')
w1.factory("prod:nsig1(mu[1,0,5],xsec1[20])")

w1.factory("SUM::model1(nsig1*signal,nbg1[1000,0,10000]*bg1)")

# Channel Two has a background that falls exponentially
# 20 signal events on a background of 100
w1.factory('Exponential::bg2(x,abg2[-0.25,-2.5,0])')
w1.factory("prod:nsig2(mu,xsec2[18])")

w1.factory("SUM::model2(nsig2*signal,nbg2[100,0,10000]*bg2)")

# To identify which channel an event belongs to
w1.factory("index[channel1,channel2]")
# Model which combines the two channels
w1.factory("SIMUL:jointModel(index,channel1=model1,channel2=model2)")

pdf = w1.pdf("jointModel")
x = w1.var("x")
index = w1.var("index")

# Our data from the "detector"
# let's pretend there is no signal
w1.var("mu").setVal(0.)
data = pdf.generate(R.RooArgSet(x, R.w1.index))
data.SetName("data")
w1_import(data)

# Show our data
plot1 = x.frame(R.RooFit.Title("Channel 1"))
plot2 = x.frame(R.RooFit.Title("Channel 2"))
data.plotOn(plot1, R.RooFit.Cut("index==index::channel1"))
data.plotOn(plot2, R.RooFit.Cut("index==index::channel2"))

# Time to do a fit
pdf.fitTo(data,
          R.RooFit.Save(True),
          R.RooFit.Minimizer("Minuit2","Migrad"),
          R.RooFit.NumCPU(4))

# ProjWData() and Slice() work together to select
# only those events and parts of the PDF for this
# category
pdf.plotOn(plot1,
           R.RooFit.ProjWData(data),
           R.RooFit.Slice(w1.cat("index"), "channel1"))
# Draw the signal component in red
pdf.plotOn(plot1,
           R.RooFit.ProjWData(data),
           R.RooFit.Slice(w1.cat("index"), "channel1"),
           R.RooFit.Components("signal"),
           R.RooFit.LineColor(R.kRed))
pdf.plotOn(plot2,
           R.RooFit.ProjWData(data),
           R.RooFit.Slice(w1.cat("index"), "channel2"))
# Draw the signal component in red
pdf.plotOn(plot2,
           R.RooFit.ProjWData(data),
           R.RooFit.Slice(w1.cat("index"), "channel2"),
           R.RooFit.Components("signal"),
           R.RooFit.LineColor(R.kRed))

c = R.TCanvas()
c.Divide(2,1)
c.cd(1)
plot1.Draw()
c.cd(2)
plot2.Draw()

raw_input("onwards?")

# Now for creating a model config which can be
# understood by RooStats to extract limits
mc = R.RooStats.ModelConfig("ModelConfig", w1)
mc.SetPdf(pdf)
mc.SetParametersOfInterest("mu")
mc.SetObservables("x,index")

w1.defineSet("nuisanceParameters", "abg1,abg2,nbg1,nbg2")
mc.SetNuisanceParameters(w1.set("nuisanceParameters"))

w1.defineSet("interestingParameter", "mu")
w1.var("mu").setVal(1)
mc.SetSnapshot(w1.set("interestingParameter"))

# Finally, save the model config to a root file
w1_import(mc)
w1.writeToFile("/tmp/toyfit.root", True)
