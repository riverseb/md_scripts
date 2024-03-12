#!/bin/bash
#SBATCH --job-name=CtdP_MPC_rep3_extend
#SBATCH --mail-user=riverseb@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/nfs/turbo/lsi-davidhs/Daniel/MD/simulations/CtdP_mono_diene/PMC_lig/exp2/logs/prod_extend3.log
#SBATCH --partition=gpu,spgpu
#SBATCH --mem-per-gpu=2g
#SBATCH --account=davidhs1
#SBATCH --gres=gpu:1
#SBATCH --time=9-00:00:00
module restore amber
export LD_LIBRARY_PATH=/afs/umich.edu/group/a/arcts/software/gaussian-16revC01-avx2/g16/bsd:/afs/umich.edu/group/a/arcts/software/gaussian-16revC01-avx2/g16:/sw/pkgs/coe/c/amber/22/lib:/sw/pkgs/arc/cuda/11.6.2/lib64:/sw/pkgs/arc/intel/2022.1.2/mpi/2021.5.1/libfabric/lib:/sw/pkgs/arc/intel/2022.1.2/mpi/2021.5.1/lib/release:/sw/pkgs/arc/intel/2022.1.2/mpi/2021.5.1/lib:/sw/pkgs/arc/python/3.10.4/lib:/sw/pkgs/arc/gcc/10.3.0/lib64
export AMBERHOME=/sw/pkgs/coe/c/amber/22

/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i prod.in -o prod3.out -p *prmtop -c prod2.rst -r prod3.rst -x prod3.nc
/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i prod.in -o prod4.out -p *prmtop -c prod3.rst -r prod4.rst -x prod4.nc
/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i prod.in -o prod5.out -p *prmtop -c prod4.rst -r prod5.rst -x prod5.nc
/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i prod.in -o prod6.out -p *prmtop -c prod5.rst -r prod6.rst -x prod6.nc
/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i prod.in -o prod7.out -p *prmtop -c prod6.rst -r prod7.rst -x prod7.nc
/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i prod.in -o prod8.out -p *prmtop -c prod7.rst -r prod8.rst -x prod8.nc
/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i prod.in -o prod9.out -p *prmtop -c prod8.rst -r prod9.rst -x prod9.nc
/sw/pkgs/coe/c/amber/22/bin/pmemd.cuda -O -i prod.in -o prod10.out -p *prmtop -c prod9.rst -r prod10.rst -x prod10.nc