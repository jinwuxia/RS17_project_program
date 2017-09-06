# -*- coding: utf-8 -*-
'''
生成除了非核心功能相关的class的特征向量
非核心功能相关的class = allclass - testcase2class(core class) - DAO - view.Action

'''
import sys
import csv

#MERGE_FUNC = 'AVG'   #class-cluster depvalue = min,max,avg
#ASSIGN_THR = 0.03

MIN_DEP_VALUE = 0   #usage in feature vector's initialization

#FINALCLUSTERDict = dict()  #[clusterID] = classIDList
DEP_DICT = dict() #dict[classname1][classname2] = [structdep, commitdep, commudep, mixeddep]

#CLASSID2NAMEDict = dict()

def readDepFile(fileName):
    resDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className1, className2, structDep, commitDep, communDep, mixedDep] = each
            if className1 not in resDict:
                resDict[className1] = dict()
            resDict[className1][className2] = [round(float(structDep), 5), round(float(commitDep), 5), round(float(communDep), 5), round(float(mixedDep), 5)]
    return resDict



#in this function,  the dep[class1, class2] is a single-direction
def getDepBetClass(className1, className2):
    if className1 in DEP_DICT:
        if className2 in DEP_DICT[className1]:
            return DEP_DICT[className1][className2][3]   #mixed value
    return round(float(0), 5)

'''
#dep from classID to clusterID
def getDep(classID, clusterID):
    resList = list()
    #print classID, clusterID, FINALCLUSTERDict
    if clusterID not in FINALCLUSTERDict:   #this cluster's classes are all overlapped
        return -1
    for otherClassID in FINALCLUSTERDict[clusterID]:
        tmpValue_1 = getDepBetClass(classID, otherClassID)
        tmpValue_2 = getDepBetClass(otherClassID, classID)
        tmpValue = max(tmpValue_2, tmpValue_1)
        #print tmpValue
        resList.append(tmpValue)
    if MERGE_FUNC == 'AVG':
        depValue = sum(resList)/ float(len(resList))
    elif MERGE_FUNC == 'MIN':
        depValue = min(resList)
    elif MERGE_FUNC == 'MAX':
        depValue = max(resList)
    return depValue

#dep from classIDList to clusterID
def getDepClassList2Cluster(classList, clusterID):
    depValueList = list()
    for classID in classList:
        depValue = getDep(classID, clusterID)
        depValueList.append(depValue)

    #filter out -1
    newDepValueList = list()
    for each in depValueList:
        if int(each) != -1:
            newDepValueList.append(each)

    if len(newDepValueList)  == 0:
        return -1
    return sum(newDepValueList) / float(len(newDepValueList))
'''


def readClassFile(fileName):
    classDict = dict()  #[id] = name
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className] = each
            if classID == 'classID':
                continue
            classDict[className] = 1
    return classDict

#return allClassDict - hasProClassDict
def getNotProClasses(allClassDict, hasProClassDict):
    classList = list()
    for className in allClassDict:
        if className not in hasProClassDict:
            classList.append(className)
    return classList


#single direction dependency
def genFeatureVector(classList):
    matrix = list()
    for i in range(0, len(classList)):
        tmpList = [MIN_DEP_VALUE] * len(classList)
        matrix.append(tmpList)
    for i in range(0, len(classList)):
        for j in range(0, len(classList)):
            if i == j:
                matrix[i][j] = 0
            else:
                matrix[i][j] = getDepBetClass(classList[i], classList[j])

    newMatrix = list()
    for i in range(0, len(classList)):
        className = classList[i]
        tmpList = [className]
        tmpList.extend(matrix[i])
        newMatrix.append(tmpList)
    return newMatrix


def write2CSV(matrix, fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(matrix)
    print fileName


#pro.py  totalDep.csv   hasProcessedClassFile,  totalClassFile(action+dao+other+testcase2class), outFeatureFileName
if __name__ == '__main__':
    depFileName = sys.argv[1]
    hasProcessedClassFileName = sys.argv[2]
    totalCLassFileName = sys.argv[3]
    outFeatureFileName = sys.argv[4]

    DEP_DICT = readDepFile(depFileName)

    #get not processed className List, which is our object
    allClassDict = readClassFile(totalCLassFileName)
    hasProClassDict = readClassFile(hasProcessedClassFileName)
    notProClassList = getNotProClasses(allClassDict, hasProClassDict)

    #compute each class's feature vector
    matrixFv = genFeatureVector(notProClassList)
    write2CSV(matrixFv, outFeatureFileName)
    #do clusteirng
