import sys
import csv

def readClass(AllclassFileName):
    classList = list()
    with open(AllclassFileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            classList.append(className)
    return classList


def readCSV(tsClassFileName):
    classList = list()
    with open(tsClassFileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className] = each
            classList.append(className)
    return classList

def diffClass(allList,tsList):
    for each in allList:
        if each not in tsList:
            print each

allClassList = readClass(sys.argv[1])
tsClassList = readCSV(sys.argv[2])
diffClass(allClassList,tsClassList)
