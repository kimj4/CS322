# Ju Yun Kim
# Github.com/kimj4
# a pretty printer for 2d data

import math

# Sample input
# prettyGraph.prettyPrintGraph(3, 3, ['Predicted Twitter', 'Predicted Instagram', 'Predicted Neither'],
#                                    ['Actual Twitter', 'Actual Instagram', 'Actual Neither'],
#                                    [[actualTwitterPredictedTwitter, actualTwitterPredictedInstagram, actualTwitterPredictedNeither],
#                                     [actualInstaPredictedTwitter, actualInstaPredictedInsta, actualInstaPredictedNeither],
#                                     [actualNeitherPredictedTwitter, actualNeitherPredictedInsta, actualNeitherPredictedNeither]])

# Sample output
# ----------------------------------------------------------------------------------
# |                  | Predicted Twitter | Predicted Instagram | Predicted Neither |
# ----------------------------------------------------------------------------------
# | Actual Twitter   |        31         |          9          |         8         |
# ----------------------------------------------------------------------------------
# | Actual Instagram |         0         |         31          |         0         |
# ----------------------------------------------------------------------------------
# | Actual Neither   |         0         |          0          |         0         |
# ----------------------------------------------------------------------------------


# number of spaces to add to either side of labels
LABEL_BUFFER = 1;

def stringCreator(char, length):
    '''
    Utility function to make a string that repeats char length number of times
    '''
    if (len(char) != 1):
        print('stringCreator Error: use single characters only please')
    string = ''
    for i in range(length):
        string += char
    return string

def prettyPrintGraph(numRows, numCols, topLabels, leftLabels, data):
    '''
    Function to print to output the given data with legends pretty-ly
    numRows = number of rows in your data
    numCols = number of columns in your data
    topLabels = labels that mark each column in a list of strings
    leftLabels = labels that mark each row in a list of strings
    data = the body of the grid. A list of lists of some str()-able objects
    '''
    if (numRows != len(leftLabels)):
        return
    if (numCols != len(topLabels)):
        return
    if (numRows != len(data)):
        return
    for row in data:
        if (numCols != len(row)):
            return

    # stores lengths of labels
    topLabelLengthList = []
    for topLabel in topLabels:
        topLabelLengthList.append(len(topLabel))


    leftLabelsLengthList = []
    for leftLabel in leftLabels:
        leftLabelsLengthList.append(len(leftLabel))

    longestLeftLabelLength = max(leftLabelsLengthList)
    for i in range(len(leftLabels)):
        if (len(leftLabels[i]) < longestLeftLabelLength):
            leftLabels[i] = leftLabels[i] + stringCreator(' ', longestLeftLabelLength - len(leftLabels[i]))




    # in the 0.0 position in the printed grid, there is going to be an empty cell
    #   This calculates the size of that empty cell
    gapLength = max(leftLabelsLengthList) + 2 * LABEL_BUFFER

    gapString = stringCreator(' ', gapLength)


    # this is a list of list similar to the data list but has the items
    #  that will be actually written.
    printItemMatrix = []
    printItemMatrix.append([gapString])
    for topLabel in topLabels:
        printItemMatrix[0].append(' ' + topLabel + ' ')

    for i in range(1, numRows + 1):
        printItemMatrix.append([])
        printItemMatrix[i].append(' ' + leftLabels[i - 1] + ' ')
        for j in range(len(data[i - 1])):
            d = str(data[i - 1][j])
            totalLabelLength = topLabelLengthList[j] + 2 * LABEL_BUFFER - len(d)
            left = math.floor(totalLabelLength / 2)
            right = totalLabelLength - left
            printItemMatrix[i].append(stringCreator(' ', left) + str(d) + stringCreator(' ', right))

    for row in printItemMatrix:
        rowToPrint = '|'
        for column in row:
            rowToPrint = rowToPrint + column + '|'

        print(stringCreator('-', len(rowToPrint)))
        print(rowToPrint)
    print(stringCreator('-', len(rowToPrint)))



def main():
    numRows = 3
    numCols = 2
    topLabels = ['top1', 'top2']
    leftLabels = ['left1', 'left2', 'left3']
    data = [[1, 2], [3, 4], [5, 6]]
    prettyPrintGraph(numRows, numCols, topLabels, leftLabels, data)

if __name__ == "__main__":
    main()
