# -*- coding: utf-8 -*-
'''
生成除了非核心功能相关的class的特征向量
非核心功能相关的class = allclass - testcase2class(core class) - DAO - view.Action
                    = to_ts_cover_class.csv + testcase_common_class.csv= nocore_class.csv

'''
import sys
import csv

MIN_DEP_VALUE = 0   #usage in feature vector's initialization
DEP_DICT = dict() #dict[classname1][classname2] = [structdep, commitdep, commudep, mixeddep]
DEP_TYPE = 'mixed'   #struct,   commit,   commun,  mixed

class DepObject:
    def __init__(self, structDep, commitDep, communDep, mixedDep):
        self.structDep = round(float(structDep), 5)
        self.commitDep = round(float(commitDep), 5)
        self.communDep =  round(float(communDep), 5)
        self.mixedDep  =  round(float(mixedDep), 5)

def readDepFile(fileName):
    resDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className1, className2, structDep, commitDep, communDep, mixedDep] = each
            aDep = DepObject(structDep, commitDep, communDep, mixedDep)
            if className1 not in resDict:
                resDict[className1] = dict()
            resDict[className1][className2] = aDep
    return resDict


#in this function,  the dep[class1, class2] is a single-direction
def getDepBetClass(className1, className2):
    res = MIN_DEP_VALUE
    if className1 in DEP_DICT:
        if className2 in DEP_DICT[className1]:
            if DEP_TYPE == 'struct':
                res = DEP_DICT[className1][className2].structDep
            elif DEP_TYPE == 'commit':
                res = DEP_DICT[className1][className2].commitDep
            elif DEP_TYPE == 'commun':
                res = DEP_DICT[className1][className2].communDep
            elif DEP_TYPE == 'mixed':
                res = DEP_DICT[className1][className2].mixedDep
            else:
                print 'Unknown type: ', DEP_TYPE
    return res

def readClassFile(fileName):
    classList = list()  #[id] = name
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
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


#pro.py  totalDep.csv   classList  outFeatureFileName
if __name__ == '__main__':
    depFileName = sys.argv[1]
    classFileName = sys.argv[2]
    featureFileName = sys.argv[3]

    DEP_DICT = readDepFile(depFileName)
    classList = readClassFile(classFileName)

    #compute each class's feature vector
    matrixFv = genFeatureVector(classList)
    write2CSV(matrixFv, featureFileName)
