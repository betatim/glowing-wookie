import os
import platform

from wookie import make_dir

base = "/tmp/%s/"%(os.getenv("USER"))

_at_cern = "lxplus" in platform.node()
if os.getenv("USER") == "thead" and not _at_cern:
    path = "/tmp/thead/ntuples/"
if os.getenv("USER") == "thead" and _at_cern:
    path = "/afs/cern.ch/work/t/tbird/demu/ntuples/"
    
plotspath = base + "demu-plots/"
# place to store output from one script/stage
# that is read in by another script, not too
# expensive to re-generate
workingpath = base +"demu-working/"
    
if os.getenv("USER") == "tbird":
    path = "/afs/cern.ch/work/t/tbird/demu/ntuples/"
    plotspath = "/afs/cern.ch/user/t/tbird/emu/glowing-wookie/scripts/fitters/"

# Slowly transition to using this
# for ntuples
ntuplepath = path

for p in (path, plotspath, workingpath):
    make_dir(p)
