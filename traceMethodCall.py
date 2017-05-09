import string
import csv




def isclassIncode(className):
    if className.startswith('com.ibatis.jpetstore'):
        return True
    else:
        return False

#note the order: delete the paralist first, then split into return type and methosname
def getMethodAndPara(fullStr):
    splitArr = fullStr.split('(')
    fullStr = splitArr[0]            #modifier returntype class.method
    paraTmp = splitArr[1].split(')') #paraArr
    splitArr = fullStr.split(' ')
    methodStr = splitArr[len(splitArr) - 1]
    if paraTmp[0] == '': #no para
        paraTypeList = list()
        methodStr = methodStr + '()'
    else:
        paraTypeList = paraTmp[0].split(', ')
        methodStr = methodStr + '(' + ','.join(paraTypeList) + ')'

    #print 'full=', fullStr, '; methodStr=', methodStr, '; paraTypeList=', paraTypeList
    return methodStr, paraTypeList

# return className
def getClassName(methodName):
    methodStr = methodName.split('(')[0]
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


#Note: infoCount  is just len(paraList)+1
def getOtherInfoFromRecord(record):
    [methodName, paraTypeList] = getMethodAndPara(record.methodName)
    time = long(record.timeOut) - long(record.timeIn)
    infoCount = len(paraTypeList) + 1
    return time,infoCount



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
    def __init__(self, vmname, classID, className):
        self.vmname = vmname
        self.classID = classID
        self.className = className

class ClassEdge:
    def __init__(self, edgeID, startClassID, endClassID, commuCost):
        self.edgeID = edgeID
        self.startClassID = startClassID
        self.endClassID = endClassID
        self.commuCost = commuCost #sum(cross-method edge's infoCount)

class MethodNode:
    def __init__(self,vmname, methodID, methodName, classID, className, executionTimeAvg, executionTimeVar, paralen, infoCount, paraTypeList):
        self.vmname = vmname
        self.methodName = methodName #methodName
        self.methodID = methodID      #methodID
        self.classID = classID
        self.className = className
        self.executionTimeAvg = executionTimeAvg
        self.executionTimeVar = executionTimeVar
        self.paralen = paralen
        self.infoCount = infoCount
        self.paraTypeList = paraTypeList

class MethodEdge:
    def __init__(self, edgeID, startMethodID, endMethodID, iscrossClass, freq, commuCost):
        self.edgeID = edgeID
        self.startMethodID = startMethodID #caller
        self.endMethodID = endMethodID #callee
        self.iscrossClass = iscrossClass #label = 0, intra edge in one class; label = 1, edge across class
        self.freq = freq
        self.commuCost = commuCost #cost=sum(callee's infocount * freq)


class KiekerParser:
    def __init__(self):
        self.methodNodeDict = dict() #Dict{methodname} = methodNodeID
        self.methodNodeList = list() #List[nodeID or index] = MethodNode(nodeID, vmname, label or methodname)
        self.methodEdgeDict = dict() #Dict[calleeID][callerID] = edgeID
        self.methodEdgeList = list() #List[edgeID or index] = MethodEdge(....)

        self.classNodeDict = dict() #Dict{classname} = classID
        self.classNodeList = list() #List[ID or index] = ClassNode(nodeID, vmname, label or methodname)
        self.classEdgeDict = dict() #Dict[StartClassID][endClassID] = edgeID
        self.classEdgeList = list() #List[edgeID or index] = ClassEdge(....)

        self.methodTimeList = list() #list[methidID] =[t1,t2,t3,...]
        self.recordList = list()
        self.sessionList = dict() # (sessionID, {traceID, recordIDlist[]})


    def firstParse(self, contentList):
        #del contentList[0] # #do not process the first record
        for eachLine in contentList:
            #update recordList
            tmp = eachLine.split(";")
            #$6 is OperationExecutionRecord
            if tmp[0] == '$1':
                if tmp[3] == '<no-session-id>':
                    tmp[3] = 'nosessionid'
                [methodName, paraTypeList] = getMethodAndPara(tmp[2])
                className = getClassName(methodName)
                if isclassIncode(className):
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
            [methodName, paraTypeList] = getMethodAndPara(record.methodName)
            className = getClassName(methodName)

            #update methodNodeDict and methodNodeList
            if methodName not in self.methodNodeDict:
                self.methodNodeDict[methodName] =  methodNodeIndex
                [time, infoCount] = getOtherInfoFromRecord(record)

                #update classNodeDict and classNodeList
                if className not in self.classNodeDict:
                    self.classNodeDict[className] = classNodeIndex
                    classNodeIndex += 1
                    oneClassNode = ClassNode(record.vmname, self.classNodeDict[className], className)
                    self.classNodeList.append(oneClassNode)

                oneMethodNode = MethodNode(record.vmname, methodNodeIndex, methodName, self.classNodeDict[className], className, 0, 0, len(paraTypeList), infoCount, paraTypeList)
                self.methodNodeList.append(oneMethodNode)
                self.methodTimeList.append(list())
                self.methodTimeList[methodNodeIndex].append(time)    #methodTimeList[methodId] =[t1,t2,t3...]
                methodNodeIndex += 1
            else:
                methodID = self.methodNodeDict[methodName]
                self.methodTimeList[methodID].append(time)

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


    def setMethodTimeAvgVar(self):
        for methodID in range(len(self.methodNodeList)):
            timeList = self.methodTimeList[methodID]
            import numpy as np
            self.methodNodeList[methodID].executionTimeAvg = np.mean(timeList)
            self.methodNodeList[methodID].executionTimeVar = np.var(timeList)

        #after calculation, clear timeList
        self.methodTimeList = list()


    def getTraceLabelAndLen(self, records):
        import operator
        cmpfunc = operator.attrgetter('eoi')  # attrgetter('eoi', 'ess')
        records.sort(key = cmpfunc, reverse = False)

        #save the method calling list = [methodID1, methodID2, ...]
        tmpMethodTraces = list()
        tmpTraceLabel = ''
        for eachRecord in records:
            [methodName, paraTypeList] = getMethodAndPara(eachRecord.methodName)
            methodID = self.methodNodeDict[methodName]
            className = getClassName(methodName)

            if isclassIncode(className):
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
        #for each in records:
        #    print each.sessionID, " ", each.traceID," ", each.methodName," ", each.timeIn, " ", each.timeOut, " ", str(each.eoi), " ", str(each.ess),"\n" 
        
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
                [callerMethodName, tmp] = getMethodAndPara(callerRecord.methodName)
                [calleeMethodName, tmp] = getMethodAndPara(calleeRecord.methodName)
                callerID = self.methodNodeDict[callerMethodName]
                calleeID = self.methodNodeDict[calleeMethodName]
                if self.methodNodeList[callerID].classID != self.methodNodeList[calleeID].classID:
                    iscrossClass = '1'
                else:
                    iscrossClass = '0'


                if calleeID in self.methodEdgeDict:
                    if callerID in self.methodEdgeDict[calleeID]: #just weight++
                        edgeID = self.methodEdgeDict[calleeID][callerID]
                        self.methodEdgeList[edgeID].freq += 1
                    else: # add a new caller
                        self.methodEdgeDict[calleeID][callerID] = edgeIndex
                        self.methodEdgeList.append(MethodEdge(edgeIndex, callerID, calleeID, iscrossClass, freq=1, commuCost=0))
                        edgeIndex += 1
                else: # add a new caller and calle
                    self.methodEdgeDict[calleeID] = dict()
                    self.methodEdgeDict[calleeID][callerID] = edgeIndex
                    self.methodEdgeList.append(MethodEdge(edgeIndex, callerID, calleeID, iscrossClass, freq=1, commuCost=0))
                    edgeIndex += 1
            #else:
                #print "%s:   Not found %d, that is no caller " %(records[curr].traceID, records[curr].ess )

            curr += 1

        return self.methodEdgeDict, self.methodEdgeList

    
    def setMethodEdgeCommuCost(self, edgeList):
        for edgeID in range(len(edgeList)):
            endMethodID = edgeList[edgeID].endMethodID
            freq = edgeList[edgeID].freq
            passInfoCount = self.methodNodeList[endMethodID].infoCount
            edgeList[edgeID].commuCost = freq * passInfoCount
        return edgeList

    def extractClassEdge(self, methodEdgeList):
        classEdgeIndex = 0
        classEdgeDict = dict()
        classEdgeList = list()
        for methodEdge in methodEdgeList:
            callerMethodID = methodEdge.startMethodID
            calleeMethodID = methodEdge.endMethodID
            iscrossClass = methodEdge.iscrossClass
            commuCost = methodEdge.commuCost
            
            if iscrossClass == '1':
                callerClassID = self.methodNodeList[callerMethodID].classID
                calleeClassID = self.methodNodeList[calleeMethodID].classID
                if calleeClassID in classEdgeDict:
                    if callerClassID in classEdgeDict[calleeClassID]: #just accumulation weight
                        classEdgeIndex = classEdgeDict[calleeClassID][callerClassID]
                        classEdgeList[classEdgeIndex].commuCost += commuCost
                    else:
                        classEdgeDict[calleeClassID][callerClassID] = classEdgeIndex
                        classEdgeList.append( ClassEdge(classEdgeIndex, callerClassID, calleeClassID, commuCost) )
                        classEdgeIndex += 1
                else:
                    classEdgeDict[calleeClassID] = dict()
                    classEdgeDict[calleeClassID][callerClassID] = classEdgeIndex
                    classEdgeList.append( ClassEdge(classEdgeIndex, callerClassID, calleeClassID, commuCost) )
                    classEdgeIndex += 1

        return classEdgeList
    #end Parser class

def genClassDeps(fileName, nodeList, edgeList):
    resList = list()
    resList.append(['From Class', 'To Class', 'CommuCost'])
    for edge in edgeList:
        startClassName = nodeList[edge.startClassID].className
        endClassName = nodeList[edge.endClassID].className
        commuCost = edge.commuCost
        resList.append([startClassName, endClassName, commuCost])
    
    import csv
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerows(resList)
    print fileName




def genClassGraphFileGexf(fileName, nodeList, edgeList):
    import networkx as nx
    DG = nx.DiGraph()
    for node in nodeList:
        DG.add_node(node.classID, label=node.className, vmname=node.vmname)
    for edge in edgeList:
        DG.add_edge(edge.startClassID, edge.endClassID, commuCost=edge.commuCost)
    print fileName
    nx.write_gexf(DG, fileName)

def genClassGraphFileIgraph(nodeFileName, edgeFileName, nodeList, edgeList):
    print nodeFileName, edgeFileName
    nodeFp = open(nodeFileName, "w")
    edgeFp = open(edgeFileName, "w")
    for node in nodeList:
        nodeFp.write(str(node.classID) + ";"+ node.vmname + ";" + node.className + "\n")
    nodeFp.close()
    for edge in edgeList:
        edgeFp.write(str(edge.startClassID) + ";" + str(edge.endClassID) + ";" + str(edge.commuCost) + "\n")
    edgeFp.close()

def genMethodGraphFileGexf(outfileName, nodeList, edgeList):
    import networkx as nx
    DG = nx.DiGraph()
    for node in nodeList:
        DG.add_node(node.methodID, label=node.methodName, classID=node.classID, className=node.className, vmname=node.vmname, paralen=node.paralen, infoCount=node.infoCount, paraTypeStr=','.join(node.paraTypeList))
        #DG.add_node(node.methodID, label=node.methodName, classID=node.classID, className=node.className, vmname=node.vmname, timeAvg=node.executionTimeAvg, timeVar=node.executionTimeVar, paralen=node.paralen, infoCount=node.infoCount, paraTypeStr=','.join(node.paraTypeList))
    for edge in edgeList:
        DG.add_edge(edge.startMethodID, edge.endMethodID, freq=edge.freq, iscrossClass=edge.iscrossClass, commuCost=edge.commuCost)
    print outfileName
    nx.write_gexf(DG, outfileName)

def genMethodGraphFileIgraph(nodeFileName, edgeFileName, nodeList, edgeList):
    print nodeFileName, edgeFileName
    nodeFp = open(nodeFileName, "w")
    edgeFp = open(edgeFileName, "w")
    for node in nodeList:
        nodeFp.write(str(node.methodID) + ";"+ node.vmname + ";" + node.methodName + ";" + str(node.classID) + ";" + node.className + ";" + str(node.executionTimeAvg) + ";" + str(node.executionTimeVar) + ";" + str(node.paralen) + ";" + str(node.infoCount) + ";" + ','.join(node.paraTypeList) + "\n")
    nodeFp.close()
    for edge in edgeList:
        #print edge.startNodeID + edge.endNodeID, edge.iscross, edge.weight
        edgeFp.write(str(edge.startMethodID) + ";" + str(edge.endMethodID) + ";" + edge.iscrossClass + ";" + str(edge.freq)  + ";" + str(edge.commuCost) + "\n")
    edgeFp.close()

#merge two dict
def addToTotal(totalEdgeDict, totalEdgeList, edgeList):
    edgeIndex = len(totalEdgeList)
    for edge in edgeList:
        if edge.endMethodID  in totalEdgeDict:
            if edge.startMethodID in totalEdgeDict[edge.endMethodID]: #exist, just weight += weight
                totalEdgeID = totalEdgeDict[edge.endMethodID][edge.startMethodID]
                totalEdgeList[totalEdgeID].freq += edge.freq
            else:
                totalEdgeDict[edge.endMethodID][edge.startMethodID] = edgeIndex
                totalEdgeList.append(MethodEdge(edgeIndex, edge.startMethodID, edge.endMethodID, edge.iscrossClass, edge.freq, edge.commuCost))
                edgeIndex += 1
        else:
            totalEdgeDict[edge.endMethodID] = dict()
            totalEdgeDict[edge.endMethodID][edge.startMethodID] = edgeIndex
            totalEdgeList.append(MethodEdge(edgeIndex, edge.startMethodID, edge.endMethodID, edge.iscrossClass, edge.freq, edge.commuCost))
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




if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2 :
        print "argument is less or more!"
    datadir = sys.argv[1]

    #1 2.first parse, init methodNode and classNode
    totalContentList = findAllDataFileContent(datadir)
    myparser = KiekerParser()
    myparser.firstParse(totalContentList) #generate recordlist,sessionlist,methodDict,methodList,classDict,classList,timeList
    myparser.setMethodTimeAvgVar()   #add timeVar, timeAvg to each methodNode

    #3 use tracelable to filter out non-duplicated sesionID-traceID-records
    traceLabelDict = dict()
    filteredSessionList = dict()
    for sessionID in myparser.sessionList:
        for traceID in myparser.sessionList[sessionID]:
            recordIDs = myparser.sessionList[sessionID][traceID]  #just ID
            records = list()
            for each in recordIDs:
                records.append(myparser.recordList[each])

            [traceLabel, traceLen] = myparser.getTraceLabelAndLen(records)
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
        methodFileNameGexf = sys.argv[1] + sessionID + "method.gexf"
        methodNodeFileName = sys.argv[1] + sessionID + "method.node"
        methodEdgeFileName = sys.argv[1] + sessionID + "method.edge"

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
        #update edge.commuCost for totalEdgeList 
        totalMethodEdgeList = myparser.setMethodEdgeCommuCost(totalMethodEdgeList)

        #5. generate method graph for eachsession
        print "methodGraph: numberOfNode= ", len(myparser.methodNodeList), "; numberOfEdge= ", len(totalMethodEdgeList)
        genMethodGraphFileGexf(methodFileNameGexf, myparser.methodNodeList, totalMethodEdgeList)
        genMethodGraphFileIgraph(methodNodeFileName, methodEdgeFileName, myparser.methodNodeList, totalMethodEdgeList)

    

    #6 generate classEdgeDict and claddEdgeList, write into file
    classEdgeList = myparser.extractClassEdge(totalMethodEdgeList)
    print "ClassGraph: numberOfNode= ", len(myparser.classNodeList), "; numberOfEdge= ", len(classEdgeList)
    classFileNameGexf = sys.argv[1] + 'class.gexf'
    classNodeFileName = sys.argv[1] + 'class.node'
    classEdgeFileName = sys.argv[1] + 'class.edge'
    classDepsFileName = sys.argv[1] + '_commmuclassdeps.csv'
    genClassGraphFileGexf(classFileNameGexf, myparser.classNodeList, classEdgeList)
    genClassGraphFileIgraph(classNodeFileName, classEdgeFileName, myparser.classNodeList, classEdgeList)
    genClassDeps(classDepsFileName, myparser.classNodeList, classEdgeList)


