# -*- coding: utf-8 -*-
# Created on Tue May 19 09:17:54 2020

# @author: egill


import matplotlib.pyplot as plt
from scipy.stats import skew, skewtest
import math
from matplotlib.lines import Line2D


# select data from highest age only
def age_df(df, age):
    if (age == None):
        age = df['age_rounded'].max()
    df_age = df[df["age_rounded"] == age]
    return df_age

'''
Function that creates a histogram.
    x-axis: modified z-score
    y-axis: number of participants or logplot of number of participants.

Bars are colour-coded to distinguish non-outliers, outliers, and extreme outliers.

Input: 
    df          DataFrame that contains a column 'mod_z_score'
    filename    Name of CSV file where data came from
    z           Threshold above which the absolute value of a modified z-score is considered an outlier
    extreme_z   Threshold above which the absolute value of a modified z-score is considered an extreme outlier
Output: histogram
'''
def plot_z_hist(df, filename, z, extreme_z):
    # Split histogram bins so that non-outliers and outliers are never in the same bin as each other.
    # Ideally we would use a bin step of 0.5 (assuming mod z-score outlier threshold is 3.5).
    # However, the bins parameter in plt.hist does not accept floats, so we cannot pass in 0.5. 
    # Instead, multiply z-scores by 10, and later use a step of 5.
    # TODO: Need to edit this so that extreme outliers and outliers never go in the same bin e.g. if our extreme threshold is 3.7.
    # TODO: Improve this by removing large gaps, e.g. one of the values bloodOxygenation age 10 has a modified_z_score of 400, which creates a very large gap in the x-axis. Solution: put any scores above a certain high number (e.g. 20) into one category and add a label for it showing the range of scores.
    constant = 10
    new_df = df['mod_z_score'] * constant
    min_z = math.floor(new_df.min())
    max_z = math.ceil(new_df.max())
    _, _, bars = plt.hist(new_df, bins=range(min_z, max_z, 5), edgecolor='k', alpha=0.6)

    # Since we multiplied the x-values by a constant, we need to adjust the x-tick values by that constant.
    tick_values, _ = plt.xticks()
    plt.xticks(tick_values, [float(value) / constant for value in tick_values])

    # Label the axes.
    plt.xlabel('Modified z-score')
    plt.ylabel('Number')
    
    # Colour code histogram bins so that we distingush non-outliers, outliers, and extreme outliers.
    for bar in bars: 
        x = bar.get_x() + 0.5 * bar.get_width() 
        if abs(x) > (extreme_z * constant): 
            bar.set_color('r')
        elif abs(x) > (z * constant): 
            bar.set_color('orange')
        else:
            bar.set_color('b')

    # Create a custom legend to describe the colour coding.
    legend_elements = [Line2D([0], [0], color='r', lw=4, label='Extreme outlier'),
                   Line2D([0], [0], color='orange', lw=4, label='Outlier'),
                   Line2D([0], [0], color='b', lw=4, label='Not an outlier')]

    plt.legend(handles=legend_elements, loc=0)

    # Save file.
    plotname = filename.replace('.csv', '_z_score_hist.png')
    plt.savefig(plotname, format="png")
    plt.show()
    

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
