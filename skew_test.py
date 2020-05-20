# -*- coding: utf-8 -*-
# Created on Tue May 19 09:17:54 2020

# @author: egill

import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew, skewtest

sys.path.append("/Users/egill/Desktop/CHILDdb/")


# weight = pd.read_csv("/Users/egill/Desktop/CHILDdb/CHILD_all_weights_outliers.csv")
# height = pd.read_csv("/Users/egill/Desktop/CHILDdb/CHILD_all_heights_outliers.csv")
# diastolic = pd.read_csv("/Users/egill/Desktop/CHILDdb/CHILD_diastolic_outliers.csv")
# systolic = pd.read_csv("/Users/egill/Desktop/CHILDdb/CHILD_systolic_outliers.csv")
# pulse = pd.read_csv("/Users/egill/Desktop/CHILDdb/CHILD_pulse_outliers.csv")


def plot_subset_5(df):
    df = df[df["outlier"] == False]
    df["age_years"] = df["age_in_days"] / 365
    df5 = df[round(df["age_years"]) == 5]
    bins = round(df5["age_years"]).nunique() * 20
    plt.hist(df5["age_years"], bins=bins)
    plt.xlabel('Age in Years')
    plt.ylabel('Number')
    histageplotname = filename.replace('.csv', '_age5histage.png')
    plt.savefig(histageplotname, format="png")
    plt.show()
    plt.hist(df5["value"], bins=20)
    plt.xlabel('Value')
    plt.ylabel('Number')
    histvalueplotname = filename.replace('.csv', '_age5histvalue.png')
    plt.savefig(histvalueplotname, format="png")
    plt.show()
    plt.plot(df5["age_years"], df5["value"], "o")
    plt.xlabel('Age in Years')
    plt.ylabel('Value')
    dotplotname = filename.replace('.csv', '_age5dotplot.png')
    plt.savefig(dotplotname, format="png")
    plt.show()
    plt.violinplot(df5["value"])
    plt.ylabel('Value')
    plt.xticks([])
    violinplotname = filename.replace('.csv', '_age5violinplot.png')
    plt.savefig(violinplotname, format="png")
    plt.show()
    print('\nSkewness for data : ', skew(df5["value"]))
    print('\n0 : normally distributed.')
    print('\n> 0 : more weight in left tail.')
    print('\n< 0 : more weight in right tail.')
    result = skewtest(df5["value"])
    # print(result[1])
    if result[1] <= 0.05:
        print('\nData are significantly skewed.')
    else:
        print('\nSkewness of data is not significant.')
    df_cov = df5[['age', 'value']]
    corr = df_cov.corr()
    print(corr)


# get user input : filname to analyze
filename = input("\n\nEnter the path to a csv file containing data you would like to analyze for skewness.\n\n")

# open file
data = pd.read_csv(filename)

# analyze data in file
plot_subset_5(data)

