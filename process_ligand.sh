cd $1 $2

antechamber -i formatted_$1.log -fi gout -o $1.mol2 -fo mol2 -c resp -rn $1 -pf y -s 2 -nc $2 -at gaff
parmchk2 -i $1.mol2 -f mol2 -o $1.frcmod -s gaff

echo "source leaprc.gaff"                 > tleap.in
echo "$1 = loadmol2 $1.mol2"             >> tleap.in
echo "loadamberparams $1.frcmod"         >> tleap.in
echo "saveoff $1 $1.lib"                 >> tleap.in
echo "savepdb $1 $1.pdb"                 >> tleap.in
echo "quit"                              >> tleap.in

tleap -f tleap.in

rm tleap.in esout punch qout leap.log
