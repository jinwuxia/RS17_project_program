import sys
import csv

def isIncluded(className):
    if className.startswith('net.jforum.view'):
        return True
    else:
        return False

def readCSV(fileName):
    resList = list() #resList[traceID] = [ [list1][list2][list3] ]
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [traceID, order, structtype, method1, method2, m1_para, m2_para, className1, className2] = each
            if traceID == 'traceID':
                continue
            if order == '0':
                resList.append(list())
            oneList = [order, structtype, method1, method2, m1_para, m2_para, className1, className2]
            resList[int(traceID)].append(oneList)
    return resList

#if one trace is repetitive or not included in view, then delete this trace
def reduceWorkflow(initList):
    resList = list()
    newID = 0
    methodID2NameDict = dict()
    methodDict = dict()
    #judge this trace should be deleted or not
    for index in range(0, len(initList)):
        isDel = True
        for eachList in initList[index]:
            [order, structtype, method1, method2, m1_para, m2_para, className1, className2] = eachList
            if isIncluded(className2):
                isDel = False
                oneStr = method2

        if isDel == False:
            if oneStr not in methodDict:
                methodID2NameDict[newID] = oneStr
                methodDict[oneStr] = newID
                print oneStr
                #save this trace
                resList.append(list())
                for eachList in initList[index]:
                    resList[newID].append(eachList)
                newID += 1
    return resList, methodID2NameDict

def writeCSV(aList, fileName):
    resList = list()
    resList.append(['traceID', 'order', 'structtype', 'method1', 'method2', 'm1_para', 'm2_para', 'className1', 'className2'])
    for traceID in range(0, len(aList)):
        for oneList in aList[traceID]:
            tmpList = [traceID]
            tmpList.extend(oneList)
            resList.append(tmpList)

    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)
    print fileName

def writeTestCase(aDict, fileName):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        for ID in aDict:
            writer.writerow([aDict[ID]])
    print fileName

#python pro.py workflowfile.csv  outputworkflowReducedworkflow.csv   outputtestcaseFileName.csv
if __name__ == "__main__":
    workflowFileName = sys.argv[1]
    reducedWorkflowFileName = sys.argv[2]
    testcaseFileName = sys.argv[3]

    initList = readCSV(workflowFileName)
    (resList, methodID2NameDict) = reduceWorkflow(initList)
    writeCSV(resList, reducedWorkflowFileName)
    writeTestCase(methodID2NameDict, testcaseFileName)
