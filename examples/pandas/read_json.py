'''
Example: load and display the ecdc_xlsx and johns_hopkins_github datasets.

Download and prepare data:

$ curl https://covid19datapool.appspot.com/v1/get_all/johns_hopkins_github | jq ".[1]" >johns_hopkins_github.json

Run this python program.
'''

import pandas as pd
import matplotlib.pyplot as plt

COUNTRY = "DE"

data = pd.read_json("file:data/%s.json" % name)
data_jh = data.loc[(data['timestamp'] > '2020-02-15') & (data['iso-3166-1'] == COUNTRY)]
data_jh.plot(x="timestamp", y=["deaths", "infected"], kind="line")
plt.show()
