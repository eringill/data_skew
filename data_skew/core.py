# Created on Tue May 19 09:17:54 2020

# @author: egill

import sys
import pandas as pd
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
# if "age_in_days" exists, convert to age_rounded
if "age_in_days" in data.columns:

    data = o.add_age(data)
# if "age exists, convert to age_rounded
elif "age" in data.columns:

    data = o.round_age(data)
# else set "age_rounded" to 1
else:

    data["age_rounded"] = 1

data_split = o.split_by_age(data)

data_stats = o.calc_stats(data_split, data)

stats_merged = o.merge_stats(data_split, data_stats)

data_outliers = o.mark_outliers(stats_merged)

data_z_scores = o.mod_z_score(data_outliers)

data_output = o.df_append(data_z_scores)

no_outliers = o.remove_z_outliers(data_output)

age5 = s.age5_df(no_outliers)

s.plot_value_hist(age5, filename)

if "age" in age5.columns:

    s.calculate_cov(age5, filename)

s.calculate_skew(age5, filename)



