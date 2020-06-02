<<<<<<< Updated upstream
data_skew:
==========

### Removes outliers from data using the modified z-score method, then plots a histogram of data values and tests for skewness.

INPUT:
------

1. This package requires a .csv file with a column labeled *"values"* as input.
2. If there is data from multiple ages in this file, place this data in columns labeled *"age_in_days"* or *"age"*.
3. Skewness will only be calculated for the data from the highest age.

OUTPUT:
-------

1. A .png file containing a histogram. The histogram will be generated in the same directory as the input .csv file, and will have the same filename with *'_histvalue.png'* appended.
2. A .txt file containing the results of the skew test. The file will be generated in the same directory as the input .csv file, and will have the same filename with *'_skewtestresults.txt'* appended.
3. If your data is from subjects that have multiple ages, a covariance test will be performed. A .txt file containing these results will be generated in the same directory as the input .csv file, and will have the same fiilename with *'_covariancetestresults.txt'* appended.
4. All three of the above should be displayed in the terminal window as well.
=======
#data_skew:
removes outliers from data using modified z-score method, then plots a histogram of data values and tests for skewness.

##INPUT:
*This package requires a .csv file with a column labeled "values" as input.
*If there is data from multiple ages in this file, place this data in columns labeled "age_in_days" or "age".
*Skewness will only be calculated for the data from the highest age.

##OUTPUT:
*A .png file containing a histogram. The histogram will be generated in the same directory as the input .csv file, and will have the same filename with '_histvalue.png' appended.
*A .txt file containing the results of the skew test. The file will be generated in the same directory as the input .csv file, and will have the same filename with '_skewtestresults.txt' appended.
*If your data is from subjects that have multiple ages, a covariance test will be performed. A .txt file containing these results will be generated in the same directory as the input .csv file, and will have the same fiilename with '_covariancetestresults.txt' appended.
*All three of the above should be displayed in the terminal window as well.
>>>>>>> Stashed changes
