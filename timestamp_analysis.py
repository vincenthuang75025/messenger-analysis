import json
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from datetime import datetime

# load json file
def load_json(path="timestamp_dict.json"):
	with open(path) as json_file:
		data = json.load(json_file)
	return data

data = load_json()

df = pd.DataFrame(data, columns=['name', 'timestamp'])
# Convert that column into a datetime datatype
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# Set the datetime column as the index
df.index = df['timestamp']
start_day = '2016-01-01' # can change this
df = df[df['timestamp'] > start_day]
min_date = df.index.min() 
max_date = df.index.max()
n_days = (max_date - min_date).days

# group by name and day
day = df.groupby([df['name'], pd.TimeGrouper(freq='D')]).count()
print(df.head())
print(day.head())

# function that takes: name_of_frined , start_time, end_time , resoluction \in (hour / day / month)
# returns 
def get_interaction(name, start_time,end_time,resolution):
	return

day['timestamp']['Raffi Hotter'].plot()
day['timestamp']['Zachary Feng'].plot()
day['timestamp']['Chris Axon'].plot()

names=['Raffi Hotter', 'Jasmine Wang','Frederick Zhang', 'Chris Axon', 'Zachary Feng', 'Jad Hamdan']
for name in names:
    data=day['timestamp'][name];plt.bar(data.index, data)
    data['int_days'] = df['timestamp'].sub(pd.Timestamp('2018-01-01')).dt.days
plt.show()

def smooth(x,window_len=11,window='hanning'):

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

result = []
names = list(df['name'].unique())
names = [name for name in names if len(df[df['name'] ==name]) > 200] #and name != 'Zachary Feng' and name != 'Gleb Posobin']


first = []
for name in names:
    data=day['timestamp'][name]
    formatted = data.to_frame()
    formatted['int_days'] = data.index.to_series().sub(min_date).dt.days
    bigarr = formatted.values
    arr = np.zeros(n_days)
    for i, num in bigarr:
        arr[num-1] = i
    first_day = np.min(bigarr.T[1])
    first.append(first_day)
    result.append(smooth(arr,window_len=25))
    # result.append(arr)
first = np.array(first)
inds = first.argsort()

colorange = first.max() + 1
viridis = cm.get_cmap('Spectral', colorange)
cmap = viridis(range(colorange))

plt.figure(figsize=(20,20))
# x = np.linspace(0,n_days, len(result[0]))
x = [min_date + pd.DateOffset(i) for i in range(len(result[0]))]
plt.stackplot(x, np.array(result)[inds], labels=np.array(names)[inds], colors=[cmap[idx] for idx in first[inds]] )
plt.legend()
plt.savefig('2016_2020.png')
