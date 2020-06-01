# -*- coding: utf-8 -*-
# Created on Tue May 19 09:17:54 2020

# @author: egill

import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew, skewtest

sys.path.append("/Users/egill/Desktop/CHILDdb/")


def age5_df(df):
    df5 = df[df["age_rounded"] == 1]
    return df5


def plot_value_hist(df, filename):
    plt.hist(df["value"], bins=20)
    plt.xlabel('Value')
    plt.ylabel('Number')
    histvalueplotname = filename.replace('.csv', '_age5histvalue.png')
    plt.savefig(histvalueplotname, format="png")
    plt.show()


def plot_dotplot(df, filename):
    plt.plot(df["age"], df["value"], "o")
    plt.xlabel('Age in Years')
    plt.ylabel('Value')
    dotplotname = filename.replace('.csv', '_age5dotplot.png')
    plt.savefig(dotplotname, format="png")
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
        line1 = "skewness = " + str(sk) + "\n"
        line2 = "significance = p " + str(result[1]) + "\n"
        skewfilename = filename.replace('.csv', '_skewtestresults.txt')
        with open(skewfilename, 'w') as file:
            file.writelines([line1, line2])


def calculate_cov(df, filename):
    df_cov = df[['age', 'value']]
    corr = df_cov.corr()
    print(corr)
    covfilename = filename.replace('.csv', '_covariancetestresults.txt')
    line3 = "correlation of data with age = " + "\n" + str(corr) + "\n"
    with open(covfilename, 'w') as file:
        file.write(line3)
