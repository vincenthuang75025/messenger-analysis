
# %%  IMPORTS

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json


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
def compute_idf(data,bag_of_words_corpus):
    idf_dict = {}
    
    def is_in(word,document): # binary
        if word in document.keys():
            return 1 
        return 0 
    
    for word in bag_of_words_corpus.keys():
        n = len(data)
        df_t = 0
        for name in data.keys():
            if word in data[name]['word_counts'].keys():
                df_t+=1
        idf_dict[word] = math.log(n/df_t) 
    return idf_dict

# takes data and bag of words of entire corpus (dic w/ key = word, value = freq)
def get_tfidf_dict(data,bag_of_words_corpus):
    tfidf_dict = {}
    idf_dict = compute_idf(data,bag_of_words_corpus)
    for name in data.keys():
        tfidf_dict[name] = {}
        tf_dict = compute_tf(data[name]["word_counts"]) 
        for word,idf_score in idf_dict.items():
            if word in tf_dict:
                tfidf_score = idf_score * tf_dict[word] 
                tfidf_dict[name][word] = tfidf_score 
    return tfidf_dict 
            
# retunrs dic key = word ; value = freq net 
def get_bag_of_words_them(data):
    bag_of_words_all_them = {}
    for name in data:
        for word,n in data[name]['word_counts'].items():
            if word in bag_of_words_all_them:
                bag_of_words_all_them[word]+= n
            else:
                bag_of_words_all_them[word]=n
    return bag_of_words_all_them
    
def get_bag_of_words_me(data):
    return

def get_bag_of_words_all(data):
    return

    



# with open('~/Documents/code/facebook/parsed_data.json') as json_file:
#     data = json.load(json_file)
    
# %%
    
if __name__ == "__main__":
    # Load json file
    with open('parsed_data.json') as json_file:
        data = json.load(json_file) 
        
    # THE CORPUS IS ALL THE PEOPLE WHO MESSAGE YOU 
    words_all = get_bag_of_words_them(data)
    # idf_dict = compute_idf(data,words_all) 
    tfidf_dict = get_tfidf_dict(data,words_all)
    
    
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
    