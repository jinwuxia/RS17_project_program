
import sys
import csv
from treelib import Node, Tree

METHODList = list() #[methodID] = MethodNode()
CLASSList = list()  #[classID] = ClassNde()
TRACEList = list()  #[traceID] = list()=[ mehod1, method2, ...]

METHODDICT = dict() #[methodname] = methodID
CLASSDICT = dict()  #[classname]  = classID

RESULTList = list() #[traceID]  = [[part1 = classID:1, classID2:3,....]   [part2 = classID:3, ...] [part3 = classID:2, ....]], [], []
PART3Dict=dict()  #[classID]
PART1Dict=dict()  #[classID]
PART2Dict=dict()  #[classID]


#filterTrace, filter the trace whose first method is 'service', then this trace is our focuse
FILTER_TRACE_NAME = "net.jforum.JForum.service"

PART1_END_METHODNAME = "net.jforum.Command.<init>()"
#= "net.jforum.context.web.WebRequestContext.getAction"
#= "net.jforum.context.web.WebRequestContext.getParameter"

PART2_END_METHODNAME = "net.jforum.JForum.handleFinally"


class MethodNode:
    def __init__(self, ID, longname, shortname, classID):
        self.ID = ID
        self.longname = longname #has paralist
        self.shortname = shortname #has paralist
        self.classID = classID

class ClassNode:
    def __init__(self, ID, longname, shortname):
        self.ID = ID
        self.longname = longname
        self.shortname = shortname

def GetMethodLongName(methodName, para):
    if para == '':
        post = '()'
    else:
        post = '(' + para + ')'
    return methodName + post


# methodname_short(prashorrtype, parashottype)
def GetMethodShortName(methodName, para):
    arr = methodName.split('.')
    if len(arr) >= 2:
        shortname = arr[len(arr) - 2] + '.' + arr[len(arr) - 1]
    else:
        shortname = methodName

    if para == '':
        post = '()'
    else:
        paraList = para.split(',')
        shortParaList = GetShortList(paraList)
        post = '('  + ','.join(shortParaList) + ')'

    return shortname + post


def GetClassShortName(className):
    arr = className.split('.')
    if len(arr) > 2:
        shortname = arr[len(arr) - 2] + '.' + arr[len(arr) - 1]
    else:
        shortname = className
    return shortname

#paraList = ['A.B.C', 'D.E.F'], return ['B.C','E.F']
def GetShortList(paraList):
    oneList = list()
    for para in paraList:
        arr = para.split('.')
        if len(arr) > 2:
            shortname = arr[len(arr) - 2] + '.' + arr[len(arr) - 1]
        else:
            shortname = para
        oneList.append(shortname)

    return oneList

def ReadCSV(filename):
    methodIndex = 0
    classIndex = 0
    #METHODDICT = dict() #dict(methodname) = ID

    with open(filename, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            #print each
            [traceID, order, structtype, startMethodName, endMethodName, m1_para, m2_para, class1, class2, m1_return, m2_return] = each

            startLongName = GetMethodLongName(startMethodName, m1_para)
            endLongName = GetMethodLongName(endMethodName, m2_para)

            startShortName = GetMethodShortName(startMethodName, m1_para)
            endShortName = GetMethodShortName(endMethodName, m2_para)

            startShortClassName = GetClassShortName(class1)
            endShortClassName = GetClassShortName(class2)

            startLongClassName = class1
            endLongClassName = class2

            if traceID == 'traceID':
                continue

            if startLongClassName not in CLASSDICT:
                CLASSDICT[startLongClassName] = classIndex
                oneClass = ClassNode(classIndex, startLongClassName, startShortClassName)
                CLASSList.append(oneClass)
                classIndex += 1
            if endLongClassName not in CLASSDICT:
                CLASSDICT[endLongClassName] = classIndex
                oneClass = ClassNode(classIndex, endLongClassName, endShortClassName)
                CLASSList.append(oneClass)
                classIndex += 1


            if startLongName not in METHODDICT:
                METHODDICT[startLongName] = methodIndex
                classID = CLASSDICT[startLongClassName]
                oneMethod = MethodNode(methodIndex, startLongName, startShortName, classID)
                METHODList.append(oneMethod)
                methodIndex += 1
            if endLongName not in METHODDICT:
                METHODDICT[endLongName] = methodIndex
                classID = CLASSDICT[endLongClassName]
                oneMethod = MethodNode(methodIndex, endLongName, endShortName, classID)
                METHODList.append(oneMethod)
                methodIndex += 1

            startID = METHODDICT[startLongName]
            endID = METHODDICT[endLongName]
            currentLen = len(TRACEList)
            if int(traceID) == currentLen:
                TRACEList.append(list())
            TRACEList[int(traceID)].append(startID)
            TRACEList[int(traceID)].append(endID)

def GetClassID(methodID):
    methodNode = METHODList[methodID]
    return methodNode.classID

def GetMethodID(partName):
    #print len(METHODDICT)
    for key in METHODDICT:
        #print key
        if key.startswith(partName):
            return METHODDICT[key]
    return -1


def GetFilterTraceID(filterTraceName):
    return GetMethodID(filterTraceName)

def GetFilterPart1End(part1EndMethodName):
    part1EndMethodID = GetMethodID(part1EndMethodName)
    return part1EndMethodID

def GetFilterPart2End(part2EndMethodName):
    part2EndMethodID = GetMethodID(part2EndMethodName)
    return part2EndMethodID

def ProcessTrace():
    part1EndMethodID = GetFilterPart1End(PART1_END_METHODNAME)
    part2EndMethodID = GetFilterPart2End(PART2_END_METHODNAME)
    filterMethodID = GetFilterTraceID(FILTER_TRACE_NAME) #filter the trace whose first method is service
    print 'part1EndMethodID, part2EndMethodID, filterMethodID', part1EndMethodID, part2EndMethodID, filterMethodID
    for traceID in range(0, len(TRACEList)):
        methodList =  TRACEList[traceID]
        if filterMethodID != methodList[0]:  #if this trace is not starting with 'service', abort it
            continue
        oneList = list()
        oneList.append(dict()) #part1Dict
        oneList.append(dict()) #part2Dict
        oneList.append(dict()) #part3Dict
        part1EndIndex = methodList.index(part1EndMethodID)
        part2EndIndex = methodList.index(part2EndMethodID)
        print 'part1EndIndex', part1EndIndex, "   ....   ", 'part2EndIndex', part2EndIndex
        if part1EndIndex == -1 or part2EndIndex == -1:
            print "part1 or part2  is not found...........\n\n"
            continue
        #part1
        for i in range(0, part1EndIndex + 1):
            if GetClassID(methodList[i]) not in oneList[0]:
                oneList[0][GetClassID(methodList[i])] = 1
            else:
                oneList[0][GetClassID(methodList[i])] += 1
        #part2
        for i in range(part1EndIndex + 1, part2EndIndex + 1):
            if GetClassID(methodList[i]) not in oneList[1]:
                oneList[1][GetClassID(methodList[i])] = 1
            else:
                oneList[1][GetClassID(methodList[i])] += 1
        #part3
        for i in range(part2EndIndex + 1, len(methodList)):
            if GetClassID(methodList[i]) not in oneList[2]:
                oneList[2][GetClassID(methodList[i])] = 1
            else:
                oneList[2][GetClassID(methodList[i])] += 1
        RESULTList.append(oneList)


#PART1Dict=dict()  #[classID]
def GetPart1():
    for traceID in range(0, len(RESULTList)):
        onePart1Dict = RESULTList[traceID][0]
        for classID in onePart1Dict:
            if classID not in PART1Dict:
                PART1Dict[classID] = 1

#PART3Dict=dict()  #[classID]
def GetPart3():
    for traceID in range(0, len(RESULTList)):
        onePart3Dict = RESULTList[traceID][2]
        for classID in onePart3Dict:
            if classID not in PART3Dict:
                PART3Dict[classID] = 1

#PART2Dict=dict()  #[classID]
def GetPart2():
    for traceID in range(0, len(RESULTList)):
        onePart2Dict = RESULTList[traceID][1]
        for classID in onePart2Dict:
            if (classID not in PART1Dict) and (classID not in PART3Dict) and (classID not in PART2Dict):
                PART2Dict[classID] = 1

def WriteFile(oneDict, fileName):
    oneList = list()
    for classID in oneDict:
        className = CLASSList[classID].longname
        oneList.append([className])
    print oneList

    with open(fileName, "w") as fp:
        writer = csv.writer(fp)
        writer.writerows(oneList)
    print fileName



#split by layer (3 layers)
#python pro.py  workflow.csv  outfile1.csv  outfile2.csv  outfile3.csv
if __name__ == '__main__':
    workflowFilename = sys.argv[1] # ../RS17_source_data/RS17_jpetstore/dynamic/source/jpetstore6_trace_method_workflow.csv
    part1FileName = sys.argv[2]
    part2FileName = sys.argv[3]
    part3FileName = sys.argv[4]
    '''
    arr = workflowFilename.split('/')
    tmp = arr.pop()
    project = tmp.split('_')[0]
    outFileNamePre = '/'.join(arr) + '/' + project + '_'
    '''
    ReadCSV(workflowFilename)
    '''
    for ID in range(0,len(TRACEList)):
        print ID, len(TRACEList[ID])
    for key in CLASSDICT:
        print key
    '''
    #print len(METHODDICT)
    ProcessTrace() #split and generate RESULTList
    #NOTICE: this processing order
    GetPart1() #process RESULTList,  generate PART1Dict
    GetPart3() #process RESULTList,  generate PART3Dict
    GetPart2() #process RESULTList,  generate PART2Dict

    WriteFile(PART1Dict, part1FileName)
    WriteFile(PART2Dict, part2FileName)
    WriteFile(PART3Dict, part3FileName)
