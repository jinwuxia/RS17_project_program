import sys
import csv

#[contains,cluterID, className]
def readCluster(fileName):
    clusterID2ClassList = dict()  #[cluterID] = [className1, className2]
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [contains, clusterID, className] = each
            if clusterID not in clusterID2ClassList:
                clusterID2ClassList[clusterID] = list()
            clusterID2ClassList[clusterID].append(className)
    return clusterID2ClassList


#coverage classList
def readClass(fileName):
    classNameList = list()
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className] = each
            classNameList.append(className)
    return classNameList

def filterOut(classList, clusterDict):
    clusterDict_1 = dict()
    for clusterID in clusterDict:
        clusterDict_1[clusterID] = list()
        for className in clusterDict[clusterID]:
            if className in classList:
                clusterDict_1[clusterID].append(className)
    newID = 0
    newClusterDict = dict()
    for clusterID in clusterDict_1:
        if len(clusterDict_1[clusterID]) != 0:
            newClusterDict[newID] = list()
            for className in clusterDict_1[clusterID]:
                newClusterDict[newID].append(className)
            newID += 1
    print ('old cluster num=', len(clusterDict))
    print ('new cluster num=', len(newClusterDict))
    return newClusterDict

def writeCSV(fileName, newClusterDict):
    listlist = list()
    for clusterID in newClusterDict:
        for className in newClusterDict[clusterID]:
            listlist.append(['contains', clusterID,  className])

    with open(fileName, 'w', newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(listlist)
    print (fileName)

'''
python filterOutCluster.py classbenchmark.csv(icws/TS_class.csv)  oldCluter.csv newCluter.csv
'''
if __name__ == '__main__':
    classFileName = sys.argv[1]
    oldClusterFileName = sys.argv[2]
    newClusterFileName = sys.argv[3]

    oldClusterDict = readCluster(oldClusterFileName)
    classList = readClass(classFileName)
    newClusterDict = filterOut(classList, oldClusterDict)
    writeCSV(newClusterFileName, newClusterDict)
