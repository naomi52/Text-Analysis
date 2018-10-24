
#!/usr/bin/pythonw
#x = 1
#if x == 1:
    # indented four spaces
from __future__ import division
import csv
import nltk
import sys
import operator
import matplotlib.pyplot as plt
import numpy as np
import itertools

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
#from stop_words 
from itertools import islice
import pandas as pd

'''
with open(sys.argv[1], 'r') as songdata:
    reader=csv.reader(songdata)
'''

lyrics = " "
stop_words = set(stopwords.words('english'))
totaluniquewords = 0
myavnumofwords = 0.0
myav = 0
keys = []
values = []
myfiltereddic = {}

'''
my_file = sys.argv[1]
df = pd.read_csv(my_file)
'''
my_file = sys.stdin
df = pd.read_csv(my_file)

def numOfArtists():
    artistcount = df['artist'].nunique()
    return artistcount
def numOfSongs():
    songcount = df['song'].nunique()
    return songcount
    
def avgNumOfSongs():
    avgsongperartist = numOfSongs()/numOfArtists()
    return avgsongperartist
    
def avgNumOfWords():
    totaluniquewords = 0
    for row in df['text']:
        lyrics = word_tokenize(row)
        l = set(lyrics)
        filtered = [w for w in l if not w in stop_words]
        filtered = []
        for w in l:
            if w not in stop_words:
                filtered.append(w)
        filtered2 = []
        for ww in filtered:
            if len(ww) != 1:
                filtered2.append(ww)
        totaluniquewords += len(filtered2)
    myavnumofwords = totaluniquewords/numOfSongs()
    return myavnumofwords
    
def pairsOfArtistAvgNumOfWords():
    myav = 0
    mydic = {}
    grouped = sorted(df.groupby('artist'))
    for name, group in grouped:
        for row_number, row in group.iterrows():
            lyricsa = word_tokenize(row['text'])
            la = set(lyricsa)
            filtered11 = [w for w in la if not w in stop_words]
            filtered11 = []
            for w in la:
                if w not in stop_words:
                    filtered11.append(w)
            filtered22 = []
            for ww in filtered11:
                if len(ww) != 1:
                    filtered22.append(ww)
            myav += len(filtered22)
        heyo = group['artist'].count()
        myav = myav/heyo
        mydic.update({name:myav})
        #print ("Artist:  " + name)
        #print ("my count is: " +str(heyo))
        #print("my av is: " +str(myav))
        myav = 0
    return mydic
def plotChart():
    sorted_x = dict(sorted(pairsOfArtistAvgNumOfWords().items(), key=operator.itemgetter(1))[:10])
  
    
    for key in sorted_x:
        print(key)
        keys.append(key)
        print (sorted_x[key])
        values.append(sorted_x[key])
   
    
    y_pos = np.arange(len(keys))
    plt.bar(y_pos, values, align='center', alpha=0.5)    
    plt.xticks(y_pos, keys, fontsize=5, wrap=True)
    plt.xlabel('Artist/Band')
    plt.ylabel('AverageNoOfSongs')
    plt.title('Top 10 Pairs')
    plt.show()
    
    
    
#-----------------RUNNING START------------------------------------------
'''
print("The number of artists in the collection: " + str(numOfArtists()))
print("The number of songs in the collection: " + str(numOfSongs()))
print("The average number of songs per artist is : " + str(avgNumOfSongs()))
print ("The average is: " + str(avgNumOfWords()))
print(pairsOfArtistAvgNumOfWords())
'''
plotChart()

#-------------------RUNNNING END-----------------------------------------

 


    
    
     
