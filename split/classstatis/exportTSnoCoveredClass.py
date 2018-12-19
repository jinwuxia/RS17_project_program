import sys
import csv

def readClass(AllclassFileName):
    classList = list()
    with open(AllclassFileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            classList.append(className)
    return classList


def readCSV(tsClassFileName):
    classList = list()
    with open(tsClassFileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            classList.append(className)
    return classList

def diffClass(allList,tsList):
    noClassList = list()
    for each in allList:
        if each not in tsList:
            noClassList.append(each)
            print (each)
    print ('classes not covered in workflow: ', len(noClassList))

allClassList = readClass(sys.argv[1])
tsClassList = readCSV(sys.argv[2])
diffClass(allClassList,tsClassList)
