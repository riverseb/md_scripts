#Authors: @dsanper
import matplotlib.pyplot as plt
import pandas as pd

df =pd.read_csv("pca_labels_metrics.dat")

#red=syn
#blue=anti

# Grouping by the 'Label_color_DH' column
grouped = df.groupby('Label_color_DH')

# Plot each group individually
fig, ax = plt.subplots()


###########################################################################################
# make a plot with everything over lapped try statements are used incase any of the 4 demoninations is not present amongst the frames

try:
    grey_group = grouped.get_group('Grey')
    ax.scatter(grey_group["PCA1"], grey_group["PCA2"], label=f"In between (n={len(grey_group)})", color='grey',marker='.', alpha=0.2)    #50% translucent
except KeyError:
    print("Grey group not found. Means there a no frames the label wizard could not label")

try:
    green_group = grouped.get_group('Green')
    ax.scatter(green_group["PCA1"], green_group["PCA2"], label=f"too far(n={len(green_group)})", color='green', marker='.', alpha=0.2) #50% translucent
except KeyError:
    print("Green group not found. Means there are no frames in which the distances are greater then 4 A ")

try:
    red_group = grouped.get_group('Red')
    ax.scatter(red_group["PCA1"], red_group["PCA2"], label=f"syn(n={len(red_group)})", color='red',marker='.',alpha=0.4)
except KeyError:
    print("Red group not found. Means there are no frames in which the molecule was syn ")

try:
    blue_group = grouped.get_group("Blue")
    ax.scatter(blue_group["PCA1"], blue_group["PCA2"], label=f"anti(n={len(blue_group)})", color='blue',marker='.',alpha=0.4)
except KeyError:
    print("Blue group not found.  Means there are no frames in which the molecule was anti")


ax.set_xlabel('PCA1') 
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca.png')


###########################################################################################
#plotting all groups vs frame 
fig, ax = plt.subplots()
scatter =ax.scatter(df["PCA1"], df["PCA2"], c=df["#Frame"], marker='.',cmap='viridis' ,alpha=0.8)
plt.colorbar(scatter, label='Frame')
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_frame.png')

###########################################################################################
#plotting syn vs DH1
fig, ax = plt.subplots()
scatter =ax.scatter(red_group["PCA1"], red_group["PCA2"], c=red_group["DH1"],label=f"syn(n={len(red_group)})",marker='.',cmap='viridis' ,alpha=0.8)
colorbar = plt.colorbar(scatter, label='DH1', extend='both')
colorbar.set_ticks([-160,-120,-80,-40,0,40,80,120,160])
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_syn_DH1.png')

#plotting anti vs DH1
fig, ax = plt.subplots()
scatter =ax.scatter(blue_group["PCA1"], blue_group["PCA2"], c=blue_group["DH1"],label=f"anti(n={len(blue_group)})", marker='.',cmap='viridis' ,alpha=0.8)
colorbar = plt.colorbar(scatter, label='DH1', extend='both')
colorbar.set_ticks([-160,-120,-80,-40,0,40,80,120,160])
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend() 
fig.savefig('DH_pca_anti_DH1.png')






###########################################################################################
#plots syn and anti individually
fig, ax = plt.subplots()
scatter =ax.scatter(red_group["PCA1"], red_group["PCA2"], label=f"syn(n={len(red_group)})", color='red', marker='.', alpha=0.8)
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_syn.png')

fig, ax = plt.subplots()
scatter =ax.scatter(blue_group["PCA1"], blue_group["PCA2"], label=f"anti(n={len(blue_group)})", color='blue', marker='.', alpha=0.8)
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_anti.png')

"""""#plot syn and anti vs total energy of dienophile DH1
###########################################################################################

fig, ax = plt.subplots()
scatter =ax.scatter(red_group["PCA1"], red_group["PCA2"], label=f"syn(n={len(red_group)})", c=red_group["E_DH1[total]"], marker='.',cmap='viridis', alpha=0.8)
plt.colorbar(scatter, label='Total Energy of Dienophile')
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_syn_E_dienophile.png')


fig, ax = plt.subplots()
scatter =ax.scatter(blue_group["PCA1"], blue_group["PCA2"], label=f"anti(n={len(blue_group)})", c=blue_group["E_DH1[total]"], marker='.',cmap='viridis', alpha=0.8)
plt.colorbar(scatter, label='Total Energy of Dienophile')
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_anti_E_dieneophile.png')
"""

"""" #plot syn and anti vs total energy of diene DH2
###########################################################################################

fig, ax = plt.subplots()
scatter =ax.scatter(red_group["PCA1"], red_group["PCA2"], label=f"syn(n={len(red_group)})", c=red_group["E_DH2[total]"], marker='.',cmap='viridis', alpha=0.8)
plt.colorbar(scatter, label='Total Energy of Diene')
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_syn_E_diene.png')


fig, ax = plt.subplots()
scatter =ax.scatter(blue_group["PCA1"], blue_group["PCA2"], label=f"anti(n={len(blue_group)})", c=blue_group["E_DH2[total]"], marker='.',cmap='viridis', alpha=0.8)
plt.colorbar(scatter, label='Total Energy of Diene')
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_anti_E_diene.png')
"""

"""" #plot syn and anti vs total frame number
###########################################################################################
  
fig, ax = plt.subplots()
scatter =ax.scatter(red_group["PCA1"], red_group["PCA2"], label=f"syn(n={len(red_group)})", c=red_group["#Frame"], marker='.',cmap='viridis', alpha=0.8)
plt.colorbar(scatter, label='Frame number')
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_syn_frame.png')


fig, ax = plt.subplots()
scatter =ax.scatter(blue_group["PCA1"], blue_group["PCA2"], label=f"anti(n={len(blue_group)})", c=blue_group["#Frame"], marker='.',cmap='viridis', alpha=0.8)
plt.colorbar(scatter, label='Frame Number')
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_anti_frame.png')
"""
print("RMSD NOW")
#plot syn and anti vs rmsd
###########################################################################################

fig, ax = plt.subplots()
scatter =ax.scatter(red_group["PCA1"], red_group["PCA2"], label=f"syn(n={len(red_group)})", c=red_group["rmsd"], marker='.',cmap='viridis', alpha=0.8)
plt.colorbar(scatter, label='Rmsd')
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_syn_rmsd.png')


fig, ax = plt.subplots()
scatter =ax.scatter(blue_group["PCA1"], blue_group["PCA2"], label=f"anti(n={len(blue_group)})", c=blue_group["rmsd"], marker='.',cmap='viridis', alpha=0.8)
plt.colorbar(scatter, label='Rmsd')
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_ylim(-150,150) 
ax.set_xlim(-250, 250) 
ax.legend()
fig.savefig('DH_pca_anti_rmsd.png')

