import string
import csv



def IsClassInCode(className, filterClassPre):
    if className.startswith(filterClassPre):
        return True
    else:
        return False

#note the order: delete the paralist first, then split into return type and methosname
def GetMethodAndPara(fullStr):
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
def GetClassName(methodName):
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

#return microsecond = 10(-6) second
def GetTimeFromRecord(record):
    time = long(record.timeOut) - long(record.timeIn)
    us = float(time) / float(1000)
    return us


#Note: infoCount  is just len(paraList)+1
def GetInfoCountFromRecord(record):
    [methodName, paraTypeList] = GetMethodAndPara(record.methodName)
    infoCount = len(paraTypeList) + 1
    return infoCount



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


class MethodNode:
    def __init__(self, methodID, methodName, className,  executionTimeAvg, executionTimeVar, infoCount):
        self.methodName = methodName #methodName
        self.methodID = methodID      #methodID
        self.className = className
        self.executionTimeAvg = executionTimeAvg
        self.executionTimeVar = executionTimeVar
        self.infoCount = infoCount



class KiekerParser:
    def __init__(self):
        self.methodNodeDict = dict() #Dict{methodname} = methodNodeID
        self.methodNodeList = list() #List[nodeID or index] = MethodNode(nodeID, vmname, label or methodname)

        self.methodTimeList = list() #list[methidID] =[t1,t2,t3,...]
        self.recordList = list()


    def FirstParse(self, contentList, filterClass):
        #del contentList[0] # #do not process the first record
        for eachLine in contentList:
            #update recordList
            tmp = eachLine.split(";")
            #$6 is OperationExecutionRecord
            if tmp[0] == '$1':
                if tmp[3] == '<no-session-id>':
                    tmp[3] = 'nosessionid'
                [methodName, paraTypeList] = GetMethodAndPara(tmp[2])
                className = GetClassName(methodName)
                if IsClassInCode(className, filterClass):
                    #Record=[seqID, methodName, sessionID, traceID, timeIn, timeOut, vmname, eoi, ess]
                    record = Record(tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], int(tmp[8]), int(tmp[9]))
                    #update recordList
                    self.recordList.append(record)
        #print "record list len = ", len(self.recordList), "......"

        recordIndex = 0
        methodNodeIndex = 0
        for record in self.recordList:
            [methodName, paraTypeList] = GetMethodAndPara(record.methodName)

            #update methodNodeDict and methodNodeList
            ustime = GetTimeFromRecord(record) 
            infoCount = GetInfoCountFromRecord(record)
            className = GetClassName(methodName)

            if methodName not in self.methodNodeDict:
                self.methodNodeDict[methodName] =  methodNodeIndex
                oneMethodNode = MethodNode(methodNodeIndex, methodName, className,  0, 0, infoCount)
                self.methodNodeList.append(oneMethodNode)
                self.methodTimeList.append(list())
                self.methodTimeList[methodNodeIndex].append(ustime)    #methodTimeList[methodId] =[t1,t2,t3...]
                methodNodeIndex += 1
            else:
                methodID = self.methodNodeDict[methodName]
                self.methodTimeList[methodID].append(ustime)

    def SetMethodTimeAttr(self):
        for methodID in range(len(self.methodNodeList)):
            timeList = self.methodTimeList[methodID]
            import numpy as np
            self.methodNodeList[methodID].executionTimeAvg = np.mean(timeList)
            self.methodNodeList[methodID].executionTimeVar = np.var(timeList)


def WriteTimeFile(fileName,  methodNodeList):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp, delimiter=",")
        for node in methodNodeList:
            writer.writerow([str(node.methodID),  node.methodName, node.className, "%.2f" % node.executionTimeAvg,  "%.2f" % node.executionTimeVar, str(node.infoCount)] )



#find all data file in this folder
def FindAllDataFileContent(dir):
    from os import walk
    fileList=[]
    for (dirpath, dirnames, filenames) in walk(dir):
    	for name in filenames:
    	    if name.startswith('kieker-') and name.endswith('.dat'):
    		f = dirpath + '/' + name
    		fileList.append(f)
            #print f
    totalContentList = list()
    for eachfile in fileList:
        with open(eachfile, "r") as fp:
            contentList = fp.readlines()
        totalContentList += contentList #merge towo list
    return totalContentList




if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3 :
        print "argument is less or more!"
    datadir = sys.argv[1]
    filterClass = sys.argv[2]

    totalContentList = FindAllDataFileContent(datadir)
    myparser = KiekerParser()
    myparser.FirstParse(totalContentList, filterClass) #generate recordlist,sessionlist,methodDict,methodList,classDict,classList,timeList
    myparser.SetMethodTimeAttr()   #add timeVar, timeAvg to each methodNode
    
    fileName = "timeList.csv"
    print fileName
    WriteTimeFile(fileName, myparser.methodNodeList)


