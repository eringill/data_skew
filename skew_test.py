# -*- coding: utf-8 -*-
# Created on Tue May 19 09:17:54 2020

# @author: egill

import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew, skewtest

sys.path.append("/Users/egill/Desktop/CHILDdb/")


def age5_df(df):
    df5 = df[round(df["age"]) == 5]
    return df5


def plot_age_hist(df, filename):
    plt.hist(df["age_years"], bins=20)
    plt.xlabel('Age in Years')
    plt.ylabel('Number')
    histageplotname = filename.replace('.csv', '_age5histage.png')
    plt.savefig(histageplotname, format="png")
    plt.show()


def plot_value_hist(df, filename):
    plt.hist(df["value"], bins=20)
    plt.xlabel('Value')
    plt.ylabel('Number')
    histvalueplotname = filename.replace('.csv', '_age5histvalue.png')
    plt.savefig(histvalueplotname, format="png")
    plt.show()


def plot_dotplot(df, filename):
    plt.plot(df["age_years"], df["value"], "o")
    plt.xlabel('Age in Years')
    plt.ylabel('Value')
    dotplotname = filename.replace('.csv', '_age5dotplot.png')
    plt.savefig(dotplotname, format="png")
    plt.show()


def plot_violinplot(df, filename):
    plt.violinplot(df["value"])
    plt.ylabel('Value')
    plt.xticks([])
    violinplotname = filename.replace('.csv', '_age5violinplot.png')
    plt.savefig(violinplotname, format="png")
    plt.show()


def calculate_skew(df, filename):
    sk = skew(df["value"])
    print('\nSkewness for data : ', str(sk))
    print('\n0 : normally distributed.')
    print('\n> 0 : more weight in left tail.')
    print('\n< 0 : more weight in right tail.')
    result = skewtest(df["value"])
    # print(result[1])
    if result[1] <= 0.05:
        print('\nData are significantly skewed.')
    else:
        print('\nSkewness of data is not significant.')
    df_cov = df[['age', 'value']]
    corr = df_cov.corr()
    print(corr)
    skewfilename = filename.replace('.csv', '_skewtestresults.txt')
    with open(skewfilename, 'w') as file:
        file.write("skewness = ", str(sk), "\n")
        file.write("significance = p ", str(result[1]), "\n")
        file.write("correlation of data with age = ", str(corr), "\n")
