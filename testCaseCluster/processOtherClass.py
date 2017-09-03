# -*- coding: utf-8 -*-
import sys
import csv

'''
算法思路：处理每一个要处理的class， 对其进行分配到已有的cluster或者
input:已有的cluster结果作为初始值，classID， 重叠的cluster ID。
读入要处理的class list，以及所在的clusterIDList
#classList = [classID1, ..]
#class2ClusterDict[classID] = [clusterID1, clusterID2]
#假设1:更新过的非Lappcluster与class没有关系
#假设2:更新过的非Lappcluster也有可能与class有关系
'''

CONSIDER_FLAG = 'onlyoverlap' # onlyoverlap, all
MERGE_FUNC = 'AVG'   #class-cluster depvalue = min,max,avg
ASSIGN_THR = 0.16

FINALCLUSTERDict = dict()  #[clusterID] = classIDList
DEP_DICT = dict() #dict[classname1][classname2] = [structdep, commitdep, commudep, mixeddep]
CLASSID2NAMEDict = dict()

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

#file=[classID, className, clusterID]
#return dict[clusterID] = classIDList
def readClusterFile(fileName):
    classID2NameDict = dict()
    clusterDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className, clusterID] = each
            if classID == 'classID':
                continue
            classID2NameDict[int(classID)] = className
            if int(clusterID) not in clusterDict:
                clusterDict[int(clusterID)] = list()
            clusterDict[int(clusterID)].append(int(classID))
    return classID2NameDict, clusterDict

#file = [classID, className, clusterIDListStr]
#return dict[classID] = clusterIDList
def readClassFile(fileName):
    class2ClusterDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className, clusterIDListStr] = each
            if classID == 'classID':
                continue
            CLASSID2NAMEDict[int(classID)] = className
            clusterList = clusterIDListStr.split(':')
            clusterIDList = [int(clusterID)  for clusterID in  clusterList]
            class2ClusterDict[int(classID)] = clusterIDList
    return class2ClusterDict


#in this function,  the dep[class1, class2] is a single-direction
def getDepBetClass(classID1, classID2):
    className1 = CLASSID2NAMEDict[classID1]
    className2 = CLASSID2NAMEDict[classID2]
    if className1 in DEP_DICT:
        if className2 in DEP_DICT[className1]:
            return DEP_DICT[className1][className2][3]   #mixed value
    return round(float(0), 5)

def getDep(classID, clusterID):
    resList = list()
    print classID, clusterID, FINALCLUSTERDict
    for otherClassID in FINALCLUSTERDict[clusterID]:
        tmpValue = getDepBetClass(classID, otherClassID)
        resList.append(tmpValue)
    if MERGE_FUNC == 'AVG':
        depValue = sum(resList)/ float(len(resList))
    elif MERGE_FUNC == 'MIN':
        depValue = min(resList)
    elif MERGE_FUNC == 'MAX':
        depValue = max(resList)
    return depValue


#depList = [clusterID, mixdep][...]
#decision= extract, multiCopy, singleCopy
#return resList=[clusterID1, clusterID2].
#if return =null, extract  it to be a single cluster
def getClusterDecision(depList):
    print 'before making decision, depList=', depList
    resList = list()
    for each in depList:
        [clusterID, depValue] = each
        if depValue > ASSIGN_THR:
            resList.append(clusterID)
    print 'after making decision, resList=', resList
    return resList


def coreProcess(class2ClusterDict, currentClusterIndex):
    classList = class2ClusterDict.keys()  #IDlist
    for eachClassID in classList:
        if CONSIDER_FLAG == 'onlyoverlap':  # hypothesis 1
            clusterList = class2ClusterDict[eachClassID]
        elif CONSIDER_FLAG == 'all':        # hypothesis 2
            clusterList = FINALCLUSTERDict.keys()

        depList = list()
        for eachClusterID in clusterList:
            #depList[]=([eachClusterID, mixedValue])
            mixedDep = getDep(eachClassID, eachClusterID)
            depList.append([eachClusterID, mixedDep])

        #make decision, clusterList = ...
        decisionClusterList = getClusterDecision(depList)
        if len(decisionClusterList) == 0:  #extract a single cluster
            FINALCLUSTERDict[currentClusterIndex] = list()
            FINALCLUSTERDict[currentClusterIndex].append(eachClassID)
            currentClusterIndex += 1
        else: #multiCopy or singleCopy
            for assignedClusterID in decisionClusterList:
                FINALCLUSTERDict[assignedClusterID].append(eachClassID)

#pro.py  filterDep.csv   initclusterFile.csv    classListFile.csv
if __name__ == '__main__':
    depFileName = sys.argv[1]
    clusterFileName = sys.argv[2]
    classListFileName = sys.argv[3]

    DEP_DICT = readDepFile(depFileName)
    [CLASSID2NAMEDict, FINALCLUSTERDict] = readClusterFile(clusterFileName)  #list[clusterID] = classIDList
    class2ClusterDict = readClassFile(classListFileName) #dict[classID] = clusterIDList
    print 'class2ClusterDict=',class2ClusterDict
    tmpList = list()
    for tmpClassID in class2ClusterDict:
        tmpClusterList = class2ClusterDict[tmpClassID]
        tmpList.extend(tmpClusterList)
    tmpList.extend(FINALCLUSTERDict.keys())
    currentClusterIndex = 1 + max(tmpList)
    print 'currentClusterIndex=', currentClusterIndex
    print 'intiClusters', FINALCLUSTERDict

    coreProcess(class2ClusterDict, currentClusterIndex)
