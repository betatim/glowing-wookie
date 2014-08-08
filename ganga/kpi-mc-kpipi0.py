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

year = 2012

j = Job(name="kpipi0-MC%i-kpistripped-mag%s%s"%(year, polarity, "-test" if test else ""))
j.application = DaVinci(version="v33r8",
                        optsfile="../wookie/options_common.py",
                        extraopts = """
execute(
  stripRun = True,
  stripConf = "default",
  stripLine = "kpi",
  dataType = "MC%i",
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
  #2011 : "/MC/2011/Beam3500GeV-2011-Mag%s-Nu2-Pythia8/Sim08a/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/27163003/ALLSTREAMS.DST",
  2012 : "/MC/2012/Beam4000GeV-2012-Mag%s-Nu2.5-Pythia8/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/27163402/ALLSTREAMS.DST",
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
