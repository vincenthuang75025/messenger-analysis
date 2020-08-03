import json
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
for name in names:
    data=day['timestamp'][name]
    formatted = data.to_frame()
    formatted['int_days'] = data.index.to_series().sub(pd.Timestamp('2018-01-01')).dt.days
    bigarr = formatted.values
    arr = np.zeros(365*2)
    for i, num in bigarr:
        arr[num-1] = i
    result.append(smooth(arr,window_len=25))
    # result.append(arr)
plt.figure(figsize=(20,20))
x = np.linspace(0,740, len(result[0]));
plt.stackplot(x, result, labels=names)
plt.legend()

