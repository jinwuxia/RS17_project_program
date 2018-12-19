'''
read proReqAPIFile, compute the provided and requested API average size in terms of apiClass and apiMethod
'''
import sys
import csv

def readCSV(fileName):
    resList = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [clusterID1,clusterID2,apiClass,apiMethod,parameter,returnType] = each
            if clusterID1 == 'clusterID1':
                continue
            resList.append([clusterID1,clusterID2,apiClass,apiMethod])
    return resList

def measureReqInterf(apiList):
    reqAPIClassDict = dict() # dict[serviceID] = [class1, class2]
    reqAPIMethodDict = dict() # dict[serviceID]  = [method1, ...]
    for oneList in apiList:
        [clusterID1,clusterID2,apiClass,apiMethod] = oneList

        if clusterID1 not in reqAPIClassDict:
            reqAPIClassDict[clusterID1] = list()
        if apiClass not in reqAPIClassDict[clusterID1]:
            reqAPIClassDict[clusterID1].append(apiClass)

        if clusterID1 not in reqAPIMethodDict:
            reqAPIMethodDict[clusterID1] = list()
        if apiMethod not in reqAPIMethodDict[clusterID1]:
            reqAPIMethodDict[clusterID1].append(apiMethod)
    #print 'reqAPIClassDict', reqAPIClassDict
    return reqAPIClassDict, reqAPIMethodDict

def measureProInterf(apiList):
    proAPIClassDict = dict() # dict[serviceID] = [class1, class2]
    proAPIMethodDict = dict() # dict[serviceID]  = [method1, ...]
    for oneList in apiList:
        [clusterID1,clusterID2,apiClass,apiMethod] = oneList

        if clusterID2 not in proAPIClassDict:
            proAPIClassDict[clusterID2] = list()
        if apiClass not in proAPIClassDict[clusterID2]:
            proAPIClassDict[clusterID2].append(apiClass)

        if clusterID2 not in proAPIMethodDict:
            proAPIMethodDict[clusterID2] = list()
        if apiMethod not in proAPIMethodDict[clusterID2]:
            proAPIMethodDict[clusterID2].append(apiMethod)
    #print 'proAPIClassDict', proAPIClassDict
    return proAPIClassDict, proAPIMethodDict

def measure(proAPIClassDict, proAPIMethodDict, reqAPIClassDict, reqAPIMethodDict):
    avgProAPIClass = 0
    avgProAPIMethod = 0
    avgReqAPIClass = 0
    avgReqAPIMethod = 0

    for clusterID in proAPIClassDict:
        apiClassList = proAPIClassDict[clusterID]
        apiMethodList = proAPIMethodDict[clusterID]
        avgProAPIClass  += len(apiClassList)
        avgProAPIMethod += len(apiMethodList)

    for clusterID in reqAPIClassDict:
        apiClassList = reqAPIClassDict[clusterID]
        apiMethodList = reqAPIMethodDict[clusterID]
        avgReqAPIClass += len(apiClassList)
        avgReqAPIMethod += len(apiMethodList)

    print 'ProAPIClass, ProAPIMethod, ReqAPIClass, ReqAPIMethod'
    print avgProAPIClass, avgProAPIMethod, avgReqAPIClass, avgReqAPIMethod

    avgProAPIClass  = round(avgProAPIClass  / float(len(proAPIClassDict.keys())), 4 )
    avgProAPIMethod = round(avgProAPIMethod / float(len(proAPIClassDict.keys())), 4 )
    avgReqAPIClass  = round(avgReqAPIClass  / float(len(reqAPIClassDict.keys())), 4 )
    avgReqAPIMethod = round(avgReqAPIMethod / float(len(reqAPIClassDict.keys())), 4 )
    print 'avgProAPIClass, avgProAPIMethod, avgReqAPIClass, avgReqAPIMethod'
    print avgProAPIClass, avgProAPIMethod, avgReqAPIClass, avgReqAPIMethod

#python pro.py   proReqAPIFile
if __name__ == '__main__':
    proReqAPIFileName = sys.argv[1]
    apiList = readCSV(proReqAPIFileName)
    [reqAPIClassDict, reqAPIMethodDict] = measureReqInterf(apiList)
    [proAPIClassDict, proAPIMethodDict] = measureProInterf(apiList)
    measure(proAPIClassDict, proAPIMethodDict, reqAPIClassDict, reqAPIMethodDict)
