'''
do testcase similarity statis
'''

import sys
import csv

MINSIMVALUE = 0
DISTFUNCVALUE = 0.5
TESTCASENAMEDict = dict() #testcase[id] = name


def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp, delimiter = ',')
        for eachLine in reader:
            resList.append(eachLine)
    return resList


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


#delete the first column, that is testcase ID
def delFirstCol(fv):
    newFv = list()
    testCaseID = 0
    for eachList in fv:
        TESTCASENAMEDict[testCaseID] = eachList[0]
        testCaseID += 1
        del eachList[0]
        for index in range(0, len(eachList)):
            eachList[index] = int(eachList[index])
        newFv.append(eachList)
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



#generate TsSimM listlist,   duichen juzhen
def WCACalTsSim(fv, distFunc):
    N = len(fv)
    tsSimM = list()

    #initialize tsSimM
    for index in range(0, N):
        tmpList = [MINSIMVALUE] * N #generat a list whole len = N
        tsSimM.append(tmpList)

    for i in range(0, N):
        for j in range(0, N):
            if i != j:
                tsSimM[i][j] = WCACalDistClass_ij(i, j, fv[i], fv[j], distFunc,  thr = DISTFUNCVALUE)
    return tsSimM


def statis(tsSimM):
    N = len(tsSimM[0])
    print N
    simList = list()
    for i in range(0, N):
        for j in range(0, N):
            if i < j:
                simList.append(tsSimM[i][j])
    statisList = [0] * 10 #[0.0-0.1], [0.1-0.2],
    for each in simList:
        if each <= 0.1:
            statisList[0] += 1
        if each <= 0.2:
            statisList[1] += 1
        if each <= 0.3:
            statisList[2] += 1
        if each <= 0.4:
            statisList[3] += 1
        if each <= 0.5:
            statisList[4] += 1
        if each <= 0.6:
            statisList[5] += 1
        if each <= 0.7:
            statisList[6] += 1
        if each <= 0.8:
            statisList[7] += 1
        if each <= 0.9:
            statisList[8] += 1
        if each <= 1.0:
            statisList[9] += 1


    rateStatisList = [round(each / float(statisList[len(statisList) - 1]), 4) for each in statisList]
    newStatisList = [0] * 10
    newStatisList[0] = statisList[0]
    for i in range(1, 10):
        newStatisList[i] = statisList[i] - statisList[i-1]
    ratenewStatisList = [round(each / float(statisList[len(statisList) - 1]), 4)  for each in newStatisList]
    #print 'accumulate number:', statisList
    #print 'accumulate rate:', [round(each / float(statisList[len(statisList) - 1]), 4) for each in statisList]
    #print 'increasement number:', newStatisList
    #print 'increasement rate:', [round(each / float(statisList[len(statisList) - 1]), 4)  for each in newStatisList]

    print ','.join([str(each) for each in statisList])
    print ','.join([str(each) for each in rateStatisList])
    print ','.join([str(each) for each in newStatisList])  #increasement
    print ','.join([str(each) for each in ratenewStatisList])  #increasement


# python ../../split/classstatis/traceSimStatis.py coreprocess/solo270_testcase1_fv.csv  jm > log.csv
if __name__ == "__main__":
    featureFileName = sys.argv[1]    #testcase feature maxtrix filename
    distFunc = sys.argv[2]           #similaroty distance metric

    #init fecture vector
    tsFv = readCSV(featureFileName)
    newTsFv = delFirstCol(tsFv)
    tsSimM = WCACalTsSim(newTsFv, distFunc)
    statis(tsSimM)
