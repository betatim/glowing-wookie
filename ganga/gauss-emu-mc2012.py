import sys
from Ganga.GPI import *
if len(sys.argv) > 1:
  polarity = sys.argv[1]
else:
  sys.exit("You need to specify the magnet polarity")
  
if len(sys.argv) > 2: # specify test after the polarity to run a test job
  test = True
  evtMax = 10
else:
  test = False
  evtMax = 1000
  
beamoptsfile = "$APPCONFIGOPTS/Gauss/Sim08-Beam4000GeV-md100-2012-nu2.5.py"
if polarity == "up":
  beamoptsfile = "$APPCONFIGOPTS/Gauss/Sim08-Beam4000GeV-mu100-2012-nu2.5.py"

j = Job(name="emu-MC2012-gen-mag%s%s"%(polarity,"-test" if test else ""))
j.application = Gauss()
j.application.optsfile = [
    beamoptsfile,
    "$DECFILESROOT/options/27183001.py",
    "$LBPYTHIA8ROOT/options/Pythia8.py",
    "$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py",
    "$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py",
    "$GAUSSOPTS/GenStandAlone.py"
  ]
j.application.extraopts = """
from Gauss.Configuration import *
GaussGen = GenInit("GaussGen")
GaussGen.FirstEventNumber = 1
GaussGen.RunNumber        = 1082
LHCbApp().EvtMax = %i
"""%(evtMax)
j.backend = Local()

print j.name
j.submit()
