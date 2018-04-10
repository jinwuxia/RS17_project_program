import sys
import csv


def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [traceID, order, structtype, method1, method2, m1_para, m2_para, className1, className2, m1_return, m2_return] = each
            if traceID == 'traceID':
                continue
            if order == '0':
                resList.append(list())
            oneList = [method1, method2, className1, className2]
            resList[int(traceID)].append(oneList)
    return resList


def statis(traceList):
    methodList = list()
    edgeDict = dict()
    methodCall = 0  #total methodCalling
    uniqueMethodCall = 0 #unique
    for eachTrace in traceList:
        methodCall += len(eachTrace)
        for each in eachTrace:
            [method1, method2, className1, className2] = each
            if method1 not in methodList:
                methodList.append(method1)
            if method2 not in methodList:
                methodList.append(method2)
            if method1 not in edgeDict:
                edgeDict[method1] = dict()
            if method2 not in edgeDict[method1]:
                edgeDict[method1][method2] = 0
            edgeDict[method1][method2] += 1

    for method1 in edgeDict:
        uniqueMethodCall += len(edgeDict[method1].keys())
    print 'traceCount', len(traceList)
    print 'methodCount', len(methodList)
    print 'methodCall', methodCall
    print 'uniqueMethodCall', uniqueMethodCall






if __name__ == '__main__':
    workflowFileName = sys.argv[1]
    traceList=readCSV(workflowFileName)
    statis(traceList)
