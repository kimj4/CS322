# http://ronny.rest/blog/post_2017_08_04_glove/
import linecache
from random import *
from math import *

def makeAllPairs(linesList):
    pairs = [] # a list of tuples
    for i in range(0, len(linesList)):
        for j in range(0, len(linesList)):
            if i == j:
                pass
            elif i < j:
                # pairs.append()
                pairs.append((linesList[i], linesList[j]))
            else:
                pass
    return pairs


def findCosSimilarity(word1, word2, wordVectorDict):
    num = 0
    denom1 = 0
    denom2 = 0
    for i in range(0,50):
        num += float(wordVectorDict[word1][i])*float(wordVectorDict[word2][i])
        denom1 += float(wordVectorDict[word1][i])**2
        denom2 += float(wordVectorDict[word2][i])**2
    denom = sqrt(denom1) + sqrt(denom2)
    # print(num)
    # print(denom)
    cosSimilarity = num/denom
    # print(cosSimilarity)
    # print('between ' + word1 + ' and ' + word2)
    return cosSimilarity


def doPart1(filepath):
    gloveFileName = filepath
    numLines = sum(1 for line in open(gloveFileName))
    linesPairList = [] # contains line number
    while (len(linesPairList) < 25):
        line1 = randint(0, numLines)
        line2 = randint(0, numLines)
        while (line1 == line2):
            line1 = randint(0, numLines)
            line2 = randint(0, numLines)
        randLinePair = (line1, line2)
        if (not (randLinePair in linesPairList)):
            linesPairList.append(randLinePair)

    #line = linecache.getline('glove.6B/glove.6B.50d.txt', 500)
    #print(line)


    # make a list of words (the 25 that were randomly chosen)
    wordsPairList = []
    for linePair in linesPairList:
        word1 = linecache.getline(gloveFileName, linePair[0]).split()[0]
        word2 = linecache.getline(gloveFileName, linePair[1]).split()[0]
        wordsPairList.append((word1, word2))

    # gets the vecs for all words in the list
    wordVectorDict = {}
    for linePair in linesPairList:
        # first word in the pair
        wordVec = linecache.getline(gloveFileName, linePair[0])
        wordVectorDict[wordVec.split()[0]] = wordVec.split()[1:]

        # second word in the pair
        wordVec = linecache.getline(gloveFileName, linePair[1])
        wordVectorDict[wordVec.split()[0]] = wordVec.split()[1:]



    # get the cosine similarity between all pairs
    cosineSimilarities = [] # a list of 2-tuple where [0] is word pair and [1] is the cosine similarity
    for pair in wordsPairList:
        cosineSimilarities.append((pair, findCosSimilarity(pair[0], pair[1], wordVectorDict)))
        # ((word1, word2), cosSimilarity between them)

    sortedCosineSimilarities = sorted(cosineSimilarities, key=lambda tup: tup[1])
    for cs in sortedCosineSimilarities:
        print('word 1: ' + cs[0][0])
        print('word 2: ' + cs[0][1])
        print('cosine similarity: ' + str(cs[1]))
        print('\n')

def getSentencePairVectors(sentencePair):
    # input sentencePair is a tuple of sentences
    s1 = sentencePair[0].strip()
    s2 = sentencePair[1].strip()
    # preprocessing step: remove end-of-sentence punctuation
    if (s1[-1] in "!?."):
        s1 = s1[:-1]
    if (s2[-1] in "!?."):
        s2 = s2[:-1]

    # preprocessing step: remove commas (and maybe other punctuation)
    s1 = s1.replace(',', '')
    s1 = s1.replace('\"', '')
    s2 = s2.replace(',', '')
    s2 = s2.replace('\"', '')

    # preprocessing step: lowercase all
    s1 = s1.lower()
    s2 = s2.lower()

    # preprocessing step: tokenize on space
    s1 = s1.split(' ')
    s2 = s2.split(' ')

    # build word count dicts: {'someword': [s1 counts, s2 counts]}
    wordCountDict = {}
    for word in s1:
        if word not in wordCountDict:
            wordCountDict[word] = [1, 0]
        else:
            wordCountDict[word][0] += 1
    for word in s2:
        if word not in wordCountDict:
            wordCountDict[word] = [0, 1]
        else:
            wordCountDict[word][1] += 1


    # extract s1 and s2 vectors from the dicts
    wordCounts = list(wordCountDict.items())
    s1Vector = []
    s2Vector = []
    for wordCount in wordCounts:
        s1Vector.append(wordCount[1][0])
        s2Vector.append(wordCount[1][1])

    #
    # print('\n' + str(list(wordCountDict.items())) + '\n' )
    # print(s1Vector)
    # print(s2Vector)

    return (s1Vector, s2Vector)


def findSentenceCosineSimilarity(s1Vector, s2Vector):
     num = 0
     denom1 = 0
     denom2 = 0
     for i in range(len(s1Vector)):
         num += float(s1Vector[i]) * float(s2Vector[i])
         denom1 += float(s1Vector[i]) ** 2
         denom2 += float(s2Vector[i]) ** 2
     denom = sqrt(denom1) + sqrt(denom2)
     cosSimilarity = num / denom
     return cosSimilarity


def doPart2(filename):
    numLines = sum(1 for line in open(filename))
    linesPairList = [] # contains line number
    while (len(linesPairList) < 25):
        line1 = randint(0, numLines)
        line2 = randint(0, numLines)
        while (line1 == line2):
            line1 = randint(0, numLines)
            line2 = randint(0, numLines)
        randLinePair = (line1, line2)
        if (not (randLinePair in linesPairList)):
            linesPairList.append(randLinePair)

    sentencesPairList = []
    for linePair in linesPairList:
        s1 = linecache.getline(filename, linePair[0]).strip()
        s2 = linecache.getline(filename, linePair[1]).strip()
        sentencesPairList.append((s1, s2))

    cosineSimilarities = []
    for sentencePair in sentencesPairList:
        sentencePairVectors = getSentencePairVectors(sentencePair)
        cosineSimilarities.append((sentencePair, findSentenceCosineSimilarity(sentencePairVectors[0], sentencePairVectors[1])))

    for item in cosineSimilarities:
        print('sentence 1: ' + item[0][0]) #s1
        print('sentence 2: ' + item[0][1]) #s2
        print('cosine similarity: ' + str(item[1])) #similarity
        print('\n')


def main():
    # gloveFileName = '/Accounts/posegae/glove.6B/glove.6B.50d.txt'
    part1FileName = 'data/glove.6B.300d.txt'
    doPart1(part1FileName)

    part2FileName = 'data/Assignment_4_Input.txt'
    doPart2(part2FileName)


if __name__ == '__main__':
    main()
