import csv;
import math;
import operator;
import sys
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

#declaring our variables
stopWords = set(stopwords.words('english')) 

#1) Text column variables
allTexts = []
list_of_lyrics =[]
text_column_id = 3
song_column_id = 1

#2)calculation lists
all_Songs = []
song_list = []
tfIdfList = []
tfList = []
idfList = []
wordFreqList = []
tfidf = {}

#function definition
'''computeTF takes a dictionary(matching words to count) and a document of words
and computes the term frequency of the words in the dictionary,
and then puts it in a new dictionary that takes the word as the key and value
is its frquency'''

def computeTF(uniqueWordDict,docOfWords):
    tfDict = {}
    documentCount = len(docOfWords)
    for word,count in uniqueWordDict.items():
        tfDict[word] = count/float(documentCount)
    return tfDict

#this calculates the IDF using the df and the equation from class'''
def computeIDF(ListOfSongs):
    tfFreqList = []
    listLength = len(ListOfSongs)
	#for every song in the csv file, find the unique words
    for song in ListOfSongs:
        idfDict = dict.fromkeys(song.keys(), 0)
        #identifies the common words across the lyrics
        for lyrics in ListOfSongs:
            for word, valu in lyrics.items():
                if valu>0 and word in idfDict:
                    idfDict[word] = idfDict[word] + 1
        for word,valu in idfDict.items():
           #formula for idf is defined here
            idfDict[word] = math.log10(listLength/float(valu))
        tfFreqList.append(idfDict)
    return tfFreqList

#complete combination function for TFIDF



def computeTFIDF(tfDocWords,wordIdfs):
    for word,valu in tfDocWords.items():
        tfidf[word] = valu * wordIdfs[word]
    return tfidf
'''
myInputFile = sys.stdin
df = pd.read_csv(myInputFile)
'''
#<----computation happens here------->

with open('sample.csv','r') as csv_file:
    songs = csv.reader(csv_file,delimiter=',')
    # Skip the header of the csv
    next(songs,None)



    for row in songs:
        line = row[text_column_id].replace('\n','')
        for w in row:
        	if w.lower() in stopWords:
        		line = line.replace(w,'')
        allTexts.append(line)
        song_list.append(row[song_column_id]) 	
    #split the lyrics into individual words
    for lyrics in allTexts:
        lWords = lyrics.split()
        all_Songs.append(lWords)
    #Using a set to eliminate duplicates
    for lyricWords in all_Songs:
        lyricsSet = set(lyricWords)
        lyricsSet = sorted(lyricsSet)
        #A dictionary of unique words is made mapping a word to its word count
        uniqueWordDict = dict.fromkeys(lyricsSet,0)
        #counting occurrences of sigle words
        for word in lyricWords:
            uniqueWordDict[word]= uniqueWordDict[word] + 1
        # Append dictionary pairing(word,wordCount) to list
        wordFreqList.append(uniqueWordDict.copy())
        uniqueWordDict.clear()
        
    # Determine the total frequency score of each dictionary pairing in the list
    for tupleList,wordsSong in zip(wordFreqList,all_Songs):
        tempTF = computeTF(tupleList,wordsSong)

        tfList.append(tempTF)

    # Determine IDF across all songs of a given word
    idfList = computeIDF(wordFreqList)

    # Determine final Results (tf-idf) for each song
    for idf,tf in zip(idfList,tfList):
        idfList.append(computeTFIDF(tf,idf))

    # VARIABLES FOR FORMATTING
    sortTfIdf = []
    top = 50

    # FORMAT SPECIFICATIONS

    for listing in idfList:
        orderedByTfIdf = dict()
        orderedByTfIdf = sorted(listing.items(), key=operator.itemgetter(1), reverse=True)[:top]
        sortTfIdf.append(orderedByTfIdf)

    #for tfidf in sortTfIdf:
       # print(tfidf)
        
    # CREATION OF SONG PROFILE

    # Variables for formatting of artist profile
    songProfile = []	#formerly artistProfile
    songProfile = zip(song_list, sortTfIdf)
    
    for profile in songProfile:
    	print(profile)
    
    
    
