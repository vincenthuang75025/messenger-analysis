#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 01:39:08 2020

@author: steve
"""

"""
PSEUDOCODE / plan

what we want is a the following dictionaries
    dictionary 1 : key = word ; value = (hour in day , counts of word)
    dictionary 2 : key = word ; value = (day in week , counts of word)
    dictionary 3 : key = word ; value = (month in life, counts of word)
    dictionary 4 : key = word ; value = array of all the date-times it was uttered
    
idea 2, something we may want to analyse is the conversation lengths and reply times 
time domain feature ideas
    the average response time for one person and for the other
    the average number of words in a speech bubble


"""



import json
import os
from datetime import datetime

# makes json with timestamp array for each person, one timestamp per message / bubble / image sent
def make_timestamps_dict():
    self_name = "Marley Xiong"

    results = []
    def parse_single_person(path):
        with open(path) as f:
            data = json.load(f) 
            if (len(data['participants']) == 2): 
                # for each person, build array of timestamps 
                person_name = data['participants'][0]['name'] 
                if person_name == self_name: 
                    person_name = data['participants'][1]['name'] 
                for msg in data['messages']: 
                    if msg['sender_name'] == self_name: 
                        results.append((person_name, msg['timestamp_ms'])) 

    path = 'messages-2018-2020/inbox/'
    folder_names = os.listdir(path)
    min_bytes = 1000
    selected_folders = []

    for f in folder_names: 
        if f != '.DS_Store':
            size = os.path.getsize(path + f + '/message_1.json')
            if size > min_bytes:
                selected_folders.append(f)
    print(len(selected_folders))

    for folder in selected_folders:
        json_name = path + folder + '/message_1.json'
        parse_single_person(path=json_name)
        
    with open('timestamp_dict.json', 'w') as outfile:
        json.dump(results, outfile)


make_timestamps_dict()
# from timestamp array, makes count array for each hour between two dates


