#!/usr/bin/env python


import sys
import subprocess

if len(sys.argv) != 5:
  sys.exit("Error script takes 4 arguments, the seed, the number of jobs to run, PIDe cut and ProbNNmu cut")

seed = int(sys.argv[1])
jobs = int(sys.argv[2])
eCut = float(sys.argv[3])
muCut = float(sys.argv[4])

print "Toy runner is running!"
sys.stdout.flush()

for i in xrange(jobs):
  subprocess.call("python fit_full.py -s {0:d} toy 1 {1:f} {2:f}".format(i+seed, eCut, muCut).split())

subprocess.call(["hadd","fitResultsTree.toy.root"]+["fitResultsTree.toy.{0:.1f}_{1:.1f}_{2:d}.root".format(eCut, muCut,i+seed) for i in xrange(jobs)])

