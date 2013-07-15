import os
import platform


_at_cern = "lxplus" in platform.node()

path = "/afs/cern.ch/work/t/tbird/demu/ntuples/"
if os.getenv("USER") == "thead" and not _at_cern:
    path = "/tmp/ntuples/"
