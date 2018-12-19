import sys
import csv

def readCommit(fileName):
    commitList = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [class1, class2, commit] = each
            commitList.append([class1, class2])
    return commitList


def readCluster(fileName, fileType):
    serviceDict = dict() #[className] = serviceID
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            if fileType == 'FOME':
                [classID, className, serviceID] = each
            else:
                [contain, serviceID, className] = each
            serviceDict[className] = serviceID
    return serviceDict



#filter commit file-file by cluster
def filterCommit(commitList, serviceDict):
    newCommitList = list()
    for each in commitList:
        [class1, class2] = each
        if class1 in serviceDict and class2 in serviceDict:
            newCommitList.append([class1, class2])
    print 'originLen:',len(commitList), '   newLen:',len(newCommitList)
    return newCommitList



def statis_back(commitList, serviceDict):
    #serviceDict[className] = serviceID

    #compute each service'size
    serviceSizeDict = dict()
    for className in serviceDict:
        serviceID = serviceDict[className]
        if serviceID not in serviceSizeDict:
            serviceSizeDict[serviceID] = 0
        serviceSizeDict[serviceID] += 1

    rateDict = dict() #[serviceID] = filePair commit times
    total = len(commitList)
    for eachList in commitList:
        [class1, class2] = eachList
        if class1 in serviceDict and class2 in serviceDict:
            id1 = serviceDict[class1]
            id2 = serviceDict[class2]
            if id1 == id2:
                if id1 not in rateDict:
                    rateDict[id1] = 1
                else:
                    rateDict[id1] += 1

    print 'total commit=',total
    print 'rateDict=', rateDict
    print 'serviceSizeDict=', serviceSizeDict

    sumPro = 0
    for serviceID in rateDict:
        serviceSize = serviceSizeDict[serviceID]
        inSize = rateDict[serviceID]
        pro = inSize / float(serviceSize * serviceSize)
        sumPro += pro
        print 'serivceID', serviceID, '  pro', pro

    print 'average=', sumPro / float(len(rateDict))




def statis(commitList, serviceDict):
    #serviceDict[className] = serviceID

    #compute each service'size
    serviceSizeDict = dict()
    for className in serviceDict:
        serviceID = serviceDict[className]
        if serviceID not in serviceSizeDict:
            serviceSizeDict[serviceID] = 0
        serviceSizeDict[serviceID] += 1

    rateDict = dict() #[serviceID] = filePair commit times
    total = len(commitList)
    for eachList in commitList:
        [class1, class2] = eachList
        id1 = serviceDict[class1]
        id2 = serviceDict[class2]
        if id1 == id2:
            if id1 not in rateDict:
                rateDict[id1] = 1
            else:
                rateDict[id1] += 1

    print 'total filtered commit=',total
    print 'rateDict[serviceID]=edgeNumber,  ', rateDict
    print 'serviceSizeDict=', serviceSizeDict

    '''
    sumPro = 0
    for serviceID in rateDict:
        serviceSize = serviceSizeDict[serviceID]
        inSize = rateDict[serviceID]
        pro = inSize / float(serviceSize * serviceSize)
        sumPro += pro
        print 'serivceID', serviceID, '  pro', pro

    print 'average=', sumPro / float(len(rateDict))
    '''


#python cochange_1.py
#../testcase_data/jpetstore6/dependency/jpetstore6cmt.csv
#../../FoME/services/jpetstore/FoME/jpetstore_service_4.csv   FOME
if __name__ == '__main__':
    commitFileName  = sys.argv[1]
    serviceFileName = sys.argv[2]
    fileType = sys.argv[3]
    commitList = readCommit(commitFileName)
    serviceDict = readCluster(serviceFileName, fileType)
    newCommitList = filterCommit(commitList, serviceDict)
    statis(newCommitList, serviceDict)
