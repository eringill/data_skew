# Created on Tue May 19 09:17:54 2020

# @author: egill

import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew, skewtest
import calc_outliers as o
import skew_test as s

sys.path.append("/Users/egill/Desktop/CHILDdb/")


# functions
def get_filename():
    print("\n\nEnter the path to a csv file containing data you would like to analyze for skewness.\n\n")
    filename = input()
    if filename == "" or filename == "\n" or filename is None:
        filename = "/Users/egill/Desktop/CHILDdb/CHILD_all_weights_outliers.csv"
    return(filename)


# get user input : filname to analyze
filename = get_filename()

# open file
data = pd.read_csv(filename)

data = o.add_age(data)

min_a = o.min_age(data)

data_split = o.split_by_age(data)

data_stats = o.calc_stats(data_split, data)

stats_merged = o.merge_stats(data_split, data_stats)

data_outliers = o.mark_outliers(stats_merged)

data_z_scores = o.mod_z_score(data_outliers)

data_output = o.df_append(data_z_scores)

no_outliers = o.remove_z_outliers(data_output)

# analyze data in file
plot_subset_5(no_outliers)
