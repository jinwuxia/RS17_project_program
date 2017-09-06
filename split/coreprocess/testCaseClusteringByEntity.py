'''
do testcase clustering according to the entiti classes
geneate clusters_0.csv
here clustering is just merge testcases whose entity used are same
'''

import sys
import csv

TESTCASENAMEDict = dict() #testcase[id] = name


def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp, delimiter = ',')
        for eachLine in reader:
            resList.append(eachLine)
    return resList

def writeCSV(listlist, fileName):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        for eachList in listlist:
            writer.writerow(eachList)
    print fileName


#delete the first column, that is testcase ID
def delFirstCol(fv):
    newFv = list()
    testcaseNameDict = dict()
    testCaseID = 0
    for eachList in fv:
        testcaseNameDict[testCaseID] = eachList[0]
        testCaseID += 1
        del eachList[0]
        for index in range(0, len(eachList)):
            eachList[index] = int(eachList[index])
        newFv.append(eachList)
    return newFv, testcaseNameDict


def change2Set(fv):
    newFv = list()
    for eachList in fv:
        newSet = set()
        for eachClassID in range(0, len(eachList)):
            if eachList[eachClassID] != 0:
                newSet.add(eachClassID)
        newFv.append(newSet)
    return newFv

def doCluster(setList):
    processedDict = dict()
    finalCluster = list()
    for testCaseID in range(0, len(setList)):
        if testCaseID not in processedDict:
            oneSet = set()
            oneSet.add(testCaseID)
            processedDict[testCaseID] = 1
            if len(setList[testCaseID]) == 0:
                finalCluster.append(oneSet)
                continue
            for otherID in range(testCaseID + 1, len(setList)):
                if otherID not in processedDict:
                    if (len(setList[testCaseID]) == len(setList[otherID])) and len(setList[testCaseID] & setList[otherID]) == len(setList[testCaseID]):
                        oneSet.add(otherID)
                        processedDict[otherID] = 1
            finalCluster.append(oneSet)
    return finalCluster




def printClustering(finalCluster):
    resList = list()   #[]clusterID, testcaseID, testcaseName
    for clusterID in range(0, len(finalCluster)):
        for testcaseID in list( finalCluster[clusterID] ):
            resList.append( [clusterID, testcaseID, TESTCASENAMEDict[testcaseID]] )
    return resList

#python pro.py   tsfv.csv    outfileName
if __name__ == "__main__":
    featureFileName = sys.argv[1]    #testcase feature maxtrix filename
    outfileName = sys.argv[2]  #Test case

    tsFv = readCSV(featureFileName)
    [newTsFv, TESTCASENAMEDict] = delFirstCol(tsFv)

    tsCount = len(newTsFv)

    newSetFv = change2Set(newTsFv)
    finalCluster = doCluster(newSetFv)

    resList = printClustering(finalCluster)
    writeCSV(resList, outfileName)
