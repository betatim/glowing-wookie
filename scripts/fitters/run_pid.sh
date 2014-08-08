#!/bin/bash

(
  set -x


  for e_cut in 2 4 6 8 10 ; do
    for mu_cut in 0.2 0.4 0.6 0.8 ; do
      echo "#cut: DLLe>${e_cut} && ProbNNmu>${mu_cut}"
      time python fit_full.py pid 4 $e_cut $mu_cut
    done
  done

  set +x
) | tee log.pid_tagged.txt

