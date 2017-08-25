import sys
import csv

#generate testcase feature vector and classnameList, the result format is as following:
'''
traceID   class1 class2  class3  class4 .......
      t1      2     3       0         1
      t2      2     1       1         0
      t3      1     1       0         3
'''


CLASSID2NAMEDict = dict()
CLASSNAME2IDDict = dict()
EXCLUDEDCLASSNAMEList = list()
INCLUDEDCLASSNAMEList = list()

def readTestCase(fileName):
    testCaseDict = dict()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        index = 0
        for each in reader:
            [testCaseName] = each
            testCaseDict[index] = testCaseName
            index += 1
    return testCaseDict

def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [traceID,order,structtype,method1,method2,m1_para,m2_para,className1,className2, m1_return, m2_return] = each
            if traceID == 'traceID':
                continue
            oneList = [int(traceID), className1, className2]
            resList.append(oneList)
    return resList

def isStrPackage(strstr):
    if '.*' in strstr:
        return True
    else:
        return False

#use excludefile to judge that  className is included or not
def isIncludedByExTag(className):
    for each in EXCLUDEDCLASSNAMEList:
        if isStrPackage(each):
            each = each[0: len(each) - 2]
            if className.startswith(each):  #belong to this package
                return False
        else:
            if className == each:   #each can be packge.* or classname
                return False
    return True

#use includefile to judge that  className is included or not
def isIncludedByInTag(className):
    #use includefile
    for each in INCLUDEDCLASSNAMEList:  #each can be packge.* or classname
        if isStrPackage(each):
            each = each[0: len(each) - 2]
            if className.startswith(each):
                return True
        else:
            if className == each:
                return True
    return False

#className is included or not
def isIncluded(className):
    #use excludefile
    if len(EXCLUDEDCLASSNAMEList) != 0:
        return isIncludedByExTag(className)
    #use includefile
    if len(INCLUDEDCLASSNAMEList) != 0:
        return isIncludedByInTag(className)

    #if len(INCLUDEDCLASSNAMEList) == 0   and len(EXCLUDEDCLASSNAMEList) == 0
    return True

#class or package name which should be excluded
def readTaggedClass(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            resList.append(className)
    return resList

#only process the calleeclass, beacause the caller class must be called by last class.
#only root class is not processed, since root class belongs to exludedClass(zong instead of fen)
def firstProcess(initList):
    resList = list()  #each element is a dict
    classIndex = 0
    className2IDDict = dict()
    classID2NameDict = dict()
    for each in initList:
        [traceID, className1, className2] = each
        if len(resList) == traceID:
            resList.append(dict())
        if isIncluded(className1) and (className1 not in className2IDDict):
            className2IDDict[className1] = classIndex
            classID2NameDict[classIndex] = className1
            classIndex += 1
        if isIncluded(className2) and (className2 not in className2IDDict):
            className2IDDict[className2] = classIndex
            classID2NameDict[classIndex] = className2
            classIndex += 1
        if isIncluded(className2):
            classID2 = className2IDDict[className2]
            if classID2 not in resList[traceID]:
                resList[traceID][classID2] = 1
            else:
                resList[traceID][classID2] += 1
    return resList, className2IDDict, classID2NameDict

def secondProcess(aList):
    resList = list()            #is a maxtrix
    N = len(aList)              #row
    M = len(CLASSNAME2IDDict)   #colum
    for i in range(0, N):
        tmpList = [0] * M
        resList.append(tmpList)
    for traceID in range(0, N):
        for classID in aList[traceID]:
            resList[traceID][classID]= aList[traceID][classID]
    return resList

def writeClass(fileName):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        for classID in CLASSID2NAMEDict:
            tmpList = [classID, CLASSID2NAMEDict[classID]]
            writer.writerow(tmpList)
    print fileName

#add first colmun save to file
def writeMatrix(matrix, testCaseDict, fileName):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        for traceID in range(0, len(matrix)):
            #print traceID, testCaseDict[traceID]
            oneList = [testCaseDict[traceID]]
            tmpList = matrix[traceID]
            oneList.extend(tmpList)
            writer.writerow(oneList)
    print fileName

#From workflowFile,  generate testcase featureVector, and classFile
#python pro.py  workflowfile  testcaseFile excluededFile    includedFileName  outClassFile   outMatrixFile
if __name__ == "__main__":
    workflowFileName = sys.argv[1]
    testcaseFileName = sys.argv[2]
    excludedFileName = sys.argv[3]
    includedFileName = sys.argv[4]
    outClassFileName = sys.argv[5]
    outFeatureVectorFileName = sys.argv[6]

    testCaseDict = readTestCase(testcaseFileName)
    initList = readCSV(workflowFileName)

    if  excludedFileName != 'null':
        #read EXCLUDEDCLASSNAMEList
        EXCLUDEDCLASSNAMEList = readTaggedClass(excludedFileName)

    if includedFileName != 'null':
        #read INCLUDEDCLASSNAMEList
        INCLUDEDCLASSNAMEList = readTaggedClass(includedFileName)

    #generate CLASSNAME2IDDict, CLASSID2NAMEDict, listDict({classID1, num1}, {classID2, num2})
    [listDict, CLASSNAME2IDDict, CLASSID2NAMEDict] = firstProcess(initList)
    matrix = secondProcess(listDict)
    writeClass(outClassFileName)
    writeMatrix(matrix, testCaseDict, outFeatureVectorFileName)
