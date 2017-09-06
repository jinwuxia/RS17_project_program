import sys
import csv

finalClusters = list()
classDict = dict()   #classDoct[classID] = className

class AlgClass:
    distFunc = ""
    distFuncA = ""
    distFuncB = ""
    distFuncC = ""
    mergeFunc = ""
    K = 0 #iteration number
    simM = list()
    alpha = 0.0
    beta = 0.0
    gama = 0.0
    alg = ""
    pre = ""

    def __init__(self):
        print "init: do nothing"
    def setAlg(self, alg):
        self.alg = alg

    def setDistFunc(self, func):
        self.distFunc = func

    def setDistFuncA(self, funcA):
        self.distFuncA = funcA

    def setDistFuncB(self, funcB):
        self.distFuncB = funcB

    def setDistFuncC(self, funcC):
        self.distFuncC = funcC

    def setMergeFunc(self, func):
        self.mergeFunc = func

    def setK(self, k):
        self.K = k

    def setAlpha(self, a):
        self.alpha = a;

    def setBeta(self, b):
        self.beta = b

    def setGama(self, c):
        self.gama = c

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

def isTwoMatch(fv1, fv2):
    if len(fv1) != len(fv2):
        print "structFeature len is not equal to len of concernFeature\n"
        return False

    for index in range(0, len(fv1)):
        if fv1[index][0] != fv2[index][0]:
            print fv1[index][0], " not equal to ", fv2[index][0]
            return False

    return True


def isThreeMatch(fv1, fv2, fv3):
    if len(fv1) != len(fv2) or len(fv3) != len(fv2):
        print "fv1 len is not equal to len of fv2 or fv3\n"
        return False

    for index in range(0, len(fv1)):
        if fv1[index][0] != fv2[index][0] or fv2[index][0] != fv3[index][0]:
            print fv1[index][0], " not equal to ", fv2[index][0], " or  ", fv3[index][0]
            return False

    return True

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


def delAndNormalize(fv):
    newFv = list()
    minList = list()
    maxList = list()
    #print fv
    classIndex = 0
    for eachList in fv:
        className = eachList[0]
        classDict[classIndex] = className
        del eachList[0]
        classIndex += 1

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



#generate structSimM listlist
def WCACalStructSim(fv, distFunc):
    N = len(fv)
    structSimM = list()

    #initialize structSimM
    for index in range(0, N):
        tmpList = [0] * N #generat a list whole len = N
        structSimM.append(tmpList)

    for i in range(0, N):
        for j in range(0, N):
            if distFunc == 'coupling':
                structSimM[i][j] = fv[i][j]
            else:
                structSimM[i][j] = WCACalDistClass_ij(i, j, fv[i], fv[j], distFunc,  thr = 0.01)

    return structSimM

def MIXTwoCalSim(structSimM, concernSimM):
    if len(structSimM) != len(concernSimM):
        print "structSimM len not euqal to concernSimM len....."
        return

    #initialize mixSimM
    N = len(structSimM)
    mixSimM = list()
    for index in range(0, N):
        tmpList = [0] * N #generat a list whole len = N
        mixSimM.append(tmpList)

    for i in range(0, N):
        for j in range(0, N):
            mixSimM[i][j] = oneAlg.alpha * structSimM[i][j] + oneAlg.beta * concernSimM[i][j]

    return mixSimM

def MIXThreeCalSim(structSimM, concernSimM, traceSimM):
    if len(structSimM) != len(concernSimM) or len(concernSimM) != len(traceSimM):
        print "structSimM len not euqal to concernSimM len or traceSimM len......"
        return

    #initialize mixSimM
    N = len(structSimM)
    mixSimM = list()
    for index in range(0, N):
        tmpList = [0] * N #generat a list whole len = N
        mixSimM.append(tmpList)

    for i in range(0, N):
        for j in range(0, N):
            mixSimM[i][j] = oneAlg.alpha * structSimM[i][j] + oneAlg.beta * concernSimM[i][j] + oneAlg.gama

    return mixSimM



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

    for i in range(0,N):
        for j in range(0,N):
            if i != j: # if i != j
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

    #compute the structSimM
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
            if N-1 <= int(origN / 10):
                outfileName = oneAlg.pre + oneAlg.alg + '_' +  oneAlg.distFunc + '_' + oneAlg.mergeFunc + '_' + str(N-1) + '.csv'
                print "clustering result file: ", outfileName
                printClustering(outfileName)
        iterk = iterk + 1
        N = N - 1

    print "WCA clustering end...."


def MIXTwoClustering(sfv, cfv):
    #compute the structSimM
    structSimM = WCACalStructSim(sfv, oneAlg.distFuncA)
    concernSimM = WCACalStructSim(cfv, oneAlg.distFuncB)

    structSimM = normalize(structSimM)
    concernSimM = normalize(concernSimM)

    mixSimM = MIXTwoCalSim(structSimM, concernSimM)
    oneAlg.setSimM(normalize(mixSimM))

    #print "mixSimM = .................."
    #for index in range(0, len(oneAlg.simM)):
    #    print oneAlg.simM[index]

    iterk = 1
    origN = len(finalClusters)
    N = len(finalClusters)

    while N > oneAlg.K:
        merge_i = -1
        merge_j = -1

        (merge_i, merge_j, merge_simVal) = WCAChooseMostSim(N)
        print finalClusters[merge_i], " and ",  finalClusters[merge_j], " simVal=", merge_simVal

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
            if N-1 <= int(origN / 10):
                outfileName = oneAlg.pre + 'mix_two' + '_' +  oneAlg.distFuncA + '_' + oneAlg.distFuncB + '_' + oneAlg.mergeFunc + '_' + str(N-1) + '.csv'
                print "clustering result file: ", outfileName
                printClustering(outfileName)
        iterk = iterk + 1
        N = N - 1

    print "MIX clustering end...."

def MIXThreeClustering(sfv, cfv, tfv):
    #compute the structSimM
    structSimM = WCACalStructSim(sfv, oneAlg.distFuncA)
    concernSimM = WCACalStructSim(cfv, oneAlg.distFuncB)
    traceSimM = WCACalStructSim(tfv, oneAlg.distFuncC)

    structSimM = normalize(structSimM)
    concernSimM = normalize(concernSimM)
    traceSimM = normalize(traceSimM)

    mixSimM = MIXThreeCalSim(structSimM, concernSimM, traceSimM)
    oneAlg.setSimM(normalize(mixSimM))

    #print "maxSimM = .................."
    #for index in range(0, len(oneAlg.simM)):
    #    print oneAlg.simM[index]

    iterk = 1
    origN = len(finalClusters)
    N = len(finalClusters)

    while N > oneAlg.K:
        merge_i = -1
        merge_j = -1

        (merge_i, merge_j, merge_simVal) = WCAChooseMostSim(N)
        print finalClusters[merge_i], " and ",  finalClusters[merge_j], " simVal=", merge_simVal

        if merge_i == -1 and merge_j == -1:
            print merge_i, merge_j, "no merge"
            break
        else:
            #merge the cluster_i and cluster_j, and update finalClusters
            #print merge_i, merge_j, merge_simVal
            finalClusters[merge_i].extend(finalClusters[merge_j])
            del finalClusters[merge_j]
            #print finalClusters

            #update  structSimM  and concernSimM, delete one row and one column, compute the new changedSim
            #updateSimM(merge_i, merge_j)
            if N-1 <= int(origN / 10):
                outfileName = oneAlg.pre + 'mix_three' + '_' +  oneAlg.distFuncA + '_' + oneAlg.distFuncB +  '_' + oneAlg.distFuncC + '_' + oneAlg.mergeFunc + '_' + str(N-1) + '.csv'
                print "clustering result file: ", outfileName
                printClustering(outfileName)
        iterk = iterk + 1
        N = N - 1

    print "MIX clustering end...."

def printClustering(fileName):
    #classDict[classID] = className
    #clusterDict = dict()
    num = len(finalClusters)
    resList = list()

    for index in range(0, num):
        clusterID = index
        for eachClassID in finalClusters[clusterID]:
            #clusterDict[eachClassID] = clusterID
            resList.append([clusterID, classDict[eachClassID]])


    #print "class number is ", len(classDict)
    """
    resList = list()
    for classID in range(0, len(classDict)):
        tmpList = [classID, classDict[classID], clusterDict[classID]]
        resList.append(tmpList)
    """
    writeCSV(fileName, resList)


def TraceStart():
    traceFileName = sys.argv[2]
    traceDistFunc = sys.argv[3]
    mergeFunc = sys.argv[4]
    K = int(sys.argv[5])

    oneAlg.setDistFunc(traceDistFunc)
    oneAlg.setMergeFunc(mergeFunc)
    oneAlg.setK(K)


    traceFv = readCSV(traceFileName)
    sfv = delAndNormalize(traceFv)
    #for index in range(0, len(sfv)):
    #    print sfv[index]

    #init clusters
    for i in range(0, len(sfv)):
        finalClusters.append([i])

    WCAClustering(sfv)

    #outfileName = "trace" + '_' +  traceDistFunc + '_' + mergeFunc + '_' + str(K) + '.csv'
    #print "clustering result file: ", outfileName
    #printClustering(outfileName)

def WCAStart():
    structFileName = sys.argv[2]
    structDistFunc = sys.argv[3]
    mergeFunc = sys.argv[4]
    K = int(sys.argv[5])

    oneAlg.setAlg(sys.argv[1])
    oneAlg.setDistFunc(structDistFunc)
    oneAlg.setMergeFunc(mergeFunc)
    oneAlg.setK(K)

    structFv = readCSV(structFileName)
    sfv = delAndNormalize(structFv)
    #for index in range(0, len(sfv)):
    #    print sfv[index]

    #init clusters
    for i in range(0, len(sfv)):
        finalClusters.append([i])

    WCAClustering(sfv)

    #outfileName = "wca" + '_' +  structDistFunc + '_' + mergeFunc + '_' + str(K) + '.csv'
    #print "clustering result file: ", outfileName
    #printClustering(outfileName)

def CommuStart():
    structFileName = sys.argv[2]
    structDistFunc = sys.argv[3]
    mergeFunc = sys.argv[4]
    K = int(sys.argv[5])

    oneAlg.setAlg(sys.argv[1])
    oneAlg.setDistFunc(structDistFunc)
    oneAlg.setMergeFunc(mergeFunc)
    oneAlg.setK(K)

    structFv = readCSV(structFileName)
    sfv = delAndNormalize(structFv)
    #for index in range(0, len(sfv)):
    #    print sfv[index]

    #init clusters
    for i in range(0, len(sfv)):
        finalClusters.append([i])

    WCAClustering(sfv)

    #outfileName = "commu" + '_' +  structDistFunc + '_' + mergeFunc + '_' + str(K) + '.csv'
    #print "clustering result file: ", outfileName
    #printClustering(outfileName)


def CONCERNStart():
    concernFileName = sys.argv[2]
    concernDistFunc = sys.argv[3]
    mergeFunc = sys.argv[4]
    K = int(sys.argv[5])

    oneAlg.setAlg(sys.argv[1])
    oneAlg.setDistFunc(concernDistFunc)
    oneAlg.setMergeFunc(mergeFunc)
    oneAlg.setK(K)

    concernFv = readCSV(concernFileName)
    cfv = delAndNormalize(concernFv)

    #for index in range(0, len(cfv)):
    #    print cfv[index]

    #init cluster
    for i in range(0, len(cfv)):
        finalClusters.append([i])

    WCAClustering(cfv)


    #outfileName = "concern" + '_' +  concernDistFunc + '_' + mergeFunc + '_' + str(K) + '.csv'
    #print "clustering result file: ", outfileName
    #printClustering(outfileName)

def MIXTwoStart():
    structFileName = sys.argv[2]
    concernFileName = sys.argv[3]
    alpha = float(sys.argv[4])
    beta = float(sys.argv[5])
    distFuncA = sys.argv[6]
    distFuncB = sys.argv[7]
    mergeFunc = sys.argv[8]
    K = int(sys.argv[9])

    oneAlg.setAlg(sys.argv[1])
    oneAlg.setDistFuncA(distFuncA)
    oneAlg.setDistFuncB(distFuncB)
    oneAlg.setMergeFunc(mergeFunc)
    oneAlg.setK(K)
    oneAlg.setAlpha(alpha)
    oneAlg.setBeta(beta)
    structFv = readCSV(structFileName)
    concernFv = readCSV(concernFileName)

    if isTwoMatch(structFv, concernFv) == False:
        print "do not match\n"
    else:
        print "match\n"

    if isEqual(alpha, 0.0001) or isEqual(beta, 0.0001):
        print "please speicfy alpha and beta"

    sfv = delAndNormalize(structFv)
    cfv = delAndNormalize(concernFv)

    #init cluster
    for i in range(0, len(sfv)):
        finalClusters.append([i])

    MIXTwoClustering(sfv, cfv)

    #outfileName = 'mix_two' + '_' +  distFuncA + '_' + distFuncB  + '_' + mergeFunc + '_' + str(K) + '.csv'
    #print "clustering result file: ", outfileName
    #printClustering(outfileName)

def MIXThreeStart():
    structFileName = sys.argv[2]
    concernFileName = sys.argv[3]
    traceFileName = sys.argv[4]
    alpha = float(sys.argv[5])
    beta = float(sys.argv[6])
    gama = float(sys.argv[7])
    distFuncA = sys.argv[8]
    distFuncB = sys.argv[9]
    distFuncC = sys.argv[10]
    mergeFunc = sys.argv[11]
    K = int(sys.argv[12])
    
    oneAlg.setAlg(sys.argv[1])
    oneAlg.setDistFuncA(distFuncA)
    oneAlg.setDistFuncB(distFuncB)
    oneAlg.setDistFuncC(distFuncC)
    oneAlg.setMergeFunc(mergeFunc)
    oneAlg.setK(K)
    oneAlg.setAlpha(alpha)
    oneAlg.setBeta(beta)
    oneAlg.setGama(gama)
    structFv = readCSV(structFileName)
    concernFv = readCSV(concernFileName)
    traceFv = readCSV(traceFileName)

    if isThreeMatch(structFv, concernFv, traceFv) == False:
        print "do not match\n"
    else:
        print "match\n"

    if isEqual(alpha, 0.0001) or isEqual(beta, 0.0001):
        print "please speicfy alpha and beta"

    sfv = delAndNormalize(structFv)
    cfv = delAndNormalize(concernFv)
    tfv = delAndNormalize(traceFv)

    #init cluster
    for i in range(0, len(sfv)):
        finalClusters.append([i])

    MIXThreeClustering(sfv, cfv, tfv)

    #outfileName = 'mix_three' + '_' +  distFuncA + '_' + distFuncB +  '_' + distFuncC + '_' + mergeFunc + '_' + str(K) + '.csv'
    #print "clustering result file: ", outfileName
    #printClustering(outfileName)

#python pro.py    wca          struct.csv    distFunc=coupling,jm, uem, uemnm    mergeFunc= MIN_SINGLE, MAX_SINGLE, AVG   K=iterNum

#python pro.py    concern      Conven.csv    distFunc = jm, uem, uemn   mergeFunc = SINGLE_MIN, SINLE_MAX, AVG    K=iterNum

#python pro.py  trace         trace.fv  distfunc = jm, uem, uemnm    mergeFuncC = SINGLE....   K=iterNum

#python pro.py    mix  struct.csv     concern.csv   alpha, beta,   disfunA = coupling, distfuncB = jm,uem,uemn,  mergeFunc, K

#python pro.py mix struct.fv  concern.fv trace.fv  alpha, beta, gama, coupling, uem, uem, AVG  K

oneAlg = AlgClass()

if __name__ == "__main__":
    clusteringAlg = sys.argv[1]
    oneAlg.pre = sys.argv[2].split('-')[0]
    if clusteringAlg == 'commu':
        CommuStart()
    elif clusteringAlg == 'wca':
        WCAStart()
    elif clusteringAlg == 'concern':
        CONCERNStart()
    elif clusteringAlg == 'trace':
        TraceStart()
    elif clusteringAlg == 'mixtwo':
        MIXTwoStart()
    elif clusteringAlg == 'mixthree':
        MIXThreeStart()
    else:
        print "unknown clutering alogorithm: ", clusteringAlg
