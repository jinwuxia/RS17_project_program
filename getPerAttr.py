
import sys
import csv

METHODList = list() #[methodID] = Method()
CLASSList = list()  #[classID] = Class()
METHODEDGEList = list()
CLASSEDGEList = list()
METHOD2ClassDict = dict() #dict[methodlongname] = classname
class MethodNode:
    def __init__(self, ID, methodName):
        self.ID = ID
        self.methodName = methodName #has paralist
class MethodEdge:
    def __init__(self, startID, endID, uniTraceCount, uniTraceList, flowType):
        self.startID = startID
        self.endID = endID
        self.uniTraceCount = uniTraceCount
        self.uniTraceList = uniTraceList
        self.flowType = flowType

class classNode:
    def __init__(self, ID, className):
        self.ID = ID
        self.className = className

class classEdge:
    def __init__(self, startID, endID, uniTraceCount, uniTraceList, uniFlowTypeList, traceCount, traceList):
        self.startID = startID
        self.endID = endID
        self.uniTraceCount = uniTraceCount
        self.uniTraceList = uniTraceList
        self.uniFlowTypeList = uniFlowTypeList
        self.traceCount = traceCount
        self.traceList = traceList


# methodname_full.(prafulltype, parafulltype)
def GetLongName(methodName, para):
    if para == '':
        post = '()'
    else:
        post = '(' + para + ')'

    return methodName + post

def getClassName(methodName):
    return METHOD2ClassDict[methodName]

    
def MergeTraceAttr(classEdgeIndex, methodEdgeIndex):
    startMethodID = METHODEDGEList[methodEdgeIndex].startID)
    endMethodID = METHODEDGEList[methodEdgeIndex].endID)
    m_uniTraceList = METHODEDGEList[methodEdgeIndex].uniTraceList
    m_uniTraceCount = METHODEDGEList[methodEdgeIndex].uniTraceCount
    flowType = METHODEDGEList[methodEdgeIndex].flowType

    #mergeTraceList and traceCount
    CLASSEDGEList[classEdgeIndex].traceCount += m_uniTraceCount
    CLASSEDGEList[classEdgeIndex].traceList.extends(m_uniTraceList)

    #merge uniTarceList and uniTraceCount, and uniFlowTYpeList
    for i in range(0, len(m_uniTraceList)):
        traceID = m_uniTraceList[i]
        if traceID not in CLASSEDGEList[classEdgeIndex].uniTraceList):
            CLASSEDGEList[classEdgeIndex].uniTraceList.append(traceID)
            CLASSEDGEList[classEdgeIndex].uniTraceCount += 1
            CLASSEDGEList[classEdgeIndex].uniFlowTypeList.append(flowType)
        #else do nothing




def ExtractClasses():
    classIndex = 0
    tmpClassDict = dict()
    classEdgeIndex = 0
    tmpClassEdgeDict=dict()

    for methodEdgeIndex in range(0, len(METHODEDGEList)):
        startMethodID = METHODEDGEList[methodEdgeIndex].startID)
        endMethodID = METHODEDGEList[methodEdgeIndex].endID)

        startClassName = GetClassName(METHODList[startMethodID].methodName)
        endClassName = GetClassName(METHODList[endMethodID].methodName)
        m_uniTraceList = METHODEDGEList[methodEdgeIndex].uniTraceList
        m_uniTraceCount = METHODEDGEList[methodEdgeIndex].uniTraceCount
        flowType = METHODEDGEList[methodEdgeIndex].flowType

        if startClassName not in tmpClassDict:
            tmpClassDict[startClassName] = classIndex
            oneClass = ClassNode(classIndex, startClassName)
            CLASSList.append(oneClass)
            classIndex += 1

        if endClassName not in tmpClassDict:
            tmpClassDict[endClassName] = classIndex
            oneClass = ClassNode(classIndex, endClassName)
            CLASSList.append(oneClass)
            classIndex += 1

        startClassID = tmpClassDict[startClassName]
        endClassID = tmpClassDict[endClassName]
        if startClassID == endClassID:
            continue

        if startClassID not in tmpClassEdgeDict:
            oneClassEdge = ClassEdge(startClassID, endClassID, uniTraceCount=m_uniTraceCount, uniTraceList=m_uniTraceList, uniFlowTypeList=[flowType], traceCount=m_uniTraceCount, traceList=m_uniTraceList)
            CLASSEDGEList.append(oneClassEdge)
            tmpClassEdgeDict[startClassID] = dict()
            tmpClassEdgeDict[startClassID][endClassID] = classEdgeIndex
            classEdgeIndex += 1
        else:
            if endClassID not in tmpClassEdgeDict:
                oneClassEdge = ClassEdge(startClassID, endClassID, uniTraceCount=m_uniTraceCount, uniTraceList=m_uniTraceList, uniFlowTypeList=[flowType], traceCount=m_uniTraceCount, traceList=m_uniTraceList)
                CLASSEDGEList.append(oneClassEdge)
                tmpClassEdgeDict[startClassID][endClassID] = classEdgeIndex
                classEdgeIndex += 1
            else:
                #modify uniTraceCount and uniTraceList, uniFlowtypeList, traceCount, traceList
                index = tmpClassEdgeDict[startClassID][endClassID]
                #merge and update above
                MergeTraceAttr(index, methodEdgeIndex)
      




def ReadCSV(filename):
    methodIndex = 0
    tmpMethodDict = dict() #dict(methodname) = ID
    methodEdgeIndex = 0
    tmpMethodEdgeDict = dict() #[sD][eID] = edgeID

    with open(filename, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            #print each
            if each[0] == 'traceID':
                continue
            else:
                resultList.append(each)
    return resultList


def ExtractMethods(initList):
    methodIndex = 0
    tmpMethodDict = dict() #dict(methodname) = ID
    methodEdgeIndex = 0
    tmpMethodEdgeDict = dict() #[sD][eID] = edgeID

    for each in initList:
        #print each
        [traceID, order, structtype, startMethodName, endMethodName, m1_para, m2_para, class1, class2] = each
        startLongName = GetLongName(startMethodName, m1_para)
        endLongName = GetLongName(endMethodName, m2_para)
          
        if startLongName not in tmpMethodDict:
            tmpMethodDict[startLongName] = methodIndex
            oneMethod = MethodNode(methodIndex, startLongName)
            METHODList.append(oneMethod)
            methodIndex += 1
            METHOD2ClassDict[startLongName] = class1


        if endLongName not in tmpMethodDict:
            tmpMethodDict[endLongName] = methodIndex
            oneMethod = Method(methodIndex, endLongName)
            METHODList.append(oneMethod)
            methodIndex += 1
            METHOD2ClassDict[endLongName] = class2


        startMethodID = tmpMethodDict[startLongName]
        endMethodID = tmpMethodDict[endLongName]
        if startMethodID not in tmpMethodEdgeDict:
            oneMethodEdge = MethodEdge(startMethodID, endMethodID, uniTraceCount=1, uniTraceList=[traceID], flowType="null")
            METHODEDGEList.append(oneMethodEdge)
            tmpMethodEdgeDict[startMethodID] = dict()
            tmpMethodEdgeDict[startMethodID][endMethodID] = methodEdgeIndex
            methodEdgeIndex += 1
        else:
            if endMethodID not in tmpMethodEdgeDict:
                oneMethodEdge = MethodEdge(startMethodID, endMethodID, uniTraceCount=1, uniTraceList=[traceID], flowType="null")
                METHODEDGEList.append(oneMethodEdge)
                tmpMethodEdgeDict[startMethodID][endMethodID] = methodEdgeIndex
                methodEdgeIndex += 1
            else:
                #modify uniTraceCount and uniTraceList
                index = tmpMethodEdgeDict[startMethodID][endMethodID]
                if traceID in METHODEDGEList[index].uniTraceList:
                    METHODEDGEList[index].uniTraceCount += 1
                    METHODEDGEList[index].uniTraceList.append(traceID)
                #else do nothing


#python pro.py  workflow.csv  shortname or longname
if __name__ == '__main__':
    workflowFilename = sys.argv[1] # ../RS17_source_data/RS17_jpetstore/dynamic/source/jpetstore6_trace_method_workflow.csv
    treeType = sys.argv[2] #shortname or longname

    arr = workflowFilename.split('/')
    tmp = arr.pop()
    project = tmp.split('_')[0]
    outFileNamePre = '/'.join(arr) + '/' + project + '_'

    initList = ReadCSV(workflowFilename)
    ExtractMethods(initList)
    ExtractClasses()

    
