# copied from https://stackoverflow.com/questions/4576077/python-split-text-on-sentences

import nltk.data
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import pprint
import random
import copy
from decimal import *
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


def calculatePerplexity(N, trainingAndTestSets):
    ''' trainingAndTestSets: (list of training sentences, list of test setences)
        Calculates the average perplexity of sentences in the test set'''

    gramDict = {}
    total1Grams = 0

    # special case for handling unigrams
    for i in range(1, N + 1):
        trainingGrams = createNgram(i, trainingAndTestSets[0])
        gramDict[str(i) + "gram"] = trainingGrams
        if (i == 1):
            # if we want to calculate the perplexity of unigrams, we need the
            #  total number of unigrams
            total1Grams = sum(gramDict['1gram'].values())


    sentencePerplexityList = []
    # TODO iterate through 1 through N
    for sentence in trainingAndTestSets[1]:
        sentenceNgrams = createNgram(N, [sentence])
        sentenceProbability = 1

        for ngram, count in sentenceNgrams.items():
            if (N == 1):
                # unigram probability is the count of that unigram / count of all unigrams
                ngramProbability = count / total1Grams
            else:
                # get count of preceding words in ngram
                prevWords = ngram.split(' ')[0:N-1]
                prevWords = ' '.join(prevWords)
                # TODO change n to curval when you change the prev todo
                prevWordsCount = 0
                if prevWords in gramDict[str(N - 1) + "gram"]:
                    prevWordsCount = gramDict[str(N - 1) + "gram"][prevWords]
                else:
                    if prevWords.split(' ')[-1] == "<s>":
                        prevWordsCount = gramDict["1gram"]['<s>']

                # if there's no prevWordsCount, there will be no ngram count because
                # that sequence of words never appears in the training set


                if ngram in gramDict[str(N) + "gram"]:
                    trainingCount = gramDict[str(N) + "gram"][ngram]

                    ngramProbability = trainingCount / prevWordsCount
                else:
                    ngramProbability = 0.000001

            sentenceProbability = Decimal(sentenceProbability * Decimal(ngramProbability))

        sentencePerplexity = (1/sentenceProbability)**Decimal(1/N)
        sentencePerplexityList.append(sentencePerplexity)
    perplexity = sum(sentencePerplexityList) / len(sentencePerplexityList)
    # print(perplexity)
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
    eightyTwenty = dataSplit(.8, sentences)
    ninetyTen = dataSplit(.9, sentences)
    #
    # for i in range(1, 4):
    #     seventyThirtyGrams.append(createNgram(i, seventyThirty[0]))
    #     eightyTwentyGrams.append(createNgram(i, eightyTwenty[0]))
    #     ninetyTenGrams.append(createNgram(i, ninetyTen[0]))
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
