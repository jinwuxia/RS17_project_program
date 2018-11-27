import sys
import csv


#duichen
className2IDDict = dict()
classID2NameDict = dict()
depM = list()  #feature vector 
MINSIMVALUE = 0
pre=""


def isInCode(className, pre):
    if className.startswith(pre):
        return True
    else:
        return False

def readCSV(fileName):
    listList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [fromClassName, toClassName, deps]  = each
            if fromClassName == 'From Class' or isInCode(fromClassName, pre) == False or isInCode(toClassName, pre) == False:
                continue
            listList.append([fromClassName, toClassName, int(deps)])

    return listList


def writeCSV(fileName):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        for i in range(0, len(classID2NameDict)):
            tmpList = list()
            tmpList.append(classID2NameDict[i])
            tmpList.extend(depM[i])
            writer.writerow(tmpList)

#init className2IDDict and classID2NameDict
def readClassList(fileName):
    classID = 0

    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            className2IDDict[className] = classID
            classID2NameDict[classID] = className
            classID += 1

#init depM  (duichen ju zhen)
def processList(listList):
    N = len(className2IDDict)
    for i in range(0, N):
        tmpList = [MINSIMVALUE] * N
        depM.append(tmpList)

    for each in listList:
        fromClassID = -1
        toClassID = -1
        [fromClassName, toClassName, deps] = each
        if fromClassName in className2IDDict:
            fromClassID = className2IDDict[fromClassName]
        if toClassName in className2IDDict:
            toClassID = className2IDDict[toClassName]
        
        if fromClassID != -1 and toClassID != -1:
            depM[fromClassID][toClassID] = deps + depM[fromClassID][toClassID] 
            depM[toClassID][fromClassID] = deps + depM[toClassID][fromClassID]
        else:
            print fromClassName, fromClassID, toClassName, toClassID

if __name__ == "__main__":
    classListFile = sys.argv[1]
    featureFile = sys.argv[2]
    featureVectorFile = sys.argv[3]
    pre = sys.argv[4]

    readClassList(classListFile)
    listList = readCSV(featureFile)
    processList(listList)
    writeCSV(featureVectorFile)



