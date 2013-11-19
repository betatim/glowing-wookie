import sys
from Ganga.GPI import *
if len(sys.argv) > 1:
  polarity = sys.argv[1]
else:
  sys.exit("You need to specify the magnet polarity")
  
if len(sys.argv) > 2: # specify test after the polarity to run a test job
  test = True
  evtMax = 10000
else:
  test = False
  evtMax = -1
  
outputType = "dst"

j = Job(name="emu-lsdata-2012-mag%s%s"%(polarity, "-test" if test else ""))
j.application = DaVinci(version="v33r4",
                        optsfile="../wookie/options_common.py", 
                        extraopts = """
execute( 
  stripRun = True,
  stripConf = "ls",
  stripLine = "emu",
  dataType = "data2012",
  blinded = False,
  hltReport = False,
  tupleDecay = "lsemu",
  evtMax = %i,
  mag = "%s",
  outputType = "%s")
""" % (evtMax, polarity, outputType)
                    )
j.backend = Dirac()

if outputType != "dst":
  j.postprocessors.append(RootMerger(overwrite = True, ignorefailed = True))
  j.postprocessors[-1].files = ['Demu_NTuple.root']
else:
  j.outputfiles = [DiracFile(namePattern="Demu.lsdata.dst")]

j.prepare()

dataset = j.application.readInputData("../data/stripping20r0p1_completecharm_%s.py"%polarity)

n_files_per_job = int(len(dataset)/50.) # try to have around 50 jobs
if n_files_per_job > 100: n_files_per_job = 100 # max 100 allowed by dirac
if n_files_per_job == 0: n_files_per_job = 1 # one file at least

if test:
  j.inputdata = dataset[:40]
  n_files_per_job = 40
else:
  j.inputdata = dataset
  
j.splitter = SplitByFiles(filesPerJob=n_files_per_job)

print j.name
j.submit()
