# http://ronny.rest/blog/post_2017_08_04_glove/
import linecache
from random import *
from math import *

def findCosSimilarity(word1, word2, wordVectorDict):
    num = 0
    denom1 = 0
    denom2 = 0
    for i in range(0,50):
        num += float(wordVectorDict[word1][i])*float(wordVectorDict[word2][i])
        denom1 += float(wordVectorDict[word1][i])**2
        denom2 += float(wordVectorDict[word2][i])**2
    denom = sqrt(denom1) + sqrt(denom2)
    print(num)
    print(denom)
    cosSimilarity = num/denom
    print(cosSimilarity)
    print('between ' + word1 + ' and ' + word2)

def main():
    gloveFileName = '/Accounts/posegae/glove.6B/glove.6B.50d.txt'
    numLines = sum(1 for line in open(gloveFileName))
    linesList = []
    while (len(linesList) < 25):
        randLine = randint(0, numLines)
        if (not (randLine in linesList)):
            linesList.append(randLine)

    #line = linecache.getline('glove.6B/glove.6B.50d.txt', 500)
    #print(line)
    wordVectorDict = {}
    for line in linesList:
        wordVec = linecache.getline(gloveFileName, line)
        print(wordVec.split()[0])
        wordVectorDict[wordVec.split()[0]] = wordVec.split()[1:]

    print(wordVectorDict)
    findCosSimilarity(list(wordVectorDict.keys())[0], list(wordVectorDict.keys())[1], wordVectorDict)


if __name__ == '__main__':
    main()
