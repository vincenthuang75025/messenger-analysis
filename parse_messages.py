#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 21:18:35 2020

@author: marley and denali
"""

"""
{
     name: { 
         word_counts: {
             the: 4,
             apples: 5
         }
         word_counts_self: {
         }
         total_num_words: int,
         total_num_words_self: int,
         [4, 9, 2, 3]
     }
         
}
"""

import json
import os
from collections import Counter

# import nltk
# from nltk.corpus import stopwords
# stopwords.words('english')

"""
Change the sender name and path to point to your download
"""
sender_name = "Marley Xiong"
path = 'messages-2018-2020/inbox/'
folder_names = os.listdir(path)
min_bytes = 1000
selected_folders = []
results = {}

def parse_single_person(path):
    with open(path) as f:
        data = json.load(f)
        if (len(data['participants']) == 2):
            person_name = data['participants'][0]['name']
            if person_name == sender_name:
                person_name = data['participants'][1]['name']
            print(person_name)
            word_counts = Counter()
            word_counts_self = Counter()
            for msg in data['messages']:
                if (msg['type'] == "Generic" and 'content' in msg):
                    count = Counter(msg['content'].split())
                    if msg['sender_name'] == person_name:
                        word_counts += count
                    else :
                        word_counts_self += count
                        
            results[person_name] = {'word_counts': dict(word_counts), 'word_counts_self': dict(word_counts_self)}
            
for f in folder_names: 
    if f != '.DS_Store':
        size = os.path.getsize(path + f + '/message_1.json')
        print(size)
        if size > min_bytes:
            selected_folders.append(f)
print(len(selected_folders))


for folder in selected_folders:
    json_name = path + folder + '/message_1.json'
    parse_single_person(json_name)
    
    
with open('parsed_data.json', 'w') as outfile:
    json.dump(results, outfile)