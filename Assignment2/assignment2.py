'''
Solution to assignment 2
Splits up a corpus into training and test sets
Trains on the trianing set using 1, 2, 3 -grams
Tests the perplexity on those models with the test set
allows user to get MLEs on input sentences

Currently set up to take as imput HW2_InputFile_NoPunctuation.txt
    (included in submission)

At the end, there is an infinite loop for user input sentences. End with control+c

Emma Posega Rappleye, Ju Yun Kim
Carleton College
CS 322: Natural Language Processing
'''

import nltk.data
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import pprint
import random
import copy
from decimal import *
import csv
import operator
import collections

nltk.download('punkt')

testSentences = ["Please return the television to Mr. Lynch on Sunday.",
"Odysseus was 17 when he first had novocain.",
"Johnny Cash was drowning in imagery of dusty roads at night.",
"While wearing blue shoes, I took a detour to find Laura Frost, the Wizard of Python Empire.",
"I built a box for the rabbits.",
"She was wearing a leather jacket.",
"I was born in 1976 and graduated high school in 1990.",
"That explanation is irrelevant to surrealists, existentialists and film snobs for purposes of interpretation, narrative form, humorous asides and soap.",
"ummm, can they be unknowns is that acceptable umm in the description, does he say anything about handling unknowns?",
"Theres his doppelgänger who eluded the Black Lodge by copying himself like a set of keys."]


def dataSplit(trainingRatio, sentences):
    ''' splits up the data into training and test sets where trainingRatio
        is some proportion '''
    # make a copy so that the original sentences is not changed
    testSet = copy.deepcopy(sentences)
    trainingSet = []
    numTrainingSentences = round(len(sentences) * trainingRatio)
    for i in range(0, numTrainingSentences):
        # select a random sentence, pop it from the testSet, push it on the trainingSet
        randSentence = random.choice(testSet)
        trainingSet.append(randSentence)
        testSet.remove(randSentence)
    return (trainingSet, testSet)

def calculateSentencePerplexity(N, sentence, gramDict, total1Grams):
    '''
    Calculates the perplexity for a single sentence

    N -- the N in N-grams
    sentence -- a string (which should be a sentence)
    gramDict -- a dictionary containing the training n-grams counts
    total1Grams -- number of unigrams for calculating perplexity with unigrams
    '''
    sentenceNgrams = createNgram(N, [sentence])
    sentenceProbability = 1

    for ngram, count in sentenceNgrams.items():
        if (N == 1):
            # unigram probability = this unigram count / all unigram count
            ngramProbability = count / total1Grams
        else:
            # ngram probability = this ngram count / this n-1gram count
            # make the n-1gram by popping off the last word in ngram
            prevGram = ngram.split(' ')[:-1]
            prevGram = ' '.join(prevGram)

            prevGramCount = 0
            if prevGram in gramDict[str(N - 1) + "gram"]:
                prevGramCount = gramDict[str(N - 1) + "gram"][prevGram]
            else:
                # special case for handling something like <s> <s> I
                #  just use the <s> count from unigrams
                if prevGram.split(' ')[-1] == "<s>":
                    prevGramCount = gramDict["1gram"]['<s>']

            # if there's no prevGramCount, there will be no ngram count because
            # that sequence of words never appears in the training set

            if ngram in gramDict[str(N) + "gram"]:
                trainingCount = gramDict[str(N) + "gram"][ngram]
                ngramProbability = trainingCount / prevGramCount
            else:
                # arbitary small probability if the ngram is not in the training set
                ngramProbability = 0.000001

        sentenceProbability = Decimal(sentenceProbability * Decimal(ngramProbability))
        sentencePerplexity = (1 / sentenceProbability) ** Decimal(1 / (len(sentence)))
    return sentencePerplexity

def calculatePerplexity(N, trainingAndTestSets):
    ''' trainingAndTestSets: (list of training sentences, list of test setences)
        Calculates the average perplexity of sentences in the test set'''

    gramDict = {}
    total1Grams = 0

    # first create the ngram models
    for i in range(1, N + 1):
        trainingGrams = createNgram(i, trainingAndTestSets[0])
        gramDict[str(i) + "gram"] = trainingGrams
        if (i == 1):
            # if we want to calculate the perplexity of unigrams, we need the
            #  total number of unigrams
            total1Grams = sum(gramDict['1gram'].values())


    # stores the perplexity of sentences so they can be averaged later
    sentencePerplexityList = []
    # so calculate perplexity for each sentence
    for sentence in trainingAndTestSets[1]:
        sentencePerplexityList.append(calculateSentencePerplexity(N, sentence, gramDict, total1Grams))
    perplexity = sum(sentencePerplexityList) / len(sentencePerplexityList)
    return perplexity


def createNgram(N, sentences):
    '''
    N -- 1 for unigram, 2 for bigram, ...
    sentences -- a list of sentences to create ngrams on ([sentence] for a single
               sentnece)
    Returns a dictionary of ngrams and their counts of the form
        {'first ngram': 2, 'second ngram': 29, ...}
    '''
    # TODO: check if we should be passing in sentences as cleaned up sequences of words
    # sentences, testSet are lists of sentences

    nGrams = {}
    endOfGram = N - 1

    for sentence in sentences:
        if (N > 1):
            sentence = ('<s> ' * (N - 1)) + sentence + ' </s>'
        else:
            sentence = '<s> ' + sentence + ' </s>'
        sentenceList = sentence.split(' ')
        while endOfGram < (len(sentenceList)):
            s = ' '
            curNgram = sentenceList[endOfGram - N + 1: endOfGram + 1]
            curNgram = s.join(curNgram)
            if (curNgram in nGrams):
                nGrams[curNgram] += 1
            else:
                nGrams[curNgram] = 1
            endOfGram += 1
        endOfGram = N - 1
    return nGrams

def calculateMLE(sentence, N, trainingAndTestSets):
    '''
    calculates the minimum likelihood estimate on sample sentences for a model
    trained on the training set in trainingAndTestSets

    sentences -- sentence that needs the MLE
    N -- the N in N-gram
    trainingAndTestSets -- a tuple containing a division of the corpus
    '''
    # create the model on the training set
    trainingNGrams = createNgram(N, trainingAndTestSets[0])

    # create the counts for n-1
    trainingNMinusOneGrams = createNgram(N - 1, trainingAndTestSets[0])

    oneGram = createNgram(1, trainingAndTestSets[0])
    oneGramTotal = sum(oneGram.values())

    probabilityDict = {}
    for key, value in trainingNGrams.items():
        prevGram = " ".join(key.split(' ')[:-1])
        if  prevGram in trainingNMinusOneGrams:
            probabilityDict[key] = trainingNGrams[key] / trainingNMinusOneGrams[prevGram]


    # get the count to get the probability
    totalNGrams = sum(trainingNGrams.values())

    sentenceMLE = 1;
    testNGrams = createNgram(N, [sentence])
    for key, value in testNGrams.items():
        if N > 1:
            if key.split(' ')[-2] == '<s>':
                sentenceMLE = sentenceMLE * (oneGram['<s>'] / oneGramTotal) * testNGrams[key]
            elif key in probabilityDict.keys():
                # print('n-gram found')
                sentenceMLE = sentenceMLE * probabilityDict[key] * testNGrams[key]
            else:
                sentenceMLE = sentenceMLE * 0.000001
        else:
            if key in probabilityDict.keys():
                # print('n-gram found')
                # print(str(probabilityDict[key]))
                sentenceMLE = sentenceMLE * probabilityDict[key] * testNGrams[key]
            else:
                sentenceMLE = sentenceMLE * 0.000001

    return sentenceMLE

def createNgramProbabilities(N, sentences):
    '''
    creates a dictionary stores the probability of an ngram in a given corpus
    should be used for the training set
    Form:
    {'this is a 4-gram': 0.003423,
     'this is another 4-gram': 0.000002340234}
    '''

    nGramCounts = createNgram(N, sentences)
    nMinusOneGramCounts = createNgram(N - 1, sentences)



    return



def writeToCSV(wordDict, filename):
    '''
    for making word frequency visualizations
    Takes wordDict, sorts it by value in descending or into a list of tuples,
        writes each tuple as a row in the csv
    '''
    # TODO: There is a bit of a problem when the word is a comma

    sortedList = sorted(wordDict.items(), key=lambda kv: kv[1], reverse=True)
    with open(filename, 'w') as f:
        for line in sortedList:
            f.write(str(line[0]) + ',' + str(line[1]) + '\n')

def main():
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    # fp = open("HW2_InputFile.txt", 'r', encoding='UTF-8')
    fp = open("HW2_InputFile_NoPunctuation.txt", 'r', encoding='UTF-8')

    data = fp.read()
    sentences = sentence_splitter.tokenize(data)


    numSentences = len(sentences)
    numWords = 0
    wordDict = {}

    modifiedSentences = []

    for sentence in sentences:
        # get rid of end-of-sentence punctuation so that they won't be
        #  counted as words
        sentence = sentence[:-1]
        sentence = sentence.lower()
        modifiedSentences.append(sentence)
        tokenized_text = nltk.word_tokenize(sentence)
        for word in tokenized_text:
            numWords += 1
            if word in wordDict:
                wordDict[word] += 1
            else:
                wordDict[word] = 1

    sentences = modifiedSentences



    numUniqueWords = len(wordDict)
    # writeToCSV(wordDict, 'wordFrequency.csv')
    print(' ')
    print("number of sentences: %d" % numSentences)
    print("number of words: %d" % numWords)
    print("number of unique words: %d" % numUniqueWords)
    # TODO: check if punctuations should be counted as words
    # TODO: check if all of these are words
    # TODO: make visualization for the word frequency

    seventyThirty = dataSplit(.7, sentences)
    eightyTwenty = dataSplit(.8, sentences)
    ninetyTen = dataSplit(.9, sentences)

    perplexityList = [
        calculatePerplexity(1, seventyThirty),
        calculatePerplexity(2, seventyThirty),
        calculatePerplexity(3, seventyThirty),
        calculatePerplexity(1, eightyTwenty),
        calculatePerplexity(2, eightyTwenty),
        calculatePerplexity(3, eightyTwenty),
        calculatePerplexity(1, ninetyTen),
        calculatePerplexity(2, ninetyTen),
        calculatePerplexity(3, ninetyTen) ]

    bestUnigramIdx = perplexityList.index(min([perplexityList[0], perplexityList[3], perplexityList[6]]))
    bestBigramIdx = perplexityList.index(min([perplexityList[1], perplexityList[4], perplexityList[7]]))
    bestTrigramIdx = perplexityList.index(min([perplexityList[2], perplexityList[5], perplexityList[8]]))

    print(' ')
    print('unigram perplexity for 70:30 split: %s' % calculatePerplexity(1, seventyThirty))
    print(' bigram perplexity for 70:30 split: %s' % calculatePerplexity(2, seventyThirty))
    print('trigram perplexity for 70:30 split: %s' % calculatePerplexity(3, seventyThirty))
    print(' ')
    print('unigram perplexity for 80:20 split: %s' % calculatePerplexity(1, eightyTwenty))
    print(' bigram perplexity for 80:20 split: %s' % calculatePerplexity(2, eightyTwenty))
    print('trigram perplexity for 80:20 split: %s' % calculatePerplexity(3, eightyTwenty))
    print(' ')
    print('unigram perplexity for 90:10 split: %s' % calculatePerplexity(1, ninetyTen))
    print(' bigram perplexity for 90:10 split: %s' % calculatePerplexity(2, ninetyTen))
    print('trigram perplexity for 90:10 split: %s' % calculatePerplexity(3, ninetyTen))

    bestUnigramSplit = ''
    if bestUnigramIdx == 0:
        bestUnigramSplit = seventyThirty
    elif bestUnigramIdx == 3:
        bestUnigramSplit = eightyTwenty
    elif bestUnigramIdx == 6:
        bestUnigramSplit = ninetyTen

    bestBigramSplit = ''
    if bestBigramIdx == 1:
        bestBigramSplit = seventyThirty
    elif bestBigramIdx == 4:
        bestBigramSplit = eightyTwenty
    elif bestBigramIdx == 7:
        bestBigramSplit = ninetyTen

    bestTrigramSplit = ''
    if bestTrigramIdx == 2:
        bestTrigramSplit = seventyThirty
    elif bestTrigramIdx == 5:
        bestTrigramSplit = eightyTwenty
    elif bestTrigramIdx == 8:
        bestTrigramSplit = ninetyTen

    for s in testSentences:
        s = s[:-1]
        s = s.lower()
        s = s.replace(',', '')
        print(' ')
        print(s)
        print('best unigram MLE: ' + str(calculateMLE(s, 1, bestUnigramSplit)))
        print('best bigram MLE:  ' + str(calculateMLE(s, 2, bestBigramSplit)))
        print('best trigram MLE: ' + str(calculateMLE(s, 3, bestTrigramSplit)))
        print(' ')

        while(True):
            inputSentence = input('Enter a new sentence: ')
            if inputSentence[-1] not in '!?.':
                inputSentence = inputSentence + '.'
            print(' ')
            print('best unigram MLE: ' + str(calculateMLE(inputSentence, 1, bestUnigramSplit)))
            print('best bigram MLE:  ' + str(calculateMLE(inputSentence, 2, bestBigramSplit)))
            print('best trigram MLE: ' + str(calculateMLE(inputSentence, 3, bestTrigramSplit)))
            print(' ')


if __name__ == "__main__":
    main()
