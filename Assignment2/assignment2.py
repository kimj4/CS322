# copied from https://stackoverflow.com/questions/4576077/python-split-text-on-sentences

import nltk.data
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import pprint
import random
import copy
nltk.download('punkt')
# tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def dataSplit(trainingRatio, sentences):
    trainingSet = []
    testSet = []
    numTrainingSentences = round(len(sentences) * trainingRatio)
    for i in range(0, numTrainingSentences):
        randSentence = random.choice(sentences)
        trainingSet.append(randSentence)
        sentences.remove(randSentence)
    testSet = copy.deepcopy(sentences)
    return (trainingSet, testSet)

def createNgram(N, trainingSet, testSet):





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
    pprint.pprint(wordDict)
    # TODO: check if punctuations should be counted as words
    # TODO: check if all of these are words
    # TODO: make visualization for the word frequency

    seventyThirty = dataSplit(.7, sentences)
    eightyTwenty = dataSplit(.8, sentences)
    ninetyTen = dataSplit(.9, sentences)

    for i in range(1, 3):
        createNgram(i, seventyThirty[0], seventyThirty[1])
        createNgram(i, eightyTwenty[0], eightyTwenty[1])
        createNgram(i, ninetyTen[0], ninetyTen[1])




if __name__ == "__main__":
    main()
