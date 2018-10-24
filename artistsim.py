import nltk
import sys
import csv
#import
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
import operator
from collections import OrderedDict


#my variables
myCount = 0
x = 0
myVar = 0
ListOfUniqueArtists = []
IndexOfUniqueWords = []
firstInd = 0
secInd = 0

#main function
#taking the argument from the command line
with open(sys.argv[1], 'r') as songdata:
    songList=csv.reader(songdata)
my_file = sys.argv[1]
df = pd.read_csv(my_file)
myIndex_1 = int(sys.argv[2]) - 1
myIndex_2 = int(sys.argv[3]) - 1

artistList = df['artist']
lyricList = df['text']
listLength = artistList.__len__()
profileList = []

myList = []
myList.append(myIndex_1)
myList.append(myIndex_2)
#defining additional stop words
stopWords = set(stopwords.words("english"))
punctuations = set(punctuation)
stopWords.add("...")
stopWords.add("'s")
stopWords.add("'m")
stopWords.add("'ll")
stopWords.add("'ve")
stopWords.add("'d")
stopWords.add("'re")


while x< listLength:
     if artistList[x] not in ListOfUniqueArtists:
         ListOfUniqueArtists.append(artistList[x])
         IndexOfUniqueWords.append(x)
     x = x + 1

#Get the profile of both artists
theDict = {}
myIndex = 0
profileList = []
while myIndex < 2:
    thisArtistSongs = []
    current = IndexOfUniqueWords[myList[myIndex]]
    while current < listLength and artistList[current] == artistList[IndexOfUniqueWords[myList[myIndex]]]:
        thisArtistSongs.append(lyricList[current])
        current = current+1
    myIndex = myIndex + 1

    ourDict = {}
    tfidf = TfidfVectorizer()
    # Convert to String
    response = tfidf.fit_transform(thisArtistSongs)
    feature = tfidf.get_feature_names()

    for col in response.nonzero()[1]:
        ourDict[feature[col]] = response[0, col]

    freshDict = {}
    fresherDict = {}
    for key in ourDict:
        if key not in stopWords:
            freshDict[key] = ourDict[key]

    sorted_x = sorted(freshDict.items(), key=operator.itemgetter(1), reverse=True)
    fresherDict = OrderedDict(sorted_x)
    profileList.append(fresherDict)

firstList = profileList[0].keys()
secondSongs = profileList[1].keys()
firstSongs = []
wordsSong2 = []

while firstInd < 100 and firstInd < firstList.__len__():
    firstSongs.append(list(firstList)[firstInd])
    firstInd = firstInd + 1

while secInd < 100 and secInd < secondSongs.__len__():
    wordsSong2.append(list(secondSongs)[secInd])
    secInd = secInd + 1

between = set(firstSongs).intersection(wordsSong2)
joined = float(firstSongs.__len__() + wordsSong2.__len__() - len(between))
jaccardIndex = between.__len__()/joined

print("Artists jaccard index is = %f" %jaccardIndex)

