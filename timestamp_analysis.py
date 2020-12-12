import json
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from datetime import datetime
# load json file

MIN_MESSAGES = 20  # minimum number of messages for person to be included in plot
OUTPUT_FILENAME = '2019_2020.png'
start_day = '2019-01-01'  # can change this


def load_json(path="timestamp_dict_3.json"):
    with open(path) as json_file:
        data = json.load(json_file)
    return data


data = load_json()

df = pd.DataFrame(data, columns=['name', 'timestamp'])
# Convert that column into a datetime datatype
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# Set the datetime column as the index
df.index = df['timestamp']
df = df[df['timestamp'] > start_day]
min_date = df.index.min()
max_date = df.index.max()
n_days = (max_date - min_date).days

# group by name and day
day = df.groupby([df['name'], pd.TimeGrouper(freq='D')]).count()
# print(df.head())
# print(day.head())


def smooth(x, window_len=11, window='hanning'):

    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(), s, mode='valid')
    return y


result = []
names = list(df['name'].unique())
names = [name for name in names if len(df[df['name'] == name]) > MIN_MESSAGES]


first = []
for name in names:
    data = day['timestamp'][name]
    formatted = data.to_frame()
    formatted['int_days'] = data.index.to_series().sub(min_date).dt.days
    bigarr = formatted.values
    arr = np.zeros(n_days)
    for i, num in bigarr:
        arr[num-1] = i
    first_day = np.min(bigarr.T[1])
    first.append(first_day)
    result.append(smooth(arr, window_len=10))
    # result.append(arr)
first = np.array(first)
inds = first.argsort()

colorange = first.max() + 1
viridis = cm.get_cmap('Spectral', colorange)
cmap = viridis(range(colorange))

plt.figure(figsize=(20, 20))
# x = np.linspace(0,n_days, len(result[0]))
x = [min_date + pd.DateOffset(i) for i in range(len(result[0]))]
plt.stackplot(x, np.array(result)[inds], labels=np.array(names)[
              inds], colors=[cmap[idx] for idx in first[inds]])
plt.legend(loc='upper left')
plt.savefig(OUTPUT_FILENAME)
