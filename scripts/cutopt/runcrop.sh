#!/bin/bash
LD_LIBRARY_PATH=/afs/cern.ch/user/t/tbird/emu/glowing-wookie/scripts/cutopt/simpletools_2.0l/lib:${LD_LIBRARY_PATH} time ./simpletools_2.0l/bin/crop weightfile.crop cutfile.crop 100 B cropout2.root -b
