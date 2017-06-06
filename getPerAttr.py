
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
        self.uniTraceList = uniTraceList # it is a string = "1 2 23 44"
        self.flowType = flowType

class ClassNode:
    def __init__(self, ID, className):
        self.ID = ID
        self.className = className

class ClassEdge:
    def __init__(self, startID, endID, uniTraceCount, uniTraceList, uniFlowTypeList, traceCount, traceList):
        self.startID = startID
        self.endID = endID
        self.uniTraceCount = uniTraceCount
        self.uniTraceList = uniTraceList #a tring
        self.uniFlowTypeList = uniFlowTypeList # it is a string
        self.traceCount = traceCount
        self.traceList = traceList #a string, use ' ' to join


# methodname_full.(prafulltype, parafulltype)
def GetLongName(methodName, para):
    if para == '':
        post = '()'
    else:
        post = '(' + para + ')'

    return methodName + post

def GetClassName(methodName):
    return METHOD2ClassDict[methodName]

    
def MergeTraceAttr(classEdgeIndex, methodEdgeIndex):
    startMethodID = METHODEDGEList[methodEdgeIndex].startID
    endMethodID = METHODEDGEList[methodEdgeIndex].endID
    m_uniTraceList = METHODEDGEList[methodEdgeIndex].uniTraceList
    m_uniTraceCount = METHODEDGEList[methodEdgeIndex].uniTraceCount
    flowType = METHODEDGEList[methodEdgeIndex].flowType

    #mergeTraceList and traceCount
    CLASSEDGEList[classEdgeIndex].traceCount += m_uniTraceCount
    if len(CLASSEDGEList[classEdgeIndex].traceList) == 0:
        CLASSEDGEList[classEdgeIndex].traceList =  m_uniTraceList
    else:
        CLASSEDGEList[classEdgeIndex].traceList += (' ' + m_uniTraceList)

    #merge uniTarceList and uniTraceCount, and uniFlowTYpeList
    m_uniTraceList = m_uniTraceList.split(' ')
    for i in range(0, len(m_uniTraceList)):
        traceID = m_uniTraceList[i]
        if IsInListStr(traceID, CLASSEDGEList[classEdgeIndex].uniTraceList) == False:
            CLASSEDGEList[classEdgeIndex].uniTraceList += (' ' + traceID)
            CLASSEDGEList[classEdgeIndex].uniTraceCount += 1
            CLASSEDGEList[classEdgeIndex].uniFlowTypeList += (' ' + flowType)
        #else do nothing



#extrace CLASSList, CLASSEDGEList
def ExtractClasses():
    classIndex = 0
    tmpClassDict = dict()
    classEdgeIndex = 0
    tmpClassEdgeDict=dict()

    for methodEdgeIndex in range(0, len(METHODEDGEList)):
        startMethodID = METHODEDGEList[methodEdgeIndex].startID
        endMethodID = METHODEDGEList[methodEdgeIndex].endID

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
            oneClassEdge = ClassEdge(startClassID, endClassID, uniTraceCount=m_uniTraceCount, uniTraceList=m_uniTraceList, uniFlowTypeList=flowType, traceCount=m_uniTraceCount, traceList=m_uniTraceList)
            CLASSEDGEList.append(oneClassEdge)
            tmpClassEdgeDict[startClassID] = dict()
            tmpClassEdgeDict[startClassID][endClassID] = classEdgeIndex
            classEdgeIndex += 1
        else:
            if endClassID not in tmpClassEdgeDict[startClassID]:
                oneClassEdge = ClassEdge(startClassID, endClassID, uniTraceCount=m_uniTraceCount, uniTraceList=m_uniTraceList, uniFlowTypeList=flowType, traceCount=m_uniTraceCount, traceList=m_uniTraceList)
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
    resultList = list()
    with open(filename, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            #print each
            if each[0] == 'traceID':
                continue
            else:
                resultList.append(each)
    return resultList


def IsInListStr(traceID, listStr):
    oneList = listStr.split(' ')
    if traceID in oneList:
        return True
    else:
        return False

#extrace METHODList, METHOD2ClassDict, METHODEDGEList
def ExtractMethods(initList):
    methodIndex = 0
    tmpMethodDict = dict() #dict(methodname) = ID
    methodEdgeIndex = 0
    tmpMethodEdgeDict = dict() #[sD][eID] = edgeID

    for each in initList:
        #print each
        [traceID, order, structtype, startMethodName, endMethodName, m1_para, m2_para, class1, class2] = each #structype = flowtype???????
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
            oneMethod = MethodNode(methodIndex, endLongName)
            METHODList.append(oneMethod)
            methodIndex += 1
            METHOD2ClassDict[endLongName] = class2


        startMethodID = tmpMethodDict[startLongName]
        endMethodID = tmpMethodDict[endLongName]
        if startMethodID not in tmpMethodEdgeDict:
            oneMethodEdge = MethodEdge(startMethodID, endMethodID, 1, traceID, flowType="null")
            METHODEDGEList.append(oneMethodEdge)
            tmpMethodEdgeDict[startMethodID] = dict()
            tmpMethodEdgeDict[startMethodID][endMethodID] = methodEdgeIndex
            methodEdgeIndex += 1
        else:
            if endMethodID not in tmpMethodEdgeDict[startMethodID]:
                oneMethodEdge = MethodEdge(startMethodID, endMethodID, 1, traceID, flowType="null")
                METHODEDGEList.append(oneMethodEdge)
                tmpMethodEdgeDict[startMethodID][endMethodID] = methodEdgeIndex
                methodEdgeIndex += 1
            else:
                #modify uniTraceCount and uniTraceList
                #print tmpMethodEdgeDict
                #print startMethodID, '    ', endMethodID
                index = tmpMethodEdgeDict[startMethodID][endMethodID]
                if IsInListStr(traceID, METHODEDGEList[index].uniTraceList) == False:
                    METHODEDGEList[index].uniTraceCount += 1
                    METHODEDGEList[index].uniTraceList += (' ' + traceID)




def genMethodDeps(fileName):
    titleList = ['From Method', 'To Method', 'uniTraceCount', 'uniTraceIDList', 'flowType']
   
    import csv
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerow(titleList)
        for edge in METHODEDGEList:
            methodName1 = METHODList[edge.startID].methodName
            methodName2 = METHODList[edge.endID].methodName
            uniTraceCount = str(edge.uniTraceCount)
            uniTraceListStr = edge.uniTraceList
            flowType = edge.flowType
            oneList = [methodName1, methodName2, uniTraceCount, uniTraceListStr, flowType]
            writer.writerow(oneList)

    print fileName

def genClassDeps(fileName):
    titleList = ['From Class', 'To Class', 'uniTraceCount', 'uniTraceIDList', 'uniFlowTypeList', 'traceCount', 'traceList']
   
    import csv
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerow(titleList)
        for edge in CLASSEDGEList:
            className1 = CLASSList[edge.startID].className
            className2 = CLASSList[edge.endID].className
            uniTraceCount = str(edge.uniTraceCount)
            uniTraceListStr = edge.uniTraceList
            uniTypeListStr = edge.uniFlowTypeList
            traceCount = str(edge.traceCount)
            traceListStr = edge.traceList
            oneList = [className1, className2, uniTraceCount, uniTraceListStr, uniTypeListStr, traceCount, traceListStr]
            writer.writerow(oneList)

    print fileName


#python pro.py  workflow.csv 
# it's result is critical influenced by trace_method_workflow.
# class-level workflow_flowing_count
if __name__ == '__main__':
    workflowFilename = sys.argv[1] # ../RS17_source_data/RS17_jpetstore/dynamic/source/jpetstore6_trace_method_workflow.csv

    arr = workflowFilename.split('/')
    tmp = arr.pop()
    project = tmp.split('_')[0]
    outFileName = '/'.join(arr) + '/' + project

    initList = ReadCSV(workflowFilename)
    ExtractMethods(initList)
    ExtractClasses()

    genMethodDeps(outFileName + '_method_workflow_deps.csv')
    genClassDeps(outFileName + '_class_workflow_deps.csv')


    
