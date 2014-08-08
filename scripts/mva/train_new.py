
from ROOT import gROOT, TMVA, TFile, TCut
TMVA.Tools.Instance()

outfileName = "TMVA.root"
outputFile  = TFile.Open( outfileName, "RECREATE" )



factory = TMVA.Factory( "TMVAClassification", outputFile,
                        "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" );

#    factory.AddVariable( "myvar1 := var1+var2", 'F' )
#    factory.AddVariable( "myvar2 := var1-var2", "Expression 2", "", 'F' )
#    factory.AddVariable( "var3",                "Variable 3", "units", 'F' )
#    factory.AddVariable( "var4",                "Variable 4", "units", 'F' )

#    factory.AddVariable( "D0_CosTheta","D0_CosTheta", "", 'F' )
#    factory.AddVariable( "D0_DOCA","D0_DOCA", "", 'F' )
#    factory.AddVariable( "-log(1-(D0_DIRA))","D0_pointing", "", 'F' )
#    factory.AddVariable( "-log(D0_VChi2_per_NDOF)","D0_VChi2_per_NDOF", "", 'F' )
#    factory.AddVariable( "D0_MinIPChi2_PRIMARY","D0_MinIPChi2_PRIMARY", "", 'F' )
#    factory.AddVariable( "-log(D0_IPChi2)","D0_IPChi2", "", 'F' )
#    factory.AddVariable( "Dst_MinIPChi2_PRIMARY","Dst_MinIPChi2_PRIMARY", "", 'F' )
#    factory.AddVariable( "(abs(x1_ID)==15||abs(x1_ID)==13||abs(x1_ID)==11)*((x1_ID<0)*x1_CosTheta+(x1_ID>0)*x2_CosTheta)+(abs(x1_ID)!=15&&abs(x1_ID)!=13&&abs(x1_ID)!=11)*((x1_ID>0)*x1_CosTheta+(x1_ID<0)*x2_CosTheta)","LepCosTheta", "", 'F' )
#    factory.AddVariable( "-log((x1_IPCHI2_OWNPV<x2_IPCHI2_OWNPV)*x1_IPCHI2_OWNPV+(x2_IPCHI2_OWNPV<x1_IPCHI2_OWNPV)*x2_IPCHI2_OWNPV)","minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV", "", 'F' )
#    factory.AddVariable( "D0_PT/(D0_PT+D0_cpt_1.00)","D0_PtScaledIso", "", 'F' )
#    factory.AddVariable( "abs(x1_TRACK_Eta-x2_TRACK_Eta)","D0_DelEta", "", 'F' )
#    factory.AddVariable( "cos(x1_TRACK_Phi-x2_TRACK_Phi)","D0_DelPhi", "", 'F' )

factory.AddVariable( "D0_CosTheta","D0_CosTheta", "", 'F' )
factory.AddVariable( "D0_DOCA","D0_DOCA", "", 'F' )
factory.AddVariable( "log_D0_VChi2_per_NDOF","log_D0_VChi2_per_NDOF", "", 'F' )
factory.AddVariable( "D0_MinIPChi2_PRIMARY","D0_MinIPChi2_PRIMARY", "", 'F' )
factory.AddVariable( "exp(-log_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV)","log_minx1_IPCHI2_OWNPV_x2_IPCHI2_OWNPV", "", 'F' )
factory.AddVariable( "D0_PtScaledIso","D0_PtScaledIso", "", 'F' )
factory.AddVariable( "D0_DelEta","D0_DelEta", "", 'F' )
factory.AddVariable( "D0_DelPhi","D0_DelPhi", "", 'F' )

factory.AddVariable( "x1_TRACK_PCHI2","x1_TRACK_PCHI2", "", 'F' )
factory.AddVariable( "x2_TRACK_PCHI2","x2_TRACK_PCHI2", "", 'F' )

factory.AddVariable( "-log(D0_IPChi2)","D0_IPChi2", "", 'F' )
factory.AddVariable( "Dst_MinIPChi2_PRIMARY","Dst_MinIPChi2_PRIMARY", "", 'F' )

factory.AddVariable( "Dst_DTF_CHI2","Dst_DTF_CHI2", "", 'F' )
factory.AddVariable( "pi_TRACK_PCHI2","pi_TRACK_PCHI2", "", 'F' )

factory.AddVariable( "D0_pointing","D0_pointing", "", 'F' )

#factory.AddVariable( "LepCosTheta","LepCosTheta", "", 'F' )
#factory.AddVariable( "D0_TAU","D0_TAU", "", 'F' )
#factory.AddVariable( "pi_PT","pi_PT", "", 'F' )

#factory.AddVariable( "log(Dst_LoKi_BPVVDCHI2)","log(Dst_LoKi_BPVVDCHI2)", "", 'F' )
#factory.AddVariable( "D0_FDCHI2_OWNPV","D0_FDCHI2_OWNPV", "", 'F' )
#factory.AddVariable( "D0_IPCHI2_OWNPV","D0_IPCHI2_OWNPV", "", 'F' )
#factory.AddVariable( "Dst_IPCHI2_OWNPV","Dst_IPCHI2_OWNPV", "", 'F' )



#factory.AddSpectator( "D0_Mass",   "D0_Mass",  "MeV", 'F' )
#factory.AddSpectator( "Dst_Mass",  "Dst_Mass", "MeV", 'F' )
#factory.AddSpectator( "Del_Mass",  "Del_Mass", "MeV", 'F' )

inputS = TFile.Open( "/afs/cern.ch/work/t/tbird/demu/ntuples/mcemu/mva_emu_2011.root" )
inputB = TFile.Open( "/afs/cern.ch/work/t/tbird/demu/ntuples/emu/mva_emu_2011_blind.root" )
#    TFile *inputS = TFile.Open( "root:#castorlhcb.cern.ch#castor/cern.ch/user/t/tbird/demu/ntuples/pipi/strip_pipi_2011.root" )
#    TFile *inputB = TFile.Open( "/afs/cern.ch/work/t/tbird/demu/ntuples/emu/strip_emu_2011_unblind.root" )

print "--- TMVAClassification       : Using input signal file: ", inputS.GetName()
print "--- TMVAClassification       : Using input background file: ", inputB.GetName()

# --- Register the training and test trees

outputFile.cd()

signal      = inputS.Get("subTree")
signalTrain = signal.CopyTree("RAND>0.5&&Dst_MinIPChi2_PRIMARY>0")
signalTest  = signal.CopyTree("RAND<0.5&&Dst_MinIPChi2_PRIMARY>0")

background      = inputB.Get("subTree")
backgroundTrain = background.CopyTree("RAND>0.5&&Dst_MinIPChi2_PRIMARY>0")
backgroundTest  = background.CopyTree("RAND<0.5&&Dst_MinIPChi2_PRIMARY>0")

# global event weights per tree (see below for setting event-wise weights)
#    Double_t signalWeight     = 1.0
#    Double_t backgroundWeight = 1.0

# You can add an arbitrary number of signal or background trees
#    factory.AddSignalTree    ( signal,     signalWeight     )
#    factory.AddBackgroundTree( background, backgroundWeight )

# To give different trees for training and testing, do as follows:
factory.AddSignalTree( signalTrain,         1., "Training" )
factory.AddSignalTree( signalTest,          1., "Test" )
factory.AddBackgroundTree( backgroundTrain, 1., "Training" )
factory.AddBackgroundTree( backgroundTest,  1., "Test" )

# Apply additional cuts on the signal and background samples (can be different)
mycuts = TCut("")
mycutb = TCut("")
# for example: TCut mycutb = "abs(var1)<0.5"

# Tell the factory how to use the training and testing events
#
# If no numbers of events are given, half of the events in the tree are used
# for training, and the other half for testing:
#    factory.PrepareTrainingAndTestTree( mycut, "SplitMode=random:!V" )
# To also specify the number of testing events, use:
#    factory.PrepareTrainingAndTestTree( mycut,
#                                         "NSigTrain=3000:NBkgTrain=3000:NSigTest=3000:NBkgTest=3000:SplitMode=Random:!V" )
factory.PrepareTrainingAndTestTree( mycuts, mycutb,
                                    "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

# --- OptimizeConfigParamete...: FOM was found : 0.129483 current best is 0.157006
# --- OptimizeConfigParamete...: For BDTG the optimized Parameters are:
# --- OptimizeConfigParamete...: MaxDepth = 3
# --- OptimizeConfigParamete...: NTrees = 287.5
# --- OptimizeConfigParamete...: NodeMinEvents = 305 # MinNodeSize? 305/5500 =5.5%
# --- OptimizeConfigParamete...: Shrinkage = 0.05


# Boosted Decision Trees
factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                    "!H:!V:MaxDepth=3:NTrees=288:MinNodeSize=5.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:UseFisherCuts:MinLinCorrForFisher=0.35:GradBaggingFraction=0.5" )

# Train MVAs using the set of training events
factory.TrainAllMethods()

# ---- Evaluate all MVAs using the set of test events
factory.TestAllMethods()

# ----- Evaluate and compare performance of all configured MVAs
factory.EvaluateAllMethods()

# Save the output
outputFile.Close()

print "==> Wrote root file: ", outputFile.GetName()
print "==> TMVAClassification is done!"


