# -*- coding: utf-8 -*-
import sys
import csv

MERGE_FUNC = 'AVG'   #class-cluster depvalue = min,max,avg
ASSIGN_THR = 0.03    #defalut, is a cmd argv

FINALCLUSTERDict = dict()  #[clusterID] = classIDList
STRUCT_DEP_DICT = dict() #dict[classname1][classname2] = structdep
CLASSID2NAMEDict = dict()
CLASSNAME2IDDict = dict()

#structDep = 0,1
def readDepFile(fileName):
    #print fileName
    resDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className1, className2, structDep] = each
            if '1' in structDep:
                structDep = 1
            else:
                structDep = 0
            if className1 not in resDict:
                resDict[className1] = dict()
            resDict[className1][className2] = structDep
    return resDict


def readClusterFile (fileName):
    finalClusterDict = dict()  #dict[clusterID] = list()
    classIndex = 0
    with open(fileName) as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className, clusterID] = each
            if classID == 'classID':
                continue
            clusterID = int(clusterID)

            if className not in CLASSNAME2IDDict:
                CLASSID2NAMEDict[classIndex] = className
                CLASSNAME2IDDict[className] = classIndex
                classIndex += 1

            if clusterID not in finalClusterDict:
                finalClusterDict[clusterID] = list()
            finalClusterDict[clusterID].append(CLASSNAME2IDDict[className])
    return finalClusterDict


def readClassFile(fileName):
    resList = list()
    with open(fileName, 'r') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            resList.append(className)
    return resList

def getStructDepBetClass(className1, className2):
    if className1 in STRUCT_DEP_DICT:
        if className2 in STRUCT_DEP_DICT[className1]:
            return STRUCT_DEP_DICT[className1][className2]
    return 0

def getDepBetClassCluster(className, clusterID):
    depValueList = list()
    for classID in FINALCLUSTERDict[clusterID]:
        className2 = CLASSID2NAMEDict[classID]
        tmp = getStructDepBetClass(className, className2)
        depValueList.append(tmp)
    return max(depValueList)


def countUnprocessedClass(classList, isProcessedDict):
    count = 0
    for className in classList:
        if className not in isProcessedDict:
            count += 1
    return count

def processClassToCluster(classList):
    isProcessedDict = dict()  #[className] = 1
    isChanged = True
    unprocessedCount = len(classList)

    while isChanged == True  and unprocessedCount > 0:
        #print '111111111111111'
        isChanged = False
        for eachClassName in classList:
            if eachClassName in isProcessedDict:
                continue
            for eachClusterID in FINALCLUSTERDict:
                if getDepBetClassCluster(eachClassName, eachClusterID) == 1:
                    print 'assign class to cluster: ', eachClassName, eachClusterID
                    if eachClassName not in CLASSNAME2IDDict:
                        currentClassID = len(CLASSNAME2IDDict)
                        CLASSNAME2IDDict[eachClassName] = currentClassID
                        CLASSID2NAMEDict[currentClassID]= eachClassName
                    else:
                        currentClassID = CLASSNAME2IDDict[eachClassName]
                    FINALCLUSTERDict[eachClusterID].append(currentClassID)
                    isProcessedDict[eachClassName] = 1
                    isChanged = True
        unprocessedCount = countUnprocessedClass(classList, isProcessedDict)
        #print isChanged, unprocessedCount
    return isProcessedDict


def writeUnproClassa2File(classList, isProcessedDict, fileName):
    resList = list()
    for className in classList:
        if className not in isProcessedDict:
            resList.append([className])

    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)
    print fileName


def writeCluster2File(fileName):
    listlist = list()
    listlist.append(['className', 'clusterID'])
    for clusterID in FINALCLUSTERDict:
        for classID in FINALCLUSTERDict[clusterID]:
            listlist.append([CLASSID2NAMEDict[classID], clusterID])
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(listlist)
    print fileName

#assign the unprocessed no_ts_cover_class to existing clusters. not adding new clusters
#python pro.py  structdepFile.csv   clusterFile.csv  classList    outcluster.csv   unprocess.class.csv
if __name__ == '__main__':
    depFileName = sys.argv[1]
    clusterFileName = sys.argv[2]
    classFileName = sys.argv[3]
    outClusterFileName = sys.argv[4]
    outClassFileName = sys.argv[5]

    STRUCT_DEP_DICT = readDepFile(depFileName)
    FINALCLUSTERDict = readClusterFile(clusterFileName)   #init FINALCLUSTERS.key
    classList = readClassFile(classFileName)               #read unprocessed class

    #if class is struct dependent to cluster, then assign it. no matter its strong value
    isProcessedDict = processClassToCluster(classList)

    writeCluster2File(outClusterFileName)
    writeUnproClassa2File(classList, isProcessedDict, outClassFileName)
