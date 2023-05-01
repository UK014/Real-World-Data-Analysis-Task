import pandas as pd
import matplotlib.pyplot as plt
import os


##Merge 12 months of data
files = [file for file in os.listdir("./Sales_Data")]
all_months_data = pd.DataFrame()
for file in files:
    df = pd.read_csv("./Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data,df])
all_months_data.to_csv("all_data.csv",index=False)

all_data = pd.read_csv("all_data.csv")

## Data Cleaning
nan_df = all_data[all_data.isna().any(axis=1)]
all_data = all_data.dropna(how='all')
all_data = all_data[all_data["Order Date"].str[0:2] != 'Or']

## Adding month column
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data["Month"] = all_data["Month"].astype('int32')

## Adding sales column
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

## What was the best month for sales? How much was earned that month?
results = all_data.groupby('Month').sum()
months = range(1,13)
plt.bar(months,results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD')
plt.xlabel('Month Number')
plt.show()

##Add a city column
all_data['City'] = all_data['Purchase Address'].apply(lambda x: x.split(',')[1] + ' ' + "("+x.split(',')[2].split(' ')[1]+")")

## What city had the highest number of sales
results = all_data.groupby('City').sum()
cities = all_data['City'].unique()
plt.bar(cities,results['Sales'])
plt.xticks(cities, rotation='vertical',size = 8)
plt.ylabel('Sales in USD')
plt.xlabel('City Name')
plt.show()

all_data['City'].value_counts().plot(kind='pie')
plt.show()





