import sys
if len(sys.argv) > 1:
  polarity = sys.argv[1]
else:
  sys.exit("You need to specify the magnet polarity")
if len(sys.argv) > 2:
  test = True
  evtMax = 10000
else:
  test = False
  evtMax = -1

j = Job(name="pipi-MC11-mag%s%s"%(polarity, "-test" if test else ""))
j.application = DaVinci(version="v33r4",
                        optsfile="../wookie/options_common.py", 
                        extraopts = """
execute( 
  stripRun = True,
  stripConf = "default",
  stripLine = "pipi",
  dataType = "MC11",
  blinded = False,
  hltReport = True,
  tupleDecay = "emu",
  evtMax = %i,
  mag = "%s")
""" % (evtMax, polarity)
                    )
j.backend = Dirac()

dataset = j.application.readInputData("../data/pipi_%s.py"%polarity)


n_files_per_job = len(dataset)/50. # try to have around 50 jobs
if n_files_per_job > 100: n_files_per_job = 100 # max 100 allowed by dirac

if test:
  j.inputdata = dataset[:40]
  n_files_per_job = 40
else:
  j.inputdata = dataset
  
j.splitter = SplitByFiles(filesPerJob=n_files_per_job)

#j.submit()
