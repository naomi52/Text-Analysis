
import nltk
import sys
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd

from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
import operator
from collections import OrderedDict

with open(sys.argv[1], 'r') as mycsv:
    songList=csv.reader(mycsv)

#Taking input from the command line
my_file = sys.argv[1]
df = pd.read_csv(my_file)
lyrics = df['text']
songprofiles = []
counter = 0
firstSong = int(sys.argv[2])
secondSong = int(sys.argv[3])

#myvariables
myList = []
firstItem = 0
secondItem = 0
songWords1 = []
songWords2 = []
stopWords = set(stopwords.words("english"))
punctuations = set(punctuation)
stopWords.add("...")
stopWords.add("'m")
stopWords.add("'d")
stopWords.add("'ll")
stopWords.add("'ve")
stopWords.add("'s")
stopWords.add("'re")

myList.append(lyrics[firstSong])
myList.append(lyrics[secondSong])

while counter < 2:
    #countOfSong = countOfSong + 1
    ourDict = {}
    tfidf = TfidfVectorizer()
    #Convert to String
    response = tfidf.fit_transform([myList[counter]])
    feature_names = tfidf.get_feature_names()

    for col in response.nonzero()[1]:
     ourDict[feature_names[col]] = response[0, col]

    newDict = {}
    newerDict = {}
    for key in ourDict:
        if key not in stopWords:
            newDict[key] = ourDict[key]

    sorted_x = sorted(newDict.items(), key = operator.itemgetter(1), reverse = True)
    newerDict = OrderedDict(sorted_x)
    songprofiles.append(newerDict)
    counter = counter + 1

firstSongList = songprofiles[0].keys()
secondSongList = songprofiles[1].keys()
while firstItem < 50 and firstItem < firstSongList.__len__():
    #songWords1.append(list(firstSongList)[firstItem])
    songWords1.append(list(firstSongList)[firstItem])
    firstItem = firstItem + 1

while secondItem < 50 and secondItem < secondSongList.__len__():
    #songWords1.append(list(secondSongList)[secondItem])
    songWords2.append(list(secondSongList)[secondItem])
    secondItem = secondItem + 1


#JACCARD INDEX
inter = set(songWords1).intersection(songWords2)
union = float(songWords1.__len__() + songWords2.__len__() - len(inter))
jaccIndex = inter.__len__()/union

print("Songs jaccard index = %f" %jaccIndex)
