import sys
import csv

#resList[traceID] = [ [list1][list2][list3] ]

def readMapFile(fileName):
    idDict = dict() #[oldID] = newID
    with open(fileName,'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [newID, oldID] = each
            if newID == 'newTrace':
                continue
            idDict[int(oldID)] = int(newID)
    return idDict

def filterCSV(idDict, fileName):
    resDict = dict()#[traceID] = onelineList
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [oldTraceID, order, structtype, method1, method2, m1_para, m2_para, className1, className2, m1_return, m2_return] = each
            if oldTraceID == 'traceID':
                resList.append(each)
                continue
            if int(oldTraceID) in idDict:
                newTraceID = idDict[int(oldTraceID)]
                oneList = [newTraceID, order, structtype, method1, method2, m1_para, m2_para, className1, className2, m1_return, m2_return]
                if newTraceID not in resDict:
                    resDict[newTraceID] = list()
                resDict[newTraceID].append(oneList)

    for traceID in resDict:
        for oneList in resDict[traceID]:
            resList.append(oneList)
    return resList

def writeCSV(fileName, listList):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)
    print fileName

#python pro.py   roller520_testcase_filter.csv  roller520_workflow.csv  roller520_workflow_reduced.csv
if __name__ == '__main__':
    filterFileName = sys.argv[1]
    workflowFileName = sys.argv[2]
    outfileName = sys.argv[3]
    idDict = readMapFile(filterFileName)
    newTraceList = filterCSV(idDict, workflowFileName)
    writeCSV(outfileName, newTraceList)
