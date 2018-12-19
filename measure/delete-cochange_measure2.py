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

#classDict[className] = serviceID
def readClass(fileName, fileType):
    classDict = dict() #[className] = serviceID
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            if fileType == 'FOME':
                [classID, className, serviceID] = each
            else:
                [contain, serviceID, className] = each
            classDict[className] = serviceID
    return classDict

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


def getPairLen(aDict):
    totalLen = 0
    for key1 in aDict:
        totalLen += len(aDict[key1].keys())
    return totalLen


#filter commit file-file by cluster
def filterCommit(commitDict, classDict):
    newCommitDict = dict()
    for class1 in commitDict:
        if class1 not in classDict:
            continue
        for class2 in commitDict[class1]:
            if class2 in classDict:   #add new
                if class1 not in newCommitDict:
                    newCommitDict[class1] = dict()
                newCommitDict[class1][class2] = commitDict[class1][class2]

    print 'originLen:', getPairLen(commitDict), '   newLen:', getPairLen(newCommitDict)
    return newCommitDict

#TP: cochange , and also in same service
def computeTP(commitDict, classDict):
    res = 0
    for class1 in commitDict:
        serviceID1 = classDict[class1]
        for class2 in commitDict[class1]:
            serviceID2 = classDict[class2]
            if serviceID1 == serviceID2:
                res += 1
    return res


#FN: cochange , and not in same service
def computeFN(commitDict, classDict):
    res = 0
    for class1 in commitDict:
        serviceID1 = classDict[class1]
        for class2 in commitDict[class1]:
            serviceID2 = classDict[class2]
            if serviceID1 != serviceID2:
                res += 1
    return res

#FP: not cochange , and in same service
def computeFP(serviceDict, tp):
    #total edge in same services - TP
    total = 0
    for serviceID in serviceDict:
        classLen = len(serviceDict[serviceID])
        total += ( classLen * (classLen - 1) )   #double direction

    return (total - tp)

#TN: not cochange , and not in same service
def computeTN(serviceDict, commitDict):
    interEdgeList = list()
    for serviceID1 in serviceDict:
        classList1 = serviceDict[serviceID1]
        for serviceID2 in serviceDict:
            if serviceID1 != serviceID2:
                classList2 = serviceDict[serviceID2]
                for class1 in classList1:
                    for class2 in classList2:
                        interEdgeList.append([class1, class2])
    res  = 0
    for each in interEdgeList:
        [class1, class2] = each
        if class1 in commitDict and class2 in commitDict[class1]:
            continue
        else:
            res += 1
    return res


def computeStatis(commitDict, classDict, serviceDict):
    tp = computeTP(commitDict, classDict)
    fp = computeFP(serviceDict, tp)
    fn = computeFN(commitDict, classDict)
    tn = computeTN(serviceDict, commitDict)

    precison = round( tp / float(tp + fp), 4 )
    recall   = round( tp / float(tp + fn), 4 )
    fscore  = round( 2 * precison * recall / float(precison + recall), 4 )
    return tp, fp, fn, tn, precison, recall, fscore

# python cochange_fmeasure.py
#  ../testcase_data/roller520/dependency/roller520cmt_simple.csv
# ../../FoME/services/roller/LIMBO/roller_service_1   ddd
if __name__ == '__main__':
    commitFileName = sys.argv[1]
    clusterFileName = sys.argv[2]
    fileType = sys.argv[3]

    commitDict = readCommit(commitFileName)
    classDict = readClass(clusterFileName, fileType)
    serviceDict = readCluster(clusterFileName, fileType)
    newCommitDict = filterCommit(commitDict, classDict)

    [tp, fp, fn, tn, precison, recall, fscore] = computeStatis(newCommitDict, classDict, serviceDict)

    tmp = [tp, fp, fn, tn, precison, recall, fscore]
    tmp = [str(each) for each in tmp]
    print 'tp,fp,fn,tn,precison,recall,fscore'
    print ','.join(tmp)
