import datetime
import json

import matplotlib.pyplot as plt
import pandas as pd


def convert_timestamp(dataframe):
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], unit='s')


def insert_date(dataframe):
    '''Inserts a date in year/month/date format'''
    dataframe.insert(0, "date",
                     dataframe.timestamp.apply(
                         lambda x: datetime.datetime(day=x.date().day,
                                                     month=x.date().month,
                                                     year=x.date().year)))


def filter_columns(dataframe):
    '''Filters data by country and dates. Here: Germany in April 2020'''
    country = 'DE'
    return dataframe.loc[(dataframe['iso-3166-1'] == country) & (dataframe['date'] > datetime.datetime(2020, 4, 1))]


def get_total_deaths(dataframe):
    dataframe.drop(labels=['timestamp', 'iso-3166-1'], axis=1, inplace=True)
    sum_deaths = dataframe.sum(axis=0, skipna=True)
    return sum_deaths


path = "/Users/teraadmin/Desktop/John Hopkins/jh.json"
plt.close('all')
# read json files from John Hopkins University
with open(path) as json_file:
    data = json.load(json_file)
    useful_data = data[1]

df = pd.DataFrame(useful_data)
df.drop(labels=['source', 'original', 'latitude', 'longitude'], axis=1, inplace=True)
convert_timestamp(df)
insert_date(df)
df = filter_columns(df)
ax = df.plot(x='date', y=['infected_total', 'recovered_total'])
plt.show()
