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
                'You did not know me.',
                'Then you fell in love with me.',
                'Now you know me.',
                'I need to go take a shower.',
                'I can not tell if I am crying.',
                'I just spent 7 hours playing with fonts.']

transductionLexicon = {
    '7':'7',
    'this':'esto',
    'the':'el',
    'a':'un',
    'any':'cualquier',
    'all':'todo',
    'like':'como',
    'with':'con',
    'out':'fuera',
    'of':'de',
    'in':'en',
    'with':'con',
    'if':'si',
    'terrible':'terrible',
    'worst':'peor',
    'can':'puede',
    'everything':'todo',
    'leak':'fuga',
    'goodness':'bondad',
    'love':'amor',
    'shower':'ducha',
    'running':'corriendo',
    'hours':'horas',
    'fonts':'fuentes',
    'I':'yo',
    'me':'yo',
    'it':'ello',
    'you':'usted',
    'sometimes':'a veces',
    'just':'solo',
    'slowly':'lentamente',
    'now':'ahora',
    'then':'entonces',
    'not':'no',
    'to':'a',
    'know':'saber',
    'go':'ir',
    'take':'tomar',
    'tell':'decir',
    'was':'era',
    'started':'comenzo',
    'did':'hizo',
    'fell':'cayo',
    'spent':'gastado',
    'crying':'llorando',
    'playing':'jugando',
    'born':'nacido',
    'spilled':'derramado',
    'gone':'ido',
    'hate':'odio',
    'feel':'sentir',
    'know':'saber',
    'need':'necesidad',
    'am':'soy',
    'is':'es'
}

translationGoldStandard = [
    'Odio esto.',
    'Correr es terrible.',
    'Todo es lo peor.',
    'A veces siento que nací con una fuga.',
    'Cualquier bondad que empecé con sólo se derramó fuera de mí.',
    'Ahora todo se ha ido.',
    'No me conoces.',
    'Entonces te enamoraste de mi.',
    'Ahora me conoces.',
    'Necesito ir a bańarme.',
    'No puedo decir si estoy llorando.',
    'Acabo de pasar 7 horas jugando con las fuentes.'
]


def testPyStatParser():
    from stat_parser import Parser
    parser = Parser()
    with open('ggg.txt', 'w') as f:
        for sentence in part1Corpus:
            f.write(str(parser.parse(sentence)))
            f.write(' \n')
        # print(parser.parse(sentence))

def wordForWordTranslation(sentence):
    words = sentence.strip()[:-1].split(' ')
    translation = []
    for word in words:
        if word == 'I':
            translation.append(transductionLexicon[word])
        elif word == 'didn’t':
            translation.append(transductionLexicon['did'])
            translation.append(transductionLexicon['not'])
        else:
            if word.lower() in transductionLexicon:
                translation.append(transductionLexicon[word.lower()])
            else:
                pass

    translation[0] = translation[0][0].upper() + translation[0][1:]
    transSentence = ' '.join(translation)
    transSentence += '.'
    return transSentence



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

    # with open('g.txt', 'w') as f:
    #     for wordList in sentenceWords:
    #         pos_list = pos_tag(wordList)
    #         to_write = ''
    #         for p in pos_list:
    #             to_write = to_write + p[1] + ' '
    #         to_write += '\n'
    #         f.write(to_write)

    testPyStatParser()

    translatedSentences = []
    with open('translations.txt', 'w') as f:
        for sentence in sentences:
            # print(wordForWordTranslation(sentence))
            f.write(wordForWordTranslation(sentence) + '\n')
            translatedSentences.append(wordForWordTranslation(sentence))

    for i in range(len(translatedSentences)):
        BLEUscore = nltk.translate.bleu_score.sentence_bleu([translationGoldStandard[i].split(' ')], translatedSentences[i].split(' '))
        print(BLEUscore)


    grammar = nltk.CFG.fromstring("""
        S -> ADVP ADVP VP
        S -> VP
        S -> NP VP
        S -> ADVP NP VP
        VP -> VBP VB NP
        VP -> VB NP
        PP -> IN NP
        VP -> ADVP VBD S
        S -> NP NP VP
        S -> ADVP S S
        NP -> DT
        SBARS -> NP VP
        NP -> NN
        NP -> NNS
        VP -> VBD SBAR
        NP -> PRP
        NP -> DT NN
        SVP -> TO VP
        ADVP -> RB
        ADJP -> DT JJS
        PRT -> RP
        NP -> CD NNS
        VP -> VBZ NP
        VP -> MD RB VB SBAR
        VP -> VBG VBZ ADJP
        VP -> VBD VBN PP
        VP -> VBG
        VP -> VBD
        VP -> VBM PRT PP
        VP -> VBG PP
        VP -> VBZ VP
        VP -> VBD RB VB NP
        VP -> VBP SVP
        VP -> VB VB NP
        ADJP -> JJ
        SBAR -> IN S
        VP -> PP PP
        NNS -> 'hours' | 'fonts'
        DT -> 'this' | 'all' | 'a' | 'the' | 'any'
        RB -> 'slowly' | 'just' | 'not' | 'now' | 'sometimes' | 'then'
        PRP -> 'me' | 'i' | 'you' | 'it'
        VBD -> 'fell' | 'spent' | 'was' | 'started' | 'did'
        VBP -> 'feel' | 'need'
        NN -> 'leak' | 'love' | 'gone' | 'goodness' | 'shower'
        IN -> 'with' | 'of' | 'in' | 'if'
        RP -> 'out'
        VBG -> 'everything' | 'playing' | 'is' | 'crying' | 'running'
        VBN -> 'born'
        VBZ -> 'is' | 'am'
        CD -> '7'
        VB -> 'know' | 'hate' | 'go' | 'like' | 'take' | 'tell'
        JJ -> 'terrible'
        JJS -> 'worst'
        VBM -> 'spilled'
        TO -> 'to'
        MD -> 'can'
    """)

    parser = nltk.ChartParser(grammar)
    for sentence in sentences:
        # sList = []
        # words = sentence[:-1].split(' ')
        # for word in words:
        #     if word == 'I':
        #         sList.append('I')
        #     else:
        #

        print('\n')
        print(sentence)
        for tree in parser.parse(sentence[:-1].lower().split(' ')):
            print(tree)
        print('\n')


    # viterbi_parser = nltk.ViterbiParser(grammar)
    # parser = nltk.ChartParser(grammar)
    # for tree in parser.parse(['I', 'need', 'to', 'go', 'take', 'a', 'shower']):
    # #     print(tree)
    # for p in grammar.productions():
    #     print(p)
    #     for sentence in generate(grammar, depth=5, start=str(p)):
    #         print(' '.join(sentence))
    loweredSentences = []
    for s in sentences:
        loweredSentences.append(s.lower()[:-1])

    print(loweredSentences)

    counter = 0
    for sentence in generate(grammar, depth=10):
        counter += 1
        if ' '.join(sentence) in loweredSentences:
            print(sentence)
        if counter % 10000 == 0:
            print(counter)






if __name__ == '__main__':
    main()
