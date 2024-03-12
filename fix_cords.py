#Authors: @dsanper086
import MDAnalysis as md
import pandas as pd

pdb_dry = "/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene_F277A/rep3/crystal_dry_Ctdp_mono_diene_F277A.pdb"
cords_nc = "/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene_F277A/rep1/plots_data/frames.nc"

u = md.Universe(pdb_dry, cords_nc)

ag = u.atoms.select_atoms('resname ZWP')

data_dict = {"Frame": [], "Atom Name": []}
for ts in u.trajectory:
    data_dict["Frame"].extend([ts.frame] * len(ag))
    data_dict["Atom Name"].extend([atom.name for atom in ag])
    for atom in ag:
        data_dict.setdefault(f"Coordinates_{atom.name}", []).append(atom.position)

df = pd.DataFrame(data_dict)

# Pivot the DataFrame
pivot_df = df.pivot_table(index=['Frame', 'Atom Name'], aggfunc='first').reset_index()

# Save to CSV
pivot_df.to_csv("cords_F277A.csv", index=False)