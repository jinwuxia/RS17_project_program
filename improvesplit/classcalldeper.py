import sys
import csv

'''
compute the dynamic dependency between classes,
if a class-call-class with one method call pair appear in one trace , it deper=1
if c1:m1->c2:m2 and c1:m3->c2:m4 in one trace, the deper = 2.
dep[c1, c2] not equal dep[c2, c1] in this program.
'''

def readCSV(fileName):
    resList = list()
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            #[traceID, order, stype, callerName, calleeName, m1_para, m2_para, className1, className2, m1_return, m2_return, addweight] = each
            traceID = each[0]
            callerName = each[3]
            calleeName = each[4]
            className1 = each[7]
            className2= each[8]
            if traceID == 'traceID':
                continue
            resList.append([int(traceID), callerName, calleeName, className1, className2])
    return resList

def writeCSV(fileName, alist):
    with open(fileName, "w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)


#input=[[traceID, callerName, calleeName, className1, className2],....]
def computeClassDep(classCallList):
    classEdgeDict = dict() #{class1,class2}=dep
    lastTraceID = -1
    methodEdgeDict = dict()
    for each in classCallList:
        [traceID, callerName, calleeName, className1, className2] = each
        if className1 == className2:
            continue
        if className1 not in classEdgeDict:
            classEdgeDict[className1] = dict()
        if className2 not in classEdgeDict[className1]:
            classEdgeDict[className1][className2] = 0

        if lastTraceID != traceID: #a new trace start, so clear the methodEdgeDict
            methodEdgeDict = dict()
            lastTraceID = traceID
        if callerName not in methodEdgeDict:
            methodEdgeDict[callerName] = dict()
        if calleeName not in methodEdgeDict[callerName]: #only when this call not show in the trace before, we count it.
            methodEdgeDict[callerName][calleeName] = 1
            classEdgeDict[className1][className2] = classEdgeDict[className1][className2] + 1
    return classEdgeDict

#adict[class1][class2] = dep
def transDict2List(aDict):
    aList = list()
    for class1 in aDict:
        for class2 in aDict[class1]:
            dep = aDict[class1][class2]
            aList.append([class1, class2, dep])
    return aList


if __name__ == "__main__":
    workflowFile = sys.argv[1]
    dynamicDepFile = sys.argv[2]
    classCallList = readCSV(workflowFile)
    classEdgeDict = computeClassDep(classCallList)
    classEdgeList = transDict2List(classEdgeDict)
    writeCSV(dynamicDepFile, classEdgeList)
