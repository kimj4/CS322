import re
import prettyGraph

# precision = # correct / # found
# recall = # found / # total
# F1 = (2 * precision * recall) / (precision + recall)


def runTwitterTest(regexString, inputFile):
    fd = open(inputFile, 'r', encoding='UTF-8')
    total = 0
    falsePositive = 0
    falseNegative = 0
    truePositive = 0
    trueNegative = 0
    for line in fd:
        regReturn = re.search(regexString, line)
        if (regReturn):
            if ('T' in line.split(',')[1]):
                total += 1
                truePositive +=1
                # print('correct')
            else:
                falsePositive += 1
                # print('incorrect')
        else:
            if ('T' in line.split(',')[1]):
                total += 1
                falseNegative +=1
                # print('correct')
            else:
                trueNegative += 1
                # print('incorrect')

    precision = truePositive / (truePositive + falsePositive)
    recall = (truePositive + falsePositive) / total
    # print('true positive: ' + str(truePositive))
    # print('true negative: ' + str(trueNegative))
    # print('false positive: ' + str(falsePositive))
    # print('false negative: ' + str(falseNegative))
    # prettyPrintGraph(numRows, numCols, topLabels, leftLabels, data):
    prettyGraph.prettyPrintGraph(2, 2, ['Predicted Yes', 'Predicted No'],
                                       ['Actual Yes', 'Actual No'],
                                       [[truePositive, falseNegative],
                                        [falsePositive, trueNegative]])
    # print('Precision: ' + str(precision))
    # print('Recall: ' + str(recall))
    # print('F1: ' + str((2 * precision * recall) / (precision + recall)))
    # print('Confusion matrix')
    # print('               --------------------------------')
    # print('               | Predicted yes | Predicted no |')
    # print('-----------------------------------------------')
    # print('   Actual yes  |      %s       |       %s      |' % (truePositive, falseNegative))
    # print('-----------------------------------------------')
    # print('   Actual no   |      %s       |       %s      |' % (falsePositive, trueNegative))
    # print('-----------------------------------------------')



def runInstagramTest(regexString, inputFile):
    fd = open(inputFile, 'r', encoding='UTF-8')
    total = 0
    falsePositive = 0
    falseNegative = 0
    truePositive = 0
    trueNegative = 0
    for line in fd:
        regReturn = re.search(regexString, line)
        if (regReturn):
            if ('I' in line.split(',')[1]):
                total += 1
                truePositive +=1
            else:
                falsePositive += 1
        else:
            if ('I' in line.split(',')[1]):
                total += 1
                falseNegative +=1
                # print('correct')
            else:
                trueNegative += 1
                # print('incorrect')

    precision = truePositive / (truePositive + falsePositive)
    recall = (truePositive + falsePositive) / total
    # print('true positive: ' + str(truePositive))
    # print('true negative: ' + str(trueNegative))
    # print('false positive: ' + str(falsePositive))
    # print('false negative: ' + str(falseNegative))

    # print('Precision: ' + str(precision))
    # print('Recall: ' + str(recall))
    # print('F1: ' + str((2 * precision * recall) / (precision + recall)))
    prettyGraph.prettyPrintGraph(2, 2, ['Predicted Yes', 'Predicted No'],
                                       ['Actual Yes', 'Actual No'],
                                       [[truePositive, falseNegative],
                                        [falsePositive, trueNegative]])

def runSystemTest(twitterRegex, instagramRegex, inputFile):
    fd = open(inputFile, 'r', encoding='UTF-8')
    total = 0
    actualTwitterPredictedTwitter = 0
    actualTwitterPredictedInsta = 0
    actualTwitterPredictedNeither = 0

    actualInstaPredictedInsta = 0
    actualInstaPredictedTwitter = 0
    actualInstaPredictedNeither = 0

    actualNeitherPredictedNeither = 0
    actualNeitherPredictedTwitter = 0
    actualNeitherPredictedInsta = 0

    isTwitter = False;
    isInsta = False;

    twitterTotal = 0
    instaTotal = 0
    neitherTotal = 0
    for line in fd:
        if ('T' in line.split(',')[1]):
            isTwitter = True;
            twitterTotal += 1
        if ('I' in line.split(',')[1]):
            isInsta = True
            instaTotal += 1
        if ('N' in line.split(',')[1]):
            neitherTotal += 1

        ######################
        ### twitter processing
        ######################

        twitterRegReturn = re.search(twitterRegex, line)
        # twitter regex matches
        if (twitterRegReturn):
            if (isTwitter):
                actualTwitterPredictedTwitter +=1
            # T regex matches a string that is I only
            elif (isInsta):
                actualInstaPredictedTwitter += 1
            # T regex matches a string that is N only
            else:
                actualNeitherPredictedTwitter += 1
        # T regex doesn't match
        else:
            a = ''
            # not sure if we have to do anything here

        ########################
        ### instagram processing
        ########################
        instaRegReturn = re.search(instagramRegex, line)
        # I regex matches
        if (instaRegReturn):
            # I regex match is correct
            if (isInsta):
                actualInstaPredictedInsta += 1
            # I regex matches a string that is T only
            elif (isTwitter):
                print(instaRegReturn)
                actualTwitterPredictedInstagram += 1
            # I regex matches a string that is N only
            else:
                actualNeitherPredictedInsta += 1
        else:
            a = ''
            # still not sure if this needs to exist


        if ((not twitterRegReturn) and (not instaRegReturn)):
            # no regex match but the string is I
            if (isInsta):
                actualInstaPredictedNeither += 1
            # no regex match but the string is T
            if (isTwitter):
                actualTwitterPredictedNeither += 1
            # I regex matches a string that is N only
            if ((not isTwitter) and (not isInsta)):
                actualNeitherPredictedNeither += 1

        isTwitter = False
        isInsta = False

    prettyGraph.prettyPrintGraph(3, 3, ['Predicted Twitter', 'Predicted Instagram', 'Predicted Neither'],
                                       ['Actual Twitter', 'Actual Instagram', 'Actual Neither'],
                                       [[actualTwitterPredictedTwitter, actualTwitterPredictedInsta, actualTwitterPredictedNeither],
                                        [actualInstaPredictedTwitter, actualInstaPredictedInsta, actualInstaPredictedNeither],
                                        [actualNeitherPredictedTwitter, actualNeitherPredictedInsta, actualNeitherPredictedNeither]])


def main():
    twitterRegex1 = '@[a-zA-Z0-9_]{1,15}'
    twitterRegex2 = '^(?!.*(A|a)+(D|d)+(M|m)+(I|i)+(N|n)+)^(?!.*(T|t)+(W|w)+(I|i)+(T|t)+(T|t)+(E|e)+(R|r)+)@[a-zA-Z0-9_]{1,15}'
    twitterRegex3 = '^(?!.+@.*)^(?!.*[%$()\^\-~\.\*\!\?\#\&"].*)^(?!.*(A|a)+(D|d)+(M|m)+(I|i)+(N|n)+)^(?!.*(T|t)+(W|w)+(I|i)+(T|t)+(T|t)+(E|e)+(R|r)+)@[a-zA-Z0-9_]{1,15}'
    testDivider = '~~~~~~~~~~~~~~~~~~'

    print('\n`````````````Twitter```````````````')
    runTwitterTest(twitterRegex1, 'Assignment1_InputFile.txt')
    # print(testDivider)
    runTwitterTest(twitterRegex2, 'Assignment1_InputFile.txt')
    # print(testDivider)
    runTwitterTest(twitterRegex3, 'Assignment1_InputFile.txt')

    instaRegex1 = '^(?!.+@.*)^(?!.*[%$()\^\-~\.\*\!\?\#\&"].*)^(?!.*(A|a)+(D|d)+(M|m)+(I|i)+(N|n)+)^(?!.*(T|t)+(W|w)+(I|i)+(T|t)+(T|t)+(E|e)+(R|r)+)@[a-zA-Z0-9_]{1,30}'
    instaRegex2 = '^(?!.+@.*)^(?!.*[%$()\^\-~\*\!\?\#\&"].*)@[a-zA-Z0-9_\.]{1,30}'
    print('````````````Instagram``````````````')
    runInstagramTest(instaRegex1, 'Assignment1_InputFile.txt')
    # print(testDivider)
    runInstagramTest(instaRegex2, 'Assignment1_InputFile.txt')

    runSystemTest(twitterRegex1, instaRegex1, 'Assignment1_InputFile.txt')
    runSystemTest(twitterRegex2, instaRegex2, 'Assignment1_InputFile.txt')
    runSystemTest(twitterRegex3, instaRegex2, 'Assignment1_InputFile.txt')

if __name__ == "__main__":
    main()
