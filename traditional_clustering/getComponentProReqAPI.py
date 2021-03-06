import sys
import csv

CLASSNAME2IDDict = dict()
CLASSID2NAMEDict = dict() #[classID] = className
CLASSID2CLUSTERDict = dict() #[classID] = list[clusterID]
CLUSTERID2CLASSDict = dict() #[clusterID] = list[classID]

TRACEList = list()  #[traceID] = list()=[ edgeID1, edgeID2 ...]
METHODList = list()  #[methodID] = METHOD()
EDGEList = list()   #[edgeID] = EDGE()

class MethodNode:
    def __init__(self, ID, justname, longname, shortname, className, parameter, returnType):
        self.ID = ID
        self.justname = justname
        self.longname = longname #has paralist
        self.shortname = shortname #has paralist
        self.className = className
        self.parameter = parameter
        self.returnType = returnType

class MethodEdge:
    def __init__(self, startID, endID):
        self.startID = startID
        self.endID = endID

# methodname_full.(prafulltype, parafulltype)
def getLongName(methodName, para):
    if para == '':
        post = '()'
    else:
        post = '(' + para + ')'
    return methodName + post

#paraList = ['A.B.C', 'D.E.F'], return ['B.C','E.F']
def getShortParaList(paraList):
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
def getShortName(methodName, para):
    arr = methodName.split('.')
    if len(arr) >= 2:
        shortname = arr[len(arr) - 2] + '.' + arr[len(arr) - 1]
    else:
        shortname = methodName

    if para == '':
        post = '()'
    else:
        paraList = para.split(',')
        shortParaList = getShortParaList(paraList)
        post = '('  + ','.join(shortParaList) + ')'
    return shortname + post


#return TRACEList
# methodNodeList,    methodEdgeList
def readWorkflowFile(filename):
    methodIndex = 0
    edgeIndex = 0
    tmpMethodDict = dict() #dict(methodname) = ID
    tmpClassDict = dict()  #dict(className) = ID
    tmpEdgeDict = dict()  #dict[startID][endID] = edgeIndex
    with open(filename, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            #print each
            [traceID, order, structtype, startMethodName, endMethodName, m1_para, m2_para, class1, class2, m1_return, m2_return] = each
            if traceID == 'traceID':
                continue
            startLongName = getLongName(startMethodName, m1_para)
            endLongName = getLongName(endMethodName, m2_para)
            startShortName = getShortName(startMethodName, m1_para)
            endShortName = getShortName(endMethodName, m2_para)
            if startLongName not in tmpMethodDict:
                tmpMethodDict[startLongName] = methodIndex
                oneMethod = MethodNode(methodIndex, startMethodName, startLongName, startShortName, class1, m1_para, m1_return)
                METHODList.append(oneMethod)
                methodIndex += 1
            if endLongName not in tmpMethodDict:
                tmpMethodDict[endLongName] = methodIndex
                oneMethod = MethodNode(methodIndex, endMethodName, endLongName, endShortName, class2, m2_para, m2_return)
                METHODList.append(oneMethod)
                methodIndex += 1

            startID = tmpMethodDict[startLongName]
            endID = tmpMethodDict[endLongName]
            if startID not in tmpEdgeDict:
                tmpEdgeDict[startID] = dict()
            if endID not in tmpEdgeDict[startID]:
                tmpEdgeDict[startID][endID] = edgeIndex
                oneEdge = MethodEdge(startID, endID)
                EDGEList.append(oneEdge)
                edgeIndex += 1

            edgeID = tmpEdgeDict[startID][endID]
            currentLen = len(TRACEList)
            if int(traceID) == currentLen:
                TRACEList.append(list())
            TRACEList[int(traceID)].append(edgeID)


def isInterEdge(startID, endID):
    className1 = METHODList[startID].className
    className2 = METHODList[endID].className
    classID1 = -1
    classID2 = -1

    if className1 in CLASSNAME2IDDict:
        classID1 = CLASSNAME2IDDict[className1]
    if className2 in CLASSNAME2IDDict:
        classID2 = CLASSNAME2IDDict[className2]
    if classID1 != -1:
        clusterID1 = CLASSID2CLUSTERDict[classID1]
    else:
        clusterID = -1
    if classID2 != -1:
        clusterID2 = CLASSID2CLUSTERDict[classID2]
    else:
        clusterID = -1
    #print classID1,classID2,
    #print className1, className2
    #print clusterID1, clusterID2
    if classID1 == -1:
        return False
    if classID2 == -1:
        return False
    if classID1 != -1 and classID2 != -1:
        if clusterID1 == clusterID2:
            return False
    return True

#operate TRACEList[traceID]=[edgeID1, edgeID2]
#generate res[traceID][interedgeID] = count
# not process fv=0 cluster, beacuse it is not in CLUSTERID2CLASSDict
def filterOutInterEdge():
    resDict = dict()  #dict[traceID][interEdgeID] = count
    for traceID in range(0, len(TRACEList)):
        #print 'traceID=', traceID
        for edgeID in TRACEList[traceID]:
            #print 'edgeID=', edgeID
            startMethodID = EDGEList[edgeID].startID
            endMethodID = EDGEList[edgeID].endID
            isCross = isInterEdge(startMethodID, endMethodID)
            if isCross == True:
                #print 'True'
                if traceID not in resDict:
                    resDict[traceID] = dict()
                if edgeID not in resDict[traceID]:
                    resDict[traceID][edgeID] = 1
                else:
                    resDict[traceID][edgeID] += 1
    return resDict


def isInitMethod(methodID):
    methodName = METHODList[methodID].justname
    if '.<init>' in methodName:
        return True
    else:
        return False


# -1 => yourself.
# other-> -1 is your provided private API
# other-> your is your provided PrivateAPI
#generate res[clusterID][apiID] = 1 in case the api is repetitive
def extractAPI(interDict):
    clusterAPIDict = dict()  #dict[cluserID] = [uniqueCalleeMethodID1, 2, ...]
    for traceID in interDict:
        #print 'traceID=', traceID,
        for interEdgeID in interDict[traceID]:
            #print 'interEdgeID=', interEdgeID,
            oneEdge = EDGEList[interEdgeID]
            className1 = METHODList[oneEdge.startID].className
            className2 = METHODList[oneEdge.endID].className

            if className2 in CLASSNAME2IDDict:
                classID2 = CLASSNAME2IDDict[className2]
                clusterID2 = CLASSID2CLUSTERDict[classID2]
            if className1 in CLASSNAME2IDDict:
                classID1 = CLASSNAME2IDDict[className1]
                clusterID1 = CLASSID2CLUSTERDict[classID1]
            # not repeat, that is, one class only belongs to one cluster
            if clusterID1 not in clusterAPIDict:
                clusterAPIDict[clusterID1] = dict()
            if clusterID2 not in clusterAPIDict[clusterID1]:
                clusterAPIDict[clusterID1][clusterID2] = dict()
            if isInitMethod(oneEdge.endID) == False and (oneEdge.endID not in clusterAPIDict[clusterID1][clusterID2]):
                clusterAPIDict[clusterID1][clusterID2][oneEdge.endID] = 1

    return clusterAPIDict

#clusterAPIDict[clusterID][apiID] = 1
def writeAPI(clusterAPIDict, fileName):
    resList = list()
    resList.append(['clusterID1', 'clusterID2', 'apiClass','apiMethod', 'parameter', 'return'])
    for clusterID1 in clusterAPIDict:
        for clusterID2 in clusterAPIDict[clusterID1]:
            for methodID in clusterAPIDict[clusterID1][clusterID2]:
                tmpList = list()
                tmpList.append(clusterID1)
                tmpList.append(clusterID2)
                oneMethod = METHODList[methodID]
                tmpList.append(oneMethod.className)
                tmpList.append(oneMethod.justname)
                tmpList.append(oneMethod.parameter)
                tmpList.append(oneMethod.returnType)
                resList.append(tmpList)

    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)
    print fileName

def readClusterFile(fileName):
    classID2NameDict = dict()
    className2IDDict = dict()
    classID2ClusterDict = dict()
    clusterID2ClassDict = dict()
    classIndex = 0
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [containes, clusterID, className] = each
            if containes == 'containes':
                continue
            clusterID = int(clusterID)

            if className not in className2IDDict:
                className2IDDict[className] = classIndex
                classID2NameDict[classIndex] = className
                classIndex += 1

            classID = className2IDDict[className]
            classID2ClusterDict[classID] = clusterID
            if clusterID not in clusterID2ClassDict:
                clusterID2ClassDict[clusterID] = list()
            clusterID2ClassDict[clusterID].append(classID)
    #print 'classID2NameDict:' ,classID2NameDict
    #print 'classID2ClusterDict:', classID2ClusterDict
    #print 'clusterID2ClassDict:', clusterID2ClassDict
    return classID2NameDict, className2IDDict, classID2ClusterDict, clusterID2ClassDict



#python pro.py
#clusterFile.csv
#workflow/jforum219_workflow_reduced.csv
#apiFileName.csv
if __name__ == '__main__':
    clusterFileName = sys.argv[1]  #[classID, className, clusterID ]
    workflowFileName = sys.argv[2]
    apiFileName = sys.argv[3]
    [CLASSID2NAMEDict, CLASSNAME2IDDict, CLASSID2CLUSTERDict, CLUSTERID2CLASSDict] = readClusterFile(clusterFileName)
    readWorkflowFile(workflowFileName) #return TRACEList, methodNodeList,    methodEdgeList.
    #print 'TRACEList', TRACEList
    #print 'METHODList', METHODList

    #operate TRACEList[traceID]=[edgeID1, edgeID2], generate res[traceID][interedgeID] = count
    interTsEdgeDict = filterOutInterEdge()
    ##print 'interTsEdgeDict=',interTsEdgeDict

    clusterAPIDict = extractAPI(interTsEdgeDict)
    writeAPI(clusterAPIDict, apiFileName)
