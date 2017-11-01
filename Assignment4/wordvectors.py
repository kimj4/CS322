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

def main():
    # gloveFileName = '/Accounts/posegae/glove.6B/glove.6B.50d.txt'
    gloveFileName = 'data/glove.6B.50d.txt'
    numLines = sum(1 for line in open(gloveFileName))
    linesList = [] # contains line number
    while (len(linesList) < 25):
        randLine = randint(0, numLines)
        if (not (randLine in linesList)):
            linesList.append(randLine)

    #line = linecache.getline('glove.6B/glove.6B.50d.txt', 500)
    #print(line)


    # make a list of words (the 25 that were randomly chosen)
    wordsList = []
    for line in linesList:
        wordsList.append(linecache.getline(gloveFileName, line).split()[0])


    pairsList = makeAllPairs(wordsList)

    # gets the vecs for all words in the list
    wordVectorDict = {}
    for line in linesList:
        wordVec = linecache.getline(gloveFileName, line)
        # print(wordVec.split()[0])
        wordVectorDict[wordVec.split()[0]] = wordVec.split()[1:]

    # get the cosine similarity between all pairs
    cosineSimilarities = [] # a list of 2-tuple where [0] is word pair and [1] is the cosine similarity
    for pair in pairsList:
        cosineSimilarities.append((pair, findCosSimilarity(pair[0], pair[1], wordVectorDict)))
        # ((word1, word2), cosSimilarity between them)

    # for cs in cosineSimilarities:
    #     print(str(cs[0]) + ': ' + str(cs[1]))


if __name__ == '__main__':
    main()
