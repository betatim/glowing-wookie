import sys
if len(sys.argv) > 1:
  comment = sys.argv[1]
else:
  sys.exit("You need to specify the magnet polarity, year and comment")

if len(sys.argv) > 2: # specify test after the polarity to run a test job
  test = True
  #eCuts = [4.]
  #muCuts = [.4]
  eCuts = [2.,4.]
  muCuts = [.4,.6]
  jobsPerCut = [
    (0,2),
    (100,2),
    ]
else:
  test = False
  #eCuts = [2.,4.,6.,8.,10.]
  #muCuts = [.2,.4,.6,.8]
  eCuts = [6.,8.]
  muCuts = [.2,.4]
  jobsPerCut = [(25*i,25) for i in xrange(6*4)]


j = Job(name="fitter-toy%s"%("-test" if test else ""))
j.application = GaudiPython(project = 'DaVinci',
                            version = "v35r1",
                            script = "/afs/cern.ch/user/t/tbird/emu/glowing-wookie/scripts/fitters/toy_runner.py"
                            )
#j.backend = Local()
j.backend = Dirac()
j.comment = comment
j.inputsandbox = ["/afs/cern.ch/user/t/tbird/emu/glowing-wookie/"+i for i in [
  "scripts/fitters/fit_full.py",
  "scripts/fitters/syst_toy.py",
  "wookie/fitter/fullPdf.py",
  "wookie/fitter/integral.py",
  "wookie/fitter/variableUtils.py",
  "wookie/config.py",
  ]] + ["/afs/cern.ch/work/t/tbird/demu/ntuples/emu/fitter_loose_emu_2011_unblind.root"]

j.outputfiles = [
  SandboxFile(namePattern="fitResultsTree*.root"),
  ]

arguments = []

for eCut in eCuts:
  for muCut in muCuts:
    for seed, jobs in jobsPerCut:
      arguments.append([str(seed),str(jobs),str(eCut),str(muCut)])

j.splitter = ArgSplitter(args=arguments)

j.postprocessors.append(RootMerger(overwrite = True, ignorefailed = True))
j.postprocessors[-1].files = ['fitResultsTree.toy.root']

print j.name
j.submit()
