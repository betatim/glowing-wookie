import sys
polarity = sys.argv[1]

j = Job(name="2012-data-mag%s"%(polarity))
j.application = DaVinci(version="v33r4",
                        optsfile="options/toms-options.py"
                    )
dataset = j.application.readInputData("data/stripping20r0p1_%s.py"%polarity)
j.inputdata = dataset[:40]

j.backend = Dirac()
#j.splitter = SplitByFiles(filesPerJob=100)

j.submit()
