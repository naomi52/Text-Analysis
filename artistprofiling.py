import csv
import math
import operator
from nltk.corpus import stopwords


stopWords = set(stopwords.words('english'))
singleChar = [',','?','!','(',')','[',']','\t']
text_list = []
lyrics_list =[]
text_lp_id = 3
list_of_artists = []
artist_lp_id = 0
list_of_songs = []
song_lp_id = 1
all_Songs = []
dictList = []
tfList = []
idfList = []
tfIdfFinal = []
top = 100


#functions are defined here

#same as in songprofiling functions definition

def retTF(wordDict,docWords):
    tfDict = {}
    docCount = len(docWords)
    for word,count in wordDict.items():
        tfDict[word] = count/float(docCount)
    return tfDict


def retIDF(songList):
    tfDictList = []
    listLen = len(songList)

    # For every song identify unique words
    for song in songList:
        idfDictionary = dict.fromkeys(song.keys(), 0)
        # Identify if the word occurs across  all song lyrics
        for lyrics in songList:
            for word, val in lyrics.items():
                # Conditional statement to ensure that word exists in present song evaluated
                if val>0 and word in idfDictionary:
                    idfDictionary[word] = idfDictionary[word] + 1

        for word,val in idfDictionary.items():
            # Apply the formula for idf
            idfDictionary[word] = math.log10(listLen/float(val))
        tfDictList.append(idfDictionary)
    return tfDictList


def retTFIDF(tfDocWords,idfs):
    tfidf = {}
    for word,val in tfDocWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf

#main functions

with open('sample.csv','r') as csv_file:
    songs = csv.reader(csv_file,delimiter=',')
    # Skip the header of the csv
    next(songs,None)

    for row in songs:
        for w in row:
        	line = row[text_lp_id].replace('\n','')
        	if w in singleChar or w in stopWords:
        		line = line.replace(w,'')
        text_list.append(line)

        
        list_of_artists.append(row[artist_lp_id])
        list_of_songs.append(row[song_lp_id])

    
    for lyrics in text_list:
        lWords = lyrics.split()
        all_Songs.append(lWords)
        
    for lyricWords in all_Songs:
        lyricsSet = set(lyricWords)
        lyricsSet = sorted(lyricsSet)
        wordDict = dict.fromkeys(lyricsSet,0)
        
        for word in lyricWords:
            wordDict[word]= wordDict[word] + 1
        dictList.append(wordDict.copy())
        wordDict.clear()

    for tupleList,wordsSong in zip(dictList,all_Songs):
        tempTF = retTF(tupleList,wordsSong)

        tfList.append(tempTF)
    idfList = retIDF(dictList)

    for idf,tf in zip(idfList,tfList):
        idfList.append(retTFIDF(tf,idf))

    #formatting
    sortTfIdf = []


    # FORMAT SPECIFICATIONS

    for listing in idfList:
        orderedByTfIdf = dict()
        orderedByTfIdf = sorted(listing.items(), key=operator.itemgetter(1), reverse=True)[:top];
        sortTfIdf.append(orderedByTfIdf)


    #formatting of artist profile
    artistSong = []
    artistProfile = []
    # Create a list of artist and song names to act as a key
    for artist,name in zip(list_of_artists,list_of_songs):
        artistSong.append(artist + ', Song name:' + name)


    artistProfile = zip(artistSong,sortTfIdf)

    for profile in artistProfile:
        print(profile)








