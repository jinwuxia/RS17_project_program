import sys
import csv

def readClass(fileName):
    classList = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            classList.append(className)
    return classList



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

def generateSample(classList, commitDcit):
    positiveSampleList = list()
    negativeSampleList = list()
    for className1 in classList:
        for className2 in classList:
            if className1 != className2:
                if className1 in commitDict and className2 in commitDict[className1]:
                    positiveSampleList.append([className1, className2])
                else:
                    negativeSampleList.append([className1, className2])
    print 'positiveSampleList', len(positiveSampleList)
    print 'negativeSampleList', len(negativeSampleList)
    return positiveSampleList, negativeSampleList


#classDict[className] = serviceID
def readClassDict(fileName, fileType):
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

def computeStatis(classDict, pSample, nSample):
    tp = 0
    fn = 0
    tn = 0
    fp = 0

    for [className1, className2] in pSample:
        if className1 in classDict and className2 in classDict:
            serviceID1 = classDict[className1]
            serviceID2 = classDict[className2]
            if serviceID1 == serviceID2:
                tp += 1
    fn = len(pSample) - tp

    for [className1, className2] in nSample:
        if className1 in classDict and className2 in classDict:
            serviceID1 = classDict[className1]
            serviceID2 = classDict[className2]
            if serviceID1 != serviceID2:
                tn += 1

    fp = len(nSample) - tn
    return tp,fn,tn,fp

# python cochange_fmeasure_sample.py  jpetstore_service_4_sample.csv
# ../testcase_data/jpetstore6/dependency/jpetstore6cmt.csv
# ../../FoME/services/jpetstore/MEM/jpetstore_service_4.csv  ddd
if __name__ == '__main__':
    classFileName = sys.argv[1]
    commitFileName = sys.argv[2]
    classDictFileName = sys.argv[3]  #service file
    fileType = sys.argv[4]          #FOME, ...

    classList = readClass(classFileName)
    commitDict = readCommit(commitFileName)
    [pSample, nSample] = generateSample(classList, commitDict)

    #sample end, start measure
    classDict = readClassDict(classDictFileName, fileType)
    [tp,fn,tn,fp] = computeStatis(classDict, pSample, nSample)
    print "tp,fn,tn,fp"
    print tp,fn,tn,fp
