data_skew: removes outliers from data using modified z-score method, then plots a histogram of data values and tests for skewness.

INPUT:\n
-This package requires a .csv file with a column labeled "values" as input.\n
-If there is data from multiple ages in this file, place this data in columns labeled "age_in_days" or "age".\n
-Skewness will only be calculated for the data from the highest age.

OUTPUT:\n
-A .png file containing a histogram. The histogram will be generated in the same directory as the input .csv file, and will have the same filename with '_histvalue.png' appended.\n
-A .txt file containing the results of the skew test. The file will be generated in the same directory as the input .csv file, and will have the same filename with '_skewtestresults.txt' appended.\n
-If your data is from subjects that have multiple ages, a covariance test will be performed. A .txt file containing these results will be generated in the same directory as the input .csv file, and will have the same fiilename with '_covariancetestresults.txt' appended.\n
-All three of the above should be displayed in the terminal window as well.
