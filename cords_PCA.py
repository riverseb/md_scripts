#Authors: @Daniel-Chem
import MDAnalysis as md
import sys 
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def label_wiz(df_inp): #as it is, the code first gives a number value and then i convert it to a string containing the name of the color realistically i can just assign the color directly 
    if df_inp["DH1"] >=0 and df_inp["ZWP_ZWP1"]<=4 and df_inp["ZWP_ZWP2"]<=4 and df_inp["DH2"] >= 0:
        return "Red" #syn on the right side of the plot within 4 A
    if df_inp["DH1"] <=0 and df_inp["ZWP_ZWP1"]<=4 and df_inp["ZWP_ZWP2"]<=4 and df_inp["DH2"] >= 0:
        return "Blue" #anti on the right side of the plot within 4 A
    if df_inp["ZWP_ZWP1"]>=4 and df_inp["ZWP_ZWP2"]>=4:
        return "Green" #it is outside of range of interest
    else:
        return "Grey" #grey would encapsulate incorrect dihedrals that are within the binding bocket 
    


pdb_dry = "/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene/rep3/crystal_wat_Ctdp_mono_diene.pdb"
cords_nc = "/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene/rep3/PCA/cords.nc"

u= md.Universe(pdb_dry,cords_nc) #First argument is the crystal_dry pdb that corresponds to the production the second is the nc file
#u= md.Universe(sys.argv[1],sys.argv[2])

ag = u.atoms.select_atoms('resname ZWP') #filter to only scan through the residue named ZWP 

data_list = [] #empty list that gets turned into the pandas data frame

for ts in u.trajectory: #loops through every frame 
    for atom in  ag: #loops through every atom in the filter ag 
        data_list.append({
            "Frame": ts.frame,
            "Atom Name": atom.name,
            "Coordinates": atom.position }) #appends the frame, atom name and position as a dictionary that gets added to data_list
        

df = pd.DataFrame(data_list) #creates data frame
#df[['Frame', 'Atom Name', 'Coordinates']].to_csv("cords_test_pca.csv", index=False,) #exports a csv of the data frame

coords = df["Coordinates"].tolist()
coords2 = np.stack(coords)
coords3 = coords2.reshape(4000,150) 




#np.savetxt("coords3.csv", coords3, delimiter=",") #uncomment this to export the array that gets fed into the pca for checking purposses

pca = PCA(n_components=2)
pca.fit(coords3)
PCA(n_components=2)


transformed_data = pca.transform(coords3)
df2 = pd.read_csv("/nfs/turbo/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene/rep3/PCA/raw_metrics.dat",delim_whitespace=True)
df2["PCA1"] = transformed_data[:, 0]
df2["PCA2"] = transformed_data[:, 1]

df2["Label_color_DH"] = df2.apply(label_wiz,axis=1) #runs the function on every row 

df2.to_csv("metrics.pca.csv",index=False)
quit()




array =df2[["PCA1","PCA2","Label_color_DH"]].to_numpy()


# Access the first column (index 0) and assign it to a variable
xs = array[:, 0] 


# Access the second column (index 1) and assign it to a variable
ys = array[:, 1]

# Access the third column (index 2) and assign it to a variable
lbls_dh = array[:, 2]


plt.scatter(xs, ys, c=lbls_dh) #makes an x y scatter and assign color based on the colors that were assigned 
plt.xlabel('PCA1') #makes the x axis called pca1
plt.ylabel('PCA2') #makes the y axis called pca2
plt.savefig('scatter_plot.png')

#find how to make colors outside of syn / anti translucent 

















# Plot the transformed data
#plt.scatter(transformed_data[:, 0], transformed_data[:, 1])
#plt.xlabel('Principal Component 1')
#plt.ylabel('Principal Component 2')
#plt.title('PCA Plot')
#plt.savefig("PCA_PLOT_TRY_1")

