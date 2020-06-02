# -*- coding: utf-8 -*-
# Created on Tue May 19 09:17:54 2020

# @author: egill


import matplotlib.pyplot as plt
from scipy.stats import skew, skewtest


# select data from highest age only
def age5_df(df):
    agemax = df['age_rounded'].max()
    df5 = df[df["age_rounded"] == agemax]
    return df5


# plot histogram of data
def plot_value_hist(df, filename):
    plt.hist(df["value"], bins=20, edgecolor='k', alpha=0.6)
    plt.xlabel('Value')
    plt.ylabel('Number')
    histvalueplotname = filename.replace('.csv', '_histvalue.png')
    plt.axvline(df['value'].mean(), color='r', linestyle='dashed', linewidth=1, label='mean')
    plt.axvline(df['value'].median(), color='b', linestyle='dashed', linewidth=1, label='median')
    plt.legend(loc=0)
    plt.savefig(histvalueplotname, format="png")
    plt.show()


# calculate skew of data
def calculate_skew(df, filename):
    sk = skew(df["value"])
    print('\nSkewness for data : ', str(sk))
    print('\n0 : normally distributed.')
    print('\n> 0 : more weight in left tail.')
    print('\n< 0 : more weight in right tail.')
    result = skewtest(df["value"])
    if result[1] <= 0.05:
        print('\nData are significantly skewed.')
    else:
        print('\nSkewness of data is not significant.')
    line1 = "skewness = " + str(sk) + "\n"
    line2 = "significance = p " + str(result[1]) + "\n"
    skewfilename = filename.replace('.csv', '_skewtestresults.txt')
    with open(skewfilename, 'w') as file:
        file.writelines([line1, line2])


# calculate covariance of data with age
def calculate_cov(df, filename):
    df_cov = df[['age', 'value']]
    corr = df_cov.corr()
    print("correlation of data with age = " + "\n" + str(corr) + "\n")
    covfilename = filename.replace('.csv', '_covariancetestresults.txt')
    line3 = "correlation of data with age = " + "\n" + str(corr) + "\n"
    with open(covfilename, 'w') as file:
        file.write(line3)
