# Authors: @riverseb
import sys
import pandas as pd
import plot_utils as pu

def main(data_file):
    df = pd.read_csv(data_file, delim_whitespace=True, header=0) #dataframe for data
    pu.scatter3d_plot(df, x="DH1", y="DH2", z="DH3", c="E_MPC[total]")
    # pu.metric_vs_time(df, column="DH1")
    # pu.metric_vs_time(df, column="DH2")
    # pu.metric_vs_time(df, column="DH3")
    # pu.metric_vs_time(df, column="E_MPC[total]")
    pu.line_multimetric_vs_time(df)

if __name__ == "__main__":
    main(sys.argv[1])