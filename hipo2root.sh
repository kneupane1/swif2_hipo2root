#!/bin/bash

source /group/clas12/packages/setup.sh
module purge
module load gcc/9.2.0
module load root/6.24.06

export PATH=/work/clas12/users/tylern/software/hipo_tools/bin:$PATH


echo "======= dst2root ========="
/work/clas12/users/tylern/software/parallel -j16 'dst2root -mc {} {.}.root' ::: *.hipo
echo "======= dst2root ========="

echo "======= hadd ========="
/site/12gev_phys/2.5/Linux_CentOS7.7.1908-gcc9.2.0/root/6.24.06/bin/hadd merged.root *.root
echo "======= hadd ========="

