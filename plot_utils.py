#Authors: @riverseb, @Daniel-Chem
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import numpy as np
import seaborn as sns

palette = sns.color_palette("Set2")
# code for 3d scatter plot with color 
def scatter3d_plot(df, x, y, z, c=None):
    df_offset = df.iloc[::3] # offset by 3 frames
    fig = plt.figure(figsize=(6,5), dpi=300) # generate matplotlib figure
    ax = plt.axes(projection='3d') # generate 3d axes
    ax.set_xlabel(x, fontsize=20, rotation=-15, labelpad=13)
    ax.set_ylabel(y, fontsize=20, rotation=45)
    ax.set_zlabel(z, fontsize=20, labelpad=5, rotation=90)
    # ax.yaxis.set_tick
    ax.xaxis.set_tick_params(rotation=50, pad=0.25)
    ax.yaxis.set_tick_params(rotation=-10, pad=0.25)
    # ax.zaxis.set_tick_params(rotation=15, pad=0.01)
    ax.set_title(f'{x} vs {y} vs {z}', fontsize=25, pad=1)
    ax.set_xlim(0, 380)
    ax.set_ylim(0, 380)
    ax.set_zlim(0, 380)
    ax.view_init(elev=15, azim=-60) # set viewing perspective
    ax.scatter(df_offset[x], df_offset[y], [0], color='gray')
    norm_energy = Normalize(vmin=df[c].min(), vmax=df[c].max()) # normalize colormap
    mappable = cm.ScalarMappable(norm=norm_energy, cmap=sns.color_palette("rocket", as_cmap=True)) # generate colormap
    mappable.set_array(df_offset[c]) # set data array for colormapping
    
    if c is not None:
        fig.colorbar(mappable, label="Energy (kcal/mol)", ax=ax, pad=0.1, shrink=0.8)
        ax.scatter(df_offset[x], df_offset[y], df_offset[z], c=mappable.get_array(), s=3, alpha=1, linewidths=0.5, 
                   cmap=sns.color_palette("rocket", as_cmap=True))
        # ax.legend( title="Energy (kcal/mol)")
    else:
        ax.scatter3D(df[x], df[y], df[z], s=10)
    fig.tight_layout()
    fig.savefig(f'{x} vs {y} vs {z}.png', dpi=300)

# create line plot for a single metric vs time w/ matplotlib
def metric_vs_time(df, column):
    plt.figure(figsize=(6,6))
    df_offset = df.iloc[::5]
    plt.plot(df_offset["Frame"], df_offset[column], marker='o', linestyle='-', color='black',
             markersize=4, markerfacecolor="mediumpurple", linewidth=1)
    plt.xlabel("Time (ns)")
    # plt.legend(fontsize=15)
    plt.xticks(rotation=45) # Only needed if X axis is overlapping
    plt.ylabel("DH1")
    plt.ylim(0, 380)  # Force y-axis to be from 200 to -200
    plt.savefig(f"{column}_vs_time.png", dpi=300)
# create line plot for multiple metrics vs time w/ matplotlib and seaborn
def line_multimetric_vs_time(df):
    fig = plt.figure(figsize=(10,6))
    df_subset = df.iloc[::5, 3:6]
    df_subset.insert(loc=0, column="Time", value=df["Frame"])
    df_subset.set_index("Time", inplace=True)
    ax = sns.lineplot(data=df_subset, palette="Set2")
    plt.xlabel("Time (ns)", fontsize=20)
    plt.legend(fontsize=15, loc='lower left', ncol=3)
    ax.tick_params(axis='both', which='major', labelsize=15)
    # plt.xticks(rotation=45) # Only needed if X axis is overlapping
    plt.ylabel("Dihderal (º)", fontsize=20)
    # plt.ylim(0, 380)  # Force y-axis to be from 200 to -200
    plt.savefig(f"DH1-3_vs_time_multi.png", dpi=300)
def subset_mean_std(df, subset, name):
    start, stop = subset.split(",")
    start = int(start)
    stop = int(stop)
    start = start * 20
    stop = stop * 20
    mean_array = df[start:stop].mean()
    std_array = df[start:stop].std()
    mean_std_df = mean_array.to_frame(name="mean")
    mean_std_df["std"] = std_array
    mean_std_df.to_csv(f"{name}_mean_std.csv", sep="\t")
    return mean_std_df
def scatter_plot(df, x, y, size=None, hue=None):
    plt.figure(figsize=(6,6))
    sns.scatterplot(data=df, x=x, y=y, size=size, palette="Set2")