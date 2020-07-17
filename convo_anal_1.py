
# %%  IMPORTS

import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
import math
import json
import os


# %% 

"""
load the json file 

tfid 
your score as aggregate (scored on average of word count divided across total # convos)
each person's score

dictionaries of every person words scored


PCA plot (single)T
reformat into pds for pca (rows = person, columns = words, cells = tfid score)
follow towards datascience tutorial

"""
# %% Imports
import numpy as np 
import json 
import math
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer


# %%

# Utility funcitons

# load json file
def load_json(path="data/bow_data_steve.json"):
	with open(path) as json_file:
		data = json.load(json_file)
	return data


# takes the word dictionary for a single document, 
# returns a dictionary of the tf values of each word in the doc
def compute_tf(word_dict):
    tf_dict = {}
    net_words = 0
    for i in word_dict.values():
        net_words += i 
    for word , count in word_dict.items():
        tf_dict[word] = count / net_words 
    return tf_dict 

# take all the word dictionaries 
# return
def compute_idf(data,bow_corpus):
    idf_dict = {}
    
    def is_in(word,document): # binary
        if word in document.keys():
            return 1 
        return 0 
    
    for word in bow_corpus.keys():
        n = len(data)
        df_t = 0
        for name in data.keys():
            if word in data[name]['word_counts'].keys():
                df_t+=1
        idf_dict[word] = math.log(n/df_t) 
    return idf_dict

# takes data and bag of words of entire corpus (dic w/ key = word, value = freq)
def get_tfidf_dict(data,bow_corpus):
    tfidf_dict = {}
    idf_dict = compute_idf(data,bow_corpus)
    for name in data.keys():
        tfidf_dict[name] = {}
        tf_dict = compute_tf(data[name]["word_counts"]) 
        for word,idf_score in idf_dict.items():
            if word in tf_dict:
                tfidf_score = idf_score * tf_dict[word] 
                tfidf_dict[name][word] = tfidf_score 
    return tfidf_dict 

# takes word dictionary for a single document
# returns the shannon entropy of this document
def get_shannon(word_dict):
    n = sum(word_dict.values())
    prob_array = [count/n for count in word_dict.values()]
    shannon = -sum([p*math.log2(p) for p in prob_array])
    return shannon,n

# function which returns a database of shannon entropy related info
def get_shannon_df(data):
    rows = {'name':[],
            'n_them':[],
            'n_me':[],
            'shannon_them':[],
            'shannon_me':[]}
    for name in data.keys():
        doc_them = data[name]['word_counts']
        doc_me = data[name]['word_counts_self']
        shannon_them,n_them = get_shannon(doc_them)
        shannon_me,n_me = get_shannon(doc_me)
        # add row to rows dictionary
        rows['name'].append(name)
        rows['n_them'].append(n_them)
        rows['n_me'].append(n_me)
        rows['shannon_them'].append(shannon_them)
        rows['shannon_me'].append(shannon_me)
        
    # convert to pandas dataframe format and return
    shannon_df = pd.DataFrame(rows)
    return shannon_df


# retunrs dic key = word ; value = freq net 
def get_bow(data,pers='word_counts'):
    bow_all_them = {}
    for name in data:
        for word,n in data[name][pers].items():
            if word in bow_all_them:
                bow_all_them[word]+= n
            else: 
                bow_all_them[word]=n
    return bow_all_them
    

# returns dictionary of word categories and lists of words belonging to this category
def get_words_dic():
    words_dic = {}
    for i in os.listdir("words"):
        word_type = i.split(".")[0]
        with open("words/{}".format(i)) as json_file:
            entry=json.load(json_file)
        words_dic[word_type] = entry
    return words_dic

# returns dataframe of types of words used by each person
def get_types_words_df(data,words_dic):
	rows = {'name':[] , 'n_them':[] , 'n_me':[]}
	for word_type in words_dic.keys():
		rows['{}_them'.format(word_type)]=[]
		rows['{}_me'.format(word_type)]=[]
	for name in data.keys():
		doc_them = data[name]['word_counts']
		doc_me = data[name]['word_counts_self']
		
		# append data to dictionary
		rows['name'].append(name)
		n_them,n_me = sum(doc_them.values()) , sum(doc_me.values())
		rows['n_them'].append(sum(doc_them.values()))
		rows['n_me'].append(sum(doc_me.values()))
		for word_type in words_dic.keys():
		    # figure out how many of this word they have, append this data
		    # perthousand of words you say
		    density_them = 1000 / (n_them + 0.001) * sum([doc_them[i] for i in doc_them if i in words_dic[word_type]])
		    rows['{}_them'.format(word_type)].append(density_them)
		    density_me = 1000 / (n_me + 0.001) * sum([doc_me[i] for i in doc_me if i in words_dic[word_type]])
		    rows['{}_me'.format(word_type)].append(density_me)
	df = pd.DataFrame(rows)
	# this next line can be commented out if youw anna see all this extra info
	df = df.drop(columns=['fpp_pro_them','fpp_pro_me','spp_pro_them','spp_pro_me','tps_pro_them','tps_pro_me'])
	return df


# %%
    
if __name__ == "__main__":
    # Load json file
    with open('data/bow_data.json') as json_file:
        data = json.load(json_file) 
        
    # THE CORPUS IS ALL THE PEOPLE WHO MESSAGE YOU 
    # them is word_counts, me is word_counts_self
    bow = get_bow(data,pers='word_counts')
    tfidf_dict = get_tfidf_dict(data,bow) 
    
    
    vocab = set()
    for name, scores in tfidf_dict.items():
        arr = sorted(scores.items(), key=lambda x: x[1])
        # print(name, [word for word, num in arr[-5:]])
        [vocab.add(word) for word, num in arr[-20:-10]]
    dataset = {}
    for name, scores in tfidf_dict.items():
        dataset[name] = np.array([scores.get(word) if scores.get(word) else 0 for word in vocab])
    
    svd_50 = TruncatedSVD(n_components=150)
    trunc_50 = svd_50.fit_transform(np.array([ val for val in dataset.values()]))
    tsne = TSNE(n_components=2, random_state=0, learning_rate=10)
    coords = tsne.fit_transform(trunc_50).T
    
    
    plt.figure(figsize=(60,60))
    plt.scatter(coords[0], coords[1])
    for coord, name in zip(coords.T, dataset.keys()):
        plt.annotate(name, xy=(coord[0], coord[1]))
    plt.savefig("yay")
    
