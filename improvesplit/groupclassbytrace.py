
import sys
import csv

CLASSID2NAMEDict = dict()

def readCSV(fileName):
    resList = list()
    with open(fileName, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            resList.append(each)
    return resList

def writeCSV(listList, fileName):
    with open(fileName, "w", newline="") as fp:
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


def getCluster2ClassMap(fvList):
    resmap = dict()#[clusterId] = [classIds]
    clusterID = -1
    for each1 in fvList:
        if sum(each1) != 0:
            clusterID += 1
            resmap[clusterID] = list()
            for classId in range(0, len(each1)):
                if each1[classId] != 0:
                    resmap[clusterID].append(classId)
    return resmap




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


#if some class are appearing in same cluterList, then they should group togeter
#that is, frequent items (classes) in traces are responsible for same functionality.
def groupClassByCluters(classID2ClusterDict):
    id = 0
    newGroupIDDict = dict() #cluterIDstr->clusterID
    newGroupIDReverseDict = dict()  #clusterID -> clusterIDStr
    resDict = dict() #[id]= classID,
    for classID in classID2ClusterDict:
        clusterIDList = classID2ClusterDict[classID]
        clusterIDList = [str(each) for each in clusterIDList]
        clusterIDStr = ';'.join(clusterIDList)
        if clusterIDStr not in newGroupIDDict:
            newGroupIDDict[clusterIDStr] = id
            newGroupIDReverseDict[id] = clusterIDStr
            id += 1

        currentId = newGroupIDDict[clusterIDStr]
        if currentId not in resDict:
            resDict[currentId] = list()
        resDict[currentId].append(classID)

    alist = list()
    alist.append(["classId", "className", "groupId", "groupLen", "groupDetail"])
    for groupId in resDict:
        groupIDStr = newGroupIDReverseDict[groupId]
        groupIDList = groupIDStr.split(";")
        for classId in resDict[groupId]:
            tmp = [classId, CLASSID2NAMEDict[classId], groupId, len(groupIDList), groupIDStr]
            alist.append(tmp)
    return alist

'''
group class by the located traceId.
'''
#python pro.py  featureVectorFileName.csv  classFileName.csv   classgroupfile.csv
if __name__ == '__main__':
    featureVectorFileName = sys.argv[1]
    classFileName = sys.argv[2]
    groupfilename = sys.argv[3]

    #read classlist which in order with cluster file
    classList = readCSV(classFileName)
    CLASSID2NAMEDict = processClass(classList)

    #read feature vector file
    fvList = readCSV(featureVectorFileName)
    fvList = processFeatureVec(fvList) #list[ts=i] = fv

    #one ts = one cluster#dict[clusterID] =[classes]
    clusterIDClassDict = getCluster2ClassMap(fvList)
    classID2ClusterDict = reverseMap(clusterIDClassDict)  #have got the classID->clusterIDset

    groupList = groupClassByCluters(classID2ClusterDict)
    writeCSV(groupList, groupfilename)
