#Authors: @riverseb, @dsanper
import sys 
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import numpy as np
import seaborn as sns
# import plotly as plty
#path = sys.argv[1] # input ZWP_DH.dat

palette = sns.color_palette("Set2")
def scatter3d_plot(df, x, y, z, c=None):
    df_offset = df.iloc[::3]
    fig = plt.figure(figsize=(6,5), dpi=300)
    ax = plt.axes(projection='3d')
    # ax_pos = [0.5, 0.5, 6, 6]
    # ax = fig.add_axes(ax_pos)
    #ax = Axes3D(fig)
    # plt.subplots_adjust(top=0.05, bottom=0.04)
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
    ax.view_init(elev=15, azim=-60)
    ax.scatter(df_offset[x], df_offset[y], [0], color='gray')
    # print(df[0])
    norm_energy = Normalize(vmin=df[c].min(), vmax=df[c].max())
    mappable = cm.ScalarMappable(norm=norm_energy, cmap=sns.color_palette("rocket", as_cmap=True))
    mappable.set_array(df_offset[c])
    
    if c is not None:
        fig.colorbar(mappable, label="Energy (kcal/mol)", ax=ax, pad=0.1, shrink=0.8)
        ax.scatter(df_offset[x], df_offset[y], df_offset[z], c=mappable.get_array(), s=3, alpha=1, linewidths=0.5, 
                   cmap=sns.color_palette("rocket", as_cmap=True))
        # ax.legend( title="Energy (kcal/mol)")
    else:
        ax.scatter3D(df[x], df[y], df[z], s=10)
    fig.tight_layout()
    fig.savefig(f'{x} vs {y} vs {z}.png', dpi=300)

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
def line_multimetric_vs_time(df):
    fig = plt.figure(figsize=(10,6))
    df_subset = df.iloc[::5, 3:6]
    df_subset.insert(loc=0, column="Time", value=df["Frame"])
    df_subset.set_index("Time", inplace=True)
    ax = sns.lineplot(data=df_subset, palette="Set2")
    
    # i = 0
    # for col in columns:
    #     plt.plot(df_offset["Frame"], df_offset[col], linestyle='-', color=palette[i], linewidth=1, marker="", label=col)
    #     i += 1
    plt.xlabel("Time (ns)", fontsize=20)
    plt.legend(fontsize=15, loc='lower left', ncol=3)
    ax.tick_params(axis='both', which='major', labelsize=15)
    # plt.xticks(rotation=45) # Only needed if X axis is overlapping
    plt.ylabel("Dihderal (º)", fontsize=20)
    # plt.ylim(0, 380)  # Force y-axis to be from 200 to -200
    plt.savefig(f"DH1-3_vs_time_multi.png", dpi=300)
def sns_multimetric_vs_time(df, *columns):
    fig = plt.figure(figsize=(10,6))
    df_offset = df.iloc[::5]
    i = 0
    for col in columns:
        sns.lineplot(x="Frame", y=col, data=df_offset, color=palette[i])
        i += 1
    plt.xlabel("Time (ns)")
    plt.legend(fontsize=15, loc='upper right', borderaxespad=5, mode="expand")
    plt.xticks(rotation=45) # Only needed if X axis is overlapping
    plt.ylabel("DH1")
    plt.ylim(0, 380)  # Force y-axis to be from 200 to -200
    plt.savefig(f"{col}_vs_time_multi.png", dpi=300)
# def plty_scatter3d(df, x, y, z, c):

# def main(data_file, *args):
#     df = pd.read_csv(data_file, delim_whitespace=True, header=0) #dataframe for data
    





# This script generates line plots for DH1 and DH2 vs time.
# Usage:
# 1. Call the script passing the file path of the dataset as the first command line argument.
# 2. Meant to be used on ZWP_DH.dat file type.
# 3. The script will automatically save the plots for the first and second data columns as 'time_DH1_line_plot.png' and 'time_DH2_line_plot.png' respectively in the current working directory.
