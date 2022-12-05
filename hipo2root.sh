#!/bin/bash

source /group/clas12/packages/setup.sh
module purge
module load gcc/9.2.0

source /work/clas12/users/tylern/software/root/bin/thisroot.sh

export PATH=/work/clas12/users/tylern/software/hipo_tools/bin:$PATH



echo "======= dst2root ========="
/work/clas12/users/tylern/software/parallel -j16 'dst2root -mc {} {.}.root' ::: *.hipo
echo "======= dst2root ========="

echo "======= hadd ========="
mkdir tmp
/work/clas12/users/tylern/software/root/bin/hadd -j 16 -d $PWD/tmp merged.root *.root
echo "======= hadd ========="

