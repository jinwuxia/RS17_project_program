import sys
import csv

class ClassClusterRelation:
    def __init__(self, details, count, Extend, Typed, Import, Call, Cast, Create, Set, Implement, Use, Throw):
        self.count = count   #the class appears number in this cluster
        self.extend_count = Extend #this class extend deps with class in this cluster
        self.typed_count = Typed
        self.import_count = Import
        self.call_count = Call
        self.cast_count = Cast
        self.create_count = Create
        self.implement_count = Implement
        self.set_count = Set
        self.use_count = Use
        self.throw_count = Throw
        self.details = details

class Depend:
    def __init__(self):
        self.Extend = 0
        self.Typed = 1
        self.Import = 2
        self.Call = 3
        self.Cast = 4
        self.Create = 5
        self.Implement = 6
        self.Set = 7
        self.Use = 8
        self.Throw = 9

def readDeps(fileName):
    aDict = dict() #[class1Name][class2Name] = '010000001'
    with open(fileName) as fp:
        reader = csv.reader(fp)
        for each in reader:
            [class1, class2, deps] = each
            if class1 not in aDict:
                aDict[class1] = dict()
                aDict[class1][class2] = deps
            else:
                aDict[class1][class2] = deps
    return aDict

#input'100000100'
#output 'Typed,Extend,Call'
def getDepStr(depIDs):
    mapDict = dict()
    mapDict[0] = 'Extend'
    mapDict[1] = 'Typed'
    mapDict[2] = 'Import'
    mapDict[3] = 'Call'
    mapDict[4] = 'Cast'
    mapDict[5] = 'Create'
    mapDict[6] = 'Implement'
    mapDict[7] = 'Set'
    mapDict[8] = 'Use'
    mapDict[9] = 'Throw'
    depStrs = list()
    for index in range(0, len(depIDs)):
        if depIDs[index] == '1':
            depStrs.append(mapDict[index])
    return depStrs

#return '100000100' and 'Typed,Extend,Call'
def searchDeps(classID1, classID2):
    class1 = CLASSID2NAMEDict[classID1]
    class2 = CLASSID2NAMEDict[classID2]
    #depIDs = ''
    depStrList = list()
    if class1 in DEPDict:
        if class2 in DEPDict[class1]:
            depIDs = DEPDict[class1][class2]
            depStrList = getDepStr(depIDs)
        else:
            print '[ERROR] searchDeps not found class2: ', class2
    else:
        print '[ERROR] searchDeps not found class1: ', class1
    #return depIDs, depStrs
    return depStrList


#classID, className,  clusterID:count;  clusterID:[XXXXXXXXXX] ;
#                     clusterID:count,  clusterID[XXXXXXXXXX]
#
#input a overlapped classID, and its belonging cluster
#output classID, className, clusterID:count;....   , clusterID:[];...
#nonoverclass->class
def structAnalysisA(classID, itsClusterID):
    #in this cluster, the class appears number
    classCount = CLUSTERList[itsClusterID][classID]
    # class and other(non-overlap) deps type in each cluster
    extend_count = 0
    typed_count= 0
    import_count =0
    call_count = 0
    cast_count = 0
    create_count = 0
    implement_count = 0
    set_count = 0
    use_count = 0
    throw_count = 0
    details = dict() # dict[classID] = deps1,deps2
    for nonoverlapClassID in NONOVERLAPCLASSIDList[itsClusterID]:
        depStrList = searchDeps(nonoverlapClassID, classID)
        if len(depStrList) > 0:
            details[nonoverlapClassID] = ','.join(depStrList)
            for each in depStrList:
                if each == 'Extend':
                    extend_count += 1
                elif each == 'Typed':
                    typed_count += 1
                elif each == 'Import':
                    import_count += 1
                elif each == 'Call':
                    call_count += 1
                elif each == 'Cast':
                    cast_count += 1
                elif each == 'Create':
                    create_count += 1
                elif each == 'Implement':
                    implement_count += 1
                elif each == 'Set':
                    set_count += 1
                elif each == 'Use':
                    use_count += 1
                elif each == 'Throw':
                    throw_count += 1
    relation = ClassClusterRelation(details, classCount, extend_count, typed_count, import_count, call_count, cast_count, create_count, set_count, implement_count, use_count, throw_count)
    return relation

#class->nonoverclass
def structAnalysisB(classID, itsClusterID):
    #in this cluster, the class appears number
    classCount = CLUSTERList[itsClusterID][classID]
    # class and other(non-overlap) deps type in each cluster
    extend_count = 0
    typed_count= 0
    import_count =0
    call_count = 0
    cast_count = 0
    create_count = 0
    implement_count = 0
    set_count = 0
    use_count = 0
    throw_count = 0
    details = dict() # dict[classID] = deps1,deps2
    for nonoverlapClassID in NONOVERLAPCLASSIDList[itsClusterID]:
        depStrList = searchDeps(classID, nonoverlapClassID)
        if len(depStrList) > 0:
            details[nonoverlapClassID] = ','.join(depStrList)
            for each in depStrList:
                if each == 'Extend':
                    extend_count += 1
                elif each == 'Typed':
                    typed_count += 1
                elif each == 'Import':
                    import_count += 1
                elif each == 'Call':
                    call_count += 1
                elif each == 'Cast':
                    cast_count += 1
                elif each == 'Create':
                    create_count += 1
                elif each == 'Implement':
                    implement_count += 1
                elif each == 'Set':
                    set_count += 1
                elif each == 'Use':
                    use_count += 1
                elif each == 'Throw':
                    throw_count += 1
    relation = ClassClusterRelation(details, classCount, extend_count, typed_count, import_count, call_count, cast_count, create_count, set_count, implement_count, use_count, throw_count)
    return relation

def batchStructAnalysis(classDict):
    allRelationsDictA = dict() #dict[classID][clusterID] = relationobject
    allRelationsDictB = dict()
    for classID in classDict:
        allRelationsDictA[classID] = dict()  #dict[clusterID] = relation
        allRelationsDictB[classID] = dict()
        itsClusterIDList = classDict[classID]
        for itsClusterID in itsClusterIDList:
            #analyze this overlap class's relationship with its cluster
            oneRelationA = structAnalysisA(classID, itsClusterID)
            oneRelationB = structAnalysisB(classID, itsClusterID)
            allRelationsDictA[classID][itsClusterID] = oneRelationA
            allRelationsDictB[classID][itsClusterID] = oneRelationB
    return allRelationsDictA, allRelationsDictB

def printStructAnalysis(allRelationsDictA, allRelationsDictB):
    for classID in allRelationsDictA:
        print '\n|-------------------------------------------------------------------------------------'
        print '|classID=', classID, ', className=', CLASSID2NAMEDict[classID]
        for clusterID  in allRelationsDictA[classID]:
            reA = allRelationsDictA[classID][clusterID]
            reB = allRelationsDictB[classID][clusterID]
            #dep A
            print '|     *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*'
            print '|     clusterID=A', clusterID, ', count=', reA.count,
            print 'depsA=', 'ext:', reA.extend_count, 'typ:', reA.typed_count, 'cal:', reA.call_count, 'cas', reA.cast_count, 'set:', reA.set_count, 'use:', reA.use_count, 'cre:', reA.create_count, 'impl:', reA.implement_count, 'impo:', reA.import_count, 'thr:', reA.throw_count
            print '|     details: '
            for overclassID in reA.details:
                print '|         ', CLASSID2NAMEDict[overclassID], ' -> ', CLASSID2NAMEDict[classID], ':  ', reA.details[overclassID]

            #dep B
            print '|     clusterID=B', clusterID, ', count=', reB.count,
            print 'depsB=', 'ext:', reB.extend_count, 'typ:', reB.typed_count, 'cal:', reB.call_count, 'cas', reB.cast_count, 'set:', reB.set_count, 'use:', reB.use_count, 'cre:', reB.create_count, 'impl:', reB.implement_count, 'impo:', reB.import_count, 'thr:', reB.throw_count
            print '|     details: '
            for overclassID in reB.details:
                print '|         ', CLASSID2NAMEDict[classID], ' -> ', CLASSID2NAMEDict[overclassID], ':  ', reB.details[overclassID]

        print '|---------------------------------------------------------------------------------------'

def changeDep2Str(re):
    dep = ''
    if re.call_count != 0:
        dep += 'call:'
        dep += str(re.call_count)
        dep += ';'
    if re.typed_count != 0:
        dep += 'typed:'
        dep += str(re.typed_count)
        dep += ';'
    if re.create_count != 0:
        dep += 'create:'
        dep += str(re.create_count)
        dep += ';'
    if re.cast_count != 0:
        dep += 'cast:'
        dep += str(re.cast_count)
        dep += ';'
    if re.extend_count != 0:
        dep += 'extend:'
        dep += str(re.extend_count)
        dep += ';'
    if re.implement_count != 0:
        dep += 'implement:'
        dep += str(re.implement_count)
        dep += ';'
    if re.import_count != 0:
        dep += 'import:'
        dep += str(re.import_count)
        dep += ';'
    if re.use_count != 0:
        dep += 'use:'
        dep += str(re.use_count)
        dep += ';'
    if re.set_count != 0:
        dep += 'set:'
        dep += str(re.set_count)
        dep += ';'
    if re.throw_count != 0:
        dep += 'throw:'
        dep += str(re.throw_count)
        dep += ';'
    return dep

def changeDetailB2Str(classID, re):
    strstr = ''
    for overclassID in re.details:
        tmp = (CLASSID2NAMEDict[classID] + ' -> ' + CLASSID2NAMEDict[overclassID] + ' = ' +  re.details[overclassID])
        strstr += tmp
        strstr += ';'
    return strstr

def changeDetailA2Str(classID, re):
    strstr = ''
    for overclassID in re.details:
        tmp = (CLASSID2NAMEDict[overclassID] + ' -> ' + CLASSID2NAMEDict[classID] + ' = ' +  re.details[overclassID])
        strstr += tmp
        strstr += ';'
    return strstr

def write2File(fileName, allRelationsDictA, allRelationsDictB):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        title = ['classID', 'className', 'clusterIDs', 'classCount', 'structA', 'structB', 'structADetail', 'structBDetail']
        writer.writerow(title)

        for classID in allRelationsDictA:
            for clusterID in allRelationsDictA[classID]:
                oneList = list()
                oneList.extend([classID, CLASSID2NAMEDict[classID], clusterID])
                reA = allRelationsDictA[classID][clusterID]
                reB = allRelationsDictB[classID][clusterID]
                oneList.append(reA.count)  #reA.count = reB.count

                depA = changeDep2Str(reA)
                oneList.append(depA)
                depB = changeDep2Str(reB)
                oneList.append(depB)

                detailA = changeDetailA2Str(classID, reA)
                detailB = changeDetailB2Str(classID, reB)
                oneList.append(detailA)
                oneList.append(detailB)
                writer.writerow(oneList)
    print fileName


def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            resList.append(each)
    return resList

#str(each)  -> int(each)
def processCluster(initList):
    resList = list()
    for eachList in initList:
        eachList = [int(each) for each in eachList]
        resList.append(eachList)
    return resList

def processClass(initList):
    resDict = dict()
    for each in initList:
        [classID, className] = each
        resDict[int(classID)] = className
    return resDict

def processNonoverlap(initList):
    resList = list()
    for each in initList:
        [classID, className, clusterID] = each
        if classID == 'classID':
            continue
        classID = int(classID)
        clusterID = int(clusterID)
        if clusterID == len(resList):
            resList.append(list())
        resList[clusterID].append(classID)
    return resList


def processOverlap(initList):
    resDict = dict()
    for each in initList:
        [classID, className, clusterIDList] = each
        if classID == 'classID':
            continue
        classID = int(classID)
        clusterIDList = clusterIDList.split(':')
        clusterIDList = [int(clusterID) for clusterID in clusterIDList]
        resDict[classID] = clusterIDList
    return resDict

# for every overlapped class, get its structure deps with its cluster
CLUSTERList = list()
CLASSID2NAMEDict = dict()
NONOVERLAPCLASSIDList = list()
DEPDict = dict()
#python pro.py  xmlcsvfile   testcaseClass clusterfile, nonlapClass,  lapclass    out.csv
if __name__ == '__main__':
    csvFileName = sys.argv[1]               #deps file
    testcaseClassFileName = sys.argv[2]     #classID and className in testcase
    clusterFileName = sys.argv[3]           #clusterList file(mergefile)
    nonOverlapFileName = sys.argv[4]        #non-overlap file
    inputFileName = sys.argv[5]             #need to be analyzed class file(overlapped class)
    outFileName = sys.argv[6]
    #CLUSTERList=[[cluster0_classcountlist], [cluster1_classdcountlist], []]
    clusterList = readCSV(clusterFileName)
    CLUSTERList = processCluster(clusterList)
    '''
    print '\nCLUSTERList'
    for each in CLUSTERList:
        print each
    '''

    #dict[classID] = className
    classID2NameList = readCSV(testcaseClassFileName)
    CLASSID2NAMEDict = processClass(classID2NameList)
    '''
    print '\nCLASSID2NAMEDict'
    for each in CLASSID2NAMEDict:
        print each, CLASSID2NAMEDict[each]
    '''

    #list[cluster0]=[classIDList], list[cluster1]=[classIDList]
    nonoverlapClassIDList = readCSV(nonOverlapFileName)
    NONOVERLAPCLASSIDList = processNonoverlap(nonoverlapClassIDList)
    '''
    print '\nNONOVERLAPCLASSIDList'
    for each in NONOVERLAPCLASSIDList:
        print each
    '''

    DEPDict = readDeps(csvFileName) #generate DEPDict

    #dict[classID] =[clusterID1, id2, id3, ...]
    overlappedClassList = readCSV(inputFileName)
    overlappedClassDict = processOverlap(overlappedClassList)
    '''
    print '\noverlappedClassDict'
    for each in overlappedClassDict:
        print each, overlappedClassDict[each]
    '''
    ##############read finiashed##########

    ##############start analysis #########
    print '\nallRelationsDict'
    [allRelationsDictA, allRelationsDictB] = batchStructAnalysis(overlappedClassDict)
    printStructAnalysis(allRelationsDictA, allRelationsDictB)
    write2File(outFileName, allRelationsDictA, allRelationsDictB)
