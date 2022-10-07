# author: egill

# imports
import pandas as pd
import scipy.stats as sstats
import statistics as stat


# functions
'''
Function that removes rows with blank values from a DataFrame.

Input: df (DataFrame that contains a column 'value')
Output: DataFrame without rows containing blank values
'''
def remove_blanks(df):
    return df[df.value.notnull()]
    
'''
Function that removes rows from a DataFrame if the row's value matches a code, and is therefore not an actual data point.

Input: df (DataFrame that contains a column 'value')
Output: DataFrame without rows containing values that match a code
'''
def remove_codes(df):
    '''
    Codes:
        888 - Not applicable
        666 - Don't know
        8888 - Subject skipped the questionnaire
        444 - Questionnaire not applicable
        555 - Participant refused to answer question/perform test
        999 - No response to this question
        777 - Question not asked
        9999 - Not recorded
    '''
    codes = [888, 666, 8888, 444, 555, 999, 777, 9999]
    # keep rows containing values that do not match a code
    return df[(~df.value.isin(codes))]
    
def add_age(data_f):
    data_f['age'] = data_f['age_in_days'] / 365
    data_f['age_rounded'] = round(data_f['age'])
    return data_f

# round age
def round_age(data_f):
    data_f['age_rounded'] = round(data_f['age'])
    return data_f


# split all data frames by age to calculate age-specific IQRs
def split_by_age(data_f):
    data_split = [i for _, i in data_f.groupby('age_rounded')]
    return data_split


# Find median, IQR, range of non-outlier datapoints for each age
def calc_stats(df_list, data_f):
    stats = []
    colnames = ['age_rounded', 'median', 'lower', 'upper']
    table = pd.DataFrame()
    for i in df_list:
        if len(i) > 5:  # must modify function so that stats are only generated with min of 5 samples
            stats.append(i['age_rounded'].iloc[0])
            stats.append(stat.median(i['value']))
            IQR = (i['value'].describe()[6] - i['value'].describe()[4])
            stats.append(i['value'].describe()[4] - (1.5 * IQR))
            stats.append(i['value'].describe()[6] + (1.5 * IQR))
            stats_df = pd.DataFrame(stats).T
            table = table.append(stats_df, ignore_index=True)
        stats = []
    table.columns = colnames
    return table


# merge stats with dataframes for transperancy when conducting outlier analysis
def merge_stats(df_list, stats):
    df_list_merged = []
    for i in df_list:
        i = i.merge(stats)
        df_list_merged.append(i)
    return df_list_merged


# determine if each row is an outlier based on IQR method
def is_outlier(row):
    if row['value'] < row['lower']:
        return True
    elif row['value'] > row['upper']:
        return True
    else:
        return False


# mark IQR outliers in data frame
def mark_outliers(df_list):
    for i in df_list:
        if i.empty:
            pass
        else:
            i['outlier'] = i.apply(lambda row: is_outlier(row), axis=1)
    return df_list


# calculate modified z-score for each data point
def mod_z_score(df_list):
    for i in df_list:
        if i.empty:
            pass
        else:
            median = stat.median(i['value'])
            MAD = sstats.median_absolute_deviation(i['value'])
            i['mod_z_score'] = (0.6745 * (i['value'] - median) / MAD)
    return df_list


# merge all dataframes back together
def df_append(df_list):
    big_df = pd.DataFrame()
    for i in df_list:
        big_df = big_df.append(i, ignore_index=True, sort=True)
    return big_df

# remove modified z-score outliers before running skew analysis
def remove_z_outliers(data_f):
    data_f['z_outlier'] = abs(data_f['mod_z_score']) > 3.5
    return data_f[data_f['z_outlier'] == False]
