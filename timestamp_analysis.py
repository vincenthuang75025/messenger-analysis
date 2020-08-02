import json
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

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

	