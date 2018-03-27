'''
extract communication cost between classes from workflow.csv
'''
import sys
import csv

METHODDict = dict() #dict[methodName] = methodID
CLASSDict = dict()  #dict[className] = classID
CLASSID2NAMEDict = dict() #dict[classID] = className
METHODEdgeDict = dict()  # dict[mid1][mid2] = edgeIndex
METHODEdgeList = list()  # list[edgeIndex] = MethodEdge(.)

class MethodEdge:
    def __init__(self, callerID, calleeID, para2List, return2Str):
        self.callerID = callerID
        self.calleeID = calleeID
        self.para2List = para2List
        self.return2Str = return2Str
'''
class ComCost:
    def __int__(self, className1, className2, call, para_num, ret_num, call_freq, para_num_freq, ret_num_freq, total, total_freq):
        self.className1 = className1
        self.className2 = className2
        self.call = call
        self.para_num = para_num
        self.ret_num = ret_num
        self.call_freq = call_freq
        self.para_num_freq = para_num_freq
        self.ret_num_freq = ret_num_freq
        self.total = total
        self.total_freq = total_freq
'''

def readCSV(fileName):
    methodDict = dict()
    classDict = dict()
    classID2NameDict = dict()
    resList = list()
    methodIndex = 0
    classIndex = 0
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [traceID, order, stype, callerName, calleeName, m1_para, m2_para, className1, className2, m1_return, m2_return] = each
            if traceID == 'traceID':
                continue
            callerName = callerName + '(' + m1_para + ')'
            calleeName = calleeName + '(' + m2_para + ')'
            if callerName  not in methodDict:
                methodDict[callerName] = methodIndex
                methodIndex += 1
            if calleeName not in methodDict:
                methodDict[calleeName] = methodIndex
                methodIndex += 1
            if className1 not in classDict:
                classDict[className1] = classIndex
                classID2NameDict[classIndex] = className1
                classIndex += 1
            if className2 not in classDict:
                classDict[className2] = classIndex
                classID2NameDict[classIndex] = className2
                classIndex += 1
            tmp = [ methodDict[callerName], methodDict[calleeName], m2_para, m2_return , classDict[className1], classDict[className2]]
            resList.append(tmp)
    return methodDict, classDict, classID2NameDict, resList

def getParalist(m2_para):
    arr = m2_para.split(',')
    if arr[0] == '':
        m2_para = list()
    else:
        m2_para = arr
    return m2_para

def genMethodEdge(initList):
    methodEdgeDict = dict()   #edgeDict[m1ID][m2ID] = edgeIndex
    methodEdgeList = list()   #[index1] = MethodEdge()

    methodEdgeIndex = 0
    for each in initList:
        #methodedge
        [methodID1, methodID2, m2_para, m2_return, classID1, classID2] = each
        m2_paraList = getParalist(m2_para)
        if methodID1 not in methodEdgeDict:
            oneEdge = MethodEdge(methodID1, methodID2, m2_paraList, m2_return)
            methodEdgeList.append(oneEdge)
            methodEdgeDict[methodID1] = dict()
            methodEdgeDict[methodID1][methodID2] = methodEdgeIndex
            methodEdgeIndex += 1
        else:
            if methodID2 not in methodEdgeDict[methodID1]:
                oneEdge = MethodEdge(methodID1, methodID2, m2_paraList, m2_return)
                methodEdgeList.append(oneEdge)
                methodEdgeDict[methodID1][methodID2] = methodEdgeIndex
                methodEdgeIndex += 1
    return methodEdgeDict, methodEdgeList

# include method1 from method method2 within a same class
def process(initList):
    classEdgeDict = dict()    #dict[c1ID][c2ID] = [MethodEdge1: freq1, MethodEdge2:freq2, ...]
    for each in initList:
        #methodedge
        [methodID1, methodID2, m2_para, m2_return, classID1, classID2] = each
        #add into classEdge
        currEdgeIndex = METHODEdgeDict[methodID1][methodID2]
        if classID1 not in classEdgeDict:  #dict[c1ID][c2ID] = [MethodEdge1: freq1, MethodEdge2:freq2, ...]
            classEdgeDict[classID1] = dict()
            classEdgeDict[classID1][classID2] = dict()
            classEdgeDict[classID1][classID2][currEdgeIndex] = 1
        else:
            if classID2 not in classEdgeDict[classID1]:
                classEdgeDict[classID1][classID2] = dict()
                classEdgeDict[classID1][classID2][currEdgeIndex] = 1
            else:
                if currEdgeIndex not in classEdgeDict[classID1][classID2]:
                    classEdgeDict[classID1][classID2][currEdgeIndex] = 1
                else:
                    classEdgeDict[classID1][classID2][currEdgeIndex] += 1
    return classEdgeDict


#dict[c1ID][c2ID] = [MethodEdge1: freq1, MethodEdge2:freq2, ...]
#NOTICE:  exclude class to class within itself
def formatProcess(classEdgeDict):
    resList = list()
    for classID1 in classEdgeDict:
        for classID2 in classEdgeDict[classID1]:
            if classID2 == classID1:  #NOTICE:  exclude class to class within itself
                continue
            sum_call = 0
            sum_call_freq = 0
            sum_para_num = 0
            sum_para_num_freq = 0
            sum_ret_num = 0
            sum_ret_num_freq = 0
            for methodEdgeIndex in classEdgeDict[classID1][classID2]:
                freq = classEdgeDict[classID1][classID2][methodEdgeIndex]
                para_num = len(METHODEdgeList[methodEdgeIndex].para2List)
                if METHODEdgeList[methodEdgeIndex].return2Str == '':
                    ret_num = 0
                else:
                    ret_num = 1
                para_num_freq = para_num * freq
                ret_num_freq = ret_num * freq
                sum_call += 1
                sum_call_freq += freq
                sum_para_num += para_num
                sum_para_num_freq += para_num_freq
                sum_ret_num += ret_num
                sum_ret_num_freq += ret_num_freq
            total =  sum_ret_num + sum_para_num
            total_freq = sum_ret_num_freq + sum_para_num_freq
            className1 = CLASSID2NAMEDict[classID1]
            className2 = CLASSID2NAMEDict[classID2]
            oneList = [className1, className2, sum_call, sum_para_num, sum_ret_num, sum_call_freq, sum_para_num_freq, sum_ret_num_freq, total, total_freq]
            resList.append(oneList)
    return resList


def writeCSV(listlist, fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerow(['className1', 'className2', 'call', 'p_num', 'r_num', 'call_f', 'p_num_f', 'r_num_f', 'total', 'total_f'])
        writer.writerows(listlist)
    print fileName


#python pro.py  workflow.csv   outfile.csv
if __name__ == '__main__':
    workflowFileName = sys.argv[1]
    outfileName = sys.argv[2]

    [METHODDict, CLASSDict, CLASSID2NAMEDict, initEdgeList] = readCSV(workflowFileName)
    [METHODEdgeDict, METHODEdgeList] = genMethodEdge(initEdgeList)

    #dict[c1ID][c2ID] = [MethodEdge1: freq1, MethodEdge2:freq2, ...]
    classEdgeDict = process(initEdgeList)
    resultList = formatProcess(classEdgeDict)
    writeCSV(resultList, outfileName)
