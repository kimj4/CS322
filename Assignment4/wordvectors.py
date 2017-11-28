# http://ronny.rest/blog/post_2017_08_04_glove/
import linecache
from random import *
from math import *
from pprint import pprint
NUM_PAIRS = 25

def printWordCosineSimilarities(filepath):
    englishWords = ''
    with open('data/english_words_list.txt', 'r') as f:
        englishWords = f.read()
    englishWords = englishWords.split('\n') #list of enlgish words
    onlyUseEnglishWords = True



    gloveFileName = filepath
    numLines = sum(1 for line in open(gloveFileName))
    linesPairList = [] # contains line number
    while (len(linesPairList) < NUM_PAIRS):
        line1 = randint(0, numLines)
        line2 = randint(0, numLines)
        while (line1 == line2):
            line1 = randint(0, numLines)
            line2 = randint(0, numLines)

        w1 = linecache.getline(gloveFileName, line1).split(' ')[0]
        w2 = linecache.getline(gloveFileName, line2).split(' ')[0]
        while (any(c.isdigit() for c in w1) or any(c.isdigit() for c in w2)):
            line1 = randint(0, numLines)
            line2 = randint(0, numLines)
            linecache.getline(gloveFileName, line1)
            linecache.getline(gloveFileName, line2)
            w1 = linecache.getline(gloveFileName, line1).split(' ')[0]
            w2 = linecache.getline(gloveFileName, line2).split(' ')[0]
        while ('.' in  w1 or '.' in w2):
            line1 = randint(0, numLines)
            line2 = randint(0, numLines)
            linecache.getline(gloveFileName, line1)
            linecache.getline(gloveFileName, line2)
            w1 = linecache.getline(gloveFileName, line1).split(' ')[0]
            w2 = linecache.getline(gloveFileName, line2).split(' ')[0]
        if onlyUseEnglishWords:
            while(w1 not in englishWords or w2 not in englishWords):
                line1 = randint(0, numLines)
                line2 = randint(0, numLines)
                linecache.getline(gloveFileName, line1)
                linecache.getline(gloveFileName, line2)
                w1 = linecache.getline(gloveFileName, line1).split(' ')[0]
                w2 = linecache.getline(gloveFileName, line2).split(' ')[0]

        randLinePair = (line1, line2)
        if (not (randLinePair in linesPairList)):
            linesPairList.append(randLinePair)

    # make a list of words (the 25 that were randomly chosen)
    # This is a list of 2-tuples of strings
    wordsPairList = []
    for linePair in linesPairList:
        line1 = linecache.getline(gloveFileName, linePair[0])
        word1 = line1.split()[0]
        vec1 = [float(a) for a in line1.split()[1:]]


        line2 = linecache.getline(gloveFileName, linePair[1])
        word2 = line2.split()[0]
        vec2 = [float(a) for a in line2.split()[1:]]
        wordsPairList.append( ((word1, vec1),  (word2, vec2)) )

    # get the cosine similarity between all pairs
    cosineSimilarities = [] # [((w1, w2), cs12), ...]
    for pair in wordsPairList:
        cs = findCosineSimilarity(pair[0][1], pair[1][1])
        cosineSimilarities.append( ((pair[0][0], pair[1][0]), cs) )

    sortedCosineSimilarities = sorted(cosineSimilarities, key=lambda tup: tup[1])

    for cs in sortedCosineSimilarities:
        # line_new = '{:<25}  {:<20}  {:<20}'.format(cs[1], cs[0][0], cs[0][1],)
        line_new = str(cs[1]) + '|' + cs[0][0] + ' / ' + cs[0][1]
        print(line_new)

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

    wordCounts = list(wordCountDict.items())
    s1Vector = []
    s2Vector = []
    for wordCount in wordCounts:
        s1Vector.append(wordCount[1][0])
        s2Vector.append(wordCount[1][1])

    return (s1Vector, s2Vector)


def findCosineSimilarity(s1Vector, s2Vector):
    '''
    finds cosine similarity between two vectors
    '''
    num = 0
    denom1 = 0
    denom2 = 0
    for i in range(len(s1Vector)):
        num += float(s1Vector[i]) * float(s2Vector[i])
        denom1 += float(s1Vector[i]) ** 2
        denom2 += float(s2Vector[i]) ** 2
    denom = sqrt(denom1) * sqrt(denom2)
    cosSimilarity = num / denom
    return cosSimilarity


def printSentenceCosineSimilarities(filename):
    numLines = sum(1 for line in open(filename))
    linesPairList = [] # contains line number
    while (len(linesPairList) < 25):
        line1 = randint(0, numLines)
        line2 = randint(0, numLines)
        while (line1 == line2):
            line1 = randint(0, numLines)
            line2 = randint(0, numLines)
        while (len(linecache.getline(filename, line1)) == 0 or len(linecache.getline(filename, line2)) == 0):
            print('here')
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
        cosineSimilarities.append((sentencePair, findCosineSimilarity(sentencePairVectors[0], sentencePairVectors[1])))

    sortedCosineSimilarities = sorted(cosineSimilarities, key=lambda tup: tup[1])

    for item in sortedCosineSimilarities:
        print('sentence 1: ' + item[0][0]) #s1
        print('sentence 2: ' + item[0][1]) #s2
        print('cosine similarity: ' + str(item[1])) #similarity


def main():
    part1FileName = 'data/glove.6B.300d.txt'
    printWordCosineSimilarities(part1FileName)

    part2FileName = 'data/Assignment_4_Input.txt'
    printSentenceCosineSimilarities(part2FileName)


if __name__ == '__main__':
    main()
