#Pandas has been imported to work with dataframes
import pandas as pd
#To read the data from the source csv file and load them to a data frame, "pd.read_csv" has been used.
df1 = pd.read_csv(r"C:/Users/Bharath/Desktop/BDA/LaqnData_OxfordRd_d.csv")
#To have a look of the loaded dataframe, below code has been used
#print(df1.head())

#Units Column has some anomalies like spaces in between the units. To clean this anomaly, ".replace" was used. Here in this case, units "ug m-3" and "ug m-3 as NO2" were considered to be the correct
# df1['Units'] = df1['Units'].replace(['ug m -3','ug/m3'], 'ug m-3')
# df1['Units'] = df1['Units'].replace(['ug m-3 as NO 2','ug m -3 as NO 2'], 'ug m-3 as NO2')

#The Date time in "Reading Date Time" column is not in the required Date Time format. Therefore "pd.to_datetime" has been used to change to the pandas accepted Date Time format
# df1['ReadingDateTime'] = pd.to_datetime(df1['ReadingDateTime'])

#Some values in the Species row were in lower case. This was found when groupby function was applied later in the program. Therefore ".str.upper()" was used to change all the values in the Species column to upper case.
# df1['Species'] = df1['Species'].str.upper()

#To load the data in the data frame to csv file ".to_csv" was used
# df1.to_csv(r"C:/Users/Bharath/Desktop/BDA/out1.csv")

#The same set of codes used for cleaning in the first data frame is again used to clean the anomalies in the second source file
df2 = pd.read_csv(r"C:/Users/Bharath/Desktop/BDA/LaqnData_Putney_d.csv")
# print(df2.head())
# df2['Units'] = df2['Units'].replace(['mg  m-3','mg m- 3'], 'mg m-3')
# df2['ReadingDateTime'] = pd.to_datetime(df2['ReadingDateTime'])
# df2['Species'] = df2['Species'].str.upper()
# df2.to_csv(r"C:/Users/Bharath/Desktop/BDA/out2.csv")


#The cleaning process mentioned above has been put in a function.
#A function is defined with data frame and 2 exception columns.
def change_df(dataframe,exceptcolumn_1,exceptcolumn_2):

    #Looping all the columns inside the dataframe
    for i in dataframe.columns:
        #Checking the data type of each column
        mycolumndatatype = dataframe[i].dtypes

        #Checking if the data type is object and it is not an exception columns & if yes, then convert it to upper case
        if (mycolumndatatype == 'object') & (i!=exceptcolumn_1) & (i!=exceptcolumn_2):
            #If the data type is object, then the values need to changed to upper case.
            dataframe[i] = dataframe[i].str.upper()

        #Check if the column name is exception column 1 and if yes, then Fix the Units here
        if (i == exceptcolumn_1):
            dataframe[i]=dataframe[i].replace(['mg m- 3','mg  m-3'],'mg m-3')
            dataframe[i]=dataframe[i].replace(['ug m -3 as NO 2','ug m-3 as NO 2'],'ug m-3 as NO2')
            dataframe[i]=dataframe[i].replace(['ug/m3'],'ug m-3')

        #Check if the column name is exception column 2 and if yes, then convert it into date time column
        if (i == exceptcolumn_2):
            dataframe[i] = pd.to_datetime(dataframe[i])

    #Return the cleaned data to the data frame
    return (dataframe)

#The function is called for the first data frame
df1_1 = change_df(df1, "Units", "ReadingDateTime")
# print(df1_1)

#The function is called for the second data frame
df2_2 = change_df(df2, "Units", "ReadingDateTime")
# print(df2_2)

#Two data frames are merged into a single data frame for analysis purpose using "pd.concat"
df = pd.concat([df1_1, df2_2])

#The NA values are dropped
df = df.dropna()

#The combined data frames output is loaded into csv file
df.to_csv(r"C:/Users/Bharath/Desktop/BDA/Combined_Output.csv")

#Matplotlib has been imported for plotting and visualizing the results
import matplotlib.pyplot as plt

#To identify and eliminate the outliers, the data points are plotted in a histogram chart
outliers = list(df['Value'])
ot = plt.hist([outliers], bins= 100)

#From the Histogram chart, it was found that Maximum number of data points were present between 0 and 400. Therefore the Value range 0-300 has been taken for analysis
df = df[(df['Value'] > 0) & (df['Value'] < 300)]
print(df)

#For comparing the Value in both the sites, groupby function is used. Mean is used here because the outliers have filtered.
ax = df.groupby(['Species','Site']).mean()[['Value']].unstack()
print(ax)

#To visualize the comparison results, unstacked bar chart is used
ax.plot.bar(rot = 0, title = "Air Quality WM6 vs WA9")
#labeling the y axis
plt.ylabel("Value")
#To view plotted chart, the below code was used.
plt.show()



# CONCLUSION:

#   From the above analysis, it is evident that WA9 site is better than WM6 site.
#   The Anamolies in the Units column were identified and changed to correct formats using the replace functions.
#   The Date Time Column was not in the date time format. Therefore using Date Time function, the format was changed.
#   When groupby function was excuted, it was found that, some letters in Species column were in lower case and some had a mixture of upper and lowercase. Therefore, all the letters were upper cased to avoid confusion.
#   Multiple null values were present in the "Value" column and using drop function all the null values were removed.
#   Some Outliers were present which were detected when the "Value" data points where plotted in the histogram chart. And it was found that, most of the data points were lying between 0 and 300. And therefore the value range between 0 and 300 were taken for plotting.
#   Using Groupby function, the Species and Site columns were grouped and their corresponding Values were plotted in unstacked bar chart.
#   From the bar chart, it was found that the value corresponding to WA9 site for all the gas species were lesser when compared with all gas species in WM6 site.
#   Asthma inducing gaseous substances are lesser in WA9 site and therefore would be suitable for John Doherty to stay in.
