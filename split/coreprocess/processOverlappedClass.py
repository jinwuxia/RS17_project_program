# -*- coding: utf-8 -*-
import sys
import csv

'''
处理重叠的class， 得出最终的非重叠+重叠 class 聚类结果。
使用的特征包括mixedDep(struct+comn+commit), 也包含traceDep.
traceDep是class 在某个cluster（根据test case聚类的结果）中出现的次数。
之所以使用traceDep 是因为在假设1的情况下，存在cluster不具有单独拥有的class，所以为空，
导致不存在class-cluster的mixeddep.
而在假设1下，traceDep肯定有（除了test caseFV=[0]）

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
ASSIGN_THR = 0.03    #defalut, is a cmd argv

FINALCLUSTERDict = dict()  #[clusterID] = classIDList
MIXED_DEP_DICT = dict() #dict[classname1][classname2] = [structdep, commitdep, commudep, mixeddep]
TRACE_DEP_DICT = dict() #dict[className][clusterID] = classCount #this class ccount in this cluster
CLASSID2NAMEDict = dict()

def readMixedDepFile(fileName):
    resDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className1, className2, structDep, commitDep, communDep, mixedDep] = each
            if className1 not in resDict:
                resDict[className1] = dict()
            resDict[className1][className2] = [round(float(structDep), 5), round(float(commitDep), 5), round(float(communDep), 5), round(float(mixedDep), 5)]
    return resDict

#fileName = 'testcase1_20_classclusterFv'
def readTraceDepFile(fileName):
    trace_dep_dict = dict()  #dict[classNAme][clusterID] = dep
    tmpList = list()
    with open(fileName, 'r') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className, clusterID, depValue] = each
            if className == 'className':
                continue
            clusterID = int(clusterID)
            depValue = float(depValue)
            if className not in trace_dep_dict:
                trace_dep_dict[className] = dict()
            trace_dep_dict[className][clusterID] = depValue
    return trace_dep_dict


#file=[classID, className, clusterID]
#this file is the non-overlap classFile
#return dict[clusterID] = classIDList
def readNonlapClassFile(fileName):
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
def readOverlapClassFile(fileName):
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
def getMixedDepBetClass(classID1, classID2):
    className1 = CLASSID2NAMEDict[classID1]
    className2 = CLASSID2NAMEDict[classID2]
    if className1 in MIXED_DEP_DICT:
        if className2 in MIXED_DEP_DICT[className1]:
            return MIXED_DEP_DICT[className1][className2][3]   #mixed value
    return round(float(0), 5)

#dep from classID to clusterID
def getMixedDep(classID, clusterID):
    resList = list()
    #print classID, clusterID, FINALCLUSTERDict
    if clusterID not in FINALCLUSTERDict:   #this cluster's classes are all overlapped
        return 0
    for otherClassID in FINALCLUSTERDict[clusterID]:
        tmpValue_1 = getMixedDepBetClass(classID, otherClassID)
        tmpValue_2 = getMixedDepBetClass(otherClassID, classID)
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


#dep from classID to clusterID
def getTraceDep(classID, clusterID):
    dep = 0
    className = CLASSID2NAMEDict[classID]
    if className in TRACE_DEP_DICT:
        if clusterID in TRACE_DEP_DICT[className]:
            dep = TRACE_DEP_DICT[className][clusterID]
    return dep


#mixed dep = (dep + trace_dep)/2   from classID to clusterID
def getFinalDep(classID, clusterID):
    depValue1 = getMixedDep(classID, clusterID)
    depValue2 = getTraceDep(classID, clusterID)
    depValue = 0
    if MERGE_FUNC == 'MIN':
        depValue = min(depValue1, depValue2)
    elif MERGE_FUNC == 'MAX':
        depValue = max(depValue1, depValue2)
    elif MERGE_FUNC == 'AVG':
        depValue = (depValue1 + depValue2) / 2.0
    return depValue



#depList = [clusterID, mixdep][...]
#decision= extract, multiCopy, singleCopy
#return resList=[clusterID1, clusterID2].
#if return =null, extract  it to be a single cluster
def getClusterDecision(depList):
    resList = list()
    for each in depList:
        [clusterID, depValue] = each
        '''
        if int(depValue) == -1: #assign the class into null cluster at first
            resList = list()
            resList.append(clusterID)
            return resList
        '''
        if depValue > ASSIGN_THR:
            resList.append(clusterID)
    return resList


def coreProcess(class2ClusterDict, currentClusterIndex):
    for classID in class2ClusterDict:
        if CONSIDER_FLAG == 'onlyoverlap':  # hypothesis 1
            clusterList = class2ClusterDict[classID]
        elif CONSIDER_FLAG == 'all':        # hypothesis 2
            clusterList = FINALCLUSTERDict.keys()

        depList = list()
        for eachClusterID in clusterList:
            #depList[]=([eachClusterID, mixedValue])
            finalDep = getFinalDep(classID, eachClusterID)
            depList.append([eachClusterID, finalDep])

        #make decision, clusterList = ...
        print 'before making decision, depList=[clusterID, dep]=', depList
        decisionClusterList = getClusterDecision(depList)
        print 'after making decision, resList[clusterID]=', decisionClusterList

        if len(decisionClusterList) == 0:  #extract a single cluster
            FINALCLUSTERDict[currentClusterIndex] = [classID]
            currentClusterIndex += 1
        else: #multiCopy or singleCopy
            for assignedClusterID in decisionClusterList:
                if assignedClusterID not in FINALCLUSTERDict:
                    FINALCLUSTERDict[assignedClusterID] = list()
                FINALCLUSTERDict[assignedClusterID].append(classID)



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


#pro.py  mixDep.csv  traceDep.csv
#        initclusterFile.csv(non-lapped classFile)
#        classListFile.csv(overlapped classFile)
#        FinalClusterFile
#        ASSIGN_THR
if __name__ == '__main__':
    #beacuse some clusters's classes are all overlapped,
    #the cluster is null, mixeddep=0.
    #so use traceDep to compensate this situation
    depFileName = sys.argv[1]
    traceDepFileName = sys.argv[2]
    clusterFileName = sys.argv[3]
    classListFileName = sys.argv[4]
    outClusterFileName = sys.argv[5]
    ASSIGN_THR = float(sys.argv[6])   #default is 0.03

    MIXED_DEP_DICT = readMixedDepFile(depFileName)
    TRACE_DEP_DICT = readTraceDepFile(traceDepFileName) #read and normalized

    [CLASSID2NAMEDict, FINALCLUSTERDict] = readNonlapClassFile(clusterFileName)  #list[clusterID] = classIDList
    class2ClusterDict = readOverlapClassFile(classListFileName) #dict[classID] = clusterIDList
    #print 'class2ClusterDict=',class2ClusterDict

    tmpList = list()
    for tmpClassID in class2ClusterDict:
        tmpClusterList = class2ClusterDict[tmpClassID]
        tmpList.extend(tmpClusterList)
    tmpList.extend(FINALCLUSTERDict.keys())
    currentClusterIndex = 1 + max(tmpList)
    #print 'currentClusterIndex=', currentClusterIndex
    #print 'intiClusters', FINALCLUSTERDict

    coreProcess(class2ClusterDict, currentClusterIndex)

    write2CSV(outClusterFileName)
    '''
    for clusterID in FINALCLUSTERDict:
        #print '\n',clusterID, ':'
        for classID in FINALCLUSTERDict[clusterID]:
            print CLASSID2NAMEDict[classID]
    '''
