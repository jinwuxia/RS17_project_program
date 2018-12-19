import sys
import csv

'''
no use, i think.
according to cluster files, filter commitfile
for a commit [class1, class2, weight] in commitfile
if class1 and class2 both are in service file
then we record (class1, class2, weight)
'''
def readCommit(fileName):
    commitList = list()
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [class1, class2, commit] = each
            commitList.append([class1, class2, commit])
    return commitList


def readCluster(fileName):
    serviceDict = dict() #[className] = serviceID
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className, serviceID] = each
            serviceDict[className] = serviceID
    return serviceDict

def isInDict(class1, class2, aDict):
    if class1 not in aDict:
        return False
    if class2 not in aDict[class1]:
        return False
    return True

#filter commit file-file by cluster
def filterCommit(commitList, serviceDict):
    newCommitList = list()
    aDict = dict()
    for each in commitList:
        [class1, class2, commit] = each
        if class1 in serviceDict and class2 in serviceDict and isInDict(class1, class2, aDict)==False:
            newCommitList.append([class1, class2, commit])
            if class1 not in aDict:
                aDict[class1] = dict()
            if class2 not in aDict:
                aDict[class2] = dict()
            aDict[class1][class2] = 1
            aDict[class2][class1] = 1

    print ('originLen:', len(commitList), '   newLen:',len(newCommitList))
    return newCommitList

def writeCSV(listList, fileName):
    with open(fileName, 'w', newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)

if __name__ == '__main__':
    commitFileName = sys.argv[1]
    clusterFileName = sys.argv[2]
    newCommitFileName = sys.argv[3]
    commitList = readCommit(commitFileName)
    serviceDict = readCluster(clusterFileName)
    newCommitList = filterCommit(commitList, serviceDict)
    writeCSV(newCommitList, newCommitFileName)
