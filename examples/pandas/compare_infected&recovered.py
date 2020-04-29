import datetime
import json

import matplotlib.pyplot as plt
import pandas as pd


# TODO: sum up US values
# TODO: sum over a week
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
    return dataframe.loc[(dataframe['iso-3166-1'] == country) & (dataframe['date'] > datetime.datetime(2020, 3, 31))
                         & (dataframe['date'] < datetime.datetime(2020, 4, 30))]


def filter_columnsp(dataframe):
    '''Filters data by country and dates. Here: Germany in March 2020'''
    country = 'DE'
    return dataframe.loc[(dataframe['iso-3166-1'] == country) & (dataframe['date'] > datetime.datetime(2020, 3, 1))
                         & (dataframe['date'] < datetime.datetime(2020, 3, 31))]


def get_total_deaths(dataframe):
    dataframe.drop(labels=['timestamp', 'iso-3166-1'], axis=1, inplace=True)
    sum_deaths = dataframe.sum(axis=0, skipna=True)
    return sum_deaths['deaths_total']


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
df = df.rename(columns={'deaths_total': 'deaths',
                        'infected_total': 'infected',
                        'recovered_total': 'recovered'})
df.plot(x='date', y=['recovered', 'infected'], title='Germany')
plt.show()
