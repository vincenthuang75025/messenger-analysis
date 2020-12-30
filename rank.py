import os
from collections import defaultdict
NUM_TOP = 50 # how many of the top chats you want
d = defaultdict(int)
rootdir = os.getcwd() + '/messages/inbox'
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if len(file) > 5 and file[-5:] == '.json':
            fin = open(subdir + '/' + file, 'r')
            count = len(fin.readlines())
            fin.close()
            d[subdir] += count

l = []
for key in d.keys():
    l.append((d[key], key))
l = sorted(l, reverse=True)
rank = 0
for x in l[:NUM_TOP]:
    rank += 1
    print("Rank: %3d     Messages: %8d    Chat name: %s"% (rank,x[0], x[1][len(rootdir):]))