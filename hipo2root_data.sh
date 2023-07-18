#!/bin/bash

source /group/clas12/packages/setup.sh
module purge
module load gcc/9.2.0

source /work/clas12/users/tylern/software/root/bin/thisroot.sh

export PATH=/work/clas12/users/tylern/software/hipo_tools/bin:$PATH



echo "======= dst2root ========="
dst2root $1 $2
echo "======= dst2root ========="


