
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



# %%
# Load json file
with open('data/parsed_data.json') as json_file:
    data = json.load(json_file) 

BAG_OF_WORDS_ALL = []
BAG_OF_WORDS_PER_CONV = {}
for i in data:
    BAG_OF_WORDS_PER_CONV[i] = []
    for j in data[i]['word_couts']:
        BAG_OF_WORDS_ALL.append(j)
        BAG_OF_WORDS_PER_CONV[i].append(j)
    for j in data[i]['word_couts_self']:
        BAG_OF_WORDS_ALL.append(j)
        BAG_OF_WORDS_PER_CONV[i].append(j)
        
    # remove dups
    BAG_OF_WORDS_PER_CONV[i] = set(BAG_OF_WORDS_PER_CONV[i])
BAG_OF_WORDS_ALL = set(BAG_OF_WORDS_ALL)


    

# with open('~/Documents/code/facebook/parsed_data.json') as json_file:
#     data = json.load(json_file)
    
# %%
    
for conv in data:
    data[conv]
    
# def computeTF(wordDict,bagOfWords)

# TF-IDF
WORDS = # all the words in the corpus
N = # Total number of documents
tf_score = # dictionary | word : tf-score
idf_score



