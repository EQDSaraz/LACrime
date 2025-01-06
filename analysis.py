# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import time


crimes = pd.read_csv("crimes.csv", parse_dates=["Date Rptd", "DATE OCC"], dtype={"TIME OCC": str})
#print(crimes.head())
print(crimes['Vict Sex'].value_counts())


#investigate data
print(crimes['DATE OCC'].dtype)
print(crimes['DATE OCC'].isna().sum())
print(crimes[['DATE OCC','TIME OCC']].head())
print(crimes['TIME OCC'].isna().sum())

#new features: hour of crime, min of crime, time of crime
crimes['HourOCC']=crimes['TIME OCC'].str[:2]
crimes['HourOCC'] =crimes['HourOCC'].astype(int)

crimes['MinOCC']=crimes['TIME OCC'].str[2:4]
crimes['MinOCC']=crimes['MinOCC'].astype(int)

crimes['timeOCC'] = crimes.apply(lambda row: time(row['HourOCC'], row['MinOCC']), axis=1)
print(crimes[['TIME OCC','HourOCC','MinOCC','timeOCC']].head()) #validate it worked

#Analysis #1: Which hour has the highest frequency of crimes?
hour_counts=crimes['HourOCC'].value_counts()
min_counts=crimes['MinOCC'].value_counts()
print(hour_counts)
sns.histplot(data=crimes, x="HourOCC")
crimes['peak_crime_hour']=12
crimes['peak_crime_hour']=crimes["peak_crime_hour"].astype(int)
print(crimes['peak_crime_hour'].head())

#new feature: setting "night time" crime
start_time = time(22, 0)  # 10:00 PM
end_time = time(4, 0)     # 4:00 AM
crimes['Night'] = crimes['timeOCC'].apply(lambda t: start_time <= t or t < end_time)
print(crimes[['timeOCC','Night']].head())

#analysis #2: Which area has the largest frequency of night crimes (between 10pm and 3:59am)?
crimes['NightCrime']=crimes.groupby("AREA NAME")['Night'].transform(sum).astype(int)
sorted_crimes = crimes.sort_values(by='NightCrime', ascending=False) #sort it
peak_night_crime_location = sorted_crimes.iloc[0]['AREA NAME'] #take the max, get the name of area
max_night_crimes = sorted_crimes.iloc[0]['NightCrime'] #take the max, get the highest number
crimes['Max Night Crimes'] = max_night_crimes #create the variable in the DF
crimes['peak_night_crime_location'] = peak_night_crime_location #create the variable in the DF
print("Peak Night Crime Loaction is:", peak_night_crime_location)

#create a feature - category of victim's age
bins = [0, 18, 26, 35, 45, 55, 65, float('inf')]
age_labels = ["0-17", "18-25", "26-34", "35-44", "45-54", "55-64", "65+"]
crimes["victim_ages"]= pd.cut(crimes["Vict Age"], bins=bins, labels=age_labels,right=False)

#Analysis #3- number of crimes committed against victims of different age groups
print(crimes["victim_ages"].value_counts())


#print(crimes['Vict Descent'].value_counts())
sns.heatmap(crimes.corr(),annot=True)
sns.countplot(data=crimes,x="Status Desc")
grouped_data = crimes.groupby(['victim_ages', 'Vict Sex']).size().reset_index(name='count')

# Create the bar plot
sns.barplot(data=grouped_data, x='victim_ages', y='count', hue='Vict Sex')


#high_crime = crimes[crimes["NightCrime"] > 1000]
#high_crime_srt = high_crime.sort_values("NightCrime", ascending=False)
#print(high_crime_srt[["AREA NAME","NightCrime"]].head())
#crimes['NightCrimeSort']=crimes.sort_values("NightCrime",ascending=False)
#print(crimes['NightCrime'].head())
#print(crimes[['timeOCC','Night','NightCrime']].head(20))
#print(crimes['NightCrime'])
#print(crimes.head())

#print(crimes['HourOCC'].min())
#print(crimes['HourOCC'].max())
#print(crimes.info())

#print(hour_counts)
#print(crimes.describe())

#Max_crime_hour=crimes['TIME OCC'].value_counts().max()
#print(Max_crime_hour)
