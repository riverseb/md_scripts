#Authors: @Daniel-Chem
import MDAnalysis as md
import sys 
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def label_wizard(df_inp): #as it is, the code first gives a number value and then i convert it to a string containing the name of the color realistically i can just assign the color directly 
    if df_inp["ZWP_ZWP1"]>=4 and df_inp["ZWP_ZWP2"]>=4:
        return "Green" #it is outside of range of interest
    
    elif df_inp["DH1"] >=0 and df_inp["ZWP_ZWP1"]<=4 and df_inp["ZWP_ZWP2"]<=4: #and df_inp["DH2"] >= 0:  #DH1 is the dienophile
        return "Red" #syn on the right side of the plot within 4 A
    
    elif df_inp["DH1"] <=0 and df_inp["ZWP_ZWP1"]<=4 and df_inp["ZWP_ZWP2"]<=4: #and df_inp["DH2"] >= 0:  #DH2 is the diene 
        return "Blue" #anti on the right side of the plot within 4 A
    
    else:
        return "Grey" #grey would encapsulate incorrect dihedrals that are within the binding bocket 

"""
Function expect to be run with df["Column_title"] = df.apply(label_wizard,axis=1) which applies the function to every row and creates a new col
this function checks the DH1 and DH2 col in the input data frame (the data frame does not have to be in any order but must have the same col title as the function) 
it assigns labels based on color, red = syn, anti = blue, green = too far (are not plotted in the DH plots)
grey is a catch all in place for when none of the previous conditions are met
"""

#input files
pdb_dry  = "/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene/PMC_lig/exp2/rep3/plots_data/crystal_dry_PMC_lig.pdb" #path to the pdb dry
cords_nc = "/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene/PMC_lig/exp2/rep3/plots_data/cords.nc" #path to the cords.nc that is given by cpptraj
raw_metric = "/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene/PMC_lig/exp2/rep3/plots_data/raw_metrics.dat" #path to raw_metrics.dat
En_DH1 = "/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene/PMC_lig/exp2/rep3/plots_data/E_DH1.dat" #path to E_DH1
En_DH2 = "/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene/PMC_lig/exp2/rep3/plots_data/E_DH2.dat" #path to E_DH1


u= md.Universe(pdb_dry,cords_nc) #First argument is the crystal_dry pdb that corresponds to the production the second is the nc file

ag = u.atoms.select_atoms('resname MPC') #filter to only scan through the residue named ZWP 




data_list = [] #empty list that gets turned into the pandas data frame


for ts in u.trajectory: #loops through every frame 
    for atom in  ag: #loops through every atom in the filter ag 
        data_list.append({
            "Frame": ts.frame,
            "Atom Name": atom.name,
            "Coordinates": atom.position }) #appends the frame, atom name and position as a dictionary that gets added to data_list
        

df = pd.DataFrame(data_list) #creates data frame from the dictionary 
df.to_csv("coords.dat",index=False)

coords = df["Coordinates"].tolist() #convert the coordinates column into a list each item is an array
coords2 = np.stack(coords)          #turns the list of arrays into a stacked column with size [40k,3]
coords3 = coords2.reshape(4000,165) #reshapes it such that each row is a frame and each column is an individual coordinate first number must be total number of frames, the second has to be the number of atoms in residue * 3 
np.savetxt('coords.csv', coords3, delimiter=',') #compare coords.dat with coords.csv and make sure the cords of the first and final atoms of frame are correct

pca = PCA(n_components=2) #states the PCA will have two compononets
pca.fit(coords3) #fits the coords 3 for pca 
PCA(n_components=2)
transformed_data = pca.transform(coords3) #does the actual PCA


df2 = pd.read_csv(raw_metric,delim_whitespace=True) #reads the raw_metrics.dat
df3 = pd.read_csv(En_DH1,delim_whitespace=True)
df4 = pd.read_csv(En_DH2,delim_whitespace=True)

df2["PCA1"] = transformed_data[:, 0] #adds a column to the data frame consisting of the first column of transformed_data array aka PCA1
df2["PCA2"] = transformed_data[:, 1] #adds a column to the data frame consisting of the second column of transformed_data array aka PCA2
df2["E_DH1[total]"]=df3["E_DH1[total]"]
df2["E_DH2[total]"]=df4["E_DH2[total]"]


#runs the function on every row and adds the output as its own column 
df2["Label_color_DH"] = df2.apply(label_wizard,axis=1)

#exports all the values right before the PCA happens
df2.to_csv("pca_labels_metrics.dat",index=False)

