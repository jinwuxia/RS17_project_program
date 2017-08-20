import sys
import csv

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

class ComCost:
    def __init__(self, call, p_num, r_num, call_f, p_num_f, r_num_f, total, total_f):
        self.call = call
        self.p_num = p_num
        self.r_num = r_num
        self.call_f = call_f
        self.p_num_f = p_num_f
        self.r_num_f = r_num_f
        self.total = total
        self.total_f = total_f


def readComDeps(fileName):
    aDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className1, className2, call, p_num, r_num, call_f, p_num_f, r_num_f, total, total_f] = each
            if className1 == 'className1':
                continue
            oneDep = ComCost(int(call), int(p_num), int(r_num), int(call_f), int(p_num_f), int(r_num_f), int(total), int(total_f))
            if className1 not in aDict:
                aDict[className1] = dict()
            aDict[className1][className2] = oneDep
    return aDict


class ClassClusterRelation:
    def __init__(self, details, call, p_num, r_num, call_f, p_num_f, r_num_f, total, total_f):
        self.call = call   #*
        self.p_num = p_num
        self.r_num = r_num
        self.call_f = call_f #*
        self.p_num_f = p_num_f
        self.r_num_f = r_num_f
        self.total = total   #*
        self.total_f = total_f #*
        self.details = details  #dict[nonlapClassID] = str

def searchComDep(classID1, classID2):
    oneDep = ''
    className1 = CLASSID2NAMEDict[classID1]
    className2 = CLASSID2NAMEDict[classID2]
    if className1 in COMDEPSDict:
        if className2 in COMDEPSDict[className1]:
            oneDep = COMDEPSDict[className1][className2]
        else:
            print '[WARN]: not found ', className2
    else:
        print '[WARN]: not found ', className1
    return oneDep

#cluster->classID
def comAnalysisA(classID, itsClusterID):
    sum_call = 0
    sum_p_num = 0
    sum_r_num = 0
    sum_call_f = 0
    sum_p_num_f = 0
    sum_r_num_f = 0
    sum_total = 0
    sum_total_f = 0
    details = dict()
    for nonlapClassID in NONOVERLAPCLASSIDList[itsClusterID]:
        oneDep = searchComDep(nonlapClassID, classID)
        if oneDep !='':
            sum_call += oneDep.call
            sum_p_num += oneDep.p_num
            sum_r_num += oneDep.r_num
            sum_call_f += oneDep.call_f
            sum_p_num_f += oneDep.p_num_f
            sum_r_num_f += oneDep.r_num_f
            sum_total += oneDep.total
            sum_total_f += oneDep.total_f
            tmp = (CLASSID2NAMEDict[nonlapClassID]  + ' -> ' + CLASSID2NAMEDict[classID] + '=')
            tmp += ('cal:' + str(oneDep.call))
            tmp += (',tot:' + str(oneDep.total))
            tmp += (',cal_f:' + str(oneDep.call_f))
            tmp += (',tot_f:' + str(oneDep.total_f))
            details[nonlapClassID] = tmp
    oneRelation = ClassClusterRelation(details, sum_call, sum_p_num, sum_r_num, sum_call_f, sum_p_num_f, sum_r_num_f, sum_total, sum_total_f)
    return oneRelation


#class--> cluster
def comAnalysisB(classID, itsClusterID):
    sum_call = 0
    sum_p_num = 0
    sum_r_num = 0
    sum_call_f = 0
    sum_p_num_f = 0
    sum_r_num_f = 0
    sum_total = 0
    sum_total_f = 0
    details = dict()
    for nonlapClassID in NONOVERLAPCLASSIDList[itsClusterID]:
        oneDep = searchComDep(classID, nonlapClassID) #NOTE_THE_STATEMENT
        if oneDep !='':
            sum_call += oneDep.call
            sum_p_num += oneDep.p_num
            sum_r_num += oneDep.r_num
            sum_call_f += oneDep.call_f
            sum_p_num_f += oneDep.p_num_f
            sum_r_num_f += oneDep.r_num_f
            sum_total += oneDep.total
            sum_total_f += oneDep.total_f
            tmp = (CLASSID2NAMEDict[classID]  + ' -> ' + CLASSID2NAMEDict[nonlapClassID] + '=')
            tmp += ('cal:' + str(oneDep.call))
            tmp += (',tot:' + str(oneDep.total))
            tmp += (',cal_f:' + str(oneDep.call_f))
            tmp += (',tot_f:' + str(oneDep.total_f))
            details[nonlapClassID] = tmp
    oneRelation = ClassClusterRelation(details, sum_call, sum_p_num, sum_r_num, sum_call_f, sum_p_num_f, sum_r_num_f, sum_total, sum_total_f)
    return oneRelation


def batchComAnalysis(classDict):
    allRelationsDictA = dict() #dict[classID][clusterID] = relationobject
    allRelationsDictB = dict()
    for classID in classDict:
        allRelationsDictA[classID] = dict()  #dict[clusterID] = relation
        allRelationsDictB[classID] = dict()
        itsClusterIDList = classDict[classID]
        for itsClusterID in itsClusterIDList:
            #analyze this overlap class's relationship with its cluster
            oneRelationA = comAnalysisA(classID, itsClusterID)
            oneRelationB = comAnalysisB(classID, itsClusterID)
            allRelationsDictA[classID][itsClusterID] = oneRelationA
            allRelationsDictB[classID][itsClusterID] = oneRelationB
    return allRelationsDictA, allRelationsDictB


def printComAnalysis(allRelationsDictA, allRelationsDictB):
    for classID in allRelationsDictA:
        print '\n|-------------------------------------------------------------------------------------'
        print '|classID=', classID, ', className=', CLASSID2NAMEDict[classID]
        for clusterID  in allRelationsDictA[classID]:
            reA = allRelationsDictA[classID][clusterID]
            reB = allRelationsDictB[classID][clusterID]
            #dep A
            print '|     *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*'
            print '|     clusterID=A', clusterID,
            print 'depsA=', 'call:', reA.call, 'total:', reA.total, 'call_f:', reA.call_f, 'total_f:', reA.total_f
            print '|     details: '
            for overclassID in reA.details:
                print '|         ', reA.details[overclassID]

            #dep B
            print '|     clusterID=B', clusterID,
            print 'depsB=', 'call:', reB.call, 'total:', reB.total, 'call_f:', reB.call_f, 'total_f:', reB.total_f
            print '|     details: '
            for overclassID in reB.details:
                print '|         ', reB.details[overclassID]

        print '|---------------------------------------------------------------------------------------'


def changeDetail2Str(re):
    strstr = ''
    for overclassID in re.details:
        strstr += re.details[overclassID]
        strstr += '. '
    return strstr

def write2File(fileName, allRelationsDictA, allRelationsDictB):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        title = ['classID', 'className', 'clusterIDs', 'A_call', 'A_total', 'A_call_f', 'A_total_f', 'B_call', 'B_total', 'B_call_f', 'B_total_f', 'comADetail', 'comBDetail']
        writer.writerow(title)

        for classID in allRelationsDictA:
            for clusterID in allRelationsDictA[classID]:
                oneList = list()
                oneList.extend([classID, CLASSID2NAMEDict[classID], clusterID])
                reA = allRelationsDictA[classID][clusterID]
                reB = allRelationsDictB[classID][clusterID]
                oneList.extend([reA.call, reA.total, reA.call_f, reA.total_f])
                oneList.extend([reB.call, reB.total, reB.call_f, reB.total_f])
                oneList.append(changeDetail2Str(reA))
                oneList.append(changeDetail2Str(reB))
                writer.writerow(oneList)
    print fileName




# for every overlapped class, get its structure deps with its cluster
CLUSTERList = list()
CLASSID2NAMEDict = dict()
NONOVERLAPCLASSIDList = list()
COMDEPSDict = dict()
#python pro.py  comcsvfile   testcaseClass clusterfile, nonlapClass,  lapclass    out.csv
if __name__ == '__main__':
    csvFileName = sys.argv[1]               #comdeps file
    testcaseClassFileName = sys.argv[2]     #classID and className in testcase
    clusterFileName = sys.argv[3]           #clusterList file(mergefile)
    nonOverlapFileName = sys.argv[4]        #non-overlap file
    inputFileName = sys.argv[5]             #need to be analyzed class file(overlapped class)
    outFileName = sys.argv[6]

    #CLUSTERList=[[cluster0_classcountlist], [cluster1_classdcountlist], []]
    clusterList = readCSV(clusterFileName)
    CLUSTERList = processCluster(clusterList)

    #dict[classID] = className
    classID2NameList = readCSV(testcaseClassFileName)
    CLASSID2NAMEDict = processClass(classID2NameList)

    #list[cluster0]=[classIDList], list[cluster1]=[classIDList]
    nonoverlapClassIDList = readCSV(nonOverlapFileName)
    NONOVERLAPCLASSIDList = processNonoverlap(nonoverlapClassIDList)

    #dict[classID] =[clusterID1, id2, id3, ...]
    overlappedClassList = readCSV(inputFileName)
    overlappedClassDict = processOverlap(overlappedClassList)

    #dict[classname1][classname2] = ComCost(p1,p2,p3,,...)
    COMDEPSDict = readComDeps(csvFileName) #generate COMDEsPDict

    ##############read finiashed#################################################

    [allRelationsDictA, allRelationsDictB] = batchComAnalysis(overlappedClassDict)
    printComAnalysis(allRelationsDictA, allRelationsDictB)
    write2File(outFileName, allRelationsDictA, allRelationsDictB)
