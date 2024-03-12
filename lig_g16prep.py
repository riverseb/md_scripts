# Authors: @riverseb
import argparse
from pymol import cmd, finish_launching
import subprocess

# extracts ligand pose from input pdb file and saves as mol2 file
def extract_lig_pose(inputPDB, lig_name3):
    cmd.load(inputPDB, "input")
    # select ligand based on 3 letter code
    cmd.select("ligand", f"input and resn {lig_name3}")
    # save as mol2
    cmd.save(f"{lig_name3}.mol2", "ligand")

# uses openbabel to convert mol2 to com
def mol2_to_com(lig_name3, obabel='obabel'):
    mol2_file = f"{lig_name3}.mol2"
    com_file = f"{lig_name3}.com"
    # executes obabel executable with mol2 file as input and com file as output
    with open("obabel.out", "w") as out:
        subprocess.run([obabel, "-imol2", mol2_file, "-ocom", "-O", com_file, "-xb", "-xk%test\n%test2"], encoding="utf-8", 
                   stdout=out)

# adds freeze option to all non-H atoms
def edit_mol_specs(mol_specs):
    frz_mol_specs = []
    # loops over each atom in the parsed molecule specifications list
    for atom in mol_specs:
        # split atom line into atom name, x, y, z coords
        atomName, x, y, z = atom.split()
        # add freeze option to non-H atoms and append new lines to frz_mol_specs
        if atomName != "H":
            frz_mol_specs.append("\t".join([atomName, "-1",x, y, z]))
        else:
            frz_mol_specs.append(atom.strip())
    return frz_mol_specs

# reads in com file and parses out molecule specifications and bond information
def split_mol_specs_bonds(lig_name3):
    # read lines after Link0, route, name, and charge multi line
    with open(f"{lig_name3}.com", "r") as input:
        lines = input.readlines()[6:]
    
    specs_bonds_split = []
    buffer = []
    # loops over lines in molecule specifications and looks for new line char that separates specifications from bonds
    for line in lines:
        # once new line char is found, append buffer to specs_bonds_split and clear buffer
        if line == "\n":
            if buffer:
                specs_bonds_split.append(buffer)
                buffer = []
        else:
            buffer.append(line)
    # append last buffer to specs_bonds_split
    if buffer:
        specs_bonds_split.append(buffer)
    # split specs_bonds_split into mol_specs and bonds
    mol_specs, bonds = specs_bonds_split 
    return mol_specs, bonds

# takes converted com file and freezes all non-H atoms and formats with route0, route1, Link0, Link1, charge, multiplicity
def prepare_g16_input(lig_name3, route0="opt b3lyp/6-31g(d) geom=connectivity", 
                      route1="hf/6-31g(d) SCF=tight Test Pop=MK iop(6/33=2) geom=connectivity",
                        charge=0, mult=1, Link0="%nprocshared=8 %mem=800MB",
                        Link1="%nprocshared=8 %mem=800MB %NoSave"):

    with open(f"formatted_{lig_name3}.com", "w") as input:
        # create list from Link0 string arg
        link0_list = Link0.split()
        # loop over Link0 list and write each line
        for i in range(len(link0_list)):
            input.write(link0_list[i] + "\n")
        input.write(f"%chk={lig_name3}_ESP.chk\n")
        # write route0 and include new line after
        input.write(f"# {route0}\n\n")
        # write molecule name
        input.write(f"{lig_name3}\n\n")
        # write charge and multiplicity
        input.write(f"{charge} {mult}\n") 
        # get molecule specifications and bond information from com file
        mol_specs, bonds = split_mol_specs_bonds(lig_name3)
        # add freeze option to all non-H atoms
        frz_mol_specs = edit_mol_specs(mol_specs)
        # write molecule specifications
        for line in frz_mol_specs:
            input.write(f"{line}\n")
        # new line to separate molecule specifications from bonds
        input.write("\n")
        # write bond information
        for line in bonds:
            # bond lines already contain new line chars
            input.write(line)
        # new line to separate bonds from Link1
        input.write("\n")
        input.write("--Link1--\n")
        # create list from Link1 string arg
        link1_list = Link1.split()
       # loop over Link1 list and write each line
        for i in range(len(link1_list)):
            input.write(link1_list[i] + "\n")
        input.write(f"%chk={lig_name3}_ESP.chk\n")
        # write route1
        input.write(f"# {route1}\n\n")
        input.write(f"{lig_name3}_ESP_calc\n\n")
        input.write(f"{charge} {mult}\n")
        input.write("\n")

def main(lig_name3, inputPDB, route0="opt b3lyp/6-31g(d) Geom=connectivity", 
                      route1="hf/6-31g(d) SCF=tight Test Pop=MK iop(6/33=2) Geom=Check",
                        charge=0, mult=1, Link0="%nprocshared=8 %mem=800MB",
                        Link1="%nprocshared=8 %mem=800MB %NoSave", obabel="obabel"):
    extract_lig_pose(inputPDB, lig_name3)
    mol2_to_com(lig_name3, obabel)
    prepare_g16_input(lig_name3, route0, route1, charge, mult, Link0, Link1)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("lig_name3", help="ligand 3 letter code")
    argparser.add_argument("inputPDB", help="input PDB file")
    argparser.add_argument("--route0", default="opt b3lyp/6-31g(d) Geom=connectivity")
    argparser.add_argument("--route1", default="hf/6-31g(d) SCF=tight Test Pop=MK iop(6/33=2) Geom=Check")
    argparser.add_argument("--charge", type=int, default=0)
    argparser.add_argument("--mult", type=int, default=1)
    argparser.add_argument("--Link0", default="%nprocshared=8 %mem=800MB")
    argparser.add_argument("--Link1", default="%nprocshared=8 %mem=800MB %NoSave")
    argparser.add_argument("--obabel", default="obabel", help="path to obabel executable")
    args = argparser.parse_args()
    
    main(**vars(args))

        