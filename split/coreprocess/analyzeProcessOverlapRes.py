import sys
import csv

CLASSNAME2IDDict = dict()
CLASSID2NAMEDict = dict() #[classID] = className
CLASSID2CLUSTERDict = dict() #[classID] = list[clusterID]
CLUSTERID2CLASSDict = dict() #[clusterID] = list[classID]

CLUSTERID2TSDict = dict() #[clusterID] = [testcaseID1, id2, ..]
TSID2NAMEDict = dict()   #[testcaseID] = testcaseName


TRACEList = list()  #[traceID] = list()=[ edgeID1, edgeID2 ...]
METHODList = list()  #[methodID] = METHOD()
EDGEList = list()   #[edgeID] = EDGE()
EDGEDict = dict()  #dict[methodID1][methodID2] = edgeID

class MethodNode:
    def __init__(self, ID, longname, shortname, className):
        self.ID = ID
        self.longname = longname #has paralist
        self.shortname = shortname #has paralist
        self.className = className

class MethodEdge:
    def __init__(self, startID, endID):
        self.startID = startID
        self.endID = endID

# methodname_full.(prafulltype, parafulltype)
def GetLongName(methodName, para):
    if para == '':
        post = '()'
    else:
        post = '(' + para + ')'
    return methodName + post

#paraList = ['A.B.C', 'D.E.F'], return ['B.C','E.F']
def GetShortParaList(paraList):
    oneList = list()
    for para in paraList:
        arr = para.split('.')
        if len(arr) > 2:
            shortname = arr[len(arr) - 2] + '.' + arr[len(arr) - 1]
        else:
            shortname = para
        oneList.append(shortname)
    return oneList


# methodname_short(prashorrtype, parashottype)
def GetShortName(methodName, para):
    arr = methodName.split('.')
    if len(arr) >= 2:
        shortname = arr[len(arr) - 2] + '.' + arr[len(arr) - 1]
    else:
        shortname = methodName

    if para == '':
        post = '()'
    else:
        paraList = para.split(',')
        shortParaList = GetShortList(paraList)
        post = '('  + ','.join(shortParaList) + ')'
    return shortname + post


#return TRACEList
# methodNodeList,    methodEdgeList. egdeDict
def readWorkflowFile(filename):
    methodIndex = 0
    edgeIndex = 0
    tmpMethodDict = dict() #dict(methodname) = ID
    tmpClassDict = dict()  #dict(className) = ID

    with open(filename, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            #print each
            [traceID, order, structtype, startMethodName, endMethodName, m1_para, m2_para, class1, class2, m1_return, m2_return] = each
            if traceID == 'traceID':
                continue
            startLongName = GetLongName(startMethodName, m1_para)
            endLongName = GetLongName(endMethodName, m2_para)
            startShortName = GetShortName(startMethodName, m1_para)
            endShortName = GetShortName(endMethodName, m2_para)
            if startLongName not in tmpMethodDict:
                tmpMethodDict[startLongName] = methodIndex
                oneMethod = MethodNode(methodIndex, startLongName, startShortName, class1)
                METHODList.append(oneMethod)
                methodIndex += 1
            if endLongName not in tmpMethodDict:
                tmpMethodDict[endLongName] = methodIndex
                oneMethod = MethodNode(methodIndex, endLongName, endShortName, class2)
                METHODList.append(oneMethod)
                methodIndex += 1

            startID = tmpMethodDict[startLongName]
            endID = tmpMethodDict[endLongName]
            if startID not in EDGEDict:
                EDGEDIct = dict()
            if endID not in EDGEDict[startID]:
                EDGEDict[startID][endID] = edgeIndex
                oneEdge = MethodEdge(startID, endID)
                EDGELIST.append(edgeIndex)
                edgeIndex += 1

            edgeID = EDGEDict[startID][endID]
            currentLen = len(TRACEList)
            if int(traceID) == currentLen:
                TRACEList.append(list())
            TRACEList[int(traceID)].append(edgeID)


def isInterEdge(clusterID, startID, endID):
    className1 = METHODList[startID].className
    className2 = METHODList[endID].className
    classID1 = -1
    classID2 = -1
    clusterIDList1 = list()
    clusterIDList2 = list()
    if className1 in CLASSNAME2IDDict:
        classID1 = CLASSNAME2IDDict[className1]
    if className2 in CLASSNAME2IDDict:
        classID2 = CLASSNAME2IDDict[className2]
    if classID1 != -1:
        clusterIDList1 = CLASSID2CLUSTERDict[classID1]
    if classID2 != -1:
        clusterIDList2 = CLASSID2CLUSTERDict[classID2]

    if classID1 == -1 and classID2 == -1:
        return False
    elif classID1 == -1 and clusterID in clusterIDList2:
        return False
    elif clusterID in clusterIDList1 and clusterID in clusterIDList2:
        return False
    elif clusterID in clusterIDList1 and classID2 == -1:
        return False
    elif classID1 != -1 and classID2 != -1:
        set1 = set(clusterIDList1)
        set2 = set(clusterIDList2)
        if len(set1 & set2) != 0:
            return False
    else:
        return True



#operate TRACEList[traceID]=[edgeID1, edgeID2]
#generate res[traceID][interedgeID] = count
# not process fv=0 cluster, beacuse it is not in CLUSTERID2CLASSDict
def filterOutInterEdge():
    resDict = dict()  #dict[traceID][interEdgeID] = count
    for clusterID in CLUSTERID2CLASSDict:
        traceIDList = CLUSTERID2TSDict[clusterID]
        for traceID in TRACEList:
            for egdeID in TRACEList[traceID]:
                startMethodID = EDGEList[edgeID].startID
                endMethodID = EDGEList[edgeID].endID
                isCross = isInterEdge(clusterID, startID, endID)
                if isCross == True:
                    if traceID not in resDict:
                        resDict[traceID] = dict()
                    if edgeID not in resDict[traceID]:
                        resDict[traceID][edgeID] = 1
                    else:
                        resDict[traceID][edgeID] += 1
    return resDict

#generate res[traceID][interedgeID] = count
def workflowMetric(interDict):
    interComWfCount = 0 # workflow number which need inter-omponent communication
    withinComWfCount = 0 #  ..............which not need inter-omponent communication
    interCallCount = 0   #sum up interCallCount in allworkflow
    interCallCount_avg = 0 #interCallCount per allworkflow
    interCallCount_f = 0
    interCallCount_avg_f = 0

    interComWfCount = len(interDict)
    withinComWfCount = len(CLUSTERID2CLASSDict) - interComWfCount
    tmpList = list()
    for traceID in interDict[traceID]:
        keyList = interDict[traceID].keys()  #interEdgeIDList
        tmpList.append(len(keyList))
    interCallCount =sum(tmpList)
    if len(tmpList) != 0:
        interCallCount_avg = interCallCount / float(len(tmpList))
    else:
        interCallCount_avg = 0.0

    tmpList = list()
    for traceID in interDict[traceID]:
        valueList = interDict[traceID].values()  #interEdgeCountList
        tmpList.append(len(valueList))
    interCallCount_f =sum(tmpList)
    if len(tmpList) != 0:
        interCallCount_avg_f = interCallCount_f / float(len(tmpList))
    else:
        interCallCount_avg_f = 0.0

    return interComWfCount, withinComWfCount, interCallCount, interCallCount_avg, interCallCount_f, interCallCount_avg_f


# -1 => yourself.
# other-> -1 is your provided private API
# other-> your is your provided PrivateAPI
#generate res[traceID][interedgeID] = count
def extractAPI(interDict):
    clusterAPIDict = list()  #dict[cluserID] = [uniqueCalleeMethodID1, 2, ...]
    for clusterID in CLUSTERID2CLASSDict:
        clusterAPIDict[clusterID] = list()
        traceID = CLUSTERID2TSDict[clusterID]
        if traceID in interDict:
            for interEdgeID in interDict[traceID]:
                oneEdge = EDGEList[interEdgeID]
                #className1 = METHODList[oneEdge.startID].className
                className2 = METHODList[oneEdge.endID].className2
                if className2 in CLASSNAME2IDDict:
                    classID = CLASSNAME2IDDict[className2]
                    if classID in CLUSTERID2CLASSDict[clusterID]:
                        clusterAPIDict[clusterID].append(oneEdge.endID)
    return clusterAPIDict


def APIMetric(clusterAPIDict):
    APICount = 0
    APICount_avg = 0 #api count /clusterNum
    for clusterID in clusterAPIDict:
        APIList = clusterAPIDict[clusterID]
        APICount += len(APIList)
    APICount_avg = APICount / float(len(clusterAPIDict))
    return APICount, APICount_avg


def readOverlapResFile(fileName):
    classID2NameDict = dict()
    classID2ClusterDict = dict()
    clusterID2ClassDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className, clusterID] = each
            if classID == 'classID':
                continue
            classID = int(classID)
            clusterID = int(clusterID)
            if classID not in classID2NameDict:
                classID2NameDict[classID] = className

            if classID not in classID2ClusterDict:
                classID2ClusterDict[classID] = list()
            classID2ClusterDict[classID].append(clusterID)

            if clusterID not in clusterID2ClassDict:
                clusterID2ClassDict[clusterID] = list()
            clusterID2ClassDict[clusterID].append(classID)
    return classID2NameDict, classID2ClusterDict, clusterID2ClassDict


def readTestCaseClusterFile(fileName):
    clusterID2TsDict = dict()
    tsID2NameDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [clusterID, testcaseID, testcaseName] = each
            clusterID = int(clusterID)
            testcaseID = int(testcaseID)
            if clusterID not in clusterID2TsDict:
                clusterID2TsDict[clusterID] = list()
            clusterID2TsDict[clusterID].append(testcaseID)

            if testcaseID not in tsID2NameDict:
                tsID2NameDict[testcaseID] = testcaseName
    return clusterID2TsDict, tsID2NameDict






#return clusterNum, noZeroFvClusterNum,  repeatClassNum,  repeatCount/repeatClassNum
def basicMetric():
    totalClusterNum = len(CLUSTERID2TSDict)
    noZeroClusterNum = len(CLUSTERID2CLASSDict)

    repeatClassDict = dict()  #classID, repeatCount
    for classID in CLASSID2CLUSTERDict:
        clusterIDList = CLASSID2CLUSTERDict[classID]
        if len(clusterIDList) > 1:
            repeatClassDict[classID] = len(clusterIDList)
    if len(repeatClassDict) == 0:
        repeatAvg = 0
    else:
        repeatAvg = round(sum(repeatClassDict.values()) / float(len(repeatClassDict)), 5)
    repeatNum = len(repeatClassDict)

    return totalClusterNum, noZeroClusterNum, repeatNum, repeatAvg


if __name__ == '__main__':
    overlapResFileName = sys.argv[1]  #[classID, className, clusterID ]
    testcaseClusterFileName = sys.argv[2] #[clusterID, testcaseID, testcaseName]
    workflowFileName = sys.argv[3]

    [CLASSID2NAMEDict, CLASSID2CLUSTERDict, CLUSTERID2CLASSDict] = readOverlapResFile(overlapResFileName)
    [CLUSTERID2TSDict, TSID2NAMEDict] = readTestCaseClusterFile(testcaseClusterFileName)

    #return TRACEList
    # methodNodeList,    methodEdgeList. egdeDict
    readWorkflowFile(workflowFileName)

    #operate TRACEList[traceID]=[edgeID1, edgeID2]
    #generate res[traceID][interedgeID] = count
    interTsEdgeDict = filterOutInterEdge()

    [totalClusterNum, noZeroClusterNum, repeatClassNum, repeatClassAvg] = basicMetric()
    [interComWfCount, withinComWfCount, interCallCount, interCallCount_avg, interCallCount_f, interCallCount_avg_f] = workflowMetric(interTsEdgeDict)

    clusterAPIDict = extractAPI(interTsEdgeDict)
    (APICount, APICount_avg) = APIMetric(clusterAPIDict)
