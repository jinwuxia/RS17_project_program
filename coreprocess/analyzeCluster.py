
import sys
import csv

SMOOTH_THR = 10



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
    '''
    print "\nfirst process cluster..."
    for each in resList:
        print each
    '''
    return resList

#print set by classname instead of classID
def printSet(oneSet, classID2NameDict):
    resList = list()
    for classID in list(oneSet):
        resList.append(classID2NameDict[classID])
    return resList

#compute the classcount for each cluster
def mergeCluster(clusterList, fvList, classCount):
    resList = list()
    for clusterID in range(0, len(clusterList)):
        tsIDList = clusterList[clusterID]
        tmpList = [0] * classCount
        for eachTsID in tsIDList:
            #two list is sumed togeter for each element
            tmpList = map(lambda x, y : x + y, tmpList, fvList[eachTsID])
        resList.append(tmpList)
    '''
    print "\nafter merge..."
    for each in resList:
        print each
    '''
    return resList

#smooth cluster, if a class total number < SMOOTH_THR, then make it 0.
def del_smoothCluster(clusterList):
    clusterCount = len(clusterList)
    classCount = len(clusterList[0])
    for j in range(0, classCount):
        tmp = 0
        for i in range(0, clusterCount):
            tmp += clusterList[i][j]
        if tmp < SMOOTH_THR:
            for i in range(0, clusterCount):
                clusterList[i][j] = 0

    return clusterList

#smooth cluster, if a cell value < SMOOTH_THR, then make it 0.
def smoothCluster(clusterList):
    n = len(clusterList)
    m = len(clusterList[0])
    for i in range(0, n):
        for j in range(0, m):
            if clusterList[i][j] < SMOOTH_THR:
                clusterList[i][j] = 0
    return clusterList


#change the list into set, that is delete the '0' column
def trans2Set(clusterList):
    clusterClassIDList = list()
    for eachList in clusterList:
        tmpList = list()
        for classID in range(0, len(eachList)):
            if eachList[classID] != 0:
                tmpList.append(classID)
        clusterClassIDList.append(tmpList)
    '''
    print "\nafter transformation"
    for each in clusterClassIDList:
        print each
    '''
    return clusterClassIDList


#dict[cluterID: [classIDList]]
def excludeNullClassCluster(clusterClassIDList):
    clusterClassIDDict = dict()
    for clusterID in range(0, len(clusterClassIDList)):
        classIDList = clusterClassIDList[clusterID]
        if len(classIDList) != 0:
            clusterClassIDDict[clusterID] = classIDList
    return clusterClassIDDict



#set operation: get each cluster's differSet
#list = [classid1, classid2,..] ,  [classid3, classid2, .. ][]
def genBuSet(clusterClassIDDict, classID2NameDict):
    #print "compute each cluster's only ..."
    buSetList = list()   #eachelement is a set
    for clusterID in clusterClassIDDict:
        otherBingSet = set()
        for otherClusterID in clusterClassIDDict:
            if otherClusterID != clusterID:
                otherBingSet = otherBingSet |  set(clusterClassIDList[otherClusterID])
        differSet = set(clusterClassIDList[clusterID]) - otherBingSet
        buSetList.append(list(differSet))
        #print "cluster: ", clusterID, "allLen:", len(clusterClassIDDict[clusterID]), ", diffLen:", len(differSet), "  differSet: ", printSet(differSet, classID2NameDict)
        #print len(clusterClassIDList[clusterID]), ' ... ',clusterClassIDList[clusterID]
    return clusterClassIDDict.keys(), buSetList

#for each cluster, contanining classes (non-overlap) are saved to file
def writeBuSet2File(clusterIDList, buSetList, classID2NameDict, fileName):
    resList = list()
    resList.append(['classID', 'className', 'clusterID'])

    for index in range(0, len(buSetList)):
        clusterID = clusterIDList[index]
        for classID in list(buSetList[index]):
            resList.append([classID, classID2NameDict[classID], clusterID])
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)
    #print fileName

#get combinations for list's all elements
#C2 + C3 + C4 + CN
def getCombination(clusterIDList):
    resList = list()
    N = len(clusterIDList)
    for m in range(2, N + 1):
        from itertools import combinations
        # comoute m zuhe
        tmp = list(combinations(clusterIDList, m))
        resList.extend(tmp)
    return resList

#set operation: get all combination's jiaoSet
def genJiaoSet(clusterClassIDDict, classID2NameDict):
    jiaoSetList = list()
    jiaoClusterIDCombList = list()
    clusterCount = len(clusterClassIDDict)
    allClusterIDList = clusterClassIDDict.keys()
    allCombinations = getCombination(allClusterIDList)
    #print "\nall combinations:\n", allCombinations
    for eachCombination in allCombinations:
        #eachCombination = (clusterID1, clusterID2, ...)
        #compute each combination's jiaoji
        tmpSet = set( clusterClassIDDict[eachCombination[0]] )
        for eachClusterID in eachCombination:
            tmpSet = tmpSet & set( clusterClassIDDict[eachClusterID] )
        if len(tmpSet) != 0:
            jiaoSetList.append(list(tmpSet))
            jiaoClusterIDCombList.append(eachCombination)
            #print "cluster: ", eachCombination, " jiaoSet: ", printSet(tmpSet, classID2NameDict)
    return jiaoClusterIDCombList, jiaoSetList



#compute list=[set1(), set2(),] all set's bing set
def genAllBingSet(setList):
    resSet = set()
    for eachSet in setList:
        resSet = resSet |  set(eachSet)
    return list(resSet)

#clusterID: [classList]  into  classID:[clusterIDList]
def reverseMap(cluster2ClassList):
    class2ClusterDict = dict()
    for clusterID in range(0, len(cluster2ClassList)):
        classIDList = cluster2ClassList[clusterID]
        for classID in classIDList:
            if classID not in class2ClusterDict:
                class2ClusterDict[classID] = list()
                class2ClusterDict[classID].append(clusterID)
            else:
                class2ClusterDict[classID].append(clusterID)
    return class2ClusterDict

#ooverlapped classIDlist save to file
#[classID, className, clusterID:clusterID]
def write2File(classIDList, classID2ClusterIDDict, classID2NameDict, fileName):
    resList = list()
    resList.append(['classID', 'className', 'clusterIDList'])

    for classID in classIDList:
        clusterList = classID2ClusterIDDict[classID]
        clusterList = [ str(eachInt) for eachInt in clusterList ]
        resList.append([classID,  classID2NameDict[classID],  ':'.join(clusterList)])
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)
    #print fileName

#buset_clusterIDList = [cluster id1, id2,...]
#buset_classIDList = [[class id1,  id2, id3],  [....], ]
#jiaoset_clusterIDList = [ [cluster id1, id2], [id2, id3], [], ...]
#jiaoset_classIDList = [[class id1,  id2, id3],  [....],]
class ClusterAnalyzeResult:
    buset_clusterIDList = list()
    buset_classIDList = list()
    buset_classAll = list()

    jiaoset_clusterIDList = list()
    jiaoset_classIDList = list()
    jiaoset_classAll = list()

    highJiaoClusterIDList = list()
    highJiaoClassIDList = list()
    highJiaoClassAll = list()

    lowJiaoClassAll = list()
    def setBusetCluster(self, buset_clusterIDList):
        self.buset_clusterIDList = buset_clusterIDList

    def setBusetClass(self, buset_classIDList):
        self.buset_classIDList = buset_classIDList

    def setBusetClassAll(self, buset_classAll):
        self.buset_classAll = buset_classAll

    def setJiaosetCluster(self, jiaoset_clusterIDList):
        self.jiaoset_clusterIDList = jiaoset_clusterIDList

    def setJiaosetClass(self, jiaoset_classIDList):
        self.jiaoset_classIDList = jiaoset_classIDList

    def setJiaosetClassAll(self, jiaoset_classAll):
        self.jiaoset_classAll = jiaoset_classAll

    def setHighJiaosetCluster(self, highJiaoClusterIDList):
        self.highJiaoClusterIDList = highJiaoClusterIDList

    def setHighJiaosetClass(self, highJiaoClassIDList):
        self.highJiaoClassIDList = highJiaoClassIDList

    def setHighJiaosetClassAll(self, highJiaoClassAll):
        self.highJiaoClassAll = highJiaoClassAll

    def setLowJiaosetClassAll(self, lowJiaoClassAll):
        self.lowJiaoClassAll = lowJiaoClassAll

def writeClusterResult2File(classID2ClusterIDDict):
    # class count who is not overlapped
    #print 'nonOverlappedclassCount=', len(clusterResult.buset_classAll)
    # each cluster own the number of non-overlap
    avg0 = len(clusterResult.buset_classAll) / float(len(clusterResult.buset_clusterIDList) )
    #print 'nonoverLappedclassCount/Cluster=',  avg0
    '''
    print 'Detail='
    for index in range(0, len(clusterResult.buset_clusterIDList)):
        clusterID = clusterResult.buset_clusterIDList[index]
        classIDList = clusterResult.buset_classIDList[index]
        print 'cluster:', clusterID, ',', 'classCount:', len(classIDList)
    '''
    #how many class are overlapped
    #print 'overlappedclassCount=', len(clusterResult.jiaoset_classAll)
    #in average, how many clusters  which the class belongs to
    avg1 = 0
    for classID in clusterResult.jiaoset_classAll:
        clusterIDList = classID2ClusterIDDict[classID]
        avg1 += len(clusterIDList)
    avg1 = avg1 / float( len(clusterResult.jiaoset_classAll) )
    #print  'overlappedclusterCount/class=', avg1

    #how many class are overlapped
    #print 'highoverlappedclassCount=', len(clusterResult.highJiaoClassAll)
    #in average, how many clusters  which the class belongs to
    avg2 = 0
    for classID in clusterResult.highJiaoClassAll:
        clusterIDList = classID2ClusterIDDict[classID]
        avg2 += len(clusterIDList)
    avg2 = avg2 / float( len(clusterResult.highJiaoClassAll) )
    #print 'highoverlappedclusterCount/class=', avg2

    #how many class are overlapped
    #print 'lowoverlappedclassCount=', len(clusterResult.lowJiaoClassAll)
    #in average, how many clusters  which the class belongs to
    avg3 = 0
    for classID in clusterResult.lowJiaoClassAll:
        clusterIDList = classID2ClusterIDDict[classID]
        avg3 += len(clusterIDList)
    avg3 = avg3 / float( len(clusterResult.lowJiaoClassAll) )
    #print 'lowoverlappedclusterCount/class=', avg3

    print str(len(clusterResult.buset_classAll)) + ',' + str(avg0) + ',' + str(len(clusterResult.jiaoset_classAll)) + ',' + str(avg1) + ',' + str(len(clusterResult.highJiaoClassAll)) + ',' + str(avg2) + ',' +  str(len(clusterResult.lowJiaoClassAll)) + ',' + str(avg3)


clusterResult = ClusterAnalyzeResult()
#process the clustering result
#python pro.py   project  clusterFileName.csv  featureVectorFileName.csv  classFileName.csv
if __name__ == '__main__':
    project = sys.argv[1]
    clusterFileName = sys.argv[2]
    featureVectorFileName = sys.argv[3]
    classFileName = sys.argv[4]

    classList = readCSV(classFileName)
    classID2NameDict = processClass(classList)
    fvList = readCSV(featureVectorFileName)
    fvList = processFeatureVec(fvList)
    clusterList = readCSV(clusterFileName)
    clusterList = processCluster(clusterList)

    #process the original cluster *******************************
    clusterList = mergeCluster(clusterList, fvList, len(classID2NameDict))  #clusterList is the final cluster
    #writeCSV(clusterList, project + "_merge_cluster_1.csv")
    clusterClassIDList = trans2Set(clusterList)  #some cluster maybe null set
    classID2ClusterIDDict = reverseMap(clusterClassIDList)

    #exclude null set cluster
    clusterClassIDDict = excludeNullClassCluster(clusterClassIDList)

    [buClusterIDList, buSetList] = genBuSet(clusterClassIDDict, classID2NameDict)
    allBuClassIDList= genAllBingSet(buSetList)
    writeBuSet2File(buClusterIDList, buSetList, classID2NameDict, project + "_split_class_overlap_non_20.csv")

    [jiaoClusterIDList, jiaoSetList] = genJiaoSet(clusterClassIDDict, classID2NameDict)
    allOverlapClassIDList = genAllBingSet(jiaoSetList)

    clusterResult.setBusetCluster(buClusterIDList)
    clusterResult.setBusetClass(buSetList)
    clusterResult.setBusetClassAll(allBuClassIDList)
    clusterResult.setJiaosetCluster(jiaoClusterIDList)
    clusterResult.setJiaosetClass(jiaoSetList)
    clusterResult.setJiaosetClassAll(allOverlapClassIDList)

    #process the new cluster (after smooth)*****************************************
    #print "\n\n\n"
    newClusterList = smoothCluster(clusterList)
    #writeCSV(newClusterList, outClusterFileName + "new_1.csv")
    newClusterClassIDList = trans2Set(newClusterList)

    #exclude null set cluster
    newClusterClassIDDict = excludeNullClassCluster(newClusterClassIDList)

    [newJiaoClusterIDList, newJiaoSetList] = genJiaoSet(newClusterClassIDDict, classID2NameDict)
    highlyOverlapClassIDList = genAllBingSet(newJiaoSetList)
    write2File(highlyOverlapClassIDList, classID2ClusterIDDict, classID2NameDict, project +  "_split_class_overlap_high_20.csv")

    lowlyOverlapClassIDList = list( set(allOverlapClassIDList) - set(highlyOverlapClassIDList) )
    write2File(lowlyOverlapClassIDList, classID2ClusterIDDict, classID2NameDict, project + "_split_class_overlap_low_20.csv")

    clusterResult.setHighJiaosetCluster(newJiaoClusterIDList)
    clusterResult.setHighJiaosetClass(newJiaoSetList)

    clusterResult.setHighJiaosetClassAll(highlyOverlapClassIDList)
    clusterResult.setLowJiaosetClassAll(lowlyOverlapClassIDList)

    writeClusterResult2File(classID2ClusterIDDict)
