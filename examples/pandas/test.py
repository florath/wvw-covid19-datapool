import matplotlib.pyplot as plt
import pandas as pd


def filter_columns(dataframe):
    country = 'US'
    return dataframe.loc[(dataframe['Country_Region'] == country)]


def delete_columns(data):
    data = filter_columns(data)
    data.drop(labels=['FIPS', 'Admin2', 'Lat', 'Long_', 'Active', 'Last_Update', 'Country_Region', 'Combined_Key',
                      'Province_State', 'Confirmed'], axis=1, inplace=True)

    return data


URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-14-2020.csv"

plt.close('all')
# read csv files from April
csv = pd.read_csv(URL, error_bad_lines=False)
csv = filter_columns(csv)
print(csv.head(10))

# csv.plot.bar()
# plt.show()
