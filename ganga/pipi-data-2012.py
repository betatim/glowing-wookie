import sys
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

j = Job(name="pipi-data-2012-mag%s%s"%(polarity, "-test" if test else ""))
j.application = DaVinci(version="v33r4",
                        optsfile="../wookie/options_common.py", 
                        extraopts = """
execute( 
  stripRun = False,
  stripConf = "default",
  stripLine = "pipi",
  dataType = "data2012",
  blinded = False,
  hltReport = False,
  tupleDecay = "pipi",
  evtMax = %i,
  mag = "%s")
""" % (evtMax, polarity)
                    )
j.backend = Dirac()

dataset = j.application.readInputData("../data/stripping20_completecharm_%s.py"%polarity)


n_files_per_job = int(len(dataset)/50.) # try to have around 50 jobs
if n_files_per_job > 100: n_files_per_job = 100 # max 100 allowed by dirac
if n_files_per_job == 0: n_files_per_job = 1 # one file at least

if test:
  j.inputdata = dataset[:50]
  n_files_per_job = 20
else:
  j.inputdata = dataset
  
j.splitter = SplitByFiles(filesPerJob=n_files_per_job)

print j.name
j.submit()
