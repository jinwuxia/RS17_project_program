'according to our class coverage, filter out semantic value'
import sys
import csv

def readClass(fileName):
    classNameList = list()
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className] = each
            classNameList.append(className)
    return classNameList


def readSynsim(fileName):
    valueList = list()  #[class1, class2, value]
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className1, className2, value] = each
            valueList.append( [className1, className2, value] )
    return valueList

def filterOut(valueList, classNameList):
    finalList = list()
    for each in valueList:
        [className1, className2, value] = each
        if (className1 in classNameList) and (className2 in classNameList):
            finalList.append( [className1, className2, value] )
    print (len(valueList), len(finalList))
    return finalList

def writeCSV(fileName, finalList):
    with open(fileName, 'w', newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(finalList)
    print (fileName)

if __name__ == '__main__':
    classFileName = sys.argv[1]    #input
    synsimFileName = sys.argv[2]   #input
    finalSynsimFileName = sys.argv[3] #output
    classNameList = readClass(classFileName)
    valueList = readSynsim(synsimFileName)
    finalList = filterOut(valueList, classNameList)
    writeCSV(finalSynsimFileName, finalList)
