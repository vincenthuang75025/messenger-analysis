#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# makes json with timestamp array for each person, one timestamp per message / bubble / image sent


import json
import os
from datetime import datetime

# modify below
self_name = "Marley Xiong"
path = 'messages_3/inbox/'
##

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
    try:
        json_name = path + folder + '/message_2.json'
        parse_single_person(path=json_name)
    except:
        pass

with open('timestamp_dict_3.json', 'w') as outfile:
    json.dump(results, outfile)
