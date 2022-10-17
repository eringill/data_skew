# -*- coding: utf-8 -*-
# Created on Tue May 19 09:17:54 2020

# @author: egill


import matplotlib.pyplot as plt
from scipy.stats import skew, skewtest
from matplotlib.lines import Line2D
from pathlib import Path
import numpy as np
import math
from textwrap import fill 


# select data from highest age only
def age_df(df, age):
    if (age == None):
        age = df['age_rounded'].max()
    df_age = df[df["age_rounded"] == age]
    return df_age

def min_max_age(df):
    min = int(df['age_rounded'].min())
    max = int(df['age_rounded'].max())
    ages_n = max - min + 1
    return [min, max, ages_n]

'''
Function that returns a custom legend label.

Input: title of the category, number of items in the category, and total number of items
Output: string that reports the category title, category count, and the percentage of total values that are part of the category
'''
def legend_label(category_title, category_count, total_count):
    return '{:<8}{:>6} / {:<6} = {:.1%}'.format(category_title, category_count, total_count, category_count / total_count)

'''
Function that plots one or more modified z-score outlier histograms on the same figure. One histogram is created for each age (year).

Input:
    df          DataFrame that contains columns 'mod_z_score' and 'age_rounded'
    filename    A CSV file name, which will be used to name the histogram PNG file
    z           Threshold above which the absolute value of a modified z-score is considered an outlier
    extreme_z   Threshold above which the absolute value of a modified z-score is considered an extreme outlier
'''
def plot_z_hists(df, filename, z, extreme_z, hist_edge):
    # Because floats cannot be used in some plt function arguments, this constant wil be used to adjust float values such as thresholds.
    constant = 10
    [min_age, _, ages_n] = min_max_age(df)

    fig, axes = plt.subplots(nrows=ages_n, ncols=1, sharex=True, sharey=False)
    plt.rcParams['font.family'] = 'monospace'
    # For each age:
    for i in range(0, ages_n):
        # Get the dataframe for that age.
        df_age = age_df(df, min_age + i)
        # Create a histogram for that age.
        plot_z_hist(df_age, axes[i], z, extreme_z, ' Age {}'.format(min_age + i), hist_edge=hist_edge, constant=constant)

    # Since we multiplied the x-values by a constant, we need to adjust the x-tick values by that constant.
    tick_values, _ = plt.xticks()
    plt.xticks(tick_values, [float(value) / constant for value in tick_values])

    # Label the title and axes.
    fig.suptitle(Path(filename).stem, fontweight='bold')
    fig.supxlabel('Modified z-score', font='monospace')
    fig.supylabel('Number', font='monospace')

    # Adjust figure size, margins, and layout.
    fig.set_figheight(8)
    fig.set_figwidth(10)
    plt.margins(x=0)
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.2, right=0.7, top=0.9, bottom=0.1, left=0.1)

    # Save file.
    plotname = filename.replace('.csv', '_z_score_hist.png')
    print("Saving modified z-outlier histogram to {}".format(plotname))
    plt.savefig(plotname, format="png", bbox_inches='tight')
    plt.show()

'''
Function that adds a vertical line to a matplotlib Axes.

Input:
    axis                    A Matplotlib Axes to add the vertical line to.
    x                       x coordinate where the line should be added.
    color                   Color of the line and text label.
    label                   Text label (will be displayed at the top of the line).
    horizontalalignment     Horizontal alignment of the text label relative to the line.
'''
def add_vline(axis, x, color, horizontalalignment, label=''):
    axis.axvline(x, color=color, linestyle='dashed', linewidth=1)
    axis.text(x, axis.get_ylim()[1], label, size=6, horizontalalignment=horizontalalignment, verticalalignment='bottom', color=color)

'''
Function that creates a histogram.
    x-axis: modified z-score
    y-axis: number of participants or logplot of number of participants.

Bars are colour-coded to distinguish non-outliers, outliers, and extreme outliers.

Input: 
    df          DataFrame that contains a column 'mod_z_score'
    axis        A matplotlib subplot
    z           Threshold above which the absolute value of a modified z-score is considered an outlier
    extreme_z   Threshold above which the absolute value of a modified z-score is considered an extreme outlier
    title       Desired title of the histogram
    constant    Constant to use when turning modified z-scores (float) into ints (required for histogram parameters).
    hist_edge   Maximum x-limit. Any modified z-scores >= hist_edge (or < -hist_edge) will not be shown on the histogram.
Output: 
    True if histogram created
    False if dataframe contained infinity, in which case no histogram is created
'''
def plot_z_hist(df, axis, z, extreme_z, title, hist_edge, constant=10):
    # Find the total rows in the dataframe.
    total_n = df.shape[0]

    # Find the total number of NaN scores.
    nan_n = df.isnull().values.sum()
    # Find the total number of inf scores.
    inf_low_n = len(df.loc[df['mod_z_score'] == -math.inf])
    inf_high_n = len(df.loc[df['mod_z_score'] == math.inf])
    # If all the modified z-scores are NaN or infinite, don't make a histogram.
    if (total_n - nan_n - inf_low_n - inf_high_n == 0):
        # Use invisible plots to report NaN and infinites in the legend.
        axis.plot([], [], ' ', label=fill('When >50% of data values are identical, modified z-scores become -inf, NaN, or inf.', 31))
        axis.plot([], [], ' ', label=legend_label('-inf', inf_low_n, total_n))
        axis.plot([], [], ' ', label=legend_label('NaN', nan_n, total_n))
        axis.plot([], [], ' ', label=legend_label('inf', inf_high_n, total_n))
        # Create the legend.
        axis.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 8}, title=title)
        return False

    # We want to split histogram bins so that non-outliers and outliers are never in the same bin as each other.
    # Ideally we would use a bin step of 0.5 (assuming the mod z-score outlier threshold is 3.5).
    # However, the bins parameter in axis.hist does not accept floats, so we cannot pass in 0.5. 
    # Instead, multiply z-scores by the constant.
    new_df = df['mod_z_score'] * constant

    # Play around with the bin width and yscale value to see what produces the most informative visuals.
    bin_width = 5
    axis.set_yscale('log')

    # Only display mod_z_scores within hist_edge.
    # Need the "+ 1" because range() function doesn't include its second argument in its output range.
    bin_range = range(-hist_edge * constant, hist_edge * constant + 1, bin_width)

    # Create the histogram.
    _, _, bars = axis.hist(new_df, bins=bin_range, edgecolor='k', alpha=0.5, align='mid')
    
    # Label each bin with the number of participants in that bin.
    # To avoid visual clutter, don't label bins with zero participants.
    labels = [int(val) if val > 0 else '' for val in bars.datavalues]
    axis.bar_label(bars, labels=labels, label_type='edge', rotation=90, fontsize=7, padding=5)
    
    # Colour code histogram bins so that we distingush non-outliers, outliers, and extreme outliers.
    for bar in bars: 
        x = bar.get_x() + 0.5 * bar.get_width() 
        if abs(x) > (extreme_z * constant): 
            bar.set_color('r')
        elif abs(x) > (z * constant): 
            bar.set_color('orange')
        else:
            bar.set_color('b')

    # Get min and max mod_z_scores.
    min_z = df['mod_z_score'].min()
    max_z = df['mod_z_score'].max()
    props = dict(boxstyle='round', alpha=0.2, facecolor='orange')
    
    # If there are any points offscreen (below -hist_edge), report this in a text box.
    if (min_z < -hist_edge):
        # Find how many points are offscreen (below -hist_edge).
        lower_n = len(df.loc[df['mod_z_score'] < -hist_edge])
        text = '{} pt(s) offscreen\nin [{:.1f}, {:.1f})'.format(lower_n, min_z, -hist_edge)
        
        # Put the text box at the top-left of the plot.
        axis.text(0.01, 0.95, text, transform=axis.transAxes, fontsize=7, verticalalignment='top', horizontalalignment='left', bbox=props)
    
    # If there are any points offscreen (above hist_edge), report this in a text box.
    if (max_z >= hist_edge):
        # Find how many points are offscreen (above hist_edge).
        upper_n = len(df.loc[df['mod_z_score'] >= hist_edge])
        text = '{} pt(s) offscreen\nin [{:.1f}, {:.1f}]'.format(upper_n, hist_edge, max_z)
        
        # Put the text box at the top-right of the plot.
        axis.text(0.99, 0.95, text, transform=axis.transAxes, fontsize=7, verticalalignment='top', horizontalalignment='right', bbox=props)

    # If there are any outliers, add vertical lines to show where the thresholds are.
    [left, right] = axis.get_xlim()
    if (constant * z < right): 
        add_vline(axis, constant * z, 'orange', 'left', 'Outlier')
    if (constant * -z > left): 
        add_vline(axis, constant * -z, 'orange', 'right', 'Outlier')
    
    # If there are any extreme outliers, add vertical lines to show where the thresholds are.
    if (constant * extreme_z < right): 
        add_vline(axis, constant * extreme_z, 'r', 'left', 'Extreme')
    if (constant * -extreme_z > left): 
        add_vline(axis, constant * -extreme_z, 'r', 'right', 'Extreme')
    
    # Find the number of extreme outliers, outliers, and non-outliers.
    extreme_n = len(df.loc[abs(df['mod_z_score']) > extreme_z])
    outlier_n = len(df.loc[abs(df['mod_z_score']) > z]) - extreme_n
    non_n = df.shape[0] - extreme_n - outlier_n

    # Add information about skewness.
    skew_result = calculate_skew(df)
    if (skew_result):
        [skew, significance] = skew_result
        skew_label = '\nSkew {:.4}'.format(skew)
        if skew > 0:
            skew_label += ': weight in left.'
        elif skew < 0:
            skew_label += ': weight in right.'
        else: 
            skew_label += ': normally distributed.'
        if significance <= 0.05:
            skew_label += '\nSignificantly skewed.'
        else:
            skew_label += '\nNot significantly skewed.'
    else: 
        skew_label = '\nNeed 8 values to calculate skew.'
    
    # Create a list of legend elements with descriptive labels. Add colour-coding.
    legend_elements = [Line2D([0], [0], color='b', lw=2, label=legend_label('Inlier', non_n, total_n)),
                   Line2D([0], [0], color='orange', lw=2, label=legend_label('Outlier', outlier_n, total_n)),
                   Line2D([0], [0], color='r', lw=2, label=legend_label('Extreme', extreme_n, total_n)),
                   Line2D([0], [0], alpha=0, lw=2, label=skew_label)]

    # Create the legend.
    axis.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 8}, title=title)

    return True

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
def calculate_skew(df, filename=None):
    sk = skew(df["value"])
    # print('\nSkewness for data : ', str(sk))
    # print('\n0 : normally distributed.')
    # print('\n> 0 : more weight in left tail.')
    # print('\n< 0 : more weight in right tail.')
    if (df.shape[0] < 8):
        return None
    result = skewtest(df["value"])
    # if result[1] <= 0.05:
    #     print('\nData are significantly skewed.')
    # else:
    #     print('\nSkewness of data is not significant.')
    line1 = "skewness = " + str(sk) + "\n"
    line2 = "significance = p " + str(result[1]) + "\n"
    if (filename):
        skewfilename = filename.replace('.csv', '_skewtestresults.txt')
        with open(skewfilename, 'w') as file:
            file.writelines([line1, line2])

    return [sk, result[1]]

# calculate covariance of data with age
def calculate_cov(df, filename):
    df_cov = df[['age', 'value']]
    corr = df_cov.corr()
    print("correlation of data with age = " + "\n" + str(corr) + "\n")
    covfilename = filename.replace('.csv', '_covariancetestresults.txt')
    line3 = "correlation of data with age = " + "\n" + str(corr) + "\n"
    with open(covfilename, 'w') as file:
        file.write(line3)
