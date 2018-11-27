import sys
import csv

finalClusters = list()
classID2NameDict = dict()   #classDoct[classID] = className
className2IDDict = dict()
MINSIMVALUE = 0

class AlgClass:
    distFunc = ""
    mergeFunc = ""
    K = 0 #iteration number
    simM = list()
    pre = "nochen"
    feature = ""

    def __init__(self):
        print "init: do nothing"

    def setDistFunc(self, func):
        self.distFunc = func

    def setMergeFunc(self, func):
        self.mergeFunc = func

    def setK(self, k):
        self.K = k
    
    def setFeature(self, feature):
        self.feature = feature

    def setSimM(self, M):
        N = len(M)
        for index in range(0, N):
            tmpList = [0] * N #generat a list whole len = N
            self.simM.append(tmpList)
        for i in range(0, N):
            for j in range(0, N):
                self.simM[i][j] = M[i][j]


def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp, delimiter = ',')
        for eachLine in reader:
            resList.append(eachLine)
    return resList

def writeCSV(fileName,listlist):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        for eachList in listlist:
            writer.writerow(eachList)

def isLess(floatNum, threshold):
    if floatNum - threshold <= 0.001:
        return True
    else:
        return False

def isEqual(floatNum1, floatNum2):
    if abs(floatNum1 - floatNum2) <= 0.0001:
        return True
    else:
        return False


def normalize(simM):
    minList = list()
    maxList = list()


    for eachList in simM:
        #print eachList
        minList.append(min(eachList))
        maxList.append(max(eachList))

    minValue = min(minList)
    maxValue = max(maxList)
    #print "min= ", minValue, ";  maxValue = ", maxValue

    for i in range(0, len(simM)):
        for j in range(0, len(simM[i])):
            simM[i][j] = (simM[i][j] - minValue)  / float(maxValue - minValue)

    return simM


#init classID2NameDict, className2IDDict
def initClassFromFile(fileName):
    classIndex = 0
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            classID2NameDict[classIndex] = className
            className2IDDict[className] = classIndex
            classIndex += 1


def delAndNormalize(fv):
    newFv = list()
    minList = list()
    maxList = list()
    #print fv
    classIndex = 0
    for eachList in fv:
        #className = eachList[0]
        #classDict[classIndex] = className
        del eachList[0]
        #classIndex += 1

        #print eachList
        for index in range(0, len(eachList)):
            eachList[index] = float(eachList[index])

        newFv.append(eachList)
        minList.append(min(eachList))
        maxList.append(max(eachList))
    minValue = min(minList)
    maxValue = max(maxList)
    #print "min= ", minValue, ";  maxValue = ", maxValue

    for i in range(0, len(newFv)):
        for j in range(0, len(newFv[i])):
            newFv[i][j] = (newFv[i][j] - minValue)  / float(maxValue - minValue)

    return newFv





#find the differ between two feature vector
def WCAFindDiffer(vector_i, vector_j, thr):
    bothIndex = list()
    onlyBIndex = list()
    onlyAIndex = list()
    bothNotIndex = list()
    bothVal = list()
    onlyBVal = list()
    onlyAVal = list()
    bothNotVal = list()

    n = len(vector_i) #  len(vector_i) = len(vector_j)
    #notice: elment of vector is float, how to compare float with 0
    for index in range(0, n): #list=[0,1,..., n-1]
        if not isLess(vector_i[index], thr)  and  not isLess(vector_j[index], thr):
            bothIndex.append(index)
            bothVal.append(vector_i[index] + vector_j[index])
        elif isLess(vector_i[index], thr) and not isLess(vector_j[index], thr):
            onlyBIndex.append(index)
            onlyBVal.append(vector_j[index])
        elif not isLess(vector_i[index], thr) and isLess(vector_j[index], thr):
            onlyAIndex.append(index)
            onlyAVal.append(vector_i[index])
	elif isLess(vector_i[index], thr) and  isLess(vector_j[index], thr):
            bothNotIndex.append(index)
            bothNotVal.append(vector_i[index])

    return bothIndex, onlyAIndex, onlyBIndex, bothNotIndex, bothVal, onlyAVal, onlyBVal, bothNotVal


#for this distance, the more, the marrier
def WCACalDistClass_ij(i, j, class1Fv, class2Fv, distFunc, thr):
    if i == j:
        return 0

    if len(class1Fv) != len(class2Fv):
        print "this two feature vector donnot have same len\n"
        return


    [bothIndex, onlyAIndex, onlyBIndex, bothNotIndex, bothVal, onlyAVal, onlyBVal, bothNotVal] = WCAFindDiffer(class1Fv, class2Fv, thr ) #aIndex is the index array
    if distFunc == "jm":
        fenzi = len(bothIndex)
        fenmu = len(bothIndex) + len(onlyAIndex) + len(onlyBIndex)
    elif distFunc == "uem":
        fenzi = 0.5 * sum(bothVal)
        fenmu = 0.5 * sum(bothVal) + len(onlyAIndex) + len(onlyBIndex)   # dist is more, the similarity is stronger
    elif distFunc == "uemnm":
        fenzi = 0.5 * sum(bothVal)
        fenmu = 0.5 * sum(bothVal) + 2 * len(onlyAIndex) + 2 * len(onlyBIndex) + len(bothIndex) + len(bothNotIndex)

    if not isEqual(fenmu, 0):
        return fenzi / float(fenmu)
    else:
        return 0



#generate structSimM listlist,   duichen juzhen
def WCACalStructSim(fv, distFunc):
    N = len(fv)
    structSimM = list()

    #initialize structSimM
    for index in range(0, N):
        tmpList = [MINSIMVALUE] * N #generat a list whole len = N
        structSimM.append(tmpList)

    for i in range(0, N):
        for j in range(0, N):
            if i != j:
                if distFunc == 'coupling':
                    structSimM[i][j] = fv[i][j]
                else:
                    structSimM[i][j] = WCACalDistClass_ij(i, j, fv[i], fv[j], distFunc,  thr = 0.01)

    return structSimM




#compute the distance/similarity between two cluster
#cluster_i =[node1, node2, node3]; clustr_j =[];
def WCACalDistCluster_ij(cluster_i, cluster_j):
    distList = list()
    #print cluster_i, cluster_j
    for eachNode_i in cluster_i:
        for eachNode_j in cluster_j:
            #print eachNode_i, eachNode_j, structSimM[eachNode_i][eachNode_j]
            distList.append(oneAlg.simM[eachNode_i][eachNode_j])

    if oneAlg.mergeFunc == "MAX_SINGLE": # choose the maxNodeDistance as cluster distance
        return max(distList)
    elif oneAlg.mergeFunc == "MIN_SINGLE": # choose the minNodeDistance as cluster distance
        return min(distList)
    elif oneAlg.mergeFunc == "AVG": # choose the avg nodeNodeDistance as cluster distance
        return sum(distList) / float(len(distList))
    else:
        print "wrong merge function!!!!!!!!!!"

#choose most similar clusters to merge
def WCAChooseMostSim(N):
    tmpList = list() # all cluster_pair distance

    for i in range(0, N):
        for j in range(0, N):
            if i != j:
                simVal = WCACalDistCluster_ij(finalClusters[i], finalClusters[j])
                #print i, j, clusters[i], clusters[j], simVal
                tmpList.append([i,j, simVal])

    #sort tmpList from big to small
    sortedList = sorted(tmpList, key=lambda x:x[2], reverse=True)

    maxValue = sortedList[0][2]
    tmpIndex = 0
    for each in sortedList:
        if not isEqual(each[2], maxValue):
            break
        else:
            tmpIndex += 1
    #print tmpIndex

    #choose from 0 to tmpIndex-1 randomly
    import random
    rd = random.randint(0, tmpIndex-1)
    merge_i = sortedList[rd][0]
    merge_j = sortedList[rd][1]
    mergeSimVal = sortedList[rd][2]

    return merge_i, merge_j, mergeSimVal


#run clustering WCA
def WCAClustering(fv):

    #compute the structSimM (a duichen juzhen)
    structSimM = WCACalStructSim(fv, oneAlg.distFunc)
    oneAlg.setSimM(normalize(structSimM))

    #print "sim M = .................."
    #for index in range(0, len(oneAlg.simM)):
    #    print oneAlg.simM[index]

    iterk = 1
    origN = len(finalClusters)
    N = len(finalClusters)

    while N > oneAlg.K:
        merge_i = -1
        merge_j = -1

        (merge_i, merge_j, merge_simVal) = WCAChooseMostSim(N)

        if merge_i == -1 and merge_j == -1:
            print merge_i, merge_j, "no merge"
            break
        else:
            #merge the cluster_i and cluster_j, and update finalClusters
            print finalClusters[merge_i], " and ",  finalClusters[merge_j], " simVal=", merge_simVal
            finalClusters[merge_i].extend(finalClusters[merge_j])
            del finalClusters[merge_j]
            #print finalClusters

            #update  structSimM  and concernSimM, delete one row and one column, compute the new changedSim
            #updateSimM(merge_i, merge_j)
            print N-1, int(origN)
            if N-1 <= int(origN):
                outfileName = oneAlg.pre + '_' + oneAlg.feature + '_' + oneAlg.distFunc + '_' + oneAlg.mergeFunc + '_' + str(N-1) + '.csv'
                print "clustering result file: ", outfileName
                printClustering(outfileName)
        iterk = iterk + 1
        N = N - 1

    print "clustering end...."


def printClustering(fileName):
    #classDict[classID] = className
    #clusterDict = dict()
    num = len(finalClusters)
    resList = list()

    for index in range(0, num):
        clusterID = index
        for eachClassID in finalClusters[clusterID]:
            #clusterDict[eachClassID] = clusterID
            resList.append([clusterID, classID2NameDict[eachClassID]])


    #print "class number is ", len(classDict)
    """
    resList = list()
    for classID in range(0, len(classDict)):
        tmpList = [classID, classDict[classID], clusterDict[classID]]
        resList.append(tmpList)
    """
    writeCSV(fileName, resList)



#init cluster from file, this file lists the classes which ahould be togtether
#init finalClusters
def initClusterFromFile(fileName):
    if fileName == "":
        for i in range(0, len(className2IDDict)):
            finalClusters.append([i])
    else:
        #init class in file into cluster
        existedClass2ClusterDict = dict()
        preClusterID = -1
        with open(fileName, "rb") as fp:
            reader = csv.reader(fp)
            for each in reader:
                [clusterID, className] = each
                classID = className2IDDict[className]
                existedClass2ClusterDict[classID] = int(clusterID)

                if preClusterID == int(clusterID):
                    finalClusters[ len(finalClusters) - 1 ].append(classID)
                else:
                    finalClusters.append([classID])
                    preClusterID = int(clusterID)

        # init other classes into cluster
        for classID in classID2NameDict.keys():  #key = ID
            if classID not in existedClass2ClusterDict:
                finalClusters.append([classID])

    #printClustering("tmp.csv")
        



#python pro.py   struct.csv   distFunc=coupling,jm, uem, uemnm       mergeFunc= MIN_SINGLE, MAX_SINGLE, AVG       K=iterNum  classListFile   clusterFile
oneAlg = AlgClass()

if __name__ == "__main__":
    structFileName = sys.argv[1]
    structDistFunc = sys.argv[2]
    mergeFunc = sys.argv[3]
    K = int(sys.argv[4])
    classConfigFileName = sys.argv[5]   #classList file
    clusterConfigFileName = sys.argv[6] #clusterList file
    feature = sys.argv[7]  #struct or commu
    oneAlg.setDistFunc(structDistFunc)
    oneAlg.setMergeFunc(mergeFunc)
    oneAlg.setK(K)
    oneAlg.setFeature(feature)
	
    #init classID2NameDict and className2IDDict
    initClassFromFile(classConfigFileName) 
	
    #init fecture vector
    structFv = readCSV(structFileName)
    sfv = delAndNormalize(structFv)

    #init clusters   
    initClusterFromFile(clusterConfigFileName) #init finalClusters

    WCAClustering(sfv)

    #outfileName = "wca" + '_' +  structDistFunc + '_' + mergeFunc + '_' + str(K) + '.csv'
    #print "clustering result file: ", outfileName
    #printClustering(outfileName)





 
