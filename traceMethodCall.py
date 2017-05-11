import string
import csv


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

    paraStr = getParaType(paraFullStr)
    if paraStr == '':
        methodStr = methodStr + '()'
    else:
        methodStr = methodStr + '(' + paraStr + ')'
    return methodStr
 
def getReturnType(fullstr):
    splitArr = fullstr.split('(')
    fullStr = splitArr[0]            #modifier returntype class.method
    splitArr = fullStr.split(' ')
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

    if methodStr.find('$') == -1 or methodStr.find('class$') != -1: #not include inner class (classname$innnerclassname) or className.class$methodname(0)
        classArr = methodStr.split('.')
        del (classArr[len(classArr) - 1]) #delete  the last ele, that is method name
    elif methodStr.find('$') != -1: #include inneer class ($)
        classArr = methodStr.split('$')
        del (classArr[len(classArr) - 1]) #delete the last ele, that is innerclass.methodname

    className = '.'.join(classArr)
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
    def __init__(self, edgeID, startMethodID, endMethodID):
        self.edgeID = edgeID
        self.startMethodID = startMethodID #caller
        self.endMethodID = endMethodID #callee


class KiekerParser:
    def __init__(self):
        self.methodNodeDict = dict() #Dict{methodname} = methodNodeID
        self.methodNodeList = list() #List[nodeID or index] = MethodNode(nodeID, vmname, label or methodname)
        self.methodEdgeDict = dict() #Dict[calleeID][callerID] = edgeID
        self.methodEdgeList = list() #List[edgeID or index] = MethodEdge(....)

        self.classNodeDict = dict() #Dict{classname} = classID
        self.classNodeList = list() #List[ID or index] = ClassNode(nodeID, vmname, label or methodname)

        self.methodTimeList = list() #list[methidID] =[t1,t2,t3,...]
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
                methodName= getMethodName(tmp[2])
                className = getClassName(tmp[2])
                if isclassIncode(className, prepackage):
                    #Record=[seqID, methodName, sessionID, traceID, timeIn, timeOut, vmname, eoi, ess]
                    record = Record(tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], int(tmp[8]), int(tmp[9]))
                    #update recordList
                    self.recordList.append(record)
        print "record list len = ", len(self.recordList), "......"

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

        #****************process recordlist, to generate sessionList,classNodeDict,classNodeList,methodNodeDict,methodNodeList,methodTimeList
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


    def extractCalls(self, records):
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
        edgeIndex = 0 #urrent index of edge
        self.methodEdgeDict = dict()
        self.methodEdgeList = list()
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
                if self.methodNodeList[callerID].classID != self.methodNodeList[calleeID].classID:
                    iscrossClass = '1'
                else:
                    iscrossClass = '0'


                if calleeID in self.methodEdgeDict:
                    if callerID in self.methodEdgeDict[calleeID]: #just weight++
                        edgeID = self.methodEdgeDict[calleeID][callerID]
                    else: # add a new caller
                        self.methodEdgeDict[calleeID][callerID] = edgeIndex
                        self.methodEdgeList.append(MethodEdge(edgeIndex, callerID, calleeID))
                        edgeIndex += 1
                else: # add a new caller and calle
                    self.methodEdgeDict[calleeID] = dict()
                    self.methodEdgeDict[calleeID][callerID] = edgeIndex
                    self.methodEdgeList.append(MethodEdge(edgeIndex, callerID, calleeID))
                    edgeIndex += 1
            #else:
                #print "%s:   Not found %d, that is no caller " %(records[curr].traceID, records[curr].ess )

            curr += 1

        return self.methodEdgeDict, self.methodEdgeList

    

#each line = m1, m2, m2returntype, m2para, c1, c2
def genMethodCallFile(fileName, nodeList, edgeList):
    print fileName
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerow(['method1', 'method2', 'method2return', 'method2para', 'class1', 'class2'])
        for edge in edgeList:
            startMethodName = nodeList[edge.startMethodID].methodName.split('(')[0]
            endMethodName = nodeList[edge.endMethodID].methodName.split('(')[0]
            oneList = [startMethodName, endMethodName, nodeList[edge.endMethodID].returnType, nodeList[edge.endMethodID].paraTypeListStr, nodeList[edge.startMethodID].className, nodeList[edge.endMethodID].className]
            writer.writerow(oneList)
    

#merge two dict
def addToTotal(totalEdgeDict, totalEdgeList, edgeList):
    edgeIndex = len(totalEdgeList)
    for edge in edgeList:
        if edge.endMethodID  in totalEdgeDict:
            if edge.startMethodID in totalEdgeDict[edge.endMethodID]: #exist, just weight += weight
                totalEdgeID = totalEdgeDict[edge.endMethodID][edge.startMethodID]
            else:
                totalEdgeDict[edge.endMethodID][edge.startMethodID] = edgeIndex
                totalEdgeList.append(MethodEdge(edgeIndex, edge.startMethodID, edge.endMethodID))
                edgeIndex += 1
        else:
            totalEdgeDict[edge.endMethodID] = dict()
            totalEdgeDict[edge.endMethodID][edge.startMethodID] = edgeIndex
            totalEdgeList.append(MethodEdge(edgeIndex, edge.startMethodID, edge.endMethodID))
            edgeIndex += 1

    return totalEdgeDict, totalEdgeList



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



#python tracemethodCall.py  logdir  filteredPrepackage
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3 :
        print "argument is less or more!"
    datadir = sys.argv[1]
    prepackage = sys.argv[2]

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
        RS17name = sys.argv[1].split('/')[len(sys.argv[1].split('/')) - 3]
        projectname = RS17name.split('_')[1]
        fileName = projectname + '_trace_method_call_full.csv'
        
        fileNameDir = sys.argv[1].split('/')
        fileNameDir.pop()

        fileName = '/'.join(fileNameDir) + '/source/' + fileName

        totalMethodEdgeDict = dict()
        totalMethodEdgeList = list()
        for traceID in filteredSessionList[sessionID]:
            recordIDs = filteredSessionList[sessionID][traceID]  #just ID
            #print 'filteresTrace= ', traceID, "recordIDs= ", recordIDs
            records = list()
            for each in recordIDs:
                records.append(myparser.recordList[each])

            (methodEdgeDict, methodEdgeList) = myparser.extractCalls(records) #methodEdgeDict no use if only generate a wholesessionGraph
            (totalMethodEdgeDict, totalMethodEdgeList) = addToTotal(totalMethodEdgeDict, totalMethodEdgeList, methodEdgeList)

        #5. generate method graph for eachsession
        print "methodGraph: numberOfNode= ", len(myparser.methodNodeList), "; numberOfEdge= ", len(totalMethodEdgeList)
        genMethodCallFile(fileName, myparser.methodNodeList, totalMethodEdgeList)

    
