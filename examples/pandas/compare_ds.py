#!/usr/bin/env python
'''
Compares the numbers from Johns-Hopkins, ECDC and RKI
'''

import pandas as pd
import matplotlib.pyplot as plt
import datetime

COUNTRY="DE"

def insert_date(df):
    df.insert(0, "date",
              df.timestamp.apply(
                  lambda x: datetime.datetime(day=x.date().day,
                                              month=x.date().month,
                                              year=x.date().year)))

def filter_data(df):
    return df.loc[(df['date'] > datetime.datetime(year=2020, month=2, day=15))
                  & (df['iso-3166-1'] == COUNTRY)]

e0 = pd.read_json("file:data/ecdc_cases.json")
e0.drop(labels=["source", "original"], axis=1, inplace=True)
insert_date(e0)
e1 = filter_data(e0)


#e1 = e1.set_index("date")

e1 = e1.rename(columns={'deaths_new': 'ecdc_deaths_new',
                        'infected_new': 'ecdc_infected_new'})

######################################################################

j0 = pd.read_json("file:data/johns_hopkins_github.json")
j0.drop(labels=['source', 'original', 'latitude', 'longitude'],
        axis=1, inplace=True)
insert_date(j0)
j1 = filter_data(j0)
j1 = j1.sort_values(by=['date'])
j1.insert(6, "deaths_new", j1.deaths_total - j1.deaths_total.shift(1))
j1.insert(7, "infected_new", j1.infected_total - j1.infected_total.shift(1))

j1 = j1.rename(columns={'deaths_new': 'jhu_deaths_new',
                        'infected_new': 'jhu_infected_new'})

######################################################################

r0 = pd.read_json("file:data/rki_cases.json")
r0.drop(labels=['original', ],
        axis=1, inplace=True)
insert_date(r0)
r1 = filter_data(r0)
#r2 = r1.set_index('date')
#r2['infected'].resample('D').sum()

r2 = r1.resample('D', on='date').sum().sort_values(by='date').reset_index()

r2 = r2.rename(columns={'deaths': 'rki_deaths_new',
                        'infected': 'rki_infected_new'})


ax = e1.plot(x="date",
             y=["ecdc_deaths_new",],# "ecdc_infected_new"],
             logy=False)
ax = j1.plot(x="date", ax=ax,
             y=["jhu_deaths_new",],# "jhu_infected_new"],
             logy=False)
ax = r2.plot(x="date", ax=ax,
             y=["rki_deaths_new",],# "rki_infected_new"],
             logy=False)
#plt.title(COUNTRY)
plt.show()
