
import sys
import csv

CLASSID2NAMEDict = dict()
SMOOTH_THR = 5

def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            resList.append(each)
    return resList

def writeCSV(listList, fileName):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)
    #print fileName
#classList=[ [id1, name1], [id2, name2], [id3, name3], ...]
def processClass(classList):
    classID2NameDict = dict()
    for each in classList:
        [classID, className] = each
        classID2NameDict[int(classID)] = className
    return classID2NameDict

#fvList = M= [ [ts1, ,,,,], [], [], ...]
def processFeatureVec(fvList):
    fvM = list()
    for eachList in fvList:
        del eachList[0] #testcaseName
        tmpList = list()
        for each in eachList:
            tmpList.append(int(each))
        fvM.append(tmpList)
    return fvM

#clusterList = [ [clusterID, testcaseID, testcaseName][][] ,  ...]
def processCluster(clusterList):
    resList = list()
    for eachList in clusterList:
        [clusterID, tsID, tsName] = eachList
        clusterID = int(clusterID)
        tsID = int(tsID)
        if len(resList) == clusterID:
            resList.append(list())
        resList[clusterID].append(tsID)
    return resList


#compute the classcount for each cluster
def mergeClusterFv(clusterList, fvList, classCount):
    resList = list()
    for clusterID in range(0, len(clusterList)):
        tsIDList = clusterList[clusterID]
        tmpList = [0] * classCount
        for eachTsID in tsIDList:
            #two list is sumed togeter for each element
            tmpList = map(lambda x, y : x + y, tmpList, fvList[eachTsID])
        resList.append(tmpList)
    return resList


#change the list into set, that is delete the '0' column
def trans2Set(clusterList):
    clusterClassIDDict = dict()
    index = 0
    for eachList in clusterList:
        tmpList = list()
        for classID in range(0, len(eachList)):
            if eachList[classID] != 0:
                tmpList.append(classID)
        clusterClassIDDict[index] = tmpList
        index += 1
    return clusterClassIDDict

#clusterID: [classList]  into  classID:[clusterIDList]
def reverseMap(cluster2ClassDict):
    class2ClusterDict = dict()
    for clusterID in cluster2ClassDict:
        classIDList = cluster2ClassDict[clusterID]
        for classID in classIDList:
            if classID not in class2ClusterDict:
                class2ClusterDict[classID] = list()
            class2ClusterDict[classID].append(clusterID)
    return class2ClusterDict

#smooth cluster, if a cell value < SMOOTH_THR, then make it 0.
def smoothClusterFv(cluster2ClassList):
    n = len(cluster2ClassList)
    m = len(cluster2ClassList[0])
    for i in range(0, n):
        for j in range(0, m):
            if cluster2ClassList[i][j] < SMOOTH_THR:
                cluster2ClassList[i][j] = 0
    return cluster2ClassList


def  getLowClass2ClusterDict(classID2ClusterDict, highClassIDList):
    #print 'high', len(highClassIDList)
    lowClassID2ClusterDict = dict() #[classID] =[clusterList]
    for classID in classID2ClusterDict:
        if classID not in highClassIDList:
            #print 'low', classID
            lowClassID2ClusterDict[classID] = classID2ClusterDict[classID]
    return lowClassID2ClusterDict

#len(clusterIDList) == 1' s class
#return arg1: nooverlapped class number
#return arg2: nooverlapped class nuymber / cluster_num
def buSetMetric(classID2ClusterDict ):
    clusterDict = dict()
    nonOverlappedClassCount =0
    for classID in classID2ClusterDict:
        clusterIDList = classID2ClusterDict[classID]
        if len(clusterIDList) == 1:
            nonOverlappedClassCount += 1
            clusterID = clusterIDList[0]
            if clusterID not in clusterDict:
                clusterDict[clusterID] = list()
            clusterDict[clusterID].append(classID)
    if nonOverlappedClassCount == 0:
        avg = 0
    else:
        avg =  nonOverlappedClassCount / float(len(clusterDict))
    return nonOverlappedClassCount, avg


def jiaoSetAll(classID2ClusterDict):
    classDict = dict()
    for classID in classID2ClusterDict:
        clusterIDList = classID2ClusterDict[classID]
        if len(clusterIDList) > 1:
            classDict[classID] = clusterIDList
    return classDict

#len(clusterIDList) > 1' s class
#return arg1 = overlapped classCount
#return argv2 = cluster_count /overlapped classCount
def jiaoSetMetric(classID2ClusterDict):
    classDict = dict()
    for classID in classID2ClusterDict:
        clusterIDList = classID2ClusterDict[classID]
        if len(clusterIDList) > 1:
            classDict[classID] = clusterIDList
    overlappedclassCount = len(classDict)

    clusterCount = 0
    for classID in classDict:
        clusterCount += len(classDict[classID])
    if overlappedclassCount == 0:
        avg = 0
    else:
        avg = clusterCount / float(overlappedclassCount)
    return overlappedclassCount, avg

def totalMetic(classID2ClusterDict, allOverlapClassID2ClusterDict, highClassID2ClusterDict, lowClassID2ClusterDict):
    [nonOverlappedClassCount, nonOverlappedAvg] = buSetMetric(classID2ClusterDict)
    [overlappedClassCount, overlappedAvg] = jiaoSetMetric(allOverlapClassID2ClusterDict)
    [high_overlappedClassCount, high_overlappedAvg] = jiaoSetMetric(highClassID2ClusterDict)
    [low_overlappedClassCount, low_overlappedAvg] = jiaoSetMetric(lowClassID2ClusterDict)
    strstr = ''
    strstr += (str(nonOverlappedClassCount) + ',')
    strstr += (str(nonOverlappedAvg) + ',')
    strstr += (str(overlappedClassCount) + ',')
    strstr += (str(overlappedAvg) + ',')
    strstr += (str(high_overlappedClassCount) + ',')
    strstr += (str(high_overlappedAvg) + ',')
    strstr += (str(low_overlappedClassCount) + ',')
    strstr +=  str(low_overlappedAvg)
    print strstr


#process the clustering result
#python pro.py    clusterFileName.csv  featureVectorFileName.csv  classFileName.csv
#../testcase_data/jforum219/coreprocess/jforum219_testcase1_jm_AVG_'${i}'.csv'
if __name__ == '__main__':
    clusterFileName = sys.argv[1]
    featureVectorFileName = sys.argv[2]
    classFileName = sys.argv[3]

    classList = readCSV(classFileName)
    CLASSID2NAMEDict = processClass(classList)
    fvList = readCSV(featureVectorFileName)
    fvList = processFeatureVec(fvList)
    clusterList = readCSV(clusterFileName)
    clusterList = processCluster(clusterList)

    #process the original cluster *******************************
    #clusterFvList [clusterID] = fv[class1, class2, ...]
    clusterFvList = mergeClusterFv(clusterList, fvList, len(CLASSID2NAMEDict))  #clusterFvList is the final cluster
    clusterIDClassDict = trans2Set(clusterFvList)  #some cluster maybe null set, has been exclude by dict
    classID2ClusterDict = reverseMap(clusterIDClassDict)  #have got the classID->clusterIDset
    allOverlapClassID2ClusterDict = jiaoSetAll(classID2ClusterDict)

    #after smooth:  high-overlap (new is high)
    newClusterFvList = smoothClusterFv(clusterFvList)
    newClusterIDClassDict = trans2Set(newClusterFvList)
    newClassID2ClusterDict = reverseMap(newClusterIDClassDict)
    highClassID2ClusterDict = jiaoSetAll(newClassID2ClusterDict)
    lowClassID2ClusterDict = getLowClass2ClusterDict(allOverlapClassID2ClusterDict, highClassID2ClusterDict)

    totalMetic(classID2ClusterDict, allOverlapClassID2ClusterDict, highClassID2ClusterDict, lowClassID2ClusterDict)
