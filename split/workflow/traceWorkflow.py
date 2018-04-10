'''
generate workflow.csv  from keker-log files
'''
import string
import csv
import re


def isclassIncode(className, prepackage):
    if className.startswith(prepackage):
        return True
    else:
        return False



# return methodStr(paralist), this is dynamic and use methodnameDict, so use para to differentiate overload methods
#note the order: delete the paralist first, then split into return type and methosname
def getMethodName(fullStr):
    paraFullStr = fullStr
    splitArr = fullStr.split('(')
    fullStr = splitArr[0]            #modifier returntype class.method
    splitArr = fullStr.split(' ')
    methodStr = splitArr[len(splitArr) - 1]

    if "_$$_jvst" in methodStr:  # mainly for solo270, eg: org.xx.xx_$$_jvst69xxx.get , org.xx.xx_$$_jvst69xxx._3get
        tmp = methodStr.split('.')
        onlyMethodName = tmp[len(tmp) - 1]
        if onlyMethodName.startswith('_'): # delete the pre number
            realIndex = re.search(r'[0-9][a-zA-Z]', onlyMethodName).span()[1] - 1
            onlyMethodName = onlyMethodName[realIndex : len(onlyMethodName)]

        tmp.pop(-1) # delete onlyMethodName
        onlyClassName = '.'.join(tmp)
        if "_$$_jvst" in onlyClassName:
            index = onlyClassName.index('_$$_jvst')
            onlyClassName = onlyClassName[0 : index]
        methodStr = (onlyClassName + '.' + onlyMethodName)


    paraStr = getParaType(paraFullStr)
    if paraStr == '':
        methodStr = methodStr + '()'
    else:
        methodStr = methodStr + '(' + paraStr + ')'
    #print 'XXXX  Fullstr:', fullStr, '  MethodStr:', methodStr
    return methodStr

#modifier returntype class.method
#modifier class.method
def getReturnType(fullstr):
    splitArr = fullstr.split('(')
    fullStr = splitArr[0]            #modifier returntype class.method
    splitArr = fullStr.split(' ')
    if '<init>' in fullStr:          #structor method name donnot have void
        returnType = ''
    else:
        returnType = splitArr[len(splitArr) - 2]
    return returnType

def getParaType(fullstr):
    splitArr = fullstr.split('(')
    paraTmp = splitArr[1].split(')') #paraArr
    if paraTmp[0] == '': #no para
        paraTypeStr = ''
    else:
        paraTypeList = paraTmp[0].split(', ')
        paraTypeStr = ','.join(paraTypeList)
    return paraTypeStr

# return className
def getClassName(fullStr):
    methodStr = fullStr.split('(')[0]
    methodArr = methodStr.split(' ')
    methodStr = methodArr[len(methodArr) - 1]

    if methodStr.find('_$$_jvst') == -1: #is not solo270
        if methodStr.find('$') == -1 or methodStr.find('class$') != -1: #not include inner class (classname$innnerclassname) or className.class$methodname(0)
            classArr = methodStr.split('.')
            del (classArr[len(classArr) - 1]) #delete  the last ele, that is method name
        elif methodStr.find('$') != -1: #include inneer class ($)
            classArr = methodStr.split('$')
            del (classArr[len(classArr) - 1]) #delete the last ele, that is innerclass.methodname

        className = '.'.join(classArr)

    else: #is  solo270
        tmp = methodStr.split('.')
        tmp.pop(-1) # delete onlyMethodName
        onlyClassName = '.'.join(tmp)
        index = onlyClassName.index('_$$_jvst')
        className = onlyClassName[0 : index]
    #print 'XXXXX   Fullstr:', fullStr, 'className', className
    return className


class Record:
    def __init__(self, seqID, methodName, sessionID, traceID, timeIn, timeOut, vmname, eoi, ess):
        self.seqID = seqID
        self.methodName = methodName
        self.sessionID = sessionID
        self.traceID = traceID
        self.timeIn = timeIn
        self.timeOut = timeOut
        self.vmname = vmname
        self.eoi = eoi
        self.ess = ess

class ClassNode:
    def __init__(self, classID, className):
        self.classID = classID
        self.className = className


class MethodNode:
    def __init__(self, methodID, methodName, classID, className, paraTypeListStr, returnType):
        self.methodName = methodName #methodName
        self.methodID = methodID      #methodID
        self.classID = classID
        self.className = className
        self.paraTypeListStr = paraTypeListStr
        self.returnType = returnType

class MethodEdge:
    def __init__(self,startMethodID, endMethodID, structureType, order):
        self.startMethodID = startMethodID #caller
        self.endMethodID = endMethodID #callee
        self.structureType = structureType
        self.order = order


class KiekerParser:
    def __init__(self):
        self.methodNodeDict = dict() #Dict{methodname} = methodNodeID
        self.methodNodeList = list() #List[nodeID or index] = MethodNode(nodeID, vmname, label or methodname)
        self.methodEdgeDict = dict() #Dict[calleeID][callerID] = edgeID
        self.methodEdgeList = list() #List[edgeID or index] = MethodEdge(....)

        self.classNodeDict = dict() #Dict{classname} = classID
        self.classNodeList = list() #List[ID or index] = ClassNode(nodeID, vmname, label or methodname)

        self.recordList = list()
        self.sessionList = dict() # (sessionID, {traceID, recordIDlist[]})


    def firstParse(self, contentList, prepackage):
        #del contentList[0] # #do not process the first record
        for eachLine in contentList:
            #update recordList
            tmp = eachLine.split(";")
            #$6 is OperationExecutionRecord
            if tmp[0] == '$1':
                if tmp[3] == '<no-session-id>':
                    tmp[3] = 'nosessionid'
                else:
                    tmp[3] = "nosessionid"
                className = getClassName(tmp[2])
                if isclassIncode(className, prepackage):
                    #Record=[seqID, methodName, sessionID, traceID, timeIn, timeOut, vmname, eoi, ess]
                    record = Record(tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], int(tmp[8]), int(tmp[9]))
                    #update recordList
                    self.recordList.append(record)
        print "origin: record list len = ", len(self.recordList), "......"

	#begin: sorting records using sequence ID  for slice
        #sort all recordList using sequenceID. beacuse the distributed system logs come from different nodes, so we merge and sort all using sequenceID
        try:
            import operator
        except ImportError:
            cmpfun = lambda x:x.eoi
        else:
            cmpfun = operator.attrgetter("seqID")
        self.recordList.sort(key = cmpfun, reverse = False)
        #end

        #****************process recordlist, to generate sessionList,classNodeDict,classNodeList,methodNodeDict,methodNodeList
        recordIndex = 0
        methodNodeIndex = 0
        classNodeIndex = 0
        for record in self.recordList:
            methodName = getMethodName(record.methodName)
            paraTypeListStr = getParaType(record.methodName)
            returnType = getReturnType(record.methodName)
            className = getClassName(record.methodName)

            #update methodNodeDict and methodNodeList
            if methodName not in self.methodNodeDict:
                self.methodNodeDict[methodName] =  methodNodeIndex

                #update classNodeDict and classNodeList
                if className not in self.classNodeDict:
                    self.classNodeDict[className] = classNodeIndex
                    classNodeIndex += 1
                    oneClassNode = ClassNode(self.classNodeDict[className], className)
                    self.classNodeList.append(oneClassNode)

                oneMethodNode = MethodNode(methodNodeIndex, methodName, self.classNodeDict[className], className, paraTypeListStr, returnType)
                self.methodNodeList.append(oneMethodNode)
                methodNodeIndex += 1
            else:
                methodID = self.methodNodeDict[methodName]

            #update sessionList
            #traceList = a dict  = sesionList[sessionID]
            #recordIDList = a list = sessionList[sessionID][traceID]
            if record.sessionID in self.sessionList:
                if record.traceID in self.sessionList[record.sessionID]:
                    self.sessionList[record.sessionID][record.traceID].append(recordIndex)
                else:
                    self.sessionList[record.sessionID][record.traceID] = list()
                    self.sessionList[record.sessionID][record.traceID].append(recordIndex)
            else:
                self.sessionList[record.sessionID] = dict() #traceList
                self.sessionList[record.sessionID][record.traceID] = list()  #recordList
                self.sessionList[record.sessionID][record.traceID].append(recordIndex)

            recordIndex += 1; #index of record

        #print "XXXXXXXXXXXXXXX", len(self.nodeList)
        #return self.recordList, self.sessionList, self.methodNodeList, self.methodNodeDict, self.classNodeList, self.classNodeDict



    def getTraceLabelAndLen(self, records, prepackage):
        import operator
        cmpfunc = operator.attrgetter('eoi')  # attrgetter('eoi', 'ess')
        records.sort(key = cmpfunc, reverse = False)

        #save the method calling list = [methodID1, methodID2, ...]
        tmpMethodTraces = list()
        tmpTraceLabel = ''
        for eachRecord in records:
            methodName = getMethodName(eachRecord.methodName)
            methodID = self.methodNodeDict[methodName]
            className = getClassName(eachRecord.methodName)

            if isclassIncode(className, prepackage):
                tmpMethodTraces.append(methodName)
                tmpTraceLabel += (str(methodID) + '_')

        return tmpTraceLabel, len(tmpMethodTraces)


    def extractWorkFlow(self, records):
        #order records using eoi
        try:
            import operator
        except ImportError:
            cmpfun = lambda x:x.eoi
        else:
            cmpfun = operator.attrgetter("eoi")
        records.sort(key = cmpfun, reverse = False)

        #print "sorted List end............\n"

        if len(records) < 2:
            return self.methodEdgeDict, self.methodEdgeList

        #tranverse each oderedrecords
        essDict=dict()
        curr = 0   # current index of record
        order = 0 #urrent index of edge
        self.methodEdgeList = list() #include repetive edge
        while curr < len(records):
            #print curr, len(records)
            #update essDict dict[ess]=recordID
            essDict[records[curr].ess] = curr
            #print essDict

            if records[curr].eoi == 0: #main
                curr += 1
                continue

            if (records[curr].ess - 1) in essDict:
                callerIndex = essDict[records[curr].ess - 1]

                callerRecord = records[callerIndex] #caller is a trace or record
                calleeRecord = records[curr] #callee is a trace or record
                callerMethodName = getMethodName(callerRecord.methodName)
                calleeMethodName = getMethodName(calleeRecord.methodName)
                callerID = self.methodNodeDict[callerMethodName]
                calleeID = self.methodNodeDict[calleeMethodName]

                self.methodEdgeList.append( MethodEdge(callerID, calleeID, "null", order) )
                order += 1

            #else:
                #print "%s:   Not found %d, that is no caller " %(records[curr].traceID, records[curr].ess )

            curr += 1

        return self.methodEdgeList


    def mergeEdgeList(self, traceIndex, methodEdgeList, mergedEdgeList):
        for edge in methodEdgeList:
            startMethodName = self.methodNodeList[edge.startMethodID].methodName.split('(')[0]
            endMethodName = self.methodNodeList[edge.endMethodID].methodName.split('(')[0]
            oneList = [traceIndex, edge.order, edge.structureType, startMethodName, endMethodName,  self.methodNodeList[edge.startMethodID].paraTypeListStr, self.methodNodeList[edge.endMethodID].paraTypeListStr,  self.methodNodeList[edge.startMethodID].className, self.methodNodeList[edge.endMethodID].className, self.methodNodeList[edge.startMethodID].returnType, self.methodNodeList[edge.endMethodID].returnType ]
            mergedEdgeList.append(oneList)

        return mergedEdgeList


def genFile(fileName,  edgeList):
    print fileName
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerow(['traceID', 'order', 'structtype', 'method1', 'method2', 'm1_para', 'm2_para',  'class1', 'class2', 'm1_return', 'm2_return'])
        writer.writerows(edgeList)


#find all data file in this folder
def findAllDataFileContent(dir):
    from os import walk
    fileList=[]
    for (dirpath, dirnames, filenames) in walk(dir):
    	for name in filenames:
    	    if name.startswith('kieker-') and name.endswith('.dat'):
    		f = dirpath + '/' + name
    		fileList.append(f)
                print f
    totalContentList = list()
    for eachfile in fileList:
        with open(eachfile, "r") as fp:
            contentList = fp.readlines()
        totalContentList += contentList #merge towo list
    return totalContentList



#python pro.py  logdir   outworkflow.csv  filteredPrepackage
#generate workflow.csv
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4 :
        print "argument is less or more!"
    datadir = sys.argv[1]
    fileName = sys.argv[2]
    prepackage = sys.argv[3]

    #1 2.first parse, init methodNode and classNode
    totalContentList = findAllDataFileContent(datadir)
    myparser = KiekerParser()
    myparser.firstParse(totalContentList, prepackage) #generate recordlist,sessionlist,methodDict,methodList,classDict,classList,timeList

    #3 use tracelable to filter out non-duplicated sesionID-traceID-records
    traceLabelDict = dict()
    filteredSessionList = dict()
    for sessionID in myparser.sessionList:
        for traceID in myparser.sessionList[sessionID]:
            recordIDs = myparser.sessionList[sessionID][traceID]  #just ID
            records = list()
            for each in recordIDs:
                records.append(myparser.recordList[each])

            [traceLabel, traceLen] = myparser.getTraceLabelAndLen(records, prepackage)
            if traceLen > 1 and ( traceLabel not in traceLabelDict):
                traceLabelDict[traceLabel] = 1
                if sessionID not in filteredSessionList:
                    filteredSessionList[sessionID] = dict()
                    filteredSessionList[sessionID][traceID] = myparser.sessionList[sessionID][traceID]
                else:
                    filteredSessionList[sessionID][traceID] = myparser.sessionList[sessionID][traceID]

    print "filtered out trace number= ", len(traceLabelDict)

    #4 second parse: init methodEdge, extrace methodGraph
    for sessionID in filteredSessionList:
        #fileName = sys.argv[1] + sessionID + "method.edge"
        """
        RS17name = sys.argv[1].split('/')[len(sys.argv[1].split('/')) - 3]
        projectname = RS17name.split('_')[1]
        fileName = projectname + '_trace_method_workflow_1.csv'

        fileNameDir = sys.argv[1].split('/')
        fileNameDir.pop()

        fileName = '/'.join(fileNameDir) + '/source/' + fileName
        """
        #fileName = "workflow.csv"
        traceIndex = 0
        mergedEdgeList = list()
        for traceID in filteredSessionList[sessionID]:
            recordIDs = filteredSessionList[sessionID][traceID]  #just ID
            #print 'filteresTrace= ', traceID, "recordIDs= ", recordIDs
            records = list()
            for each in recordIDs:
                records.append(myparser.recordList[each])

            methodEdgeList = myparser.extractWorkFlow(records) #methodEdgeList has repetive edge, so they are workflows
            #print 'traceIndex=', traceIndex, 'methodEdgeList=', methodEdgeList
            if len(methodEdgeList) != 0:
                mergedEdgeList = myparser.mergeEdgeList(traceIndex, methodEdgeList, mergedEdgeList)
                traceIndex += 1

        genFile(fileName, mergedEdgeList)
