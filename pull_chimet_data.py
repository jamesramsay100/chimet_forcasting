import pandas as pd
import time
import datetime
from tqdm import tqdm

start = pd.datetime(2020, 1, 1)
end = pd.datetime(2020, 12, 1)
dates = pd.date_range(start, end)
data = pd.DataFrame()

for d in tqdm(dates):
    
    day = d.strftime('%d')
    month3 = d.strftime('%b')
    month_full = d.strftime('%B')
    year = d.strftime('%Y')
    url = f'https://chimet.co.uk/archive/{year}/{month_full}/CSV/Chi{day}{month3}{year}.csv'

    try:
        df = pd.read_csv(url)

        # create date-time column and keep only this and windspeed
        df['date_time'] = pd.to_datetime((df['Date'] + df['Time']), format="%d/%m/%Y%H:%M")
        df = df[['date_time', 'WSPD']]

        # reindex to minute resolution
        df.set_index('date_time', inplace=True, drop=True)
        new_idxs = pd.date_range(d, d + datetime.timedelta(minutes=(24 * 60 - 1)), freq='T')
        df = df.reindex(df.index.append(new_idxs).unique())
        df.sort_index(inplace=True)
        df.interpolate(inplace=True)
        df = df.loc[new_idxs]

        data = data.append(df)

        time.sleep(1)

    except:
        print(f'Not CSV found for {day}/ {month3}/{year}')
        pass


data.to_csv('data/chimet_2020.csv')