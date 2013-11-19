import sys
from Ganga.GPI import *
if len(sys.argv) > 1:
  #polarity = sys.argv[1]
  oldjob = int(sys.argv[1])
else:
  sys.exit("You need to specify the old job ID and comment")
  
if jobs(oldjob).application.__class__ is not DaVinci:
  sys.exit("The given job is not a DaVinci job.")

if jobs(oldjob).backend.__class__ is not Dirac:
  sys.exit("The given job was not run on the grid.")

if len(sys.argv) > 3: # specify test after the polarity to run a test job
  test = True
  evtMax = 1000
else:
  test = False
  evtMax = -1

j = Job(name="temp")
j.application = Moore(version="v20r4",
                        optsfile="../wookie/options_moore.py", 
                    )
j.backend = Dirac()

j.comment = sys.argv[2]
j.name = jobs(oldjob).name + ("-test" if test else "")
j.application.extraopts = jobs(oldjob).application.extraopts

j.outputfiles = [DiracFile(namePattern="Demu.lsdata.dst")]

dataset = LHCbDataset()
for sj in jobs(oldjob).subjobs:
  for f in sj.outputfiles:
    if f.__class__ is DiracFile:
      if f.lfn != "":
        dataset.extend(["LFN:"+f.lfn])

n_files_per_job = 100

if test:
  j.inputdata = dataset[:40]
  n_files_per_job = 40
else:
  j.inputdata = dataset
  
j.splitter = SplitByFiles(filesPerJob=n_files_per_job)

j.prepare()
print j.name
j.submit()
