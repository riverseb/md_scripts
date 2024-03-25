# Authors: @riverseb
import sys
import pandas as pd
import plot_utils as pu

def cluster_label(df):
    labels=[]
    DH1 = df["DH1"]
    DH3 = df["DH3"]
    for i in range(len(DH1)):
        if 175.0 <= DH1[i] <= 260.0 and 20.0 <= DH3[i] <= 84.0:
            labels.append("\u03B1-anti")
        elif 100.0 <= DH1[i] <= 175.0 and 290.0 <= DH3[i] <= 350.5:
            labels.append("\u03B1-syn")
        elif 271.0 <= DH1[i] <= 332.0 and 296.0 <= DH3[i] <= 345.0:
            labels.append("unprod_conf1")
        elif 0.0 <= DH1[i] <= 100.0 and 20.0 <= DH3[i] <= 90.0:
            labels.append("unprod_conf2")
        # elif DH1[i] in range(116, 162) and DH3[i] in range(301, 333):
        #     labels.append("\u03B1-syn")
        # elif DH1[i] in range(271, 332) and DH3[i] in range(296, 345):
        #     labels.append("unprod_conf1")
        # elif DH1[i] in range(17, 90) and DH3[i] in range(34, 72):
        #     labels.append("unprod_conf2")
        else:
            labels.append("Other")
    return labels
def conformation_analysis():
    pass
def main(data_file):
    df = pd.read_csv(data_file, delim_whitespace=True, header=0) #dataframe for data
    df["DH1"] = df["DH1"].astype(float)
    df["DH3"] = df["DH3"].astype(float)
    df['Conf_label'] = cluster_label(df)
    print(df)
    pu.scatter_plot(df, x="DH1", y="DH3", style="Conf_label", hue="Conf_label")
    pu.scatter3d_plot(df, x="DH1", y="DH2", z="DH3", c="E_MPC[total]")
    pu.line_multimetric_vs_time(df)
    # pu.subset_mean_std(df, subset="363,497", name="alpha_syn")
    # pu.subset_mean_std(df, subset="315,1000", name="alpha_anti")
    # pu.subset_mean_std(df, subset="614,762", name="unprod_conf1")
    # pu.subset_mean_std(df, subset="4,277", name="unprod_conf2")
    pu.metric_vs_time(df, column="ZWP_NAP1", ymin=0, ymax=10)
if __name__ == "__main__":
    main(sys.argv[1])