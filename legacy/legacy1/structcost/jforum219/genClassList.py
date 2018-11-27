import sys
import csv

def ReadCSV(filename):
    listlist = list()
    with open(filename, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [name] = each
            listlist.append(name)
    return listlist


def WriteCSV(fileName, oneList):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        for each in oneList:
            writer.writerow([each])
    print fileName


def IsInPackList(className, packList):
    tmpArr = className.split('.')
    tmpArr.pop()
    thisPackName = '.'.join(tmpArr)
    if thisPackName in packList:
        return True
    else:
        return False

def Process(beforeClassList, filterPackList):
    afterClassList = list()
    for eachClass in beforeClassList:
        if IsInPackList(eachClass, filterPackList):
            afterClassList.append(eachClass)
    return afterClassList


#for big project,  we need to specify the package to be analyized.
#this program filter out the classList which need to be analyzed.
#python pro.py   fullclassListFile    filterpackListfile  afterClassListFile
if __name__ == '__main__':
    beforeFileName = sys.argv[1]
    filterFileName = sys.argv[2]
    afterFileName = sys.argv[3]

    beforeClassList = ReadCSV(beforeFileName)
    filterPackList =  ReadCSV(filterFileName)
    afterClassList = Process(beforeClassList, filterPackList)
    WriteCSV(afterFileName, afterClassList)

