import re

def runTwitterTest(regexString, inputFile):
    fd = open(inputFile, 'r', encoding='UTF-8')
    falsePositive = 0
    falseNegative = 0
    truePositive = 0
    trueNegative = 0
    for line in fd:
        regReturn = re.search(regexString, line)
        if (regReturn):
            if ('T' in line.split(',')[1]):
                truePositive +=1
                # print('correct')
            else:
                falsePositive += 1
                # print('incorrect')
        else:
            if ('T' in line.split(',')[1]):
                falseNegative +=1
                # print('correct')
            else:
                trueNegative += 1
                # print('incorrect')

    print('true positive: ' + str(truePositive))
    print('true negative: ' + str(trueNegative))
    print('false positive: ' + str(falsePositive))
    print('false negative: ' + str(falseNegative))

def runInstagramTest(regexString, inputFile):
    fd = open(inputFile, 'r', encoding='UTF-8')
    falsePositive = 0
    falseNegative = 0
    truePositive = 0
    trueNegative = 0
    for line in fd:
        regReturn = re.search(regexString, line)
        if (regReturn):
            if ('I' in line.split(',')[1]):
                truePositive +=1
            else:
                falsePositive += 1
        else:
            if ('I' in line.split(',')[1]):
                falseNegative +=1
                # print('correct')
            else:
                trueNegative += 1
                # print('incorrect')

    print('true positive: ' + str(truePositive))
    print('true negative: ' + str(trueNegative))
    print('false positive: ' + str(falsePositive))
    print('false negative: ' + str(falseNegative))


def main():
    twitterRegex1 = '@[a-zA-Z0-9_]{1,15}'
    twitterRegex2 = '^(?!.*(A|a)+(D|d)+(M|m)+(I|i)+(N|n)+)^(?!.*(T|t)+(W|w)+(I|i)+(T|t)+(T|t)+(E|e)+(R|r)+)@[a-zA-Z0-9_]{1,15}'
    twitterRegex3 = '^(?!.+@.*)^(?!.*[%$()\^\-~\.\*\!\?\#\&"].*)^(?!.*(A|a)+(D|d)+(M|m)+(I|i)+(N|n)+)^(?!.*(T|t)+(W|w)+(I|i)+(T|t)+(T|t)+(E|e)+(R|r)+)@[a-zA-Z0-9_]{1,15}'
    testDivider = '~~~~~~~~~~~~~~~~~~'

    print(testDivider)
    runTwitterTest(twitterRegex1, 'Assignment1_InputFile.txt')
    print(testDivider)
    runTwitterTest(twitterRegex2, 'Assignment1_InputFile.txt')
    print(testDivider)
    runTwitterTest(twitterRegex3, 'Assignment1_InputFile.txt')

    instaRegex1 = '^(?!.+@.*)^(?!.*[%$()\^\-~\.\*\!\?\#\&"].*)^(?!.*(A|a)+(D|d)+(M|m)+(I|i)+(N|n)+)^(?!.*(T|t)+(W|w)+(I|i)+(T|t)+(T|t)+(E|e)+(R|r)+)@[a-zA-Z0-9_]{1,30}'
    instaRegex2 = '^(?!.+@.*)^(?!.*[%$()\^\-~\*\!\?\#\&"].*)@[a-zA-Z0-9_\.]{1,30}'
    print('````````````Instagram``````````````')
    runInstagramTest(instaRegex1, 'Assignment1_InputFile.txt')


if __name__ == "__main__":
    main()
