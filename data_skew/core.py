# Created on Tue May 19 09:17:54 2020

# @author: egill

from optparse import OptionParser
import sys
import os
import pandas as pd
import calc_outliers as o
import skew_test as s

# functions
_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, 'data', path)

'''
Function to get the name of the file that contains the data the user wants to analyze

Input: input_file (the path to the file that the user inputted when calling the script)
Ouput: filename
'''
def get_filename(input_file):
    filename = None
    if input_file == None:
        # if no filename is specified, ask user to specify one
        print("\n\nEnter the path to a csv file containing data you would like to analyze for outliers OR re-run this program using the -i flag: python core.py -i /absolute/path/to/file.csv'\n\n")
        # allow the user to type in the filename
        filename = input()
        # if the user doesn't type anything or presses 'enter', use the sample data file
        if filename == "" or filename == "\n" or filename is None:
            filename = get_data('test_data.csv')
        else: 
            filename = get_data(filename) 
    else:
        # get filename and fix FileNotFoundError when the input is just the filename.
        filename = get_data(input_file) 
    return filename


# allow user to specify input file name as command line argument
parser = OptionParser()
parser.add_option("-i", "--input-file", dest="input_file", action="store", type="string", help="The input filepath.")
parser.add_option("-a", "--age", dest="age", action="store", type="float", help="The age to examine. Default is the max age in the input file.")
parser.add_option("-z", "--z-outlier-threshold", dest="z_outlier_threshold", action="store", type="int", default=3.5, help="A value whose modified z-score has an absolute value above this threshold is considered an outlier. Default is 3.5.")
parser.add_option("-e", "--extreme-outlier-threshold", dest="extreme_outlier_threshold", action="store", type="float", default=7, help="A value whose modified z-score has an absolute value above this threshold is considered an extreme outlier. Default is 7.")


(options, args) = parser.parse_args()

# get the .csv filename
filename = get_filename(options.input_file)
# open file
data = pd.read_csv(filename)

# remove rows containing empty/blank values.
data = o.remove_blanks(data)

# remove rows containing values that correspond to codes.
# for example, a code could represent lack of data, not an actual data point.
data = o.remove_codes(data)

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

# Comment this out so that we change functionality to include outliers in the histogram.
# no_outliers = o.remove_z_outliers(data_output)

# age5 = s.age5_df(no_outliers)

df_age = s.age_df(data_output, options.age)

s.plot_z_hist(df_age, filename, options.z_outlier_threshold, options.extreme_outlier_threshold)

# s.plot_value_hist(df_age, filename)

# if "age" in df_age.columns:

#     s.calculate_cov(df_age, filename)

# s.calculate_skew(df_age, filename)



