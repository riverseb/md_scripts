#!/bin/bash

#SBATCH --job-name=MPC
#SBATCH --mail-user=dsanper@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/nfs/turbo/umms-maom/projects/IMDAase/md/ligands/MPC/MPC_geom_esp.log
#SBATCH --partition=standard
#SBATCH	--account=maom0
#SBATCH --mem-per-cpu=2g
#SBATCH --time=01-00:00:00

module restore
g16 formatted_ZWP.com 