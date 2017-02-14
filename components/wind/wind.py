import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Extract month == 10 from raw data to wd_m_10.csv
'''wd = pd.read_csv('C:\\Users\\Sam Matuba\\Documents\\GitHub\\Microgrid\\components\\wind\\2010_wind_data.csv', parse_dates = False, infer_datetime_format=True)
wd['DateTime'] = pd.to_datetime(wd['DateTime'], errors='coerce')
per = wd.DateTime.dt.to_period("M")
wd_m = wd.groupby(per).agg(['mean', 'count']) 
wd_m_10 = wd[wd.DateTime.dt.month == 10]
wd_m_10.to_csv("wd_m_10.csv", sep=',', encoding='utf-8')'''

# Data Analysis for month == 10: Diurnal Variation
wd_m_10 = pd.read_csv('C:\\Users\\Sam Matuba\\Documents\\GitHub\\Microgrid\\components\\wind\\wd_m_10.csv', infer_datetime_format=True)
wd_m_10['DateTime'] = pd.to_datetime(wd_m_10['DateTime'])
wd_m_10.set_index(wd_m_10['DateTime'], inplace=True)
del wd_m_10['Unnamed: 0']
del wd_m_10['DateTime']
wd_m_10 = pd.DataFrame(wd_m_10.groupby(pd.TimeGrouper(freq='H')).mean())
#wd_m_10.resample('D')
'''for i, group in wd_m_10:
    plt.figure()
    group.plot()'''

print (wd_m_10)
print (wd_m_10.dtypes)
#plt.show()

#groupby(pd.TimeGrouper("M"))
#wdg = wd.groupby(pd.TimeGrouper(freq='M'))
#pd.groupby(wd,by=[wd.index.month, wd.index.year])
#wd.groupby(pd.TimeGrouper(freq='M'))

#resamp = wd_g.set_index('date').groupby('DateTime').resample('M', how='mean')
#m = wd_g.groupby(pd.TimeGrouper("M"))
#print (wd.dtypes)


#wd['Date'], wd['Time'] = wd['DateTime'].str.split(' ', 1).str
#a = pd.to_datetime(pd.Series(['05/23/2005 10:30']))


# Choose month according to most number of rows

'''temp = pd.DatetimeIndex(wd["DateTime"])
wd['Date'] = temp.date
wd['Time'] = temp.time'''
#mean_wind_speed = wd['Wind Speed, m/s'].mean()
#mean_gust_speed = wd['Gust Speed, m/s'].mean()
#print (mean_wind_speed)

 
'''import csv
wind_data_file = open('C:\\Users\\Sam Matuba\\Documents\\GitHub\\Microgrid\\components\\wind\\2010_wind_data.csv', 'r')
wind_data_reader = csv.reader(wind_data_file, delimiter=',')
wind_data_d = []
wind_data = []

for row in wind_data_reader:
    wind_data_d.append(row[:5])
    print (row)
for row in wind_data_d:
	if row[3] != " ":
		wind_data.append(row)
	elif row[3] == " ":
		break 

print (wind_data)

# Learn about API authentication here: https://plot.ly/pandas/getting-started
# Find your api_key here: https://plot.ly/settings/api

import pandas as pd
import colorlover as cl
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/wind_rose.csv')
df.head()

data = []
counter = 0
for col in df.columns:
    if col != 'r':
        data.append(
            go.Area(t=df['r'],
                    r=df[col],
                    marker=dict(color=cl.scales['9']['seq']['PuBu'][counter]),
                    name=col+' m/s' ) )
        counter+=1

fig = Figure(data=data, layout=go.Layout(orientation=270, barmode='stack'))

# IPython notebook
# py.iplot(fig, filename='pandas-wind-rose-chart')

url = py.plot(fig, filename='pandas-wind-rose-chart')
'''