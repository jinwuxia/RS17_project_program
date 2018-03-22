import sys
import csv


#note: input file includes a->b, and also b->a
def readCommit(fileName):
    commitDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [class1, class2, commit] = each
            if class1 not in commitDict:
                commitDict[class1] = dict()
            commitDict[class1][class2] = int(commit)
    return commitDict

#[serviceID] = [class1, class2, ...]
def readCluster(fileName, fileType):
    serviceDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            if fileType == 'FOME':
                [classID, className, serviceID] = each
            else:
                [contain, serviceID, className] = each
            if serviceID not in serviceDict:
                serviceDict[serviceID] = list()
            serviceDict[serviceID].append(className)
    return serviceDict

def getMin(aList):
    return min(aList)

def getMax(aList):
    return max(aList)

#junzhi
def getAvg(aList):
    return round(sum(aList) / float(len(aList)), 4)

#zhongweishu
def getMed(aList):
    if len(aList) == 0:
        return 0
    if len(aList) == 1:
        return aList[0]
    aList.sort()
    if len(aList) % 2 == 1:
        index = len(aList) / 2
        return aList[index]
    else:
        index = len(aList) / 2
        return ( aList[index - 1] + aList[index] ) / float(2)


#1/4,  3/4
def getFour(aList):
    aList.sort()
    mid_index = len(aList) / 2
    preList = aList[0: mid_index]
    postList = aList[mid_index: len(aList)]

    pre_four = getMed(preList)
    post_four = getMed(postList)
    return pre_four, post_four

def intraCo(serviceID, serviceDict, commitDict):
    resList = list()
    for class1 in serviceDict[serviceID]:
        for class2 in serviceDict[serviceID]:
            if (class1 in commitDict) and (class2 in commitDict[class1]):
                res = 1
            else:
                res = 0
            resList.append(res)
    minV = getMin(resList)
    maxV = getMax(resList)
    avgV = getAvg(resList)
    midV = getMed(resList)
    [pre4V, post4V] = getFour(resList)
    return [avgV, minV, maxV, pre4V, midV, post4V]

def intraCoWei(serviceID, serviceDict, commitDict):
    resList = list()
    for class1 in serviceDict[serviceID]:
        for class2 in serviceDict[serviceID]:
            if (class1 in commitDict) and (class2 in commitDict[class1]):
                res = commitDict[class1][class2]
            else:
                res = 0
            resList.append(res)
    minV = getMin(resList)
    maxV = getMax(resList)
    avgV = getAvg(resList)
    midV = getMed(resList)
    [pre4V, post4V] = getFour(resList)
    return [avgV, minV, maxV, pre4V, midV, post4V]


def interCo(serviceID1, serviceID2, serviceDict, commitDict):
    resList = list()
    for class1 in serviceDict[serviceID1]:
        for class2 in serviceDict[serviceID2]:
            if class1 in commitDict and class2 in commitDict[class1]:
                res = 1
            else:
                res = 0
            resList.append(res)

    minV = getMin(resList)
    maxV = getMax(resList)
    avgV = getAvg(resList)
    midV = getMed(resList)
    [pre4V, post4V] = getFour(resList)
    return [avgV, minV, maxV, pre4V, midV, post4V]

def interCoWei(serviceID1, serviceID2,  serviceDict, commitDict):
    resList = list()
    for class1 in serviceDict[serviceID1]:
        for class2 in serviceDict[serviceID2]:
            if class1 in commitDict and class2 in commitDict[class1]:
                res = commitDict[class1][class2]
            else:
                res = 0
            resList.append(res)
    minV = getMin(resList)
    maxV = getMax(resList)
    avgV = getAvg(resList)
    midV = getMed(resList)
    [pre4V, post4V] = getFour(resList)
    return [avgV, minV, maxV, pre4V, midV, post4V]

def statis(serviceDict, commitDict):

    #compute the intraCo for each service
    print '\n'
    print 'intraCo:  serviceID,avg,  minV, pre4V, midV, post4V, maxV'
    for serviceID in serviceDict:
        [avgV,minV, maxV, pre4V, midV, post4V] = intraCo(serviceID, serviceDict, commitDict)
        tmp = [serviceID, avgV, minV, pre4V, midV, post4V, maxV]
        tmp = [str(each) for each in tmp]
        print ','.join(tmp)


    #compute the intraCoWei for each service
    print '\n'
    print 'intraCowei:  serviceID, avg, minV, pre4V, midV, post4V, maxV'
    for serviceID in serviceDict:
        [avgV,minV, maxV, pre4V, midV, post4V] = intraCoWei(serviceID, serviceDict, commitDict)
        tmp = [serviceID, avgV, minV, pre4V, midV, post4V, maxV]
        tmp = [str(each) for each in tmp]
        print ','.join(tmp)

    #compute the interCo for each service
    print '\n'
    print 'interCo:  serviceID1, serviceID2, avg, minV, pre4V, midV, post4V, maxV'
    for serviceID1 in serviceDict:
        for serviceID2 in serviceDict:
            if serviceID1 != serviceID2:
                [avgV,minV, maxV, pre4V, midV, post4V] = interCo(serviceID1, serviceID2, serviceDict, commitDict)
                tmp = [serviceID1, serviceID2, avgV,minV, pre4V, midV, post4V, maxV]
                tmp = [str(each) for each in tmp]
                print ','.join(tmp)

    #compute the interCowei for each service
    print '\n'
    print 'interCoWei:  serviceID1, serviceID2, avg, minV, pre4V, midV, post4V, maxV'
    for serviceID1 in serviceDict:
        for serviceID2 in serviceDict:
            if serviceID1 != serviceID2:
                [avgV,minV, maxV, pre4V, midV, post4V] = interCoWei(serviceID1, serviceID2, serviceDict, commitDict)
                tmp = [serviceID1, serviceID2, avgV, minV, pre4V, midV, post4V, maxV]
                tmp = [str(each) for each in tmp]
                print ','.join(tmp)


#python cochange_1.py
#../testcase_data/jpetstore6/dependency/jpetstore6cmt.csv
#../../FoME/services/jpetstore/FoME/jpetstore_service_4.csv   FOME
if __name__ == '__main__':
    commitFileName  = sys.argv[1]
    serviceFileName = sys.argv[2]
    fileType = sys.argv[3]

    #commitDict[class1][class2]= commitTimes
    commitDict = readCommit(commitFileName)

    #serviceDict[serviceID] = [class1, class2, ...]
    serviceDict = readCluster(serviceFileName, fileType)

    statis(serviceDict, commitDict)
