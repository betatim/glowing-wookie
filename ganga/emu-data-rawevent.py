import sys
from Ganga.GPI import *
if len(sys.argv) > 2:
  polarity = sys.argv[1]
  comment = sys.argv[2]
else:
  sys.exit("You need to specify the magnet polarity")

if len(sys.argv) > 3: # specify test after the polarity to run a test job
  test = True
  evtMax = 1000
else:
  test = False
  evtMax = -1

j = Job(name="emu-data-2012-mag%s%s"%(polarity, "-test" if test else ""))
j.application = DaVinci(version="v33r8",
                        optsfile="../wookie/options_common.py",
                        extraopts = """
execute(
  stripRun = True,
  stripConf = "default",
  stripLine = "emu",
  dataType = "data2012",
  blinded = False,
  hltReport = False,
  tupleDecay = "emu",
  evtMax = %i,
  mag = "%s")
""" % (evtMax, polarity)
                    )
j.backend = Dirac()
j.comment = comment
#dataset = [LogicalFile("/lhcb/user/a/acontu/648/2014_06/80153/80153692/charmcompleteeventS20_WITHRAW.dst")]
dataset = [LogicalFile("/lhcb/user/a/acontu/648/2014_06/80153/80153692/charmcompleteeventS20_NoRAW.dst")]

#j.application.readInputData("../data/stripping20r0p1_completecharm_%s.py"%polarity)


n_files_per_job = int(len(dataset)/50.) # try to have around 50 jobs
if n_files_per_job > 100: n_files_per_job = 100 # max 100 allowed by dirac
if n_files_per_job == 0: n_files_per_job = 1 # one file at least

if test:
  j.inputdata = dataset[:40]
  n_files_per_job = 40
else:
  j.inputdata = dataset

j.splitter = SplitByFiles(filesPerJob=n_files_per_job)

j.postprocessors.append(RootMerger(overwrite = True, ignorefailed = True))
j.postprocessors[-1].files = ['Demu_NTuple.root']


j.prepare()
print j.name
j.submit()
