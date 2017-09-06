
import sys
import csv

CLASSID2NAMEDict = dict()

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

#for each cluster, contanining classes (non-overlap) are saved to file
def writeBuSet2File(clusterIDList, buSetList, clusterFvList, fileName):
    resList = list()
    resList.append(['classID', 'className', 'clusterID', ])

    for index in range(0, len(buSetList)):
        clusterID = clusterIDList[index]
        for classID in list(buSetList[index]):
            resList.append([classID, CLASSID2NAMEDict[classID], clusterID, clusterFvList[clusterID][classID]])
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)
    #print fileName

#len(clusterIDList) == 1' s class
def writeBuSet2File(classID2ClusterDict , fileName ):
    resList = list()
    for classID in classID2ClusterDict:
        clusterIDList = classID2ClusterDict[classID]
        if len(clusterIDList) == 1:
            tmp = [classID, CLASSID2NAMEDict[classID], clusterIDList[0] ]
            resList.append(tmp)
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerow(['classID', 'className', 'clusterID'])
        writer.writerows(resList)
    print fileName

#len(clusterIDList) > 1' s class
def writeJiaoSet2File(classID2ClusterDict, fileName):
    resList = list()
    for classID in classID2ClusterDict:
        clusterIDList = classID2ClusterDict[classID]
        if len(clusterIDList) > 1:
            clusterIDList = [str(each) for each in clusterIDList]
            clusterIDStr = ':'.join(clusterIDList)
            tmp = [classID, CLASSID2NAMEDict[classID], clusterIDStr ]
            resList.append(tmp)
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerow(['classID', 'className', 'clusterIDList'])
        writer.writerows(resList)
    print fileName

def writeMergedFv2File(clusterFvList, fileName):
    resList = list()
    for clusterID in range(0, len(clusterFvList)):
        for classID in range(0, len(clusterFvList[clusterID])):
            if clusterFvList[clusterID][classID] != 0:
                tmp = [ CLASSID2NAMEDict[classID], clusterID, clusterFvList[clusterID][classID] ]
                resList.append(tmp)
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerow(['className', 'clusterID', 'count'])
        writer.writerows(resList)
    print fileName


#process the clustering result
#python pro.py    clusterFileName.csv  featureVectorFileName.csv  classFileName.csv  nonlapFileName lapFileName  class2clusterfv.csv
#../testcase_data/jforum219/coreprocess/jforum219_testcase1_jm_AVG_'${i}'.csv'
if __name__ == '__main__':
    clusterFileName = sys.argv[1]
    featureVectorFileName = sys.argv[2]
    classFileName = sys.argv[3]
    nonlapFileName = sys.argv[4] #output
    lapFileName =sys.argv[5] #output
    mergedFvFileName = sys.argv[6]
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

    writeBuSet2File(classID2ClusterDict , nonlapFileName )
    writeJiaoSet2File(classID2ClusterDict, lapFileName)
    writeMergedFv2File(clusterFvList, mergedFvFileName)
