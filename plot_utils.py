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
def metric_vs_time(df, column, ymin=0, ymax=380):
    plt.figure(figsize=(6,6))
    df_offset = df.iloc[::5]
    ax = sns.lineplot(data=df, x="Frame", y=column)
    plt.xlabel("Time (ns)", fontsize=15)
    plt.ylabel(f"{column}", fontsize=15)
    plt.tick_params(labelsize=15)
    plt.title(f"{column} vs Time", fontsize=20, pad=10)
    plt.ylim(ymin, ymax)  # Force y-axis to be from ymin to ymax
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
    plt.savefig("DH1-3_vs_time_multi.png", dpi=300)
def subset_mean_std(df, subset, name):
    """
    Usage: calculates the mean and std for metrics in a subset of the dataframe

    :param df: dataframe
    :param subset: subset of the dataframe
    :param name: name of the subset
    """
    start, stop = subset.split(",")
    start = int(start)
    stop = int(stop)
    start = start * 20 # converts time to index
    stop = stop * 20 # converts time to index
    df_subset = df[start:stop]
    mean_array = df_subset.mean()
    std_array = df_subset.std()
    # calculate lower and upper bounds
    lower_bound = mean_array - std_array * 2 
    upper_bound = mean_array + std_array * 2
    df_filtered_subset = df_subset[(df_subset >= lower_bound) & (df_subset <= upper_bound)] # filter out outliers
    filt_means = df_filtered_subset.mean()
    filt_stds = df_filtered_subset.std()
    mean_std_df = mean_array.to_frame(name="mean")
    mean_std_df["std"] = std_array
    mean_std_df["lower_bound"] = lower_bound
    mean_std_df["upper_bound"] = upper_bound
    mean_std_df["filt_mean"] = filt_means
    mean_std_df["filt_std"] = filt_stds
    mean_std_df["filt_lower_bound"] = filt_means - filt_stds * 2
    mean_std_df["filt_upper_bound"] = filt_means + filt_stds * 2
    mean_std_df.to_csv(f"{name}_mean_std.csv", sep="\t")
    return mean_std_df
def scatter_plot(df, x, y, style=None, hue=None):
    fig = plt.figure(figsize=(10,6))
    # TODO: make a variable for a label list
    ax = sns.scatterplot(data=df, x=x, y=y, style=style, hue=hue, palette="Set2", 
                        legend="brief", hue_order=["\u03B1-anti", "\u03B1-syn", "unprod_conf1", "unprod_conf2", "Other"],
                        style_order=["\u03B1-anti", "\u03B1-syn", "unprod_conf1", "unprod_conf2", "Other"])
    label_counts = df[hue].value_counts()
    print(label_counts)
    ax.set_xlabel(x, fontsize=20)
    ax.set_ylabel(y, fontsize=20)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(labels=["\u03B1-anti n={})".format(label_counts['\u03B1-anti']), 
                      "\u03B1-syn (n={})".format(label_counts['\u03B1-syn']), 
                      "unprod_conf1 (n={})".format(label_counts['unprod_conf1']), 
                      "unprod_conf2 (n={})".format(label_counts['unprod_conf2']), 
                      "Other (n={})".format(label_counts['Other'])],loc="upper left", bbox_to_anchor=(1, 1))
    ax.set_title(f'{x} vs {y}', fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=15)
    plt.savefig(f'{x} vs {y}.png', dpi=300)