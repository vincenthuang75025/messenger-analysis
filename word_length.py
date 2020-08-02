
import json
from collections import Counter
import matplotlib.pyplot as plt

# load json file
def load_json(path="bow_data.json"):
	with open(path) as json_file:
		data = json.load(json_file)
	return data


data = load_json()

result = {}
# an array which gives the wordlength distribution 
for name in data.keys():
    word_counts = data[name]['word_counts']
    frequency_by_length = Counter()
    total = 0
    total_length = 0
    for word, freq in word_counts.items():
        frequency_by_length[len(word)] += freq
        total += freq
        total_length += freq*len(word)
    if (total_length):
        result[name] = {'them': {'freq': dict(frequency_by_length), 'average':total_length/total }}
        print(name, total_length/total)

for name in data.keys():
    word_counts = data[name]['word_counts_self']
    frequency_by_length = Counter()
    total = 0
    total_length = 0
    for word, freq in word_counts.items():
        frequency_by_length[len(word)] += freq
        total += freq
        total_length += freq*len(word)
    if (total_length):
        result[name] = {'self': {'freq': dict(frequency_by_length), 'average':total_length/total }}
    

def plot_words(w_them, w_self, name):
    d = w_them[name]
    m = w_self[name]
    width = 0.35       # the width of the bars
    plt.bar(d.keys(), d.values(), -width, align='edge')
    plt.bar(m.keys(), m.values(), width, align='edge')
with open('word_lengths.json', 'w') as outfile:
    json.dump(word_counts_them, outfile)