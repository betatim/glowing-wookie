import sys
polarity = sys.argv[1]

j = Job(name="emu-MC10-mag%s"%(polarity))
j.application = DaVinci(version="v33r4",
                        optsfile="options/toms-options.py"
                    )
dataset = j.application.readInputData("data/emu_%s.py"%polarity)
j.inputdata = dataset
j.backend = Dirac()
j.splitter = SplitByFiles(filesPerJob=2)

j.submit()
