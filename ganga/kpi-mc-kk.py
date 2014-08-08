import sys
if len(sys.argv) > 2:
  polarity = sys.argv[1]
  #year = int(sys.argv[2])
  comment = sys.argv[2]
else:
  sys.exit("You need to specify the magnet polarity and comment")

if len(sys.argv) > 3: # specify test after the polarity to run a test job
  test = True
  evtMax = 1000
else:
  test = False
  evtMax = -1

year = "MC11a"

j = Job(name="kk-%s-kpistripped-mag%s%s"%(year, polarity, "-test" if test else ""))
j.application = DaVinci(version="v33r8",
                        optsfile="../wookie/options_common.py",
                        extraopts = """
execute(
  stripRun = True,
  stripConf = "default",
  stripLine = "kpi",
  dataType = "%s",
  blinded = False,
  hltReport = False,
  tupleDecay = "kpi",
  evtMax = %i,
  mag = "%s")
""" % (year, evtMax, polarity)
                    )
j.backend = Dirac()
j.comment = comment

lfns = {
  "MC11a" : "/MC/MC11a/Beam3500GeV-2011-Mag%s-Nu2-EmNoCuts/Sim05a/Trig0x40760037Flagged/Reco12a/Stripping17NoPrescalingFlagged/27163002/ALLSTREAMS.DST",
  }

#dataset = j.application.readInputData("../data/kpi_%s.py"%polarity)
lfn = lfns[year]%(polarity.capitalize(),)
print "Getting data from:", lfn
dataset = BKQuery(lfn).getDataset()

n_files_per_job = int(len(dataset)/50.) # try to have around 50 jobs
if n_files_per_job > 100: n_files_per_job = 100 # max 100 allowed by dirac
if n_files_per_job == 0: n_files_per_job = 1 # one file at least

if test:
  j.inputdata = dataset[:2]
  n_files_per_job = 2
else:
  j.inputdata = dataset

j.splitter = SplitByFiles(filesPerJob=n_files_per_job)

j.postprocessors.append(RootMerger(overwrite = True, ignorefailed = True))
j.postprocessors[-1].files = ['Demu_NTuple.root']

print j.name
j.submit()
