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
                        "classID==1 && BDT_ada<0.")
dataset2 = R.RooDataSet("MVATestDataSet2",
                        "MVATestDataSet2",
                        tree,
                        w.set("dataset_args"),
                        "classID==1 && BDT_ada>0.0 && BDT_ada<0.08")
dataset3 = R.RooDataSet("MVATestDataSet3",
                        "MVATestDataSet3",
                        tree,
                        w.set("dataset_args"),
                        "classID==1 && BDT_ada>0.08")
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
    w.factory("RooGenericPdf::blind%(n)i('(D0_MM<1700||D0_MM>1900)',{D0_MM})"%({"n":n}))
    
    w.factory("RooChebychev::D0M_Bkg_Poly%(n)i(D0_MM,{})"%({"n":n}))
    w.factory("PROD::D0M_Bkg_Poly%(n)i_Blind(D0M_Bkg_Poly%(n)i,blind%(n)i)"%({"n":n}))
    
    w.factory("RooExponential::D0M_Bkg_Exp%(n)i(D0_MM,D0M_Bkg_Exp%(n)i_Const[-0.001,-0.01,0])"%({"n":n}))
    w.factory("PROD::D0M_Bkg_Exp%(n)i_Blind(D0M_Bkg_Exp%(n)i,blind%(n)i)"%({"n":n}))
    
    w.factory("SUM:model%(n)i(D0M_Bkg_Poly%(n)i_Frac[0.5,0,1]*D0M_Bkg_Poly%(n)i_Blind, D0M_Bkg_Exp%(n)i_Blind)"%({"n":n}))
    #w.factory("PROD::model%(n)i(blind%(n)i,sum%(n)i)"%({"n":n}))



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
tf = R.TFile(config.plotspath + "/emubkgfit.root", "RECREATE")
for p in (plot1,plot2,plot3):
    p.Write()
    #p.Draw()
    #raw_input("next?")
tf.Close()
