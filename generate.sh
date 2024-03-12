export AMBERHOME=/sw/pkgs/coe/c/amber/22

cd $1
mkdir logs
echo "source leaprc.protein.ff14SB                                       " >  tleap.in
echo "source leaprc.gaff                                                 " >> tleap.in
echo "source leaprc.water.tip3p                                          " >> tleap.in
echo "loadAmberParams ../../ligands/NAP_syn/NAP.frcmod                       " >> tleap.in ## change based on ligand being used 
#echo "loadAmberParams ../../ligands/NDP/NDP.frcmod                       " >> tleap.in
#echo "loadAmberParams ../../ligands/PM7/PM7.frcmod                       " >> tleap.in
echo "loadAmberParams ../../ligands/ZWP_anti/ZWP.frcmod                       " >> tleap.in ## change based on ligand
echo "loadoff ../../ligands/NAP_syn/NAP.lib                                  " >> tleap.in ## change based on ligand
#echo "loadoff ../../ligands/NDP/NDP.lib                                  " >> tleap.in
#echo "loadoff ../../ligands/PM7/PM7.lib                                  " >> tleap.in
echo "loadoff ../../ligands/ZWP_anti/ZWP.lib                                  " >> tleap.in ## change based on ligand
echo "a = loadpdb PhqE_tetramer.pdb                                           " >> tleap.in ## change based on input structure file name
echo "center a                                                           " >> tleap.in
echo "alignAxes a                                                        " >> tleap.in
echo "savepdb a crystal_dry.pdb                                          " >> tleap.in
echo "addions a Cl- 0                                                    " >> tleap.in
echo "addions a Na+ 0                                                    " >> tleap.in
echo "solvateBox a TIP3PBOX 10 iso                                       " >> tleap.in
echo "saveamberparm a crystal_wat.prmtop crystal_wat.inpcrd              " >> tleap.in
echo "savepdb a crystal_wat.pdb                                          " >> tleap.in
echo "                                                                   " >> tleap.in
echo "quit                                                               " >> tleap.in

$AMBERHOME/bin/tleap -f tleap.in -s
rm tleap.in leap.log 

echo "initial minimization                           " >  min.in 
echo " &cntrl                                        " >> min.in
echo "  imin   = 1, irest = 0, ntx = 1,              " >> min.in
echo "  maxcyc = 5000, ncyc = 2500,                  " >> min.in
echo "  ntc    = 1, ntf = 1,                         " >> min.in
echo "  cut    = 8.0,                                " >> min.in
echo "  ntb    = 1,                                  " >> min.in
echo "  iwrap  = 1,                                  " >> min.in
echo "  ig     = -1,                                 " >> min.in
echo "  ioutfm = 1,                                  " >> min.in
echo "  ntpr   = 500, ntwx = 500, ntwr = 500,        " >> min.in
echo "  ntr    = 1, restraint_wt = 2.0,              " >> min.in
echo "  restraintmask = ':1-1027@C,CA,N,O|:1028-1034&!@H='," >> min.in ## change based on res numbering from crystal_dry.pdb
echo " /                                             " >> min.in

echo "1ns heating in NVT                             " >  eq1.in
echo " &cntrl                                        " >> eq1.in
echo "  imin   = 0, irest = 0, ntx = 1,              " >> eq1.in
echo "  ntc    = 2, ntf = 2,                         " >> eq1.in
echo "  cut    = 8.0,                                " >> eq1.in
echo "  ntt    = 3, gamma_ln = 5.0,                  " >> eq1.in
echo "  tempi  = 0.0, temp0  = 300.0,                " >> eq1.in
echo "  ntb    = 1,                                  " >> eq1.in
echo "  iwrap  = 1,                                  " >> eq1.in
echo "  ig     = -1,                                 " >> eq1.in
echo "  ioutfm = 1,                                  " >> eq1.in
echo "  nstlim = 1000000, dt = 0.001,                " >> eq1.in
echo "  ntpr   = 50000, ntwx = 50000, ntwr = 50000,  " >> eq1.in
echo "  ntr    = 1, restraint_wt = 2.0,              " >> eq1.in
echo "  restraintmask = ':1-1027@C,CA,N,O|:1028-1034&!@H='," >> eq1.in ## change based on res numbering from crystal_dry.pdb
echo "  nmropt = 1,                                  " >> eq1.in
echo " /                                             " >> eq1.in
echo " &wt TYPE='TEMP0', istep1=0, istep2=1000000,   " >> eq1.in
echo " value1=0.0, value2=300.0, /                   " >> eq1.in
echo " &wt TYPE='END' /                              " >> eq1.in

echo "2ns equilibration in NPT at high restraint     " >  eq2.in
echo " &cntrl                                        " >> eq2.in
echo "  imin   = 0, irest = 1, ntx = 5,              " >> eq2.in
echo "  ntc    = 2, ntf = 2,                         " >> eq2.in
echo "  cut    = 8.0,                                " >> eq2.in
echo "  ntt    = 3, gamma_ln = 5.0,                  " >> eq2.in
echo "  tempi  = 300.0, temp0  = 300.0,              " >> eq2.in
echo "  ntb    = 2, ntp = 1, barostat = 2, taup=5.0, " >> eq2.in
echo "  pres0  = 1.0,                                " >> eq2.in
echo "  iwrap  = 1,                                  " >> eq2.in
echo "  ig     = -1,                                 " >> eq2.in
echo "  ioutfm = 1,                                  " >> eq2.in
echo "  nstlim = 1000000, dt = 0.002,                " >> eq2.in
echo "  ntpr   = 25000, ntwx = 25000, ntwr = 25000,  " >> eq2.in
echo "  ntr    = 1,	restraint_wt = 2.0,              " >> eq2.in
echo "  restraintmask = ':1-1027@C,CA,N,O|:1028-1034&!@H='," >> eq2.in ## change based on res numbering from crystal_dry.pdb
echo " /                                             " >> eq2.in

echo "2ns equilibration in NPT at low restraint      " >  eq3.in
echo " &cntrl                                        " >> eq3.in
echo "  imin   = 0, irest = 1, ntx = 5,              " >> eq3.in
echo "  ntc    = 2, ntf = 2,                         " >> eq3.in
echo "  cut    = 8.0,                                " >> eq3.in
echo "  ntt    = 3, gamma_ln = 5.0,                  " >> eq3.in
echo "  tempi  = 300.0, temp0  = 300.0,              " >> eq3.in
echo "  ntb    = 2, ntp = 1, barostat = 2, taup=5.0, " >> eq3.in
echo "  pres0  = 1.0,                                " >> eq3.in
echo "  iwrap  = 1,                                  " >> eq3.in
echo "  ig     = -1,                                 " >> eq3.in
echo "  ioutfm = 1,                                  " >> eq3.in
echo "  nstlim = 1000000, dt = 0.002,                " >> eq3.in
echo "  ntpr   = 25000, ntwx = 25000, ntwr = 25000,  " >> eq3.in
echo "  ntr    = 1, restraint_wt = 0.5,              " >> eq3.in
echo "  restraintmask = ':1-1027@C,CA,N,O|:1028-1034&!@H='," >> eq3.in ## change based on res numbering from crystal_dry.pdb
echo " /                                             " >> eq3.in

echo "100ns production in NPT                        " >  prod.in
echo " &cntrl                                        " >> prod.in
echo "  imin   = 0, irest = 1, ntx = 5,              " >> prod.in
echo "  ntc    = 2, ntf = 2,                         " >> prod.in
echo "  cut    = 8.0,                                " >> prod.in
echo "  ntt    = 3, gamma_ln = 5.0,                  " >> prod.in
echo "  tempi  = 300.0, temp0 = 300.0,               " >> prod.in
echo "  ntb    = 2, ntp = 1, barostat = 2, taup=5.0, " >> prod.in
echo "  pres0  = 1.0,                                " >> prod.in
echo "  iwrap  = 1,                                  " >> prod.in
echo "  ig     = -1,                                 " >> prod.in
echo "  ioutfm = 1,                                  " >> prod.in
echo "  nstlim = 50000000, dt = 0.002,               " >> prod.in
echo "  ntpr   = 25000, ntwx = 25000, ntwr = 25000,  " >> prod.in
echo " /                                             " >> prod.in

echo "#!/bin/bash" >protocol.sh
echo "#SBATCH --job-name=$1" >>protocol.sh
echo "#SBATCH --mail-user=$2" >>protocol.sh
echo "#SBATCH --mail-type=BEGIN,END,FAIL" >>protocol.sh
echo "#SBATCH --output=/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/$1/logs/prod.log" >>protocol.sh
echo "#SBATCH --partition=gpu" >>protocol.sh
echo "#SBATCH --mem-per-gpu=2g" >>protocol.sh
echo "#SBATCH --gres=gpu:1" >>protocol.sh
echo "#SBATCH --account=maom0" >>protocol.sh
echo "#SBATCH --time=9-00:00:00" >>protocol.sh
echo "module restore " >>protocol.sh
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH                                                                " >>  protocol.sh
echo "export AMBERHOME=/sw/pkgs/coe/c/amber/22                                                                        " >> protocol.sh
echo "                                                                                                                    " >> protocol.sh

echo "$AMBERHOME/bin/pmemd.cuda -O -i min.in  -o min.out   -p *prmtop -c *.inpcrd -r min.rst   -x min.nc   -ref *.inpcrd  " >> protocol.sh
echo "                                                                                                                    " >> protocol.sh
echo "$AMBERHOME/bin/pmemd.cuda -O -i eq1.in  -o eq1.out   -p *prmtop -c min.rst  -r eq1.rst   -x eq1.nc   -ref min.rst   " >> protocol.sh
echo "                                                                                                                    " >> protocol.sh
echo "$AMBERHOME/bin/pmemd.cuda -O -i eq2.in  -o eq2.out   -p *prmtop -c eq1.rst  -r eq2.rst   -x eq2.nc   -ref eq1.rst   " >> protocol.sh
echo "                                                                                                                    " >> protocol.sh
echo "$AMBERHOME/bin/pmemd.cuda -O -i eq3.in  -o eq3.out   -p *prmtop -c eq2.rst  -r eq3.rst   -x eq3.nc   -ref eq2.rst   " >> protocol.sh
echo "                                                                                                                    " >> protocol.sh
echo "$AMBERHOME/bin/pmemd.cuda -O -i prod.in -o prod1.out -p *prmtop -c eq3.rst  -r prod1.rst -x prod1.nc                " >> protocol.sh

for (( i=2; i<=2; i++ ))
do 
((j=i-1))
echo "$AMBERHOME/bin/pmemd.cuda -O -i prod.in -o prod${i}.out -p *prmtop -c prod${j}.rst -r prod${i}.rst -x prod${i}.nc                " >> protocol.sh
done

#qsub -cwd -q teslak40c_gpu.q protocol.sh
