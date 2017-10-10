# copied from https://stackoverflow.com/questions/4576077/python-split-text-on-sentences

import nltk.data
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import pprint
import random
import copy
nltk.download('punkt')
# tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

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

def prod(lst, excludeSmallNumbers):
    smallNums = 0
    p = 1
    for item in lst:
        if excludeSmallNumbers:
            if item <= 0.000001:
                smallNums += 1
            else:
                p *= item
        else:
            p *= item

    if excludeSmallNumbers:
        print('there were ' + str(smallNums) + ' small numbers')
    return p



def calculatePerplexity(N, trainingAndTestSets):
    ''' trainingAndTestSets: (list of training sentences, list of test setences)
        Calculates the perplexity for a given data split and N '''
    trainingGrams = createNgram(N, trainingAndTestSets[0])
    trainingGramsTotal = sum(trainingGrams.values())

    testGrams = createNgram(N, trainingAndTestSets[1])

    probabilities = {}
    for key, value in testGrams.items():
        if (not key in trainingGrams.keys()):
            # if the training set had no instance of this ngram
            probabilities[key] = 0.000001
        else:
            probabilities[key] = (trainingGrams[key] / trainingGramsTotal) * value


    # print(probabilities)
    p = prod(probabilities.values(), True)
    # print()
    perplexity = (1.0 / p) ** (1.0 / N)
    print(str(perplexity))



def createNgram(N, sentences):
    # TODO: check if we should be passing in sentences as cleaned up sequences of words
    # sentences, testSet are lists of sentences

    nGrams = {}

    endOfGram = N - 1


    for sentence in sentences:
        if (N > 1):
            sentence = ('<s> ' * (N - 1)) + sentence + ' </s>'
            # print(sentence)
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

def main():
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)


    fp = open("HW2_InputFile.txt", 'r', encoding='UTF-8')
    data = fp.read()
    sentences = sentence_splitter.tokenize(data)
    # print ('\n-----\n'.join(tokenizer.tokenize(data)))

    numSentences = len(sentences)
    numWords = 0
    wordDict = {}

    for sentence in sentences:
        print (sentence + '\n')
        tokenized_text = nltk.word_tokenize(sentence)
        for word in tokenized_text:
            numWords += 1
            if word in wordDict:
                wordDict[word] += 1
            else:
                wordDict[word] = 1

    numUniqueWords = len(wordDict)
    # print(len(sentences))
    print(numSentences)
    print(numWords)
    print(numUniqueWords)
    # pprint.pprint(wordDict)
    # TODO: check if punctuations should be counted as words
    # TODO: check if all of these are words
    # TODO: make visualization for the word frequency


    # list containing n-gram models
    # seventyThirtyGrams = []
    # eightyTwentyGrams = []
    # ninetyTenGrams = []
    #
    seventyThirty = dataSplit(.7, sentences)
    # eightyTwenty = dataSplit(.8, sentences)
    # ninetyTen = dataSplit(.9, sentences)
    #
    # for i in range(1, 4):
    #     seventyThirtyGrams.append(createNgram(i, seventyThirty[0]))
    #     eightyTwentyGrams.append(createNgram(i, eightyTwenty[0]))
    #     ninetyTenGrams.append(createNgram(i, ninetyTen[0]))
    calculatePerplexity(1, seventyThirty)





if __name__ == "__main__":
    main()
