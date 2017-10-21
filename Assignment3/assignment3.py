import nltk.data
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import pprint
import random
import copy
from decimal import *
import csv
import operator
import collections

from nltk.tokenize import wordpunct_tokenize
from nltk import pos_tag
from nltk import CFG
from nltk.parse.generate import generate, demo_grammar


nltk.download('averaged_perceptron_tagger')


part1Corpus = ['I hate this.',
                'Running is terrible.',
                'Everything is the worst.',
                'Sometimes I feel like I was born with a leak.',
                'Any goodness I started with just slowly spilled out of me.',
                'Now it is all gone.',
                'You didn’t know me .',
                'Then you fell in love with me.',
                'Now you know me.',
                'I need to go take a shower.',
                'I can not tell if I am crying.',
                'I just spent 7 hours playing with fonts.']



def main():
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    sentences = part1Corpus


    numSentences = len(sentences)
    numWords = 0
    wordDict = {}

    modifiedSentences = []

    # list of lists of words for each sentence
    sentenceWords = []

    for sentence in sentences:
        sentenceWords.append(wordpunct_tokenize(sentence))

    for wordList in sentenceWords:
        print(str(pos_tag(wordList)) + '\n' )


    # grammar = CFG.fromstring(demo_grammar)



if __name__ == '__main__':
    main()
