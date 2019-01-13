import sys
import csv



class ClassElement:
    def __init__(self, classId, className, traceLen, traceList):
        self.classId = classId
        self.className = className
        self.traceLen = traceLen
        self.traceList = traceList


#read classgroup file
def readCSV(filename):
    alist = list()
    with open(filename, 'r', newline='') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classId, className, groupId, groupLen, groupDetail] = each
            if classId == 'classId':
                continue
            alist.append([classId, className, groupLen, groupDetail])
    return alist


#
def storeElementToStruct(alist):
    classList = list()
    for [classId, className, groupLen, groupDetail] in alist:
        groupList = groupDetail.split(";")
        oneclass = ClassElement(int(classId), className, groupLen, groupList)
        classList.append(oneclass)
    return classList


#according to classlsit, to init group. group[i] = [classid]
def initGroup(classList):
    groupList = list()
    for oneclass in classList:
        classId = oneclass.classId
        groupList.append([classId])
    return groupList

#get tracecset of the classes in classset
def getTraceSetByClassSet(classset, classList):
    traceSet  = set()
    for classId in classset:
        traceList = classList[classId].traceList
        traceSet.update(traceList)
    return traceSet


#compute distance according to traceset
def computeDiffDistance(traceset1, traceset2):
    diff1 = len(traceset1 - traceset2)
    diff2 = len(traceset2 - traceset1)
    return diff1 + diff2

#compute merged size according to traceset
def computeMergeSize(traceset1, traceset2):
    size = len(traceset1 | traceset2) # union of sets
    return size


def printMergeGroup(sortedValueList, groupList):
    groupId1 = sortedValueList[0][0]
    groupId2 = sortedValueList[0][1]
    currentDiffThr = sortedValueList[0][2]#update the currentDiffThr
    jiaosize = sortedValueList[0][3]
    mergesize = sortedValueList[0][4]
    jaccard = sortedValueList[0][5]
    #print("class ", groupList[groupId1], " and ", groupList[groupId2], " jaccard=", jaccard, " diff=", currentDiffThr, " jiaosize=", jiaosize, " mergesize=", mergesize)


def operateSet(traceset1, traceset2):
    diff = computeDiffDistance(traceset1,traceset2)
    mergeSize = computeMergeSize(traceset1,traceset2)
    jiaosize = len(traceset1 & traceset2)
    return diff, mergeSize, jiaosize


def mergeForAllThisDiff(currentDiffThr, sortedValueList, groupList):
    for each in sortedValueList:
        diff = each[2]
        if diff > currentDiffThr:
            break
        else:
            groupId1 = each[0]
            groupId2 = each[1]
            if len(groupList[groupId1]) != 0 and len(groupList[groupId2]) != 0:
                groupList[groupId1].extend(groupList[groupId2])
                groupList[groupId2] = list()

    newGroupList = list()
    for each in groupList:
        if len(each) != 0:
            newGroupList.append(each)
    return newGroupList

#group class according to trace set diff and mergedSize
#choose the diffdistance mininum and size minimum to merge
#form small function logic unit
def groupClassProcess(groupList, classList, THR):
    currentDiffThr = 0
    while((currentDiffThr <= THR) and (len(groupList) > 1)):
        valueList = list()  #groupId1, groupId2, diffdistance,  size
        for groupId1 in range(0, len(groupList)-1):
            for groupId2 in range(groupId1 + 1, len(groupList)):
                classSet1 = set( groupList[groupId1])
                classSet2 = set(groupList[groupId2])
                traceset1 = getTraceSetByClassSet(classSet1, classList)
                traceset2 = getTraceSetByClassSet(classSet2, classList)
                [diff, mergeSize, jiaosize] = operateSet(traceset1, traceset2)
                avalue = [groupId1, groupId2, diff, -jiaosize, mergeSize, -jiaosize/float(mergeSize)]
                valueList.append(avalue)
                #print(classSet1, classSet2,traceset1, traceset2, diff, mergeSize)

        #choose minum diffsize and minimum mergesize groups to merge
        sortedValueList = sorted(valueList, key = lambda x: (x[5],x[2], x[4]))
        currentDiffThr = sortedValueList[0][2]#update the currentDiffThr
        if currentDiffThr <= THR:
            #merge operation
            groupList = mergeForAllThisDiff(currentDiffThr, sortedValueList, groupList)
            '''
            printMergeGroup(sortedValueList, groupList)
            groupId1 = sortedValueList[0][0]
            groupId2 = sortedValueList[0][1]
            groupList[groupId1].extend(groupList[groupId2])
            del groupList[groupId2]
            '''
            #print("process diff:", str(currentDiffThr) + ",  grouplen:" + str(len(groupList)))
            #for each in groupList:
            #    print(each)
    return groupList


#find isolated groups
def searchGroupWithOneClass(groupList):
    isolatedGroupList = list()
    for groupId  in range(0, len(groupList)):
        classList = groupList[groupId]
        if len(classList) == 1:
            isolatedGroupList.append(groupId)
            #print("islated:", groupList[groupId])
    return isolatedGroupList


#group1 belongs to group2 if traceset1 belong to traceset2
def isOnegroupbelong2OtherByTrace(groupId1, groupId2, allClassList):
    if groupId2 != groupId1:
        traceset1 = getTraceSetByClassSet(groupList[groupId1], allClassList)
        traceset2 = getTraceSetByClassSet(groupList[groupId2], allClassList)
        if len(traceset1 - traceset2) == 0:
            return True
    return False


def groupIsolatedClass(groupList, allClassList):
    isolatedGroupList = searchGroupWithOneClass(groupList)
    for groupId1 in isolatedGroupList:
        singleclass = groupList[groupId1][0]
        #find all groups which contain this singleclass
        containergroupIds = list()
        for groupId in range(0, len(groupList)):
            if isOnegroupbelong2OtherByTrace(groupId1, groupId, allClassList):
                containergroupIds.append(groupId)
        #print(singleclass, containergroupIds)

        #if only in one other group, then merge
        if len(containergroupIds) == 1:
            objectiveGroupId = containergroupIds[0]
            groupList[objectiveGroupId].append(singleclass)
            #print("single class: ", singleclass, ", mergeinto group ", groupList[objectiveGroupId])
            groupList[groupId1] = list()

    newGroupList = list()
    for index in range(0, len(groupList)):
        if len(groupList[index]) != 0:
            newGroupList.append(groupList[index])
    return newGroupList


def formatGroupResult(newGroupList, classList):
    resList = list()
    alist = ['classid', 'classname', 'groupId', 'trace', 'grouptrace']
    resList.append(alist)
    for groupId in range(0, len(newGroupList)):
        classes = newGroupList[groupId]
        grouptraceset = list(getTraceSetByClassSet(set(classes), classList) )
        grouptracestr = ";".join(grouptraceset)
        for classId in classes:
            classobject = classList[classId]
            traceStr = ";".join(classobject.traceList)
            alist = [classId, classobject.className, groupId, traceStr, grouptracestr]
            resList.append(alist)
    return resList

def writeCSV(alist, filename):
    with open(filename, 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)


if __name__ == "__main__":
    classgroupfile = sys.argv[1]
    diffThr = int(sys.argv[2])#jpetstore=3,
    outfilename = sys.argv[3]

    alist = readCSV(classgroupfile)
    classList = storeElementToStruct(alist)

    groupList = initGroup(classList)
    newGroupList = groupClassProcess(groupList,classList, diffThr)

    #for each in newGroupList:
    #    print(each)
    #newGroupList = groupIsolatedClass(newGroupList, classList)
    #print (newGroupList)

    print(classgroupfile + ",diff," +  str(diffThr) + ",grouplen,"  + str(len(newGroupList)) + ",oldgrouplen," + str(len(groupList)))
    alist = formatGroupResult(newGroupList, classList)
    writeCSV(alist, outfilename)
