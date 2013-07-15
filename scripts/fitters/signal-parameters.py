import ROOT as R
from ROOT import RooFit as RF
from wookie import config


R.RooRandom.randomGenerator().SetSeed(54321)

w = R.RooWorkspace("w", True)
w_import = getattr(w, "import")

# D mass and BDT output
w.factory("D0_MM[1600,2000]")
D0_MM = w.var("D0_MM")
w.factory("BDT_ada[-1,1]")
BDT = w.var("BDT_ada")
w.factory("classID[0,1]")
w.defineSet("dataset_args", "D0_MM,BDT_ada,classID")

w.factory("BDT_region[Cat1,Cat2,Cat3]")

f_input = R.TFile(config.path + "/d2emu-tmva.root")
tree = f_input.TestTree
# Need to create three datasets from the tree
# then create one big one from them with
# appropriate categories
dataset1 = R.RooDataSet("MVATestDataSet1",
                        "MVATestDataSet1",
                        tree,
                        w.set("dataset_args"),
                        "classID==0 && BDT_ada<0.3")
dataset2 = R.RooDataSet("MVATestDataSet2",
                        "MVATestDataSet2",
                        tree,
                        w.set("dataset_args"),
                        "classID==0 && BDT_ada>0.0 && BDT_ada<0.3")
dataset3 = R.RooDataSet("MVATestDataSet3",
                        "MVATestDataSet3",
                        tree,
                        w.set("dataset_args"),
                        "classID==0 && BDT_ada>0.3")
dataset = R.RooDataSet("MVATestDataSet",
                       "MVATestDataSet",
                       w.set("dataset_args"),
                       RF.Index(w.cat("BDT_region")),
                       RF.Import("Cat1",dataset1),
                       RF.Import("Cat2",dataset2),
                       RF.Import("Cat3",dataset3))
w_import(dataset)

# Start with splitting the BDT range in two halves
for n in (1,2,3):
    # attempt at a double CB, there must be a better way
    # shared mean and sigma, different alpha and n
    w.factory("CBShape:signalleft%(n)i(D0_MM, D_mean%(n)i[2000,0,10000], D_sigma%(n)i[10,0,200], D_alphaleft%(n)i[0.5,0,5], D_nleft%(n)i[2,0,10])"%({"n":n}))
    w.factory("CBShape:signalright%(n)i(D0_MM, D_mean%(n)i, D_sigma%(n)i, D_alpharight%(n)i[-0.5,-5,0], D_nright%(n)i[2,0,10])"%({"n":n}))
    w.factory("SUM:model%(n)i(nsigleft%(n)i[0,8000]*signalleft%(n)i, nsigright%(n)i[0,8000]*signalright%(n)i)"%({"n":n}))

#w.factory('Exponential::bg1(DM,abg1[-0.5,-2.5,0])')
#w.factory('Exponential::bg2(DM,abg2[-0.5,-2.5,0])')

#w.factory("prod:nsig1(mu[1,0,5],xsec1[8000])")
#w.factory("prod:nsig2(mu[1,0,5],xsec2[8000])")
#w.factory("prod:nsig3(mu[1,0,5],xsec2[8000])")
#w.factory("SUM::model1(nsig1[0,8000]*signal1)")
#w.factory("SUM::model2(nsig2[0,8000]*signal2)")
#w.factory("SUM::model3(nsig3[0,8000]*signal3)")


# Model which combines the two channels
w.factory("SIMUL:jointModel(BDT_region,Cat1=model1,Cat2=model2,Cat3=model3)")
pdf = w.pdf("jointModel")

pdf.fitTo(dataset,
          R.RooFit.Save(True),
          R.RooFit.Minimizer("Minuit2", "Migrad"),
          R.RooFit.NumCPU(1))

plot1 = D0_MM.frame(R.RooFit.Title("Channel 1"), R.RooFit.Name("channel1"))
plot2 = D0_MM.frame(R.RooFit.Title("Channel 2"), R.RooFit.Name("channel2"))
plot3 = D0_MM.frame(R.RooFit.Title("Channel 3"), R.RooFit.Name("channel3"))
dataset.plotOn(plot1, R.RooFit.Cut("BDT_region==BDT_region::Cat1"))
pdf.plotOn(plot1,
           R.RooFit.ProjWData(dataset),
           R.RooFit.Slice(w.cat("BDT_region"), "Cat1"))

dataset.plotOn(plot2, R.RooFit.Cut("BDT_region==BDT_region::Cat2"))
pdf.plotOn(plot2,
           R.RooFit.ProjWData(dataset),
           R.RooFit.Slice(w.cat("BDT_region"), "Cat2"))

dataset.plotOn(plot3, R.RooFit.Cut("BDT_region==BDT_region::Cat3"))
pdf.plotOn(plot3,
           R.RooFit.ProjWData(dataset),
           R.RooFit.Slice(w.cat("BDT_region"), "Cat3"))

#c = R.TCanvas()
tf = R.TFile(config.plotspath + "/emufit.root", "RECREATE")
for p in (plot1,plot2,plot3):
    p.Write()
    #p.Draw()
    raw_input("next?")
tf.Close()
