import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

## Read data
data = pd.read_json("file:johns_hopkins_github.json")

## Cleanup and filter
d1 = data[['timestamp', 'iso-3166-1', 'infected', 'deaths']]
# Add date column - which is needed to accumulate the available data per day
# Also take care that the resulting object is a datetime (and not a date).
d1.insert(0, "date",
          d1.timestamp.apply(
              lambda x: datetime.datetime(day=x.date().day,
                                          month=x.date().month,
                                          year=x.date().year)))
# 'timestamp' is not needed any longer
d2 = d1.drop(columns="timestamp")
# filter all the data which is interesing for this observation
d3 = d2.loc[(d2['date'] > datetime.datetime(year=2020, month=2, day=15))
            & (d2['iso-3166-1'] == "DE")]
# Sometimes there is more than one data entry for a day - take the
# bigger one,
d4 = d3.groupby(by=['date',]).max()
# Flatten the dataset.
d5 = d4.reset_index()

## The following is based on the paper from the RKI
## where the probabilities are given.
d5.insert(4, "recovered_int_care", d5.deaths)

d5.insert(5, "int_care_end", d5.date)
d5.insert(5, "int_care_start", d5.int_care_end - datetime.timedelta(days=10))

# But ignore the time intervals where there is no deaths number
d5.loc[d5.deaths == 0, 'int_care_start'] = pd.NaT
d5.loc[d5.deaths == 0, 'int_care_end'] = pd.NaT

date_range = pd.date_range(d5.int_care_start.min(), d5.int_care_end.max())
date_range_df = pd.DataFrame(date_range, columns=["date", ])

d5d = pd.DataFrame(d5.date, columns=["date", ])

# d5d and date_range_df must have the same type: datetime.datetime
# which is internally converted to pandas._libs.tslibs.timestamps.Timestamp
# check with type(date_range_df.date[0])
# Also the column names must match!

missing_data = pd.concat([date_range_df, d5d, d5d]).drop_duplicates(keep=False)

# Add all the missing columns
for col in d5.columns:
    if col not in missing_data.columns:
        missing_data[col] = np.nan

d6 = pd.concat([d5, missing_data])
        
d6.insert(7, "int_care", 0)

# ??? ranges = map(range, d5['int_care_start'], d5['int_care_end'])

for idx, ds in d6.iterrows():
    if pd.isnull(ds.int_care_start):
        continue
    print(ds)

# Add dates which are not there.
# Looks that this is needed 
#d5.append({'date': '2020-02-08', 'int_care': 0}, ignore_index=True)

# For the time beeing: print the result
#d6.plot(x="date", y=["deaths", "infected"], kind="line", logy=True)

#d6.plot(x="date", y=["deaths"], kind="line")
#plt.show()
