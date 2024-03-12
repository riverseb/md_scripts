#!/bin/bash
#SBATCH --job-name=CM_mut_CitL_v6
#SBATCH --mail-user=dsanper@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/nfs/turbo/lsi-davidhs/Daniel/MD/simulations/CM_mut_CitL_v6/logs/prod.log
#SBATCH --partition=gpu
#SBATCH --mem-per-gpu=2g
#SBATCH --gres=gpu:1
#SBATCH --time=9-2:00:00
module restore
export LD_LIBRARY_PATH=/afs/umich.edu/group/a/arcts/software/gaussian-16revC01-avx2/g16/bsd:/afs/umich.edu/group/a/arcts/software/gaussian-16revC01-avx2/g16:/sw/pkgs/coe/c/amber/22/lib:/sw/pkgs/arc/cuda/11.6.2/lib64:/sw/pkgs/arc/intel/2022.1.2/mpi/2021.5.1/libfabric/lib:/sw/pkgs/arc/intel/2022.1.2/mpi/2021.5.1/lib/release:/sw/pkgs/arc/intel/2022.1.2/mpi/2021.5.1/lib:/sw/pkgs/arc/python/3.10.4/lib:/sw/pkgs/arc/gcc/10.3.0/lib64
export AMBERHOME=/sw/pkgs/coe/c/amber/22

/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i min.in  -o min.out   -p *prmtop -c *.inpcrd -r min.rst   -x min.nc   -ref *.inpcrd

/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i eq1.in  -o eq1.out   -p *prmtop -c min.rst  -r eq1.rst   -x eq1.nc   -ref min.rst

/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i eq2.in  -o eq2.out   -p *prmtop -c eq1.rst  -r eq2.rst   -x eq2.nc   -ref eq1.rst

/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i eq3.in  -o eq3.out   -p *prmtop -c eq2.rst  -r eq3.rst   -x eq3.nc   -ref eq2.rst

/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i prod.in -o prod1.out -p *prmtop -c eq3.rst  -r prod1.rst -x prod1.nc
/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i prod.in -o prod2.out -p *prmtop -c prod1.rst -r prod2.rst -x prod2.nc
