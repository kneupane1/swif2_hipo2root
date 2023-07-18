#!/bin/bash

source /group/clas12/packages/setup.sh
module purge
module load gcc/9.2.0
source /work/clas12/users/tylern/software/root/bin/thisroot.sh

export PATH=/home/tylern/clas12_analysis/build:$PATH

export NUM_THREADS=$SLURM_CPUS_PER_TASK

echo "Starting csv maker"
clas12_csv clas12.csv *.root