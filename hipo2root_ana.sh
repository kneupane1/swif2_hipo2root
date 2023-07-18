#!/bin/bash

source /group/clas12/packages/setup.sh

module load gcc/9.2.0
module load root/6.26.10

export PATH=/work/clas12/users/kneupane/sim_multi_thr_clas12_ana/build:$PATH


echo "======= clas12_mc ========="
clas12_mc out.root *.root
echo "======= clas12_mc ========="


