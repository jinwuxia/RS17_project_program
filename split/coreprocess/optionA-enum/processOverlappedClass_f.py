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
    #print fileName
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


def readOrignalClusterFile (fileName):
    finalClusterDict = dict()  #dict[clusterID] = list()
    with open(fileName) as fp:
        reader = csv.reader(fp)
        for each in reader:
            [clusterID, testcaseID, testcaseName] = each
            clusterID = int(clusterID)
            if clusterID not in finalClusterDict:
                finalClusterDict[clusterID] = list()
    return finalClusterDict

#file=[classID, className, clusterID]
#this file is the non-overlap classFile
#return dict[clusterID] = classIDList
def readNonlapClassFile(fileName):
    classID2NameDict = dict()
    global FINALCLUSTERDict
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className, clusterID] = each
            if classID == 'classID':
                continue
            classID2NameDict[int(classID)] = className
            FINALCLUSTERDict[int(clusterID)].append(int(classID))
    return classID2NameDict

#file = [classID, className, clusterIDListStr]
#return dict[classID] = clusterIDList
def readOverlapClassFile(fileName):
    global CLASSID2NAMEDict
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
    global MIXED_DEP_DICT
    global CLASSID2NAMEDict
    className1 = CLASSID2NAMEDict[classID1]
    className2 = CLASSID2NAMEDict[classID2]
    if className1 in MIXED_DEP_DICT:
        if className2 in MIXED_DEP_DICT[className1]:
            return MIXED_DEP_DICT[className1][className2][3]   #mixed value
    return round(float(0), 5)

#dep from classID to clusterID
def getMixedDep(classID, clusterID):
    global MERGE_FUNC
    global FINALCLUSTERDict
    global MIXED_DEP_DICT
    global CLASSID2NAMEDict

    resList = list()
    #print classID,clusterID, FINALCLUSTERDict[clusterID]
    #print classID, clusterID, FINALCLUSTERDict
    if len(FINALCLUSTERDict[clusterID]) == 0:   #this cluster's classes are all overlapped
        return 0
    for otherClassID in FINALCLUSTERDict[clusterID]:
        tmpValue_1 = getMixedDepBetClass(classID, otherClassID)
        tmpValue_2 = getMixedDepBetClass(otherClassID, classID)
        tmpValue = max(tmpValue_2, tmpValue_1)

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
    global CLASSID2NAMEDict
    global TRACE_DEP_DICT
    dep = 0
    className = CLASSID2NAMEDict[classID]
    if className in TRACE_DEP_DICT:
        if clusterID in TRACE_DEP_DICT[className]:
            dep = TRACE_DEP_DICT[className][clusterID]
    return dep


#mixed dep = (dep + trace_dep)/2   from classID to clusterID
def getFinalDep(classID, clusterID):
    global CLASSID2NAMEDict
    global FINALCLUSTERDict
    global MIXED_DEP_DICT
    global CLASSID2NAMEDict

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
    global ASSIGN_THR
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


def getFinalDep_class_cluster(classList, clusterID):
    global MERGE_FUNC
    global FINALCLUSTERDict
    global MIXED_DEP_DICT
    global CLASSID2NAMEDict
    depValueList = list()
    for classID in classList:
        depValue = getFinalDep(classID, clusterID)
        depValueList.append(depValue)
    return sum(depValueList) / len(depValueList)





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
    #print '\nafter merging class: ', classSetList
    return classSetList, clusterSetList





def coreProcess(mergedClassList, mergedClusterList, currentClusterIndex):
    #for classID in class2ClusterDict:
    global CONSIDER_FLAG
    global MERGE_FUNC
    global ASSIGN_THR
    global FINALCLUSTERDict
    global MIXED_DEP_DICT
    global CLASSID2NAMEDict
    for index in range(0, len(mergedClassList)):
        if CONSIDER_FLAG == 'onlyoverlap':  # hypothesis 1
            #clusterList = class2ClusterDict[classID]
            clusterList = mergedClusterList[index]
        elif CONSIDER_FLAG == 'all':        # hypothesis 2
            clusterList = FINALCLUSTERDict.keys()

        depList = list()
        for eachClusterID in clusterList:
            #depList[]=([eachClusterID, mixedValue])
            finalDep = getFinalDep_class_cluster(mergedClassList[index], eachClusterID)
            depList.append([eachClusterID, finalDep])

        #make decision, clusterList = ...
        #print 'before making decision, depList=[clusterID, dep]=', depList
        decisionClusterList = getClusterDecision(depList)
        #print 'after making decision, resList[clusterID]=', decisionClusterList

        if len(decisionClusterList) == 0:  #extract a single cluster
            #FINALCLUSTERDict[currentClusterIndex] = [classID]
            FINALCLUSTERDict[currentClusterIndex] = mergedClassList[index]
            currentClusterIndex += 1
        else: #multiCopy or singleCopy
            for assignedClusterID in decisionClusterList:
                if assignedClusterID not in FINALCLUSTERDict:
                    FINALCLUSTERDict[assignedClusterID] = list()
                #FINALCLUSTERDict[assignedClusterID].append(classID)
                FINALCLUSTERDict[assignedClusterID].extend(mergedClassList[index])




def coreProcess1(class2ClusterDict, currentClusterIndex):
    global CONSIDER_FLAG
    for classID in class2ClusterDict:
        if CONSIDER_FLAG == 'onlyoverlap':  # hypothesis 1
            clusterList = class2ClusterDict[classID]
        elif CONSIDER_FLAG == 'all':        # hypothesis 2
            clusterList = FINALCLUSTERDict.keys()

        depList = list()
        for eachClusterID in clusterList:
            #depList[]=([eachClusterID, mixedValue])
            finalDep = getFinalDep(classID, eachClusterID, MERGE_FUNC, FINALCLUSTERDict)
            depList.append([eachClusterID, finalDep])

        #make decision, clusterList = ...
        #print 'before making decision, depList=[clusterID, dep]=', depList
        decisionClusterList = getClusterDecision(depList)
        #print 'after making decision, resList[clusterID]=', decisionClusterList

        if len(decisionClusterList) == 0:  #extract a single cluster
            FINALCLUSTERDict[currentClusterIndex] = [classID]
            currentClusterIndex += 1
        else: #multiCopy or singleCopy
            for assignedClusterID in decisionClusterList:
                if assignedClusterID not in FINALCLUSTERDict:
                    FINALCLUSTERDict[assignedClusterID] = list()
                FINALCLUSTERDict[assignedClusterID].append(classID)




def write2CSV(fileName):
    global FINALCLUSTERDict
    global CLASSID2NAMEDict
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
#        originalClusterFile.csv (classID, testcaseID, testcaseName)(include fv=0 clusters)
#        initclusterFile.csv(non-lapped classFile)
#        classListFile.csv(overlapped classFile)
#        FinalClusterFile
#        ASSIGN_THR
'''
if __name__ == '__main__':
    #beacuse some clusters's classes are all overlapped,
    #the cluster is null, mixeddep=0.
    #so use traceDep to compensate this situation
    depFileName = sys.argv[1]
    traceDepFileName = sys.argv[2]
    orignalClusterFileName = sys.argv[3]
    clusterFileName = sys.argv[4]
    classListFileName = sys.argv[5]
    outClusterFileName = sys.argv[6]
    ASSIGN_THR = float(sys.argv[7])   #default is 0.03
'''
def processOverlappedClass(depFileName, traceDepFileName, orignalClusterFileName, clusterFileName, classListFileName, outClusterFileName, thr):
    global MIXED_DEP_DICT
    global TRACE_DEP_DICT
    global ASSIGN_THR
    global CONSIDER_FLAG
    global FINALCLUSTERDict
    global CLASSID2NAMEDict
    global MERGE_FUNC

    FINALCLUSTERDict = dict()
    CLASSID2NAMEDict = dict()
    ASSIGN_THR = thr
    CONSIDER_FLAG = 'onlyoverlap'
    MERGE_FUNC = 'AVG'
    MIXED_DEP_DICT = readMixedDepFile(depFileName)
    TRACE_DEP_DICT = readTraceDepFile(traceDepFileName) #read and normalized

    #overlappedClassFIle and nonoverlapclassFIle are not including fv=0 clusterID, alloverlapedCLusterID
    FINALCLUSTERDict = readOrignalClusterFile (orignalClusterFileName)   #init FINALCLUSTERS.key
    CLASSID2NAMEDict = readNonlapClassFile(clusterFileName)  #init dict[clusterID] = classIDList
    class2ClusterDict = readOverlapClassFile(classListFileName) #dict[classID] = clusterIDList
    #print 'class2ClusterDict=',class2ClusterDict

    currentClusterIndex = len(FINALCLUSTERDict) #include fv=0 clustersID

    #print 'currentClusterIndex=', currentClusterIndex
    #print 'intiClusters', FINALCLUSTERDict

    [mergedClassList, mergedClusterList]= preProcess(class2ClusterDict)
    coreProcess(mergedClassList, mergedClusterList, currentClusterIndex)
    write2CSV(outClusterFileName)
