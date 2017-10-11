# copied from https://stackoverflow.com/questions/4576077/python-split-text-on-sentences

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
"Sentence of your choosing.",
"Another sentence of your choosing."]



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

        sentencePerplexity = (1 / sentenceProbability) ** Decimal(1 / N)
        sentencePerplexityList.append(sentencePerplexity)
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
            # print(sentence)
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

    for sentence in sentences:
        tokenized_text = nltk.word_tokenize(sentence)
        for word in tokenized_text:
            numWords += 1
            if word in wordDict:
                wordDict[word] += 1
            else:
                wordDict[word] = 1

    numUniqueWords = len(wordDict)
    writeToCSV(wordDict, 'wordFrequency.csv')
    print("number of sentences: %d" % numSentences)
    print("number of words: %d" % numWords)
    print("number of unique words: %d" % numUniqueWords)
    # TODO: check if punctuations should be counted as words
    # TODO: check if all of these are words
    # TODO: make visualization for the word frequency

    seventyThirty = dataSplit(.7, sentences)
    eightyTwenty = dataSplit(.8, sentences)
    ninetyTen = dataSplit(.9, sentences)

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


if __name__ == "__main__":
    main()
