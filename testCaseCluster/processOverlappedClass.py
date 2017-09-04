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
ASSIGN_THR = 0.03

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


#depList = [clusterID, mixdep][...]
#decision= extract, multiCopy, singleCopy
#return resList=[clusterID1, clusterID2].
#if return =null, extract  it to be a single cluster
def getClusterDecision(depList):
    resList = list()
    for each in depList:
        [clusterID, depValue] = each
        if int(depValue) == -1: #assign the class into null cluster at first
            resList = list()
            resList.append(clusterID)
            return resList
        if depValue > ASSIGN_THR:
            resList.append(clusterID)
    return resList


#judge the two list is equal or not
def isEqualList(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    if len(set1 & set2) == len(set1) and len(set1 & set2) == len(set2):
        return True
    else:
        return False


#if merge class into classList, when the classes appears same dependency pattern with clusters
def preProcess(class2ClusterDict):
    isProcessed = dict()  #[classID] = 1
    classSetList = list() #list[1] = classIDs
    clusterSetList = list() # list[1] = clusterIDs.   classIDs and clusterSetList is corresponding

    classIDKeysList = class2ClusterDict.keys()
    for index1 in range(0, len(classIDKeysList)):
        classID1 = classIDKeysList[index1]
        if classID1 not in isProcessed:
            classSetList.append([classID1])
            isProcessed[classID1] = 1
            clusterIDList1 = class2ClusterDict[classID1]
            clusterSetList.append(clusterIDList1)
            for index2 in range(index1 + 1, len(classIDKeysList)):
                classID2 = classIDKeysList[index2]
                if classID2 not in isProcessed:
                    clusterIDList2 = class2ClusterDict[classID2]
                    if isEqualList(clusterIDList1, clusterIDList2):
                        classSetList[len(classSetList) - 1].append(classID2)
                        isProcessed[classID2] = 1
    print '\nafter merging class: ', classSetList
    return classSetList, clusterSetList


def coreProcess(mergedClassList, mergedClusterList, currentClusterIndex):
    for index in range(0, len(mergedClassList)):
        print '\nProcessing: classes=', mergedClassList[index], ' clusters=', mergedClusterList[index]
        if CONSIDER_FLAG == 'onlyoverlap':  # hypothesis 1
            clusterList = mergedClusterList[index]
        elif CONSIDER_FLAG == 'all':        # hypothesis 2
            clusterList = FINALCLUSTERDict.keys()

        depList = list()
        for eachClusterID in clusterList:
            #depList[]=([eachClusterID, mixedValue])
            mixedDep = getDepClassList2Cluster(mergedClassList[index], eachClusterID)
            depList.append([eachClusterID, mixedDep])

        #make decision, clusterList = ...
        print 'before making decision, depList=', depList
        decisionClusterList = getClusterDecision(depList)
        print 'after making decision, resList=', decisionClusterList

        if len(decisionClusterList) == 0:  #extract a single cluster
            FINALCLUSTERDict[currentClusterIndex] = mergedClassList[index]
            currentClusterIndex += 1
        else: #multiCopy or singleCopy
            for assignedClusterID in decisionClusterList:
                if assignedClusterID not in FINALCLUSTERDict:
                    FINALCLUSTERDict[assignedClusterID] = list()
                FINALCLUSTERDict[assignedClusterID].extend(mergedClassList[index])



def write2CSV(fileName):
    listlist = list()
    listlist.append(['classID', 'className', 'clusterID'])
    for clusterID in FINALCLUSTERDict:
        for classID in FINALCLUSTERDict[clusterID]:
            listlist.append([classID, CLASSID2NAMEDict[classID], clusterID])
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(listlist)
    print fileName


#pro.py  filterDep.csv   initclusterFile.csv    classListFile.csv
if __name__ == '__main__':
    depFileName = sys.argv[1]
    clusterFileName = sys.argv[2]
    classListFileName = sys.argv[3]
    outClusterFileName = sys.argv[4]

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

    [mergedClassList, mergedClusterList]= preProcess(class2ClusterDict)
    coreProcess(mergedClassList, mergedClusterList, currentClusterIndex)

    write2CSV(outClusterFileName)
    for clusterID in FINALCLUSTERDict:
        print '\n',clusterID, ':'
        for classID in FINALCLUSTERDict[clusterID]:
            print CLASSID2NAMEDict[classID]
